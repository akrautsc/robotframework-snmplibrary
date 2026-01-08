*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
SNMPV2c GET
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get  .1.3.6.1.2.1.1.5  0
    Log  ${value}  console=true
    ${value} =  Get Display String  .1.3.6.1.2.1.1.5
    Log  ${value}  console=true
    Close Snmp connection

SNMPV2c GET Display String
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get Display String  .1.3.6.1.2.1.1.5  0
    Log  ${value}  console=true
    Close Snmp connection

SNMPV2c Walk
    Open Snmp V2c Connection  localhost  community_string=public
    @{value} =  Walk  .1.3.6.1.2.1.1.9.1.3
    Log Many  @{value}
#    Log  ${value}  console=true
    Close Snmp connection

SNMPV2c SET
    Open Snmp V2c Connection  localhost  community_string=public
    ${octectStr} =  Convert to OctetString  Test
    ${value} =  Set  .1.3.6.1.4.1.1254.1.1.13  ${octectStr}
    Log  ${value}  console=true
    Close Snmp connection

SNMPV2c SET Many
    Open Snmp V2c Connection  localhost  community_string=public
    ${octectStr1} =  Convert to OctetString  Test1
    ${octectStr2} =  Convert to OctetString  Test2
    ${value} =  Set Many  .1.3.6.1.4.1.1254.1.1.13  ${octectStr1}  .1.3.6.1.4.1.1254.1.1.14  ${octectStr2}
    Log  ${value}  console=true
    Close Snmp connection

SNMPV2c receive trap
    Open Snmp V2c Connection  localhost  community_string=public
    New Trap Filter  traptest1  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.5.1
    New Trap Filter  traptest2  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.4.1
    Wait until Trap is received  traptest1  timeout=0  host=127.0.0.1  port=1620
    Log  Trap received  console=true
    Wait until Trap is received  traptest2  host=127.0.0.1  port=1620
    Log  Trap not received. Next step after timeout.  console=true
    Close Snmp connection
