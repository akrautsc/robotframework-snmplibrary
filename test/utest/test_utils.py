from SnmpLibrary.utils import parse_oid, parse_idx, format_oid


def test_parse_oid():
    assert parse_oid('.1.2.3') == (1, 2, 3)
    assert parse_oid('SNMPv2-MIB::sysDescr.0') == ('SNMPv2-MIB', 'sysDescr', 0)
    assert parse_oid('.iso.org.6') == (None, 'iso', 'org', 6)
    assert parse_oid('sysDescr.0') == (None, 'sysDescr', 0)
    assert parse_oid('LINUX-SWDL-MIB::swdlConsoleCurrentVersion') == ('LINUX-SWDL-MIB', 'swdlConsoleCurrentVersion')

def test_format_oid():
    assert format_oid((1, 2, 3)) == '.1.2.3'
    assert format_oid((1, 'iso', 'org', 3)) == '.1.iso.org.3'

def test_parse_idx():
    assert parse_idx('1.2.3') == ('1', '2', '3')
    assert parse_idx(1) == (1,)
    assert parse_idx([1, 2, 3]) == (1, 2, 3)
    assert parse_idx((1, '2', 3)) == (1, 2, 3)
    assert parse_idx(('str_index1', 'str.index2')) == ('str_index1', 'str.index2')
