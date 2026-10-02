from app.connectors.ofac import OfficialOfacConnector


def test_official_ofac_parser_joins_aliases_by_uid() -> None:
    primary = '''1001,"ALPHA TEST ENTITY","Entity","PROGRAM"
1002,"BETA TEST PERSON","Individual","PROGRAM"
'''
    aliases = '''1001,1,"aka","ALPHA TRADING"
1001,2,"aka","ALPHA HOLDINGS"
1002,3,"aka","BETA PERSON"
'''

    records = OfficialOfacConnector._parse_primary(primary)
    alias_map = OfficialOfacConnector._parse_aliases(aliases)

    assert records["1001"].full_name == "ALPHA TEST ENTITY"
    assert alias_map["1001"] == ["ALPHA TRADING", "ALPHA HOLDINGS"]
    assert alias_map["1002"] == ["BETA PERSON"]
