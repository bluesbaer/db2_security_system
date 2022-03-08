#!/usr/bin/env python3

import sec_db2
import sec_obj
from copy import deepcopy

class ModObj():

    stack: list = []

    def __init__(self,conn):
        self.table:str          = ""
        self.key:str            = ""
        self.id_field:list      = ""
        self.update_fields:list = []
        self.conn               = conn
        self.objtyp             = sec_obj.SecObj()
        self.var:str            = ""

    def do_search(self,search:dict) -> list:
        tmp:list = []
        out:list = deepcopy(self.stack)
        if out[0] is not None:
            for key in search.keys():
                for row in out:
                    exec(f"self.p = row.{key}")
                    if self.p == search[key]:
                        tmp.append(deepcopy(row))
                out = deepcopy(tmp)
                tmp = []
        else:
            out = []
        return out
    
    def get_id(self,search:dict) -> int:
        value:int = 0
        out = self.do_search(search)
        try:
            exec(f"self.p = out[0].{self.key}")
            value = self.p
        except:
            value = 0
        return value

    def move_data_2_obj(self,row):
        tmpobj = sec_obj.SecObj()
        #tmpobj = self.objtyp.new_obj()
        for key in row.keys():
            _ = f"tmpobj.{key} = '{row[key]}'"
            exec(_)
        return tmpobj

    def read_data(self):
        self.stack = []
        empty_obj = self.objtyp.new_obj()
        self.stack.append(deepcopy(empty_obj))
        sql = f"SELECT * FROM sec.{self.table} WHERE {self.key} > 0"
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            tmp = self.move_data_2_obj(row)
            self.stack.append(deepcopy(tmp))
            row = self.conn.fetch()

    def get_key_val(self,record:dict) -> int:
        search:dict = {}
        for name in self.id_field:
            search[name] = record[name]
        tmp = self.get_id(search)
        return tmp

    def get_upd_val(self,record:dict) -> str:
        tmp:list = []
        for key in record.keys():
            if key in self.update_fields:
                tmp.append(f"'{record[key]}'")
        tmp = ','.join(tmp)
        return tmp

    def write_data(self,record):
        key_data = self.get_key_val(record)
        update_data = self.get_upd_val(record)
        update_str = ','.join(self.update_fields)
        sql = f"""MERGE INTO sec.{self.table} trg 
            USING (SELECT {key_data},{update_data} FROM sysibm.sysdummy1) src
            ON ({self.key} = {key_data})
            WHEN MATCHED THEN
                UPDATE SET ({update_str}) = ({update_data})
            WHEN NOT MATCHED THEN
                INSERT ({update_str}) VALUES ({update_data})"""
        self.conn.exec(sql)
        self.read_data()

    def delete_data(self,id:int):
        sql = f"DELETE FROM sec.{self.table} WHERE {self.key} = {id}"
        self.conn.exec(sql)
        self.read_data()

    def get_list(self,view:str,search:dict) -> list:
        out:list = []
        data = self.do_search(search)
        for row in data:
            exec(f"self.p = row.{view}")
            out.append(self.p)
        out = list(set(out))
        out.sort()
        return out


