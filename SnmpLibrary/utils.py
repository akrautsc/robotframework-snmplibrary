# Copyright 2014-2015 Kontron Europe GmbH
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

import sys
from robot.api import logger
from pyasn1.type import univ
from pysnmp.smi import rfc1902

def try_int(i):
    try:
        return int(i)
    except ValueError:
        return i


def is_string(string):
    if (sys.version_info[0] >= 3):
        return isinstance(string, str)
    return isinstance(string, basestring)


# Interpret a string as OID. The following notations are possible:
#   SNMPv2-MIB::sysDescr.0
#   .1.3.6.1.2.1.1.1.0
#   .iso.org.6.internet.2.1.1.1.0
def parse_oid(oid_arg):
    mib=None

    # Already a tuple
    if not is_string(oid_arg):
        oid=oid_arg

    # MIB name present
    elif '::' in oid_arg:
        mib, sym = oid_arg.split('::', 1)
        oid = None
    # No MIB name given
    else:
        if oid_arg.startswith('.'):
            oid = map(try_int, oid_arg[1:].split('.'))
        else:
            oid = map(try_int, oid_arg.split('.'))
        oid=tuple(oid)
        is_only_int = all(isinstance(x, int) for x in oid)
        # If not numeric oid, mib is needed as first element
        if not is_only_int:
            oid=(mib, ) + oid

    if oid is None:
        try:
            sym, suffixes = sym.split('.', 1)
            suffixes = suffixes.split('.')
            suffixes = map(try_int, suffixes)
            suffixes = tuple(suffixes)
        # No suffix
        except ValueError:
            suffixes = tuple()
        oid = (mib, sym,) + suffixes

    return oid

def build_object_identity(oid, idx, MibViewer):
    # Parse oid & index
    parsed_idx = parse_idx(idx)
    parsed_oid = parse_oid(oid)

    if parsed_oid[-1]!=0:
        parsed_oid=parsed_oid + parsed_idx

    # Numeric form
    is_only_int = all(isinstance(x, int) for x in parsed_oid)
    if is_only_int: 
        obj_ident=rfc1902.ObjectIdentity(parsed_oid)

    # Symbolic name
    else:
        obj_ident=rfc1902.ObjectIdentity(*parsed_oid)

    # oid is incomplete until resolved
    resolved_o_identitity=obj_ident.resolve_with_mib(MibViewer)
    logger.debug(resolved_o_identitity.prettyPrint())
    logger.debug(resolved_o_identitity._ObjectIdentity__oid._value)
    return resolved_o_identitity

def format_oid(oid):
    return '.' + '.'.join(map(str, oid))

def format_value(var, expect_string = False):

    if expect_string:
        if not univ.OctetString().isSuperTypeOf(var):
            raise RuntimeError('Returned value is not an octetstring')
    if univ.OctetString().isSuperTypeOf(var):
        value = str(var)
    else:
        value = var.prettyOut(var)
    return  value

# Interpret a string as an SNMP index. The following values are parsed:
#  '1.2.3.4' -> (1,2,3,4)
#  ('1', '2', '3') -> (1, 2, 3)
#  1 -> (1,)
# ('str_index1', 'str.index2') -> ('str_index1', 'str.index2')
def parse_idx(idx):
    if is_string(idx):
        index = map(int, idx.split('.'))
    elif isinstance(idx, int):
        index = idx,
    else:
        # Assume interable list
        try:
            index=tuple(map(int, idx))
        # idx is a list/tuple of strings, nothing to change
        except ValueError:
           index=idx
    return tuple(index)

