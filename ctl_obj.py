#!/usr/bin/env python3

from chk_err import ErrorChecker
import mod_obj
import sec_db2

class CtlObj():

    def __init__(self,conn):
        self.modtyp = mod_obj.ModObj(conn)
        self.conn   = conn

    def read_data(self):
        self.modtyp.read_data()

    def get_data_list(self,view:str,search:dict) -> list:
        data:list = []
        data = self.modtyp.get_list(view,search)
        return data

    def get_data_record(self,search:dict) -> dict:
        data:dict = {}
        data = self.modtyp.do_search(search)
        return data

    def write_data(self,record):
        self.modtyp.write_data(record)

    def delete_data(self,id):
        self.modtyp.delete_data(id)

    def check4error(self):
        te:list = []
        re:list = []
        se:list = []
        result:dict = {}
        ec = mod_obj.ErrorChecker(self.conn)
        te = ec.table_checker()
        re = ec.routine_checker()
        se = ec.sequence_checker()
        result['table'] = te
        result['routine'] = re
        result['sequence'] = se
        return result


# --------------------------------------------------------------------------------
# -- CtlUsr                                                                     --
# --------------------------------------------------------------------------------
class CtlUsr(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModUsr(self.conn)


# --------------------------------------------------------------------------------
# -- CtlRol                                                                     --
# --------------------------------------------------------------------------------
class CtlRol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModRol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlSch                                                                     --
# --------------------------------------------------------------------------------
class CtlSch(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModSch(self.conn)


# --------------------------------------------------------------------------------
# -- CtlTbl                                                                     --
# --------------------------------------------------------------------------------
class CtlTbl(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModTbl(self.conn)


# --------------------------------------------------------------------------------
# -- CtlRou                                                                     --
# --------------------------------------------------------------------------------
class CtlRou(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModRou(self.conn)


# --------------------------------------------------------------------------------
# -- CtlSeq                                                                     --
# --------------------------------------------------------------------------------
class CtlSeq(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModSeq(self.conn)


# --------------------------------------------------------------------------------
# -- CtlUsr2Rol                                                                 --
# --------------------------------------------------------------------------------
class CtlUsr2Rol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModUsr2Rol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlSch2Rol                                                                 --
# --------------------------------------------------------------------------------
class CtlSch2Rol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModSch2Rol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlTbl2Rol                                                                 --
# --------------------------------------------------------------------------------
class CtlTbl2Rol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModTbl2Rol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlRou2Rol                                                                 --
# --------------------------------------------------------------------------------
class CtlRou2Rol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModRou2Rol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlSeq2Rol                                                                 --
# --------------------------------------------------------------------------------
class CtlSeq2Rol(CtlObj):

    def __init__(self,conn):
        super().__init__(conn)
        self.conn   = conn
        self.modtyp = mod_obj.ModSeq2Rol(self.conn)


# --------------------------------------------------------------------------------
# -- CtlRbacTree                                                                --
# --------------------------------------------------------------------------------
class CtlRbacTree():

    def __init__(self,conn):
        self.modtyp = mod_obj.BuildRbacTree(conn)

    def build(self,sql):
        work:list = []
        work = self.modtyp.build(sql)
        return work


# --------------------------------------------------------------------------------
# -- CtlDbConn                                                                  --
# --------------------------------------------------------------------------------
class CtlDbConn():

    def __init__(self):
        self.modtyp = mod_obj.ModDbConn()

    def read_dbc(self):
        con_list:list = []
        self.modtyp.read_dbc()
        self.modtyp.build_con_list()
        con_list = self.modtyp.con_list
        return con_list

    def get_con(self,sel_con):
        return self.modtyp.select_con(sel_con)

    def write_dbc(self):
        self.modtyp.write_dbc()

    def stack_append(self,record):
        self.modtyp.stack_append(record)

    def stack_update(self,record):
        self.modtyp.stack_update(record)

    def delete_dbc(self,del_name):
        self.modtyp.delete_dbc(del_name)




# --------------------------------------------------------------------------------
# -- TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST --
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    conn = sec_db2.Db2()
    conn.open('localhost',50000,'newsecdb','','manfred','IhMW&bue50')
    print("*** USER ***")
    usr = CtlUsr(conn)
    usr.read_data()
    data = usr.get_data_list('USR_NAME',{})
    print(f"USER data:{data}")
    data = usr.get_data_record({'USR_NAME':'KARL'})
    for row in data:
        print(f"USER row:{row}")
    #record = {'USR_ID':4,'USR_NAME':'HEIDI','USR_START':'2021-05-01','USR_END':'2999-12-31','USR_MARK':'A','USR_CONNECT':'KARL'}
    #usr.write_data(record)
    #data = usr.get_data_record({'USR_NAME':'HEIDI'})
    #for row in data:
    #    print(f"row:{row}")
    #data = usr.get_data_list('USR_NAME',{})
    #print(f"data:{data}")
    #record = {'USR_ID':4,'USR_NAME':'HEIDI','USR_START':'2021-01-01','USR_END':'2999-12-31','USR_MARK':'A','USR_CONNECT':'KARL'}
    #usr.write_data(record)
    print("*** ROLE ***")
    rol = CtlRol(conn)
    rol.read_data()
    data = rol.get_data_list('ROL_NAME',{})
    print(f"ROLE data:{data}")
    data = rol.get_data_record({'ROL_NAME':'DUMMY1'})
    for row in data:
        print(f"ROLE row:{row}")
