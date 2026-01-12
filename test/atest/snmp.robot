*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
SNMPV2c GET
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get  .1.3.6.1.2.1.1.5  0
    Log  ${value}
    ${value} =  Get Display String  .1.3.6.1.2.1.1.5
    Log  ${value}
    Close Snmp connection

SNMPV2c GET Display String
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get Display String  .1.3.6.1.2.1.1.5  0
    Log  ${value}
    Close Snmp connection

SNMPV2c Walk
    Open Snmp V2c Connection  localhost  community_string=public
    @{value} =  Walk  .1.3.6.1.2.1.1.9.1.3
    Log Many  @{value}
    Close Snmp connection

SNMPV2c SET
    Open Snmp V2c Connection  localhost  community_string=public
    ${octectStr} =  Convert to OctetString  Test
    ${value} =  Set  .1.3.6.1.4.1.1254.1.1.13  ${octectStr}
    Log  ${value}
    Close Snmp connection

SNMPV2c SET Many
    Open Snmp V2c Connection  localhost  community_string=public
    ${octectStr1} =  Convert to OctetString  Test1
    ${octectStr2} =  Convert to OctetString  Test2
    ${value} =  Set Many  .1.3.6.1.4.1.1254.1.1.13  ${octectStr1}  .1.3.6.1.4.1.1254.1.1.14  ${octectStr2}
    Log  ${value}
    Close Snmp connection

SNMPV2c receive trap
    Open Snmp V2c Connection  localhost  community_string=public
    New Trap Filter  traptest1  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.5.1
    New Trap Filter  traptest2  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.4.1
    Log to Console  Waiting for trap
    &{pdu} =  Wait until Trap is received  traptest1  timeout=30  host=127.0.0.1  port=1620
    Should Not Be Empty  ${pdu}
    Log Many  &{pdu}
    ${pdu} =  Wait until Trap is received  traptest2  host=127.0.0.1  port=1620
    Should be Empty  ${pdu}
    Log  ${pdu}
    Close Snmp connection