# --------------------------------------------------------------------------------
# -- ModUsr                                                                     --
# --------------------------------------------------------------------------------
class ModUsr(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_USER"
        self.key:str            = "USR_ID"
        self.id_field:list      = ["USR_NAME"]
        self.update_fields:list = ["USR_NAME","USR_START","USR_END","USR_MARK","USR_CONNECT"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecUsr()


# --------------------------------------------------------------------------------
# -- ModRol                                                                     --
# --------------------------------------------------------------------------------
class ModRol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_ROLE"
        self.key:str            = "ROL_ID"
        self.id_field:list      = ["ROL_NAME"]
        self.update_fields:list = ["ROL_NAME","ROL_START","ROL_END","ROL_DESCRIPTION","ROL_TYPE"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecRol()

    def read_data(self):
        self.stack = []
        empty_obj = self.objtyp.new_obj()
        self.stack.append(deepcopy(empty_obj))
        sql = f"SELECT * FROM sec.{self.table}"
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            tmp = self.move_data_2_obj(row)
            self.stack.append(deepcopy(tmp))
            row = self.conn.fetch()


# --------------------------------------------------------------------------------
# -- ModSch                                                                     --
# --------------------------------------------------------------------------------
class ModSch(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_SCHEMA"
        self.key:str            = "SCH_ID"
        self.id_field:list      = ["SCH_NAME"]
        self.update_fields:list = ["SCH_NAME","SCH_START","SCH_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecSch()


# --------------------------------------------------------------------------------
# -- ModTbl                                                                     --
# --------------------------------------------------------------------------------
class ModTbl(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_TABLE"
        self.key:str            = "TBL_ID"
        self.id_field:list      = ["TBL_SCHEMA","TBL_NAME"]
        self.update_fields:list = ["TBL_SCHEMA","TBL_NAME","TBL_START","TBL_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecTbl()


# --------------------------------------------------------------------------------
# -- ModRou                                                                     --
# --------------------------------------------------------------------------------
class ModRou(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_ROUTINE"
        self.key:str            = "ROU_ID"
        self.id_field:list      = ["ROU_SCHEMA","ROU_NAME"]
        self.update_fields:list = ["ROU_SCHEMA","ROU_NAME","ROU_START","ROU_END","ROU_SPECIFIC","ROU_TYPE"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecRou()


# --------------------------------------------------------------------------------
# -- ModSeq                                                                     --
# --------------------------------------------------------------------------------
class ModSeq(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_SEQUENCE"
        self.key:str            = "SEQ_ID"
        self.id_field:list      = ["SEQ_SCHEMA","SEQ_NAME"]
        self.update_fields:list = ["SEQ_SCHEMA","SEQ_NAME","SEQ_START","SEQ_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecSeq()


# --------------------------------------------------------------------------------
# -- ModUsr2Rol                                                                 --
# --------------------------------------------------------------------------------
class ModUsr2Rol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_USR2ROL"
        self.key:str            = "U2R_ID"
        self.id_field:list      = ["U2R_USR_ID","U2R_ROL_ID"]
        self.update_fields:list = ["U2R_USR_ID","U2R_ROL_ID","U2R_START","U2R_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecUsr2Rol()


# --------------------------------------------------------------------------------
# -- ModSch2Rol                                                                 --
# --------------------------------------------------------------------------------
class ModSch2Rol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_SCH2ROL"
        self.key:str            = "S2R_ID"
        self.id_field:list      = ["S2R_SCH_ID","S2R_ROL_ID"]
        self.update_fields:list = ["S2R_SCH_ID","S2R_ROL_ID","S2R_START","S2R_END","S2R_SCHADM","S2R_SCHSEC"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecSch2Rol()


# --------------------------------------------------------------------------------
# -- ModTbl2Rol                                                                 --
# --------------------------------------------------------------------------------
class ModTbl2Rol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_TBL2ROL"
        self.key:str            = "T2R_ID"
        self.id_field:list      = ["T2R_TBL_ID","T2R_ROL_ID"]
        self.update_fields:list = ["T2R_TBL_ID","T2R_ROL_ID","T2R_START","T2R_END","T2R_CTLAUTH",\
            "T2R_DELAUTH","T2R_INSAUTH","T2R_SELAUTH","T2R_UPDAUTH"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecTbl2Rol()


# --------------------------------------------------------------------------------
# -- ModRou2Rol                                                                 --
# --------------------------------------------------------------------------------
class ModRou2Rol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_ROU2ROL"
        self.key:str            = "R2R_ID"
        self.id_field:list      = ["R2R_ROU_ID","R2R_ROL_ID"]
        self.update_fields:list = ["R2R_ROU_ID","R2R_ROL_ID","R2R_START","R2R_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecRou2Rol()


# --------------------------------------------------------------------------------
# -- ModSeq2Rol                                                                 --
# --------------------------------------------------------------------------------
class ModSeq2Rol(ModObj):

    stack: list = []

    def __init__(self,conn):
        super().__init__(conn)
        self.table:str          = "T_SEQ2ROL"
        self.key:str            = "S2R_ID"
        self.id_field:list      = ["S2R_SEQ_ID","S2R_ROL_ID"]
        self.update_fields:list = ["S2R_SEQ_ID","S2R_ROL_ID","S2R_START","S2R_END"]
        self.conn               = conn
        self.objtyp             = sec_obj.SecSeq2Rol()


# --------------------------------------------------------------------------------
# -- BuildRbactree                                                              --
# --------------------------------------------------------------------------------
class BuildRbacTree():

    def __init__(self,conn):
        self.conn = conn

    def build(self,sql):
        work:list = []
        self.conn.exec(sql)
        row = self.conn.fetch('X')
        while row != False:
            work.append(row)
            row = self.conn.fetch('X')
        return work


# --------------------------------------------------------------------------------
# -- ModDbConn                                                                  --
# --------------------------------------------------------------------------------
class ModDbConn():

    stack:list = []

    def __init__(self):
        self.dbconn = sec_db2.Db2()

    def read_dbc(self):
        self.stack:list = []
        with open ('./db2_connections','r') as file:
            for row in file:
                self.stack.append(row)

    def build_con_list(self):
        self.con_list:list = []
        for row in self.stack:
            fields = row.split(";")
            self.con_list.append(fields[0])

    def select_con(self,sel_con):
        for row in self.stack:
            fields = row.split(";")
            if fields[0] == sel_con:
                return row
    
    def write_dbc(self):
        with open ('./db2_connections','w+') as file:
            for row in self.stack:
                file.write(row)

    def stack_append(self,record):
        self.stack.append(record)

    def stack_update(self,record):
        fields = record.split(";")
        for nr,row in enumerate(self.stack):
            tmp = row.split(";")
            if tmp[0] == fields[0]:
                self.stack[nr] = record

    def delete_dbc(self,del_name):
        for nr, row in enumerate(self.stack):
            tmp = row.split(";")
            if tmp[0] == del_name:
                del self.stack[nr]


# --------------------------------------------------------------------------------
# -- ErrorChecker                                                               --
# --------------------------------------------------------------------------------
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
        return table_error

    def routine_checker(self):
        routine_error:list = []
        sql = f"""SELECT rou_schema,rou_name,rou_specific
                  FROM sec.t_routine LEFT OUTER JOIN syscat.routines ON (rou_schema,rou_name,rou_specific) = (routineschema,routinename,specificname)
                  WHERE (routineschema IS NULL OR routinename IS NULL OR specificname IS NULL)"""
        self.conn.exec(sql)
        row = self.conn.fetch()
        while row != False:
            routine_error.append(row)
            row = self.conn.fetch()
        return routine_error

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
        return sequence_error





# --------------------------------------------------------------------------------
# -- TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST --
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    #conn = sec_db2.Db2()
    #conn.open('localhost',50000,'newsecdb','','manfred','IhMW&bue50')
    #print("*** USER ***")
    #usr = ModUsr(conn)
    #usr.read_data()
    #for _ in usr.stack:
    #    print('USER 1',_)
    #usr.write_data({'USR_ID':0,'USR_NAME':'HEINZ','USR_START':'2021-05-01','USR_END':'2999-12-31','USR_MARK':'A','USR_CONNECT':'DBCONUSR'})
    #usr.write_data({'USR_ID':2,'USR_NAME':'KARL','USR_START':'2999-12-30','USR_END':'2999-12-31','USR_MARK':'U','USR_CONNECT':'DBCONUSR'})
    #for _ in usr.stack:
    #    print('2',_)
    #usr.delete_data(29)
    #usr.write_data({'USR_ID':2,'USR_NAME':'KARL','USR_START':'2021-05-01','USR_END':'2999-12-31','USR_MARK':'U','USR_CONNECT':'DBCONUSR'})
    #for _ in usr.stack:
    #    print('3',_)
    #data = usr.get_list('USR_NAME',{})
    #print(f"USER data:{data}")
    # --------------------------------------------------------------------------------
    #print("*** ROLE ***")
    #rol = ModRol(conn)
    #rol.write_data({'ROL_ID':0,'ROL_NAME':'DUMMY1','ROL_START':'2021-01-01','ROL_END':'2999-12-31','ROL_DESCRIPTION':'ist is silly','ROL_TYPE':'R'})
    #rol.read_data()
    #for _ in rol.stack:
    #    print('ROLE 1',_)
    #data = rol.get_list('ROL_NAME',{})
    #print(f"ROLE data:{data}")
    # --------------------------------------------------------------------------------
    #print("*** TABLE ***")
    #tbl = ModTbl(conn)
    #tbl.write_data({'TBL_ID':0,'TBL_SCHEMA':'EIS','TBL_NAME':'PERSON','TBL_START':'2021-01-01','TBL_END':'2999-12-31'})
    #tbl.read_data()
    #for _ in tbl.stack:
    #    print('TABLE 1',_)
    #data = tbl.get_list('TBL_NAME',{})
    #print(f"TABLE data:{data}")
    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    xcon = ModDbConn()
    xcon.read_dbc()
    for row in xcon.stack:
        print(f"row:{row}")
    xcon.build_con_list()
    print(f"connections:{xcon.con_list}")
    new_con = xcon.select_con('EIST')
    print(f"new:{new_con}")
