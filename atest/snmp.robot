*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
Connect to SNMP controlled device
    Open Snmp V2c Connection  10.98.2.254  community_string=akrautsc
    ${value} =  get  .1.3.6.1.4.1.2356.11.2.1  0
    Log  ${value}
