*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
SNMPV2c GET
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get  .1.3.6.1.2.1.1.5  0
    Log  ${value}  console=true
#    ${value} =  Get Display String  .1.3.6.1.2.1.1.5.0
#    Log  ${value}  console=true
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
