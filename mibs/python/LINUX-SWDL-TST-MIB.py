# SNMP MIB module (LINUX-SWDL-TST-MIB) expressed in pysnmp data model.
#
# Manual reduction of MIB module LINUX-SWD-MIB for test purpose

if 'mibBuilder' not in globals():
    import sys

    sys.stderr.write(__doc__)
    sys.exit(1)

# Import base ASN.1 objects even if this MIB does not use it

(Integer,
 OctetString,
 ObjectIdentifier) = mibBuilder.importSymbols(
    "ASN1",
    "Integer",
    "OctetString",
    "ObjectIdentifier")


(ConstraintsIntersection,
 SingleValueConstraint,
 ValueRangeConstraint,
 ValueSizeConstraint,
 ConstraintsUnion) = mibBuilder.importSymbols(
    "ASN1-REFINEMENT",
    "ConstraintsIntersection",
    "SingleValueConstraint",
    "ValueRangeConstraint",
    "ValueSizeConstraint",
    "ConstraintsUnion")

# Import SMI symbols from the MIBs this MIB depends on

(NotificationGroup,
 ModuleCompliance) = mibBuilder.importSymbols(
    "SNMPv2-CONF",
    "NotificationGroup",
    "ModuleCompliance")

(Integer32,
 ModuleIdentity,
 Counter32,
 MibIdentifier,
 Gauge32,
 TimeTicks,
 Counter64,
 ObjectIdentity,
 Bits,
 NotificationType,
 IpAddress,
 MibScalar,
 MibTable,
 MibTableRow,
 MibTableColumn,
 Unsigned32,
 iso,
 NotificationType) = mibBuilder.importSymbols(
    "SNMPv2-SMI",
    "Integer32",
    "ModuleIdentity",
    "Counter32",
    "MibIdentifier",
    "Gauge32",
    "TimeTicks",
    "Counter64",
    "ObjectIdentity",
    "Bits",
    "NotificationType",
    "IpAddress",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "Unsigned32",
    "iso",
    "NotificationType")

(DisplayString,
 TextualConvention) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "TextualConvention")


# Types definitions
class ConsoleId(DisplayString):
    """Custom type ConsoleId based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(1, 16),
    )

class VersionId(DisplayString):
    """Custom type VersionId based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 96),
    )

class SubsystemId(DisplayString):
    """Custom type SubsystemId based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 16),
    )

class HostName(DisplayString):
    """Custom type HostName based on DisplayString"""
    subtypeSpec = DisplayString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 16),
    )


# MIB Managed Objects in the order of their OIDs
_Swdl_ObjectIdentity = ObjectIdentity
swdl = _Swdl_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13)
)
_SwdlVersion_Type = VersionId
_SwdlVersion_Object = MibScalar
swdlVersion = _SwdlVersion_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 1),
    _SwdlVersion_Type()
)
swdlVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    swdlVersion.setStatus("mandatory")

_SwdlConsoleTable_Object = MibTable
swdlConsoleTable = _SwdlConsoleTable_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2)
)
if mibBuilder.loadTexts:
    swdlConsoleTable.setStatus("mandatory")
_SwdlConsoleEntry_Object = MibTableRow
swdlConsoleEntry = _SwdlConsoleEntry_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2, 1)
)
swdlConsoleEntry.setIndexNames(
    (0, "LINUX-SWDL-TST-MIB", "swdlConsoleSubsystemId"),
    (0, "LINUX-SWDL-TST-MIB", "swdlConsoleId"),
)
if mibBuilder.loadTexts:
    swdlConsoleEntry.setStatus("mandatory")
_SwdlConsoleSubsystemId_Type = SubsystemId
_SwdlConsoleSubsystemId_Object = MibTableColumn
swdlConsoleSubsystemId = _SwdlConsoleSubsystemId_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2, 1, 1),
    _SwdlConsoleSubsystemId_Type()
)
swdlConsoleSubsystemId.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    swdlConsoleSubsystemId.setStatus("mandatory")
_SwdlConsoleId_Type = ConsoleId
_SwdlConsoleId_Object = MibTableColumn
swdlConsoleId = _SwdlConsoleId_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2, 1, 2),
    _SwdlConsoleId_Type()
)
swdlConsoleId.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    swdlConsoleId.setStatus("mandatory")
_SwdlConsoleCurrentHostname_Type = HostName
_SwdlConsoleCurrentHostname_Object = MibTableColumn
swdlConsoleCurrentHostname = _SwdlConsoleCurrentHostname_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2, 1, 3),
    _SwdlConsoleCurrentHostname_Type()
)
swdlConsoleCurrentHostname.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    swdlConsoleCurrentHostname.setStatus("mandatory")

_SwdlConsoleCurrentVersion_Type = VersionId
_SwdlConsoleCurrentVersion_Object = MibTableColumn
swdlConsoleCurrentVersion = _SwdlConsoleCurrentVersion_Object(
    (1, 3, 6, 1, 4, 1, 1254, 1, 1, 13, 3, 2, 1, 5),
    _SwdlConsoleCurrentVersion_Type()
)
swdlConsoleCurrentVersion.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    swdlConsoleCurrentVersion.setStatus("mandatory")

# Export all MIB objects to the MIB builder
mibBuilder.exportSymbols(
    "LINUX-SWDL-TST-MIB",
    **{"swdl": swdl,
       "swdlVersion": swdlVersion,
       "swdlConsoleTable": swdlConsoleTable,
       "swdlConsoleEntry": swdlConsoleEntry,
       "swdlConsoleSubsystemId": swdlConsoleSubsystemId,
       "swdlConsoleId": swdlConsoleId,
       "swdlConsoleCurrentHostname": swdlConsoleCurrentHostname,
       "swdlConsoleCurrentVersion": swdlConsoleCurrentVersion,
}
)
