*** Settings ***
Library  SnmpLibrary

*** Test Cases ***
SNMPV2c GET Display String GENTSS
    @{index_list}=  Create List  DGW  dgw-re
    Open Snmp Connection   st05u  tsc666  161  1.0  5
    Add Mib Search Path  mibs/python/
    Preload Mibs     LINUX-SWDL-TST-MIB
    ${intended_server_mode} =  Get Display String  LINUX-SWDL-TST-MIB::swdlConsoleCurrentVersion  ${index_list}
    Log To Console  ${intended_server_mode}
