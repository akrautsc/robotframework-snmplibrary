# Copyright 2015 Kontron Europe GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import warnings
import functools

import robot.utils
from robot.api import logger

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
    from pysnmp.carrier.asyncio.dgram import udp
    # from pysnmp.proto.api import verdec, v2c, protoVersion2c
    from pysnmp.proto.api import verdec, v2c
    from pyasn1.codec.ber import decoder

from . import utils

class _TrapFilters:

    @staticmethod
    def generic_trap_filter(domain, sock, pdu, **kwargs):
        logger.trace("Filter parameter: %s" % kwargs)
        logger.trace("Received PDU:\n%s" % pdu)
        snmpTrapOID = (1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0)
        if 'host' in kwargs and kwargs['host']:
            if sock[0] != kwargs['host']:
                return False

        for oid, val in v2c.apiPDU.get_varbinds(pdu):
            if 'oid' in kwargs and kwargs['oid']:
                if oid == snmpTrapOID:
                    if val != v2c.ObjectIdentifier(kwargs['oid']):
                        logger.info("Expected trap not received!")
                        return False
        logger.info("Expected trap received!")
        return True

class _TrapReceiver:
    def __init__(self):
        self.trap_pdu = dict()
        self.started = None
        self.trap_filter = None
        self.timeout = None

    def _trap_timer_cb(self, now):
        if now - self.started > self.timeout:
            raise AssertionError('No matching trap received in %s.' %
                                 robot.utils.secs_to_timestr(self.timeout))

    def _trap_receiver_cb(self, transport, domain, sock, msg):
        # TODO: Check comparsion
        # In previous version following comparison was done
        # decodeMessageVersion(msg) != protoVersion2c
        # It's defined protoVersion2c = 1
        if verdec.decode_message_version(msg) != 1:
            raise RuntimeError('Only SNMP v2c traps are supported.')

        req, msg = decoder.decode(msg, asn1Spec=v2c.Message())
        pdu = v2c.apiMessage.get_pdu(req)
        self.trap_pdu.clear()

        # ignore any non trap PDUs
        if not pdu.isSameTypeWith(v2c.TrapPDU()):
            return

        # Stop the receiver if the trap we are looking for was received.
        if self.trap_filter(domain, sock, pdu):
            for oid, val in v2c.apiPDU.get_varbinds(pdu):
                self.trap_pdu[oid] = val
            transport.job_finished(1)
            transport._AsyncioDispatcher__close_dispatcher()

    def trap_receiver(self, trap_filter, host, port, timeout):
        self.started = time.time()
        self.trap_filter = trap_filter
        self.timeout = timeout

        dispatcher = AsyncioDispatcher()
        dispatcher.register_recv_callback(self._trap_receiver_cb)
        # Timer call back doesn't pass Exception (see below).
        # It's not working as expected and therefore currently not used.
        # dispatcher.register_timer_callback(self._trap_timer_cb)

        transport = udp.UdpAsyncioTransport().open_server_mode((host, port))
        dispatcher.register_transport(udp.DOMAIN_NAME, transport)

        dispatcher.job_started(1)
        dispatcher.run_dispatcher(timeout)

        # Following code is not working as expected. Currently it's not clear why this is happening.
        # Raised exception is not caught. In case the issue is found, it will be re-implemented.
        # we'll never finish, except through an exception
        # try:
        #     dispatcher.run_dispatcher()
        # finally:
        #     # Not using public method as described in next line.
        #     # dispatcher.close_dispatcher()
        #     # This is due to issue of pysnmp lib reported here: https://github.com/lextudio/pysnmp/issues/203
        #     dispatcher._AsyncioDispatcher__close_dispatcher()


class _Traps:
    def __init__(self):
        self._trap_filters = dict()

    def new_trap_filter(self, name, host=None, oid=None):
        """Defines a new SNMP trap filter.

        At the moment, you can only filter on the sending host and on the trap
        OID.
        """
        trap_filter = functools.partial(_TrapFilters.generic_trap_filter,
                                        host=host,
                                        oid=utils.parse_oid(oid))
        self._trap_filters[name] = trap_filter

    def wait_until_trap_is_received(self, trap_filter_name, timeout=5.0,
                                    host='0.0.0.0', port=1620):
        """Wait until the first matching trap is received.

        Returns PDU of received trap.
        """
        _trap_receiver = _TrapReceiver()

        if trap_filter_name not in self._trap_filters:
            raise RuntimeError('Trap filter "%s" not found.' % trap_filter_name)

        trap_filter = self._trap_filters[trap_filter_name]
        timeout = robot.utils.timestr_to_secs(timeout)

        _trap_receiver.trap_receiver(trap_filter, host, port, timeout)

        return _trap_receiver.trap_pdu

