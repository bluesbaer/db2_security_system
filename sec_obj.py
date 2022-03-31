#!/usr/bin/env python3

## Db2 Security-System
## Version 1.0
## Manfred Wagner
## info@manfred-wagner.at


from datetime import datetime, date

class SecObj():

    def __init__(self):
        self.id:int          = 0
        self.schema:str      = ""
        self.name:str        = ""
        self.start:date      = "2999-12-30"
        self.end:date        = "2999-12-31"
        self.mark:str        = "U"
        self.connect:str     = ""
        self.description:str = ""
        self.type:str        = ""
        self.specific:str    = ""
        # ----------------------------------------
        self.parent:int      = 0
        self.child:int       = 0
        self.ctlauth:str     = 'N'
        self.delauth:str     = 'N'
        self.insauth:str     = 'N'
        self.selauth:str     = 'N'
        self.updauth:str     = 'N'
        self.exeauth:str     = 'N'
        self.useauth:str     = 'N'
        self.schadm:str      = 'N'
        self.schsec:str      = 'N'

    def check_int(self,val:int) -> int:
        tmp:int = 0
        if type(val) == int:
            tmp = val
        else:
            try:
                tmp = int(val)
            except:
                tmp = 0
        return tmp

    def check_str(self,val:str) -> str:
        tmp:str = ""
        if type(val) == str:
            tmp = val.upper()
        return tmp

    def check_date(self,val:date,mode:str = 'end') -> date:
        tmp:date = (2999, 12, 30)
        try:
            _ = val.split("-")
            tmp = date(int(_[0]), int(_[1]), int(_[2]))
        except:
            if mode == 'start':
                tmp = date(2999, 12, 30)
            else:
                tmp = date(2999, 12, 31)
        return tmp

    def check_mark(self,val):
        tmp:str = 'U'
        if type(val) == str:
            if val.upper() in ('A','C','S','U'):
                tmp = val.upper()
        return tmp

    def check_roletype(self,val):
        tmp:str = 'R'
        if type(val) == str:
            if val.upper() in ['R','L']:
                tmp = val.upper()
        return tmp

    def check_routype(self,val):
        tmp:str = 'F'
        if type(val) == str:
            if val.upper() in ['F','P']:
                tmp = val.upper()
        return tmp

    def check_YN(self,val):
        tmp:str = 'N'
        if type(val) == str:
            if val.upper() in ['Y','N']:
                tmp = val.upper()
        return tmp

    def new_obj(self):
        print(f"*** NEW_OBJ IS NOT IMPLEMENTED ***")

