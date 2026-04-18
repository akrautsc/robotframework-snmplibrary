*** Settings ***
Library  SnmpLibrary

*** Test Cases ***

SNMPV2c Faulty GET
    Open Snmp V2c Connection  localhost  community_string=public
    Run Keyword and expect error  *UNKNOWN-MIB* not found in search path *  Get  UNKNOWN-MIB::sysUpTime
    Run Keyword and expect error  * No symbol SNMPv2-MIB::UnkownSymbol *   Get  SNMPv2-MIB::UnkownSymbol
    Run Keyword and expect error  NoSuchObjectError: NoSuchObjectError* 'No such symbol ::UnkownSymbol at *  Get  UnkownSymbol
    Run Keyword and expect error  Object with OID .1.3.6.1.4.1.2363.3.30.10.0 not found  Get  .1.3.6.1.4.1.2363.3.30.10
    Close Snmp connection


SNMPV2c Faulty GET Display String
    Open Snmp V2c Connection  localhost  community_string=public
    Run Keyword and expect error  Returned value is not an octetstring  Get Display String  .1.3.6.1.2.1.1.3.0 
    Close Snmp connection

SNMPV2c GET - scalar
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get  SNMPv2-MIB::sysName.0
    Log To Console  ${value}
    ${value} =  Get  sysName.0
    Log To Console  ${value}
    Close Snmp connection

SNMPV2c GET - scalar2
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get  SNMPv2-MIB::sysUpTime
    Log To Console  ${value}
    ${value} =  Get  .1.3.6.1.2.1.1.3.0 
    Log To Console  ${value}
    Close Snmp connection

SNMPV2c GET Display String - scalar
    Open Snmp V2c Connection  localhost  community_string=public
    ${value} =  Get Display String  SNMPv2-MIB::sysName.0
    Log To Console  ${value}
    Close Snmp connection

SNMPV2c GET Display String - table
    Open Snmp V2c Connection  localhost  community_string=public
    ${value1} =  Get Display String  SNMPv2-MIB::sysORDescr.1
    Log To Console  ${value1}
    ${value2} =  Get Display String  SNMPv2-MIB::sysORDescr  1
    Log To Console  ${value2}
    ${value3} =  Get Display String  1.3.6.1.2.1.1.9.1.3  1
    Log To Console  ${value3}
    Should Be Equal  ${value1}  ${value2} 
    Should Be Equal  ${value1}  ${value3} 
    Close Snmp connection

SNMPV2c GET Display String - resiliency
    [Template]  SNMPV2c GET Display String Should Be Equal
    SNMPv2-MIB::sysName  0  SNMPv2-MIB::sysName     ${None}
    SNMPv2-MIB::sysName  0  SNMPv2-MIB::sysName.0   ${None}
    SNMPv2-MIB::sysName  0  SNMPv2-MIB::system.5    ${None}
    SNMPv2-MIB::sysName  0  SNMPv2-MIB::system.5.0  ${None}
    SNMPv2-MIB::sysName  0  .1.3.6.1.2.1.1.5  0
    SNMPv2-MIB::sysName  0  .1.3.6.1.2.1.1.5  ${None}
    SNMPv2-MIB::sysName  0  .1.3.6.1.2.1.1.5.0  ${None}
    SNMPv2-MIB::sysName  0  .1.3.6.1.2.1.1.5.0  0
    SNMPv2-MIB::sysName  0  1.3.6.1.2.1.1.5  0
    SNMPv2-MIB::sysName  0  1.3.6.1.2.1.1.5  ${None}
    SNMPv2-MIB::sysName  0  1.3.6.1.2.1.1.5.0  ${None}
    SNMPv2-MIB::sysName  0  1.3.6.1.2.1.1.5.0  0

SNMPV2c Walk
    Open Snmp V2c Connection  localhost  community_string=public
    @{value} =  Walk  .1.3.6.1.2.1.1  
    Log Many  @{value}
    Close Snmp connection

SNMPV2c Walk Pretty
    Open Snmp V2c Connection  localhost  community_string=public
    @{value} =  Walk  .1.3.6.1.2.1.1  pretty=${True}
    Log Many  @{value}
    Close Snmp connection

