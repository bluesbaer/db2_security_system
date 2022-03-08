
class ErrorChecker():

    def __init__(self,conn):
        self.conn = conn
        pass

    def table_checker(self):
        table_error:list = []
        sql = f"""SELECT tbl_schema,tbl_name
                  FROM sec.t_table LEFT OUTER JOIN syscat.tables ON (tbl_schema,tbl_name) = (tabschema,tabname)
                  WHERE (tabschema IS NULL OR tabname IS NULL)"""
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            table_error.append(row)
            row = self.conn.fetch()

    def routine_checker(self):
        routine_error:list = []
        sql = f"""SELECT rou_schema,rou_name,rou_specific
                  FROM sec.t_routine LEFT OUTER JOIN syscat.routines ON (rou_schema,rou_name,rou_specific) = (routineschema,routinename,specificname)
                  WHERE (rouschema IS NULL OR rou_name IS NULL OR rou_specific IS NULL)"""
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            routine_error.append(row)
            row = self.conn.fetch()

    def sequence_checker(self):
        sequence_error:list = []
        sql = f"""SELECT seq_schema,seq_name
                  FROM sec.t_sequence LEFT OUTER JOIN syscat.sequences ON (seq_schema,seq_name) = (seqschema,seqname)
                  WHERE (seqschema IS NULL OR seqname IS NULL)"""
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            sequence_error.append(row)
            row = self.conn.fetch()
