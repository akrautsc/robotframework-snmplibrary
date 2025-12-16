*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
Connect to SNMP controlled device
    Open Snmp V2c Connection  10.98.2.254  community_string=public
    ${value} =  Get  .1.3.6.1.2.1.1.4.0
    Log  ${value}
    ${value} =  Get Display String  .1.3.6.1.2.1.1.5.0
    Log  ${value}