SNMPV2c SET String
    [Documentation]  Sets new value to System Contact item and put its back to original value 
    ...  If element is readonly, comment out the entry in /etc/snmp/snmpd.conf
    ...  "syscontact OPE/SRS" => "#syscontact OPE/SRS"

    Open Snmp V2c Connection  localhost  community_string=public
    VAR  ${new_value}  Test System Contact
    ${octectStr_new} =  Convert to OctetString  ${new_value}
    ${orignal_value} =  Get Display String  SNMPv2-MIB::sysContact.0
    ${octectStr_orignal} =  Convert to OctetString  ${orignal_value}
    Log To Console  ${orignal_value}

    ${value} =  Set  SNMPv2-MIB::sysContact.0  ${octectStr_new}
    Log To Console  ${value}

    # Check new value applied
    ${modified_value} =  Get Display String  SNMPv2-MIB::sysContact.0
    Log To Console  ${modified_value}
    Should Be Equal  ${new_value}  ${modified_value} 

    # Put back original value
    ${value} =  Set  SNMPv2-MIB::sysContact.0  ${octectStr_orignal}
    Log To Console  ${value}

    Close Snmp connection

SNMPV2c SET Integer
    Open Snmp V2c Connection  localhost  community_string=public
    ${integer} =  SnmpLibrary.Convert To Integer  10
    ${value} =  Set  .1.3.6.1.4.1.1254.1.1.13  ${integer}
    Log  ${value}
    Close Snmp connection

SNMPV2c SET Integer Resiliency
    Open Snmp V2c Connection  localhost  community_string=public
    ${integer} =  SnmpLibrary.Convert To Integer  10
    ${value} =  Set  .1.3.6.1.4.1.1254.1.1.13  ${integer}
    ${value} =  Set  1.3.6.1.4.1.1254.1.1.13  ${integer}
    ${value} =  Set  1.3.6.1.4.1.1254.1.1.13.0  ${integer}
    ${value} =  Set  SNMPv2-SMI::enterprises.1254.1.1.13  ${integer}
    ${value} =  Set  SNMPv2-SMI::enterprises.1254.1.1.13.0  ${integer}
    Log  ${value}
    Close Snmp connection

SNMPV2c SET Many
    Open Snmp V2c Connection  localhost  community_string=public
    ${integer} =  SnmpLibrary.Convert To Integer  10
    ${new_string_value} =  Get Display String  SNMPv2-MIB::sysContact.0
    ${octectStr_orignal} =  Convert to OctetString  ${new_string_value}
    @{value} =  Set Many  .1.3.6.1.4.1.1254.1.1.13  ${integer}  SNMPv2-MIB::sysContact.0  ${octectStr_orignal}
    Log Many  @{value}
    Close Snmp connection


SNMPV2c receive trap
    Open Snmp V2c Connection  localhost  community_string=public
    New Trap Filter  traptest1  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.5.1
    New Trap Filter  traptest2  host=127.0.0.1  oid=.1.3.6.1.6.3.1.1.4.1
    Log to Console  Waiting for trap
    @{pdu} =  Wait until Trap is received  traptest1  timeout=30  host=127.0.0.1  port=1620
    Should Not Be Empty  ${pdu}
    Log Many  @{pdu}
    ${pdu} =  Wait until Trap is received  traptest2  host=127.0.0.1  port=1620
    Should be Empty  ${pdu}
    Log  ${pdu}
    Close Snmp connection

MIB search path
    Open Snmp V2c Connection  localhost  community_string=public
    Add Mib Search path  /tmp

*** Keywords ***

SNMPV2c GET Display String 
    [Arguments]    ${oid}  ${index}=${None}
    Open Snmp V2c Connection  localhost  community_string=public
    IF  "${index}" == "${None}"
        ${value}=  Get Display String  ${oid}
    ELSE 
        ${value}=  Get Display String  ${oid}  ${index}
    END
    RETURN  ${value}
    Close Snmp connection

SNMPV2c GET Display String Should Be Equal  
    [Arguments]    ${oid1}  ${index1}  ${oid2}  ${index2}
    ${value1}=  SNMPV2c GET Display String  ${oid1}  ${index1}
    ${value2}=  SNMPV2c GET Display String  ${oid2}  ${index2}
    Should Be Equal  ${value1}  ${value2} 