# --------------------------------------------------------------------------------
# -- SecUsr                                                                     --
# --------------------------------------------------------------------------------
class SecUsr(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def USR_ID(self):
        return self.id
    
    @USR_ID.setter
    def USR_ID(self,val):
        self.id = self.check_int(val)

    @property
    def USR_NAME(self):
        return self.name 

    @USR_NAME.setter
    def USR_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def USR_START(self):
        return self.start 
    
    @USR_START.setter 
    def USR_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def USR_END(self):
        return self.end

    @USR_END.setter
    def USR_END(self,val):
        self.end = self.check_date(val,'end')
    
    @property
    def USR_MARK(self):
        return self.mark

    @USR_MARK.setter
    def USR_MARK(self,val):
        self.mark = self.check_mark(val)

    @property
    def USR_CONNECT(self):
        return self.connect 

    @USR_CONNECT.setter
    def USR_CONNECT(self,val):
        self.connect = self.check_str(val)

    def __str__(self):
        return f"{self.id},{self.name},{self.start},{self.end},{self.mark},{self.connect}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecRol                                                                     --
# --------------------------------------------------------------------------------
class SecRol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def ROL_ID(self):
        return self.id
    
    @ROL_ID.setter
    def ROL_ID(self,val):
        self.id = self.check_int(val)

    @property
    def ROL_NAME(self):
        return self.name 

    @ROL_NAME.setter
    def ROL_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def ROL_START(self):
        return self.start 
    
    @ROL_START.setter 
    def ROL_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def ROL_END(self):
        return self.end

    @ROL_END.setter
    def ROL_END(self,val):
        self.end = self.check_date(val,'end')
    
    @property
    def ROL_DESCRIPTION(self):
        return self.description

    @ROL_DESCRIPTION.setter
    def ROL_DESCRIPTION(self,val):
        self.description = self.check_str(val)

    @property
    def ROL_TYPE(self):
        return self.type 

    @ROL_TYPE.setter
    def ROL_TYPE(self,val):
        self.type = self.check_roletype(val)

    def __str__(self):
        return f"{self.id},{self.name},{self.start},{self.end},{self.description},{self.type}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecSch                                                                     --
# --------------------------------------------------------------------------------
class SecSch(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def SCH_ID(self):
        return self.id
    
    @SCH_ID.setter
    def SCH_ID(self,val):
        self.id = self.check_int(val)

    @property
    def SCH_NAME(self):
        return self.name 

    @SCH_NAME.setter
    def SCH_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def SCH_START(self):
        return self.start 
    
    @SCH_START.setter 
    def SCH_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def SCH_END(self):
        return self.end

    @SCH_END.setter
    def SCH_END(self,val):
        self.end = self.check_date(val,'end')
    
    def __str__(self):
        return f"{self.id},{self.name},{self.start},{self.end}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecTbl                                                                     --
# --------------------------------------------------------------------------------
class SecTbl(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def TBL_ID(self):
        return self.id
    
    @TBL_ID.setter
    def TBL_ID(self,val):
        self.id = self.check_int(val)

    @property
    def TBL_SCHEMA(self):
        return self.schema  

    @TBL_SCHEMA.setter
    def TBL_SCHEMA(self,val):
        self.schema = self.check_str(val)

    @property
    def TBL_NAME(self):
        return self.name 

    @TBL_NAME.setter
    def TBL_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def TBL_START(self):
        return self.start 
    
    @TBL_START.setter 
    def TBL_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def TBL_END(self):
        return self.end

    @TBL_END.setter
    def USR_END(self,val):
        self.end = self.check_date(val,'end')
    
    def __str__(self):
        return f"{self.id},{self.schema},{self.name},{self.start},{self.end}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecRou                                                                     --
# --------------------------------------------------------------------------------
class SecRou(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def ROU_ID(self):
        return self.id
    
    @ROU_ID.setter
    def ROU_ID(self,val):
        self.id = self.check_int(val)

    @property
    def ROU_SCHEMA(self):
        return self.schema 

    @ROU_SCHEMA.setter
    def ROU_SCHEMA(self,val):
        self.schema = self.check_str(val)

    @property
    def ROU_NAME(self):
        return self.name 

    @ROU_NAME.setter
    def ROU_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def ROU_START(self):
        return self.start 
    
    @ROU_START.setter 
    def ROU_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def ROU_END(self):
        return self.end

    @ROU_END.setter
    def ROU_END(self,val):
        self.end = self.check_date(val,'end')
    
    @property
    def ROU_SPECIFIC(self):
        return self.specific

    @ROU_SPECIFIC.setter
    def ROU_SPECIFIC(self,val):
        self.specific = self.check_str(val)

    @property
    def ROU_TYPE(self):
        return self.type 

    @ROU_TYPE.setter
    def ROU_TYPE(self,val):
        self.type = self.check_routype(val)

    def __str__(self):
        return f"{self.id},{self.schema},{self.name},{self.start},{self.end},{self.specific},{self.type}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecSeq                                                                     --
# --------------------------------------------------------------------------------
class SecSeq(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def SEQ_ID(self):
        return self.id
    
    @SEQ_ID.setter
    def SEQ_ID(self,val):
        self.id = self.check_int(val)

    @property
    def SEQ_SCHEMA(self):
        return self.schema

    @SEQ_SCHEMA.setter
    def SEQ_SCHEMA(self,val):
        self.schema = self.check_str(val)

    @property
    def SEQ_NAME(self):
        return self.name 

    @SEQ_NAME.setter
    def SEQ_NAME(self,val):
        self.name = self.check_str(val)

    @property
    def SEQ_START(self):
        return self.start 
    
    @SEQ_START.setter 
    def SEQ_START(self,val):
        self.start = self.check_date(val,'start')

    @property
    def SEQ_END(self):
        return self.end

    @SEQ_END.setter
    def SEQ_END(self,val):
        self.end = self.check_date(val,'end')
    
    def __str__(self):
        return f"{self.id},{self.schema},{self.name},{self.start},{self.end}"
    
    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecUsr2Rol                                                                 --
# --------------------------------------------------------------------------------
class SecUsr2Rol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def U2R_ID(self):
        return self.id
    
    @U2R_ID.setter
    def U2R_ID(self,val):
        self.id = self.check_int(val)

    @property
    def U2R_USR_ID(self):
        return self.child
    
    @U2R_USR_ID.setter
    def U2R_USR_ID(self,val):
        self.child = self.check_int(val)

    @property
    def U2R_ROL_ID(self):
        return self.parent
    
    @U2R_ROL_ID.setter
    def U2R_ROL_ID(self,val):
        self.parent = self.check_int(val)

    @property
    def U2R_START(self):
        return self.start
    
    @U2R_START.setter
    def U2R_START(self,val):
        self.start = self.check_date(val)


    @property
    def U2R_END(self):
        return self.end
    
    @U2R_END.setter
    def U2R_END(self,val):
        self.end = self.check_date(val)

    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecSch2Rol                                                                 --
# --------------------------------------------------------------------------------
class SecSch2Rol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def S2R_ID(self):
        return self.id
    
    @S2R_ID.setter
    def S2R_ID(self,val):
        self.id = self.check_int(val)

    @property
    def S2R_SCH_ID(self):
        return self.child
    
    @S2R_SCH_ID.setter
    def S2R_SCH_ID(self,val):
        self.child = self.check_int(val)

    @property
    def S2R_ROL_ID(self):
        return self.parent
    
    @S2R_ROL_ID.setter
    def S2R_ROL_ID(self,val):
        self.parent = self.check_int(val)

    @property
    def S2R_START(self):
        return self.start
    
    @S2R_START.setter
    def S2R_START(self,val):
        self.start = self.check_date(val)


    @property
    def S2R_END(self):
        return self.end
    
    @S2R_END.setter
    def S2R_END(self,val):
        self.end = self.check_date(val)

    @property 
    def S2R_SCHADM(self):
        return self.schadm

    @S2R_SCHADM.setter 
    def S2R_SCHADM(self,val):
        self.schadm = self.check_YN(val)

    @property 
    def S2R_SCHSEC(self):
        return self.schsec

    @S2R_SCHSEC.setter 
    def S2R_SCHSEC(self,val):
        self.schsec = self.check_YN(val)

    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecTbl2Rol                                                                 --
# --------------------------------------------------------------------------------
class SecTbl2Rol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def T2R_ID(self):
        return self.id
    
    @T2R_ID.setter
    def T2R_ID(self,val):
        self.id = self.check_int(val)

    @property
    def T2R_TBL_ID(self):
        return self.child
    
    @T2R_TBL_ID.setter
    def T2R_TBL_ID(self,val):
        self.child = self.check_int(val)

    @property
    def T2R_ROL_ID(self):
        return self.parent
    
    @T2R_ROL_ID.setter
    def T2R_ROL_ID(self,val):
        self.parent = self.check_int(val)

    @property
    def T2R_START(self):
        return self.start
    
    @T2R_START.setter
    def T2R_START(self,val):
        self.start = self.check_date(val)


    @property
    def T2R_END(self):
        return self.end
    
    @T2R_END.setter
    def T2R_END(self,val):
        self.end = self.check_date(val)

    @property
    def T2R_CTLAUTH(self):
        return self.ctlauth
    
    @T2R_CTLAUTH.setter 
    def T2R_CTLAUTH(self,val):
        self.ctlauth = self.check_YN(val)

    @property
    def T2R_DELAUTH(self):
        return self.delauth
    
    @T2R_DELAUTH.setter 
    def T2R_DELAUTH(self,val):
        self.delauth = self.check_YN(val)

    @property
    def T2R_INSAUTH(self):
        return self.insauth
    
    @T2R_INSAUTH.setter 
    def T2R_INSAUTH(self,val):
        self.insauth = self.check_YN(val)

    @property
    def T2R_SELAUTH(self):
        return self.selauth
    
    @T2R_SELAUTH.setter 
    def T2R_SELAUTH(self,val):
        self.selauth = self.check_YN(val)

    @property
    def T2R_UPDAUTH(self):
        return self.updauth
    
    @T2R_UPDAUTH.setter 
    def T2R_UPDAUTH(self,val):
        self.updauth = self.check_YN(val)

    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecRou2Rol                                                                 --
# --------------------------------------------------------------------------------
class SecRou2Rol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def R2R_ID(self):
        return self.id
    
    @R2R_ID.setter
    def R2R_ID(self,val):
        self.id = self.check_int(val)

    @property
    def R2R_ROU_ID(self):
        return self.child
    
    @R2R_ROU_ID.setter
    def R2R_ROU_ID(self,val):
        self.child = self.check_int(val)

    @property
    def R2R_ROL_ID(self):
        return self.parent
    
    @R2R_ROL_ID.setter
    def R2R_ROL_ID(self,val):
        self.parent = self.check_int(val)

    @property
    def R2R_START(self):
        return self.start
    
    @R2R_START.setter
    def R2R_START(self,val):
        self.start = self.check_date(val)

    @property
    def R2R_END(self):
        return self.end
    
    @R2R_END.setter
    def R2R_END(self,val):
        self.end = self.check_date(val)

    @property 
    def R2R_EXEAUTH(self):
        return self.exeauth

    @R2R_EXEAUTH.setter
    def R2R_EXEAUTH(self,val):
        self.exeauth = self.check_YN(val)

    def new_obj(self):
        return self

    def __del__(self):
        pass


# --------------------------------------------------------------------------------
# -- SecSeq2Rol                                                                 --
# --------------------------------------------------------------------------------
class SecSeq2Rol(SecObj):

    def __init__(self):
        super().__init__()

    @property
    def S2R_ID(self):
        return self.id
    
    @S2R_ID.setter
    def S2R_ID(self,val):
        self.id = self.check_int(val)

    @property
    def S2R_SEQ_ID(self):
        return self.child
    
    @S2R_SEQ_ID.setter
    def S2R_SEQ_ID(self,val):
        self.child = self.check_int(val)

    @property
    def S2R_ROL_ID(self):
        return self.parent
    
    @S2R_ROL_ID.setter
    def S2R_ROL_ID(self,val):
        self.parent = self.check_int(val)

    @property
    def S2R_START(self):
        return self.start
    
    @S2R_START.setter
    def S2R_START(self,val):
        self.start = self.check_date(val)


    @property
    def S2R_END(self):
        return self.end
    
    @S2R_END.setter
    def S2R_END(self,val):
        self.end = self.check_date(val)

    @property 
    def S2R_USEAUTH(self):
        return self.useauth

    @S2R_USEAUTH.setter
    def S2R_USEAUTH(self,val):
        self.useauth = self.check_YN(val)

    def new_obj(self):
        return self

    def __del__(self):
        pass





# --------------------------------------------------------------------------------
# -- TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST --
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    usr = SecUsr()
    print(f"User Empty:{usr}")
    usr.USR_NAME = 'karl'
    print(f"Name:{usr} / written in lowercase")
    usr.USR_START = '2021-02-30'
    print(f"Date:{usr} / 2021-02-30")
    usr.USR_START = '2021-O1-30'
    print(f"Date:{usr} / 2021-O1-30 ? 0 = O")
    usr.USR_START = '2021-05-01'
    print(f"Date:{usr} / 2021-05-01")
    usr.USR_MARK = 'X'
    print(f"Mark:{usr} / X")
    usr.USR_MARK = 'C'
    print(f"Mark:{usr} / C")
    # --------------------------------------------------------------------------------
    rol = SecRol()
    print(f"Role Empty:{rol}")
    rol.ROL_ID = 10
    rol.ROL_NAME = 'dummy1'
    rol.ROL_DESCRIPTION = 'It is so silly'
    rol.ROL_TYPE = 'x'
    print(f"Role:{rol}")
    # --------------------------------------------------------------------------------
    sch = SecSch()
    print(f"Schema Empty:{sch}")
    sch.SCH_ID = 20
    sch.SCH_NAME = 'eis'
    print(f"Schema:{sch}")
    # --------------------------------------------------------------------------------
    tbl = SecTbl()
    print(f"Table Empty:{tbl}")
    tbl.TBL_ID = 30
    tbl.TBL_SCHEMA = 'eis'
    tbl.TBL_NAME = 'person'
    print(f"Table:{tbl}")
    # --------------------------------------------------------------------------------
    rou = SecRou()
    print(f"Routine Empty:{rou}")
    rou.ROU_ID = 40
    rou.ROU_SCHEMA = 'eis'
    rou.ROU_NAME = 'adress'
    rou.ROU_SPECIFIC = 'adress_simple'
    rou.ROU_TYPE = 'f'
    print(f"Routine:{rou}")
    # --------------------------------------------------------------------------------
    seq = SecSeq()
    print(f"Sequence Empty:{seq}")
    seq.SEQ_ID = 50
    seq.SEQ_SCHEMA = 'eis'
    seq.SEQ_NAME = 'person_id'
    print(f"Sequence:{seq}")


