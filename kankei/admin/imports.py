from admin import resets, converts


def import_rawdata_neo4j(excludes=None):
    print("importing raw data to neo4j")
    import_rawdata_csv(excludes)
    import_csv_neo4j()


def import_rawdata_csv(excludes=None):
    print("importing raw data to csv")
    resets.reset_csv()
    converts.convert_rawdata_csv(excludes)


def import_csv_neo4j():
    print("importing csv data to neo4j")
    resets.reset_neo4j()
    converts.convert_csv_neo4j()
