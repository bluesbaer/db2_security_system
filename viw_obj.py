#!/usr/bin/env python3

## Db2 Security-System
## Version 1.0
## Manfred Wagner
## info@manfred-wagner.at


import tkinter as tk
from tkinter import ttk, simpledialog
import ctl_obj
import sec_db2

class Gui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.root = self
        self.root.title('Database Security System by M. Wagner')


# --------------------------------------------------------------------------------
# -- GuiUsr                                                                     --
# --------------------------------------------------------------------------------
class GuiUsr():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlUsr(conn)

    def build(self,anchor):
        user_edit = ttk.LabelFrame(anchor,text='User Edit')
        user_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(user_edit,text='User Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('W'))
        self.usr_nam_cmb = ttk.Combobox(user_edit)
        self.usr_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_nam_cmb.bind("<<ComboboxSelected>>",self.read_user_record)
        ttk.Label(user_edit,text='User Mark:').grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_mrk_cmb = ttk.Combobox(user_edit,values=('A','C','S','U'))
        self.usr_mrk_cmb.grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(user_edit,text='User Connect:').grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_con_ent = ttk.Entry(user_edit)
        self.usr_con_ent.grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(user_edit,text='User Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_sta_ent = ttk.Entry(user_edit)
        self.usr_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(user_edit,text='User End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_end_ent = ttk.Entry(user_edit)
        self.usr_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(user_edit,text='SAVE',command=self.save_user).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(user_edit,text='DELETE',command=self.delete_user).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_user()
        self.read_user_list()
        self.usr_nam_cmb.focus_set()
        user_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.usr_nam_cmb.set('')
        self.usr_mrk_cmb.set('')
        self.usr_con_ent.delete(0,'end')
        self.usr_sta_ent.delete(0,'end')
        self.usr_end_ent.delete(0,'end')

    def read_user(self):
        self.ctltyp.read_data()

    def read_user_list(self):
        usr_name_list:list = []
        usr_name_list = self.ctltyp.get_data_list('USR_NAME',{})
        self.usr_nam_cmb['values'] = usr_name_list
    
    def read_user_record(self,event_object):
        sel_name = event_object.widget.get()
        self.clear_screen()
        user_record = self.ctltyp.get_data_record({'USR_NAME':sel_name})
        self.usr_id = user_record[0].USR_ID
        self.usr_nam_cmb.set(sel_name)
        self.usr_mrk_cmb.set(user_record[0].USR_MARK)
        self.usr_con_ent.insert(0,user_record[0].USR_CONNECT)
        self.usr_sta_ent.insert(0,user_record[0].USR_START)
        self.usr_end_ent.insert(0,user_record[0].USR_END)
    
    def save_user(self):
        user_name = self.usr_nam_cmb.get()
        user_mark = self.usr_mrk_cmb.get()
        user_connect = self.usr_con_ent.get()
        user_start = self.usr_sta_ent.get()
        user_end = self.usr_end_ent.get()
        try:
            x = self.usr_id
        except:
            self.usr_id = 0
        record:dict = {'USR_ID':self.usr_id,'USR_NAME':user_name.upper(),'USR_START':user_start,'USR_END':user_end,\
            'USR_MARK':user_mark.upper(),'USR_CONNECT':user_connect.upper()}
        #self.ctltyp.write_user(record)
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_user_list()

    def delete_user(self):
        #self.ctltyp.delete_user(self.usr_id)
        self.ctltyp.delete_data(self.usr_id)
        self.clear_screen()
        self.read_user_list()


# --------------------------------------------------------------------------------
# -- GuiRol                                                                     --
# --------------------------------------------------------------------------------
class GuiRol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlRol(conn)

    def build(self,anchor):
        role_edit = ttk.LabelFrame(anchor,text='Role Edit')
        role_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(role_edit,text='Role Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('W'))
        self.rol_nam_cmb = ttk.Combobox(role_edit)
        self.rol_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_role_record)
        ttk.Label(role_edit,text='Role Type:').grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_typ_cmb = ttk.Combobox(role_edit,values=('R','L'),state='readonly')
        self.rol_typ_cmb.grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(role_edit,text='Role Description:').grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_des_ent = ttk.Entry(role_edit)
        self.rol_des_ent.grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(role_edit,text='Role Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_sta_ent = ttk.Entry(role_edit)
        self.rol_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(role_edit,text='Role End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_end_ent = ttk.Entry(role_edit)
        self.rol_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(role_edit,text='SAVE',command=self.save_role).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(role_edit,text='DELETE',command=self.delete_role).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_role()
        self.read_role_list()
        self.rol_nam_cmb.focus_set()
        role_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.rol_nam_cmb.set('')
        self.rol_typ_cmb.set('')
        self.rol_des_ent.delete(0,'end')
        self.rol_sta_ent.delete(0,'end')
        self.rol_end_ent.delete(0,'end')

    def read_role(self):
        self.ctltyp.read_data()

    def read_role_list(self):
        rol_name_list:list = []
        rol_name_list = self.ctltyp.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = rol_name_list
    
    def read_role_record(self,event_object):
        sel_name = event_object.widget.get()
        self.clear_screen()
        role_record = self.ctltyp.get_data_record({'ROL_NAME':sel_name})
        self.rol_id = role_record[0].ROL_ID
        self.rol_nam_cmb.set(sel_name)
        self.rol_typ_cmb.set(role_record[0].ROL_TYPE)
        self.rol_sta_ent.insert(0,role_record[0].ROL_START)
        self.rol_end_ent.insert(0,role_record[0].ROL_END)
        self.rol_des_ent.insert(0,role_record[0].ROL_DESCRIPTION)

    def save_role(self):
        role_name = self.rol_nam_cmb.get()
        role_type = self.rol_typ_cmb.get()
        role_description = self.rol_des_ent.get()
        role_start = self.rol_sta_ent.get()
        role_end = self.rol_end_ent.get()
        try:
            x = self.rol_id
        except:
            self.rol_id = 0
        record:dict = {'ROL_ID':self.rol_id,'ROL_NAME':role_name.upper(),'ROL_START':role_start,'ROL_END':role_end,\
            'ROL_DESCRIPTION':role_description.upper(),'ROL_TYPE':role_type.upper()}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_role_list()

    def delete_role(self):
        self.ctltyp.delete_data(self.rol_id)
        self.clear_screen()
        self.read_role_list()


# --------------------------------------------------------------------------------
# -- GuiSch                                                                     --
# --------------------------------------------------------------------------------
class GuiSch():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlSch(conn)

    def build(self,anchor):
        schema_edit = ttk.LabelFrame(anchor,text='Schema Edit')
        schema_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(schema_edit,text='Schema Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('W'))
        self.sch_nam_cmb = ttk.Combobox(schema_edit)
        self.sch_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.sch_nam_cmb.bind("<<ComboboxSelected>>",self.read_schema_record)
        ttk.Label(schema_edit,text='Schema Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.sch_sta_ent = ttk.Entry(schema_edit)
        self.sch_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(schema_edit,text='Schema End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.sch_end_ent = ttk.Entry(schema_edit)
        self.sch_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(schema_edit,text='SAVE',command=self.save_schema).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(schema_edit,text='DELETE',command=self.delete_schema).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_schema()
        self.read_schema_list()
        self.sch_nam_cmb.focus_set()
        schema_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.sch_nam_cmb.set('')
        self.sch_sta_ent.delete(0,'end')
        self.sch_end_ent.delete(0,'end')

    def read_schema(self):
        self.ctltyp.read_data()

    def read_schema_list(self):
        sch_name_list:list = []
        sch_name_list = self.ctltyp.get_data_list('SCH_NAME',{})
        self.sch_nam_cmb['values'] = sch_name_list
    
    def read_schema_record(self,event_object):
        sel_name = event_object.widget.get()
        self.clear_screen()
        schema_record = self.ctltyp.get_data_record({'SCH_NAME':sel_name})
        self.sch_id = schema_record[0].SCH_ID
        self.sch_nam_cmb.set(sel_name)
        self.sch_sta_ent.insert(0,schema_record[0].SCH_START)
        self.sch_end_ent.insert(0,schema_record[0].SCH_END)

    def save_schema(self):
        schema_name = self.sch_nam_cmb.get()
        schema_start = self.sch_sta_ent.get()
        schema_end = self.sch_end_ent.get()
        try:
            x = self.sch_id
        except:
            self.sch_id = 0
        record:dict = {'SCH_ID':self.sch_id,'SCH_NAME':schema_name.upper(),'SCH_START':schema_start,'SCH_END':schema_end}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_schema_list()

    def delete_schema(self):
        self.ctltyp.delete_data(self.sch_id)
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiTbl                                                                     --
# --------------------------------------------------------------------------------
class GuiTbl():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlTbl(conn)

    def build(self,anchor):
        table_edit = ttk.LabelFrame(anchor,text='Table Edit')
        table_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(table_edit,text='Table Schema:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.tbl_sch_cmb = ttk.Combobox(table_edit)
        self.tbl_sch_cmb.grid(row=7,column=0,padx=3,pady=3,sticky=('E','W'))
        self.tbl_sch_cmb.bind("<<ComboboxSelected>>",self.read_table_list)
        ttk.Label(table_edit,text='Table Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.tbl_nam_cmb = ttk.Combobox(table_edit)
        self.tbl_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.tbl_nam_cmb.bind("<<ComboboxSelected>>",self.read_table_record)
        ttk.Label(table_edit,text='Table Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.tbl_sta_ent = ttk.Entry(table_edit)
        self.tbl_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(table_edit,text='Table End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.tbl_end_ent = ttk.Entry(table_edit)
        self.tbl_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(table_edit,text='SAVE',command=self.save_table).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(table_edit,text='DELETE',command=self.delete_table).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_table()
        self.read_schema_list()
        self.tbl_sch_cmb.focus_set()
        table_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.tbl_sch_cmb.set('')
        self.tbl_nam_cmb.set('')
        #self.tbl_typ_cmb.set('')
        #self.tbl_des_ent.delete(0,'end')
        self.tbl_sta_ent.delete(0,'end')
        self.tbl_end_ent.delete(0,'end')

    def read_table(self):
        self.ctltyp.read_data()

    def read_schema_list(self):
        tbl_schema_list:list = []
        tbl_schema_list = self.ctltyp.get_data_list('TBL_SCHEMA',{})
        self.tbl_sch_cmb['values'] = tbl_schema_list

    def read_table_list(self,event_object):
        tbl_name_list:list = []
        tmp_name = event_object.widget.get()
        tbl_name_list = self.ctltyp.get_data_list('TBL_NAME',{'TBL_SCHEMA':tmp_name})
        self.tbl_nam_cmb['values'] = tbl_name_list
        self.clear_screen()
        self.tbl_sch_cmb.set(tmp_name)
    
    def read_table_record(self,event_object):
        sel_name = event_object.widget.get()
        sel_schema = self.tbl_sch_cmb.get()
        self.clear_screen()
        table_record = self.ctltyp.get_data_record({'TBL_SCHEMA':sel_schema,'TBL_NAME':sel_name})
        self.tbl_id = table_record[0].TBL_ID
        self.tbl_sch_cmb.set(sel_schema)
        self.tbl_nam_cmb.set(sel_name)
        #self.tbl_typ_cmb.set(role_record[0].ROL_TYPE)
        self.tbl_sta_ent.insert(0,table_record[0].TBL_START)
        self.tbl_end_ent.insert(0,table_record[0].TBL_END)
        #self.tbl_des_ent.insert(0,role_record[0].ROL_DESCRIPTION)

    def save_table(self):
        table_name = self.tbl_nam_cmb.get()
        table_schema = self.tbl_sch_cmb.get()
        #table_description = self.tbl_des_ent.get()
        table_start = self.tbl_sta_ent.get()
        table_end = self.tbl_end_ent.get()
        try:
            x = self.tbl_id
        except:
            self.tbl_id = 0
        record:dict = {'TBL_ID':self.tbl_id,'TBL_SCHEMA':table_schema.upper(),'TBL_NAME':table_name.upper(),'TBL_START':table_start,'TBL_END':table_end}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_schema_list()

    def delete_table(self):
        self.ctltyp.delete_data(self.tbl_id)
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiRou                                                                     --
# --------------------------------------------------------------------------------
class GuiRou():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlRou(conn)

    def build(self,anchor):
        routine_edit = ttk.LabelFrame(anchor,text='Routine Edit')
        routine_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(routine_edit,text='Routine Schema:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.rou_sch_cmb = ttk.Combobox(routine_edit)
        self.rou_sch_cmb.grid(row=7,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_sch_cmb.bind("<<ComboboxSelected>>",self.read_name_list)
        ttk.Label(routine_edit,text='Routine Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_nam_cmb = ttk.Combobox(routine_edit)
        self.rou_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_nam_cmb.bind("<<ComboboxSelected>>",self.read_specific_list)

        ttk.Label(routine_edit,text='Specific Name:').grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_spe_cmb = ttk.Combobox(routine_edit)
        self.rou_spe_cmb.grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_spe_cmb.bind("<<ComboboxSelected>>",self.read_routine_record)
        ttk.Label(routine_edit,text='Routine Type:').grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_typ_cmb = ttk.Combobox(routine_edit,values=('F','P'),state='readonly')
        self.rou_typ_cmb.grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))

        ttk.Label(routine_edit,text='Table Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_sta_ent = ttk.Entry(routine_edit)
        self.rou_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(routine_edit,text='Table End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_end_ent = ttk.Entry(routine_edit)
        self.rou_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(routine_edit,text='SAVE',command=self.save_routine).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(routine_edit,text='DELETE',command=self.delete_routine).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_routine()
        self.read_schema_list()
        self.rou_sch_cmb.focus_set()
        routine_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.rou_sch_cmb.set('')
        self.rou_nam_cmb.set('')
        self.rou_typ_cmb.set('')
        self.rou_spe_cmb.delete(0,'end')
        self.rou_sta_ent.delete(0,'end')
        self.rou_end_ent.delete(0,'end')

    def read_routine(self):
        self.ctltyp.read_data()

    def read_schema_list(self):
        rou_schema_list:list = []
        rou_schema_list = self.ctltyp.get_data_list('ROU_SCHEMA',{})
        self.rou_sch_cmb['values'] = rou_schema_list

    def read_name_list(self,event_object):
        rou_name_list:list = []
        tmp_name = event_object.widget.get()
        rou_name_list = self.ctltyp.get_data_list('ROU_NAME',{'ROU_SCHEMA':tmp_name})
        self.rou_nam_cmb['values'] = rou_name_list
        self.clear_screen()
        self.rou_sch_cmb.set(tmp_name)

    def read_specific_list(self,event_object):
        rou_specific_list:list = []
        tmp_name = event_object.widget.get()
        tmp_schema = self.rou_sch_cmb.get()
        rou_specific_list = self.ctltyp.get_data_list('ROU_SPECIFIC',{'ROU_SCHEMA':tmp_schema,'ROU_NAME':tmp_name})
        self.rou_spe_cmb['values'] = rou_specific_list
        self.clear_screen()
        self.rou_sch_cmb.set(tmp_schema)
        self.rou_nam_cmb.set(tmp_name)
    
    def read_routine_record(self,event_object):
        sel_name = self.rou_nam_cmb.get()
        sel_schema = self.rou_sch_cmb.get()
        sel_specific = event_object.widget.get()
        self.clear_screen()
        routine_record = self.ctltyp.get_data_record({'ROU_SCHEMA':sel_schema,'ROU_NAME':sel_name,'ROU_SPECIFIC':sel_specific})
        self.rou_id = routine_record[0].ROU_ID
        self.rou_sch_cmb.set(sel_schema)
        self.rou_nam_cmb.set(sel_name)
        self.rou_typ_cmb.set(routine_record[0].ROU_TYPE)
        self.rou_sta_ent.insert(0,routine_record[0].ROU_START)
        self.rou_end_ent.insert(0,routine_record[0].ROU_END)
        self.rou_spe_cmb.insert(0,routine_record[0].ROU_SPECIFIC)

    def save_routine(self):
        routine_name = self.rou_nam_cmb.get()
        routine_schema = self.rou_sch_cmb.get()
        routine_specific = self.rou_spe_cmb.get()
        routine_type = self.rou_typ_cmb.get()
        routine_start = self.rou_sta_ent.get()
        routine_end = self.rou_end_ent.get()
        try:
            x = self.rou_id
        except:
            self.rou_id = 0
        record:dict = {'ROU_ID':self.rou_id,'ROU_SCHEMA':routine_schema.upper(),'ROU_NAME':routine_name.upper(),\
            'ROU_START':routine_start,'ROU_END':routine_end,'ROU_SPECIFIC':routine_specific.upper(),'ROU_TYPE':routine_type}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_schema_list()

    def delete_routine(self):
        self.ctltyp.delete_data(self.rou_id)
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiSeq                                                                     --
# --------------------------------------------------------------------------------
class GuiSeq():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlSeq(conn)

    def build(self,anchor):
        sequence_edit = ttk.LabelFrame(anchor,text='Sequence Edit')
        sequence_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(sequence_edit,text='Sequence Schema:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.seq_sch_cmb = ttk.Combobox(sequence_edit)
        self.seq_sch_cmb.grid(row=7,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_sch_cmb.bind("<<ComboboxSelected>>",self.read_sequence_list)
        ttk.Label(sequence_edit,text='Sequence Name:').grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_nam_cmb = ttk.Combobox(sequence_edit)
        self.seq_nam_cmb.grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_nam_cmb.bind("<<ComboboxSelected>>",self.read_sequence_record)
        ttk.Label(sequence_edit,text='Sequence Start:').grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_sta_ent = ttk.Entry(sequence_edit)
        self.seq_sta_ent.grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(sequence_edit,text='Sequence End:').grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_end_ent = ttk.Entry(sequence_edit)
        self.seq_end_ent.grid(row=55,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(sequence_edit,text='SAVE',command=self.save_sequence).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(sequence_edit,text='DELETE',command=self.delete_sequence).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_sequence()
        self.read_schema_list()
        self.seq_sch_cmb.focus_set()
        sequence_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.seq_sch_cmb.set('')
        self.seq_nam_cmb.set('')
        self.seq_sta_ent.delete(0,'end')
        self.seq_end_ent.delete(0,'end')

    def read_sequence(self):
        self.ctltyp.read_data()

    def read_schema_list(self):
        seq_schema_list:list = []
        seq_schema_list = self.ctltyp.get_data_list('SEQ_SCHEMA',{})
        self.seq_sch_cmb['values'] = seq_schema_list

    def read_sequence_list(self,event_object):
        seq_name_list:list = []
        tmp_name = event_object.widget.get()
        seq_name_list = self.ctltyp.get_data_list('SEQ_NAME',{'SEQ_SCHEMA':tmp_name})
        self.seq_nam_cmb['values'] = seq_name_list
        self.clear_screen()
        self.seq_sch_cmb.set(tmp_name)
    
    def read_sequence_record(self,event_object):
        sel_name = event_object.widget.get()
        sel_schema = self.seq_sch_cmb.get()
        self.clear_screen()
        sequence_record = self.ctltyp.get_data_record({'SEQ_SCHEMA':sel_schema,'SEQ_NAME':sel_name})
        self.seq_id = sequence_record[0].SEQ_ID
        self.seq_sch_cmb.set(sel_schema)
        self.seq_nam_cmb.set(sel_name)
        self.seq_sta_ent.insert(0,sequence_record[0].SEQ_START)
        self.seq_end_ent.insert(0,sequence_record[0].SEQ_END)

    def save_sequence(self):
        sequence_name = self.seq_nam_cmb.get()
        sequence_schema = self.seq_sch_cmb.get()
        sequence_start = self.seq_sta_ent.get()
        sequence_end = self.seq_end_ent.get()
        try:
            x = self.seq_id
        except:
            self.seq_id = 0
        record:dict = {'SEQ_ID':self.seq_id,'SEQ_SCHEMA':sequence_schema.upper(),'SEQ_NAME':sequence_name.upper(),\
            'SEQ_START':sequence_start,'SEQ_END':sequence_end}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_schema_list()

    def delete_sequence(self):
        self.ctltyp.delete_data(self.seq_id)
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiUsr2Rol                                                                 --
# --------------------------------------------------------------------------------
class GuiUsr2Rol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlUsr2Rol(conn)
        self.ctlchild = ctl_obj.CtlUsr(conn)
        self.ctlparent = ctl_obj.CtlRol(conn)

    def build(self,anchor):
        usr2rol_edit = ttk.LabelFrame(anchor, text='User 2 Role edit')
        usr2rol_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # -- Child_Liste (cmb)
        tk.Label(usr2rol_edit,text='User Name:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.usr_nam_cmb = ttk.Combobox(usr2rol_edit,state='readonly')
        self.usr_nam_cmb.grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.usr_nam_cmb.bind("<<ComboboxSelected>>",self.read_role_list)
        # -- Role_Liste (cmb)
        ttk.Label(usr2rol_edit,text='Role Name:').grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb = ttk.Combobox(usr2rol_edit,state='readonly')
        self.rol_nam_cmb.grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_u2r_record)
        # -- x2R_Attribute
        ttk.Label(usr2rol_edit,text='Start:').grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        self.u2r_sta_ent = ttk.Entry(usr2rol_edit)
        self.u2r_sta_ent.grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(usr2rol_edit,text='End:').grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))
        self.u2r_end_ent = ttk.Entry(usr2rol_edit)
        self.u2r_end_ent.grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(usr2rol_edit,text='SAVE',command=self.save_usr2rol).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(usr2rol_edit,text='DELETE',command=self.delete_usr2rol).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_user_list()
        self.usr_nam_cmb.focus_set()
        usr2rol_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.usr_nam_cmb.set('')
        self.rol_nam_cmb.set('')
        self.u2r_sta_ent.delete(0,'end')
        self.u2r_end_ent.delete(0,'end')

    def read_user_list(self):
        self.ctlchild.read_data()
        usr_name_list:list = []
        usr_name_list = self.ctlchild.get_data_list('USR_NAME',{})
        self.usr_nam_cmb['values'] = usr_name_list

    def read_role_list(self,event_object):
        tmp = event_object.widget.get()
        self.ctlparent.read_data()
        rol_name_list:list = []
        rol_name_list = self.ctlparent.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = rol_name_list
        self.clear_screen()
        self.usr_nam_cmb.set(tmp)

    def read_u2r_record(self,event_object):
        self.ctltyp.read_data()
        sel_role = event_object.widget.get()
        sel_child = self.usr_nam_cmb.get()
        # get ID for child
        user_record = self.ctlchild.get_data_record({'USR_NAME':sel_child})
        self.usr_id = user_record[0].USR_ID
        # get ID for role
        role_record = self.ctlparent.get_data_record({'ROL_NAME':sel_role})
        self.rol_id = role_record[0].ROL_ID
        # get RECORD for usr2rol
        u2r_record = self.ctltyp.get_data_record({'U2R_USR_ID':self.usr_id,'U2R_ROL_ID':self.rol_id})
        self.u2r_sta_ent.delete(0,'end')
        self.u2r_end_ent.delete(0,'end')
        if u2r_record:
            self.u2r_id = u2r_record[0].U2R_ID
            self.u2r_sta_ent.insert(0,u2r_record[0].U2R_START)
            self.u2r_end_ent.insert(0,u2r_record[0].U2R_END)
        else:
            self.u2r_id = 0
            self.u2r_sta_ent.insert(0,'2999-12-30')
            self.u2r_end_ent.insert(0,'2999-12-31')

    def save_usr2rol(self):
        start = self.u2r_sta_ent.get()
        end = self.u2r_end_ent.get()
        try:
            x = self.u2r_id
        except:
            self.u2r_id = 0
        record = {'U2R_ID':self.u2r_id,'U2R_USR_ID':self.usr_id,'U2R_ROL_ID':self.rol_id,'U2R_START':start,'U2R_END':end}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_user_list()

    def delete_usr2rol(self):
        self.ctltyp.delete_data(self.u2r_id)
        self.clear_screen()
        self.read_user_list()


# --------------------------------------------------------------------------------
# -- GuiSch2Rol                                                                 --
# --------------------------------------------------------------------------------
class GuiSch2Rol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlSch2Rol(conn)
        self.ctlchild = ctl_obj.CtlSch(conn)
        self.ctlparent = ctl_obj.CtlRol(conn)
        self.schadm = tk.StringVar()
        self.schsec = tk.StringVar()

    def build(self,anchor):
        sch2rol_edit = ttk.LabelFrame(anchor, text='Schema 2 Role edit')
        sch2rol_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # -- Child_Liste (cmb)
        tk.Label(sch2rol_edit,text='Schema Name:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'),columnspan=2)
        self.sch_nam_cmb = ttk.Combobox(sch2rol_edit,state='readonly')
        self.sch_nam_cmb.grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.sch_nam_cmb.bind("<<ComboboxSelected>>",self.read_role_list)
        # -- Role_Liste (cmb)
        ttk.Label(sch2rol_edit,text='Role Name:').grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.rol_nam_cmb = ttk.Combobox(sch2rol_edit,state='readonly')
        self.rol_nam_cmb.grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_s2r_record)
        # -- x2R_Auth
        ttk.Label(sch2rol_edit,text="Schema-Admin").grid(row=21,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        ttk.Radiobutton(sch2rol_edit,text="Yes:",variable=self.schadm,value='Y').grid(row=22,column=0,padx=3,pady=3,sticky= ('E','W'))
        ttk.Radiobutton(sch2rol_edit,text="No:",variable=self.schadm,value='N').grid(row=22,column=1,padx=3,pady=3,sticky= ('E','W'))
        ttk.Label(sch2rol_edit,text="Schema-Security").grid(row=23,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        ttk.Radiobutton(sch2rol_edit,text="Yes:",variable=self.schsec,value='Y').grid(row=24,column=0,padx=3,pady=3,sticky= ('E','W'))
        ttk.Radiobutton(sch2rol_edit,text="No:",variable=self.schsec,value='N').grid(row=24,column=1,padx=3,pady=3,sticky= ('E','W'))
        # -- x2R_Attribute
        ttk.Label(sch2rol_edit,text='Start:').grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.s2r_sta_ent = ttk.Entry(sch2rol_edit)
        self.s2r_sta_ent.grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        ttk.Label(sch2rol_edit,text='End:').grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.s2r_end_ent = ttk.Entry(sch2rol_edit)
        self.s2r_end_ent.grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        tk.Button(sch2rol_edit,text='SAVE',command=self.save_sch2rol).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        tk.Button(sch2rol_edit,text='DELETE',command=self.delete_sch2rol).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=2)
        self.read_schema_list()
        self.sch_nam_cmb.focus_set()
        sch2rol_edit.columnconfigure(0,weight=1)
        sch2rol_edit.columnconfigure(1,weight=1)

    def clear_screen(self):
        self.sch_nam_cmb.set('')
        self.rol_nam_cmb.set('')
        self.s2r_sta_ent.delete(0,'end')
        self.s2r_end_ent.delete(0,'end')

    def read_schema_list(self):
        self.ctlchild.read_data()
        sch_name_list:list = []
        sch_name_list = self.ctlchild.get_data_list('SCH_NAME',{})
        self.sch_nam_cmb['values'] = sch_name_list

    def read_role_list(self,event_object):
        tmp_schema = event_object.widget.get()
        self.ctlparent.read_data()
        rol_name_list:list = []
        rol_name_list = self.ctlparent.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = rol_name_list
        self.clear_screen()
        self.sch_nam_cmb.set(tmp_schema)
   
    def read_s2r_record(self,event_object):
        tmp_role = event_object.widget.get()
        tmp_schema = self.sch_nam_cmb.get()
        self.ctltyp.read_data()
        # get ID for Schema
        schema_record = self.ctlchild.get_data_record({'SCH_NAME':tmp_schema})
        self.sch_id = schema_record[0].SCH_ID
        # get ID for Role
        role_record = self.ctlparent.get_data_record({'ROL_NAME':tmp_role})
        self.rol_id = role_record[0].ROL_ID
        # get Record
        s2r_record = self.ctltyp.get_data_record({'S2R_SCH_ID':self.sch_id,'S2R_ROL_ID':self.rol_id})
        self.s2r_sta_ent.delete(0,'end')
        self.s2r_end_ent.delete(0,'end')
        if s2r_record:
            self.s2r_id = s2r_record[0].S2R_ID
            self.schadm.set(s2r_record[0].S2R_SCHADM)
            self.schsec.set(s2r_record[0].S2R_SCHSEC)
            self.s2r_sta_ent.insert(0,s2r_record[0].S2R_START)
            self.s2r_end_ent.insert(0,s2r_record[0].S2R_END)
        else:
            self.s2r_id = 0
            self.schadm.set('N')
            self.schsec.set('N')
            self.s2r_sta_ent.insert(0,'2999-12-30')
            self.s2r_end_ent.insert(0,'2999-12-31')

    def save_sch2rol(self):
        start = self.s2r_sta_ent.get()
        end = self.s2r_end_ent.get()
        try:
            x = self.s2r_id
        except:
            self.s2r_id = 0
        record = {'S2R_ID':self.s2r_id,'S2R_SCH_ID':self.sch_id,'S2R_ROL_ID':self.rol_id,'S2R_START':start,\
            'S2R_END':end,'S2R_SCHADM':self.schadm.get(),'S2R_SCHSEC':self.schsec.get()}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.read_schema_list()


    def delete_sch2rol(self):
        self.ctltyp.delete_data(self.s2r_id)
        self.clear_screen()
        self.read_schema_list()




# --------------------------------------------------------------------------------
# -- GuiTbl2Rol                                                                 --
# --------------------------------------------------------------------------------
class GuiTbl2Rol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlTbl2Rol(conn)
        self.ctlchild = ctl_obj.CtlTbl(conn)
        self.ctlparent = ctl_obj.CtlRol(conn)

    def build(self,anchor):
        self.ctlauth = tk.StringVar()
        self.delauth = tk.StringVar()
        self.insauth = tk.StringVar()
        self.selauth = tk.StringVar()
        self.updauth = tk.StringVar()
        self.tbl2rol_edit = ttk.LabelFrame(anchor, text='User 2 Role edit')
        self.tbl2rol_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # -- Child_Liste (cmb)
        tk.Label(self.tbl2rol_edit,text='Table Schema:').grid(row=2,column=0,padx=3,pady=3,sticky=('W'),columnspan=3)
        self.tbl_sch_cmb = ttk.Combobox(self.tbl2rol_edit,state='readonly')
        self.tbl_sch_cmb.grid(row=3,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.tbl_sch_cmb.bind("<<ComboboxSelected>>",self.read_table_list)

        tk.Label(self.tbl2rol_edit,text='Table Name:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'),columnspan=3)
        self.tbl_nam_cmb = ttk.Combobox(self.tbl2rol_edit,state='readonly')
        self.tbl_nam_cmb.grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.tbl_nam_cmb.bind("<<ComboboxSelected>>",self.read_role_list)
        # -- Role_Liste (cmb)
        ttk.Label(self.tbl2rol_edit,text='Role Name:').grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.rol_nam_cmb = ttk.Combobox(self.tbl2rol_edit,state='readonly')
        self.rol_nam_cmb.grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_t2r_record)
        # -- x2R_Auth
        ttk.Label(self.tbl2rol_edit,text='Control').grid(row=21,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='Yes:',variable=self.ctlauth,value='Y',relief='sunken').grid(row=21,column=1,padx=3,pady=3,sticky=('E','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='No:',variable=self.ctlauth,value='N',relief='sunken').grid(row=21,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.tbl2rol_edit,text='Delete').grid(row=23,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='Yes:',variable=self.delauth,value='Y',relief='sunken').grid(row=23,column=1,padx=3,pady=3,sticky=('E','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='No:',variable=self.delauth,value='N',relief='sunken').grid(row=23,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.tbl2rol_edit,text='Insert').grid(row=25,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='Yes:',variable=self.insauth,value='Y',relief='sunken').grid(row=25,column=1,padx=3,pady=3,sticky=('E','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='No:',variable=self.insauth,value='N',relief='sunken').grid(row=25,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.tbl2rol_edit,text='Select').grid(row=27,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='Yes:',variable=self.selauth,value='Y',relief='sunken').grid(row=27,column=1,padx=3,pady=3,sticky=('E','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='No:',variable=self.selauth,value='N',relief='sunken').grid(row=27,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.tbl2rol_edit,text='Update').grid(row=29,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='Yes:',variable=self.updauth,value='Y',relief='sunken').grid(row=29,column=1,padx=3,pady=3,sticky=('E','W'))
        tk.Radiobutton(self.tbl2rol_edit,text='No:',variable=self.updauth,value='N',relief='sunken').grid(row=29,column=2,padx=3,pady=3,sticky=('E','W'))
        # -- x2R_Attribute
        ttk.Label(self.tbl2rol_edit,text='Start:').grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.t2r_sta_ent = ttk.Entry(self.tbl2rol_edit)
        self.t2r_sta_ent.grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        ttk.Label(self.tbl2rol_edit,text='End:').grid(row=45,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.t2r_end_ent = ttk.Entry(self.tbl2rol_edit)
        self.t2r_end_ent.grid(row=50,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        tk.Button(self.tbl2rol_edit,text='SAVE',command=self.save_tbl2rol).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        tk.Button(self.tbl2rol_edit,text='DELETE',command=self.delete_tbl2rol).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'),columnspan=3)
        self.read_schema_list()
        self.tbl2rol_edit.columnconfigure(0,weight=1)
        self.tbl2rol_edit.columnconfigure(1,weight=1)
        self.tbl2rol_edit.columnconfigure(2,weight=1)

    def clear_screen(self):
        self.tbl_nam_cmb.set('')
        self.rol_nam_cmb.set('')
        self.ctlauth.set('N')
        self.delauth.set('N')
        self.insauth.set('N')
        self.selauth.set('N')
        self.updauth.set('N')
        self.t2r_sta_ent.delete(0,'end')
        self.t2r_end_ent.delete(0,'end')

    def read_schema_list(self):
        self.ctlchild.read_data()
        tbl_schema_list:list = []
        tbl_schema_list = self.ctlchild.get_data_list('TBL_SCHEMA',{})
        self.tbl_sch_cmb['values'] = tbl_schema_list

    def read_table_list(self,event_object):
        tmp_schema = event_object.widget.get()
        tbl_name_list:list = []
        tbl_name_list = self.ctlchild.get_data_list('TBL_NAME',{'TBL_SCHEMA':tmp_schema})
        self.tbl_nam_cmb['values'] = tbl_name_list


    def read_role_list(self,event_object):
        self.ctlparent.read_data()
        tmp_role_list:list = []
        tmp_role_list = self.ctlparent.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = tmp_role_list

    def read_t2r_record(self,event_object):
        tmp_role = event_object.widget.get()
        tmp_schema = self.tbl_sch_cmb.get()
        tmp_name = self.tbl_nam_cmb.get()
        # get ID for Table
        schema_record = self.ctlchild.get_data_record({'TBL_SCHEMA':tmp_schema,'TBL_NAME':tmp_name})
        self.tbl_id = schema_record[0].TBL_ID
        # get ID for Role
        role_record = self.ctlparent.get_data_record({'ROL_NAME':tmp_role})
        self.rol_id = role_record[0].ROL_ID
        # get Record
        self.ctltyp.read_data()
        t2r_record = self.ctltyp.get_data_record({'T2R_TBL_ID':self.tbl_id,'T2R_ROL_ID':self.rol_id})
        self.t2r_sta_ent.delete(0,'end')
        self.t2r_end_ent.delete(0,'end')
        if t2r_record:
            self.t2r_id = t2r_record[0].T2R_ID
            self.ctlauth.set(t2r_record[0].T2R_CTLAUTH)
            self.delauth.set(t2r_record[0].T2R_DELAUTH)
            self.insauth.set(t2r_record[0].T2R_INSAUTH)
            self.selauth.set(t2r_record[0].T2R_SELAUTH)
            self.updauth.set(t2r_record[0].T2R_UPDAUTH)
            self.t2r_sta_ent.insert(0,t2r_record[0].T2R_START)
            self.t2r_end_ent.insert(0,t2r_record[0].T2R_END)
        else:
            self.s2r_id = 0
            self.ctlauth.set('N')
            self.delauth.set('N')
            self.insauth.set('N')
            self.selauth.set('N')
            self.updauth.set('N')
            self.t2r_sta_ent.insert(0,'2999-12-30')
            self.t2r_end_ent.insert(0,'2999-12-31')


    def save_tbl2rol(self):
        start = self.t2r_sta_ent.get()
        end = self.t2r_end_ent.get()
        try:
            x = self.t2r_id
        except:
            self.t2r_id = 0
        record = {'T2R_ID':self.t2r_id,'T2R_TBL_ID':self.tbl_id,'T2R_ROL_ID':self.rol_id,'T2R_START':start,\
            'T2R_END':end,'T2R_CTLAUTH':self.ctlauth.get(),'T2R_DELAUTH':self.delauth.get(),\
            'T2R_INSAUTH':self.insauth.get(),'T2R_SELAUTH':self.selauth.get(),'T2R_UPDAUTH':self.updauth.get()}
        self.ctltyp.write_data(record)
        record = {}
        self.clear_screen()
        self.tbl_sch_cmb.set('')
        self.read_schema_list()

    def delete_tbl2rol(self):
        self.ctltyp.delete_data(self.t2r_id)
        self.tbl_sch_cmb.set('')
        self.clear_screen()
        self.read_schema_list()



# --------------------------------------------------------------------------------
# -- GuiRou2Rol                                                                 --
# --------------------------------------------------------------------------------
class GuiRou2Rol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlRou2Rol(conn)
        self.ctlchild = ctl_obj.CtlRou(conn)
        self.ctlparent = ctl_obj.CtlRol(conn)

    def build(self,anchor):
        rou2rol_edit = ttk.LabelFrame(anchor, text='Routine 2 Role edit')
        rou2rol_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # -- Child_Liste (cmb)
        tk.Label(rou2rol_edit,text='Routine Schema:').grid(row=1,column=0,padx=3,pady=3,sticky=('W'))
        self.rou_sch_cmb = ttk.Combobox(rou2rol_edit,state='readonly')
        self.rou_sch_cmb.grid(row=2,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_sch_cmb.bind("<<ComboboxSelected>>",self.read_name_list)

        tk.Label(rou2rol_edit,text='Routine Name:').grid(row=3,column=0,padx=3,pady=3,sticky=('W'))
        self.rou_nam_cmb = ttk.Combobox(rou2rol_edit,state='readonly')
        self.rou_nam_cmb.grid(row=4,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_nam_cmb.bind("<<ComboboxSelected>>",self.read_specific_list)

        tk.Label(rou2rol_edit,text='Specific Name:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.rou_spe_cmb = ttk.Combobox(rou2rol_edit,state='readonly')
        self.rou_spe_cmb.grid(row=6,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rou_spe_cmb.bind("<<ComboboxSelected>>",self.read_role_list)
        # -- Role_Liste (cmb)
        ttk.Label(rou2rol_edit,text='Role Name:').grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb = ttk.Combobox(rou2rol_edit,state='readonly')
        self.rol_nam_cmb.grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_r2r_record)
        # -- x2R_Attribute
        ttk.Label(rou2rol_edit,text='Start:').grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        self.r2r_sta_ent = ttk.Entry(rou2rol_edit)
        self.r2r_sta_ent.grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(rou2rol_edit,text='End:').grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))
        self.r2r_end_ent = ttk.Entry(rou2rol_edit)
        self.r2r_end_ent.grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(rou2rol_edit,text='SAVE',command=self.save_rou2rol).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(rou2rol_edit,text='DELETE',command=self.delete_rou2rol).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_schema_list()
        rou2rol_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.r2r_sta_ent.delete(0,'end')
        self.r2r_end_ent.delete(0,'end')

    def read_schema_list(self):
        self.ctlchild.read_data()
        rou_schema_list:list = []
        rou_schema_list = self.ctlchild.get_data_list('ROU_SCHEMA',{})
        self.rou_sch_cmb['values'] = rou_schema_list

    def read_name_list(self,event_object):
        tmp_schema = event_object.widget.get()
        rou_name_list:list = []
        rou_name_list = self.ctlchild.get_data_list('ROU_NAME',{'ROU_SCHEMA':tmp_schema})
        self.rou_nam_cmb['values'] = rou_name_list

    def read_specific_list(self,event_object):
        tmp_schema = self.rou_sch_cmb.get()
        tmp_name = event_object.widget.get()
        rou_specific_list:list = []
        rou_specific_list = self.ctlchild.get_data_list('ROU_SPECIFIC',{'ROU_SCHEMA':tmp_schema,'ROU_NAME':tmp_name})
        self.rou_spe_cmb['values'] = rou_specific_list

    def read_role_list(self,event_object):
        self.ctlparent.read_data()
        tmp_role_list:list = []
        tmp_role_list = self.ctlparent.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = tmp_role_list

    def read_r2r_record(self,event_object):
        tmp_role = event_object.widget.get()
        tmp_schema = self.rou_sch_cmb.get()
        tmp_name = self.rou_nam_cmb.get()
        tmp_specific = self.rou_spe_cmb.get()
        # get ID for Routine
        routine_record = self.ctlchild.get_data_record({'ROU_SCHEMA':tmp_schema,'ROU_NAME':tmp_name,'ROU_SPECIFIC':tmp_specific})
        self.rou_id = routine_record[0].ROU_ID
        # get ID for Role
        role_record = self.ctlparent.get_data_record({'ROL_NAME':tmp_role})
        self.rol_id = role_record[0].ROL_ID
        # get Record
        self.ctltyp.read_data()
        r2r_record = self.ctltyp.get_data_record({'R2R_ROU_ID':self.rou_id,'R2R_ROL_ID':self.rol_id})
        self.r2r_sta_ent.delete(0,'end')
        self.r2r_end_ent.delete(0,'end')
        if r2r_record:
            self.r2r_id = r2r_record[0].R2R_ID
            self.r2r_sta_ent.insert(0,r2r_record[0].R2R_START)
            self.r2r_end_ent.insert(0,r2r_record[0].R2R_END)
        else:
            self.r2r_id = 0
            self.r2r_sta_ent.insert(0,'2999-12-30')
            self.r2r_end_ent.insert(0,'2999-12-31')

    def save_rou2rol(self):
        start = self.r2r_sta_ent.get()
        end = self.r2r_end_ent.get()
        try:
            x = self.r2r_id
        except:
            self.r2r_id = 0
        record = {'R2R_ID':self.r2r_id,'R2R_ROU_ID':self.rou_id,'R2R_ROL_ID':self.rol_id,'R2R_START':start,'R2R_END':end}
        self.ctltyp.write_data(record)
        record = {}
        self.rou_sch_cmb.set('')
        self.rou_nam_cmb.set('')
        self.rou_spe_cmb.set('')
        self.clear_screen()
        self.read_schema_list()

    def delete_rou2rol(self):
        self.ctltyp.delete_data(self.r2r_id)
        self.rou_sch_cmb.set('')
        self.rou_nam_cmb.set('')
        self.rou_spe_cmb.set('')
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiSeq2Rol                                                                 --
# --------------------------------------------------------------------------------
class GuiSeq2Rol():

    def __init__(self,conn):
        self.conn   = conn
        self.ctltyp = ctl_obj.CtlSeq2Rol(conn)
        self.ctlchild = ctl_obj.CtlSeq(conn)
        self.ctlparent = ctl_obj.CtlRol(conn)

    def build(self,anchor):
        seq2rol_edit = ttk.LabelFrame(anchor, text='Sequence 2 Role edit')
        seq2rol_edit.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # -- Child_Liste (cmb)
        tk.Label(seq2rol_edit,text='Sequence Schema:').grid(row=5,column=0,padx=3,pady=3,sticky=('W'))
        self.seq_sch_cmb = ttk.Combobox(seq2rol_edit,state='readonly')
        self.seq_sch_cmb.grid(row=7,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_sch_cmb.bind("<<ComboboxSelected>>",self.read_name_list)
        tk.Label(seq2rol_edit,text='Sequence Name:').grid(row=9,column=0,padx=3,pady=3,sticky=('W'))
        self.seq_nam_cmb = ttk.Combobox(seq2rol_edit,state='readonly')
        self.seq_nam_cmb.grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.seq_nam_cmb.bind("<<ComboboxSelected>>",self.read_role_list)
        # -- Role_Liste (cmb)
        ttk.Label(seq2rol_edit,text='Role Name:').grid(row=15,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb = ttk.Combobox(seq2rol_edit,state='readonly')
        self.rol_nam_cmb.grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        self.rol_nam_cmb.bind("<<ComboboxSelected>>",self.read_s2r_record)
        # -- x2R_Attribute
        ttk.Label(seq2rol_edit,text='Start:').grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        self.s2r_sta_ent = ttk.Entry(seq2rol_edit)
        self.s2r_sta_ent.grid(row=30,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(seq2rol_edit,text='End:').grid(row=35,column=0,padx=3,pady=3,sticky=('E','W'))
        self.s2r_end_ent = ttk.Entry(seq2rol_edit)
        self.s2r_end_ent.grid(row=40,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(seq2rol_edit,text='SAVE',command=self.save_seq2rol).grid(row=60,column=0,padx=3,pady=3,sticky=('E','W'))
        tk.Button(seq2rol_edit,text='DELETE',command=self.delete_seq2rol).grid(row=65,column=0,padx=3,pady=3,sticky=('E','W'))
        self.read_schema_list()
        seq2rol_edit.columnconfigure(0,weight=1)

    def clear_screen(self):
        self.s2r_sta_ent.delete(0,'end')
        self.s2r_end_ent.delete(0,'end')
        pass

    def read_schema_list(self):
        self.ctlchild.read_data()
        seq_schema_list:list = []
        seq_schema_list = self.ctlchild.get_data_list('SEQ_SCHEMA',{})
        self.seq_sch_cmb['values'] = seq_schema_list

    def read_name_list(self,event_object):
        tmp_schema = event_object.widget.get()
        seq_name_list:list = []
        seq_name_list = self.ctlchild.get_data_list('SEQ_NAME',{'SEQ_SCHEMA':tmp_schema})
        self.seq_nam_cmb['values'] = seq_name_list

    def read_role_list(self,event_object):
        self.ctlparent.read_data()
        tmp_role_list:list = []
        tmp_role_list = self.ctlparent.get_data_list('ROL_NAME',{})
        self.rol_nam_cmb['values'] = tmp_role_list

    def read_s2r_record(self,event_object):
        tmp_role = event_object.widget.get()
        tmp_schema = self.seq_sch_cmb.get()
        tmp_name = self.seq_nam_cmb.get()
        # get ID for Routine
        sequence_record = self.ctlchild.get_data_record({'SEQ_SCHEMA':tmp_schema,'SEQ_NAME':tmp_name})
        self.seq_id = sequence_record[0].SEQ_ID
        # get ID for Role
        role_record = self.ctlparent.get_data_record({'ROL_NAME':tmp_role})
        self.rol_id = role_record[0].ROL_ID
        # get Record
        self.ctltyp.read_data()
        s2r_record = self.ctltyp.get_data_record({'S2R_SEQ_ID':self.seq_id,'S2R_ROL_ID':self.rol_id})
        self.s2r_sta_ent.delete(0,'end')
        self.s2r_end_ent.delete(0,'end')
        if s2r_record:
            self.s2r_id = s2r_record[0].S2R_ID
            self.s2r_sta_ent.insert(0,s2r_record[0].S2R_START)
            self.s2r_end_ent.insert(0,s2r_record[0].S2R_END)
        else:
            self.s2r_id = 0
            self.s2r_sta_ent.insert(0,'2999-12-30')
            self.s2r_end_ent.insert(0,'2999-12-31')

    def save_seq2rol(self):
        start = self.s2r_sta_ent.get()
        end = self.s2r_end_ent.get()
        try:
            x = self.s2r_id
        except:
            self.s2r_id = 0
        record = {'S2R_ID':self.s2r_id,'S2R_SEQ_ID':self.seq_id,'S2R_ROL_ID':self.rol_id,'S2R_START':start,'S2R_END':end}
        self.ctltyp.write_data(record)
        record = {}
        self.seq_sch_cmb.set('')
        self.seq_nam_cmb.set('')
        self.rol_nam_cmb.set('')
        self.clear_screen()
        self.read_schema_list()

    def delete_seq2rol(self):
        self.ctltyp.delete_data(self.s2r_id)
        self.seq_sch_cmb.set('')
        self.seq_nam_cmb.set('')
        self.rol_nam_cmb.set('')
        self.clear_screen()
        self.read_schema_list()


# --------------------------------------------------------------------------------
# -- GuiFrames                                                                 --
# --------------------------------------------------------------------------------

class GuiFrames(tk.Tk):

    def __init__(self):
        super().__init__()
        self.root = self
        self.root.title('Database Security System by M. Wagner')
        self.dbctyp = ctl_obj.CtlDbConn()
        self.conn = None
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)

    def build(self):
        # dbconn
        self.dbconn = ttk.LabelFrame(self.root,text='Database Connections')
        self.dbconn.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(self.dbconn,text="Database Connection").grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.build_dbconn()

    def bottom(self):
        # secbook
        self.secbook = ttk.Notebook(self.root)
        self.secbook.grid(row=1,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.secbook.columnconfigure(0,weight=1)
        self.secbook.rowconfigure(0,weight=1)
        # rbac
        self.rbac = ttk.LabelFrame(self.secbook,text='Role Based Access Control')
        self.rbac.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.secbook.add(self.rbac,text="RBAC")
        self.rbac.columnconfigure(0,weight=1)
        self.rbac.columnconfigure(1,weight=1)
        self.rbac.columnconfigure(2,weight=0)
        # lbac
        self.lbac = ttk.LabelFrame(self.secbook,text='Label Based Access Control')
        self.lbac.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.secbook.add(self.lbac,text="LBAC")
        # rbactree
        self.rbactree = ttk.LabelFrame(self.rbac,text='Tree View')
        self.rbactree.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(self.rbactree,text='TREE').grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.rbactree.columnconfigure(0,weight=1)
        self.rbactree.rowconfigure(0,weight=1)
        # rbactreeselect
        self.rbactreeselect = ttk.Labelframe(self.rbac,text='Tree View Select')
        self.rbactreeselect.grid(row=1,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(self.rbactreeselect,text='TREE SELECT').grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.build_rbac_tree_select()
        # rbacedit
        self.rbacedit = ttk.LabelFrame(self.rbac,text='Edit View')
        self.rbacedit.grid(row=0,column=1,padx=3,pady=3,sticky=('N','E','S','W'),rowspan=2)
        self.rbacedit.columnconfigure(0,weight=1)
        self.rbacedit.rowconfigure(0,weight=1)
        # rbaceditselect
        self.rbaceditselect = ttk.LabelFrame(self.rbac,text='Edit View Select')
        self.rbaceditselect.grid(row=0,column=2,padx=3,pady=3,sticky=('N','E','S','W'),rowspan=2)
        self.build_rbac_edit_select()

    # -- DB-Connection ---------------------------------------------------------------
    def build_dbconn(self):
        self.con_info = tk.StringVar()
        my_style = ttk.Style()
        my_style.configure('TLabelFrame',background='PaleTurquoise1')
        dbconn = ttk.LabelFrame(self.root,text='Database Connection')
        dbconn.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Label(dbconn,text='Connection').grid(row=0,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='Server').grid(row=0,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='Port').grid(row=0,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='Database').grid(row=0,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.con_name = ttk.Combobox(dbconn)
        self.con_name.grid(row=1,column=0,padx=3,pady=3,sticky=('E','W'))
        self.con_name.bind("<<ComboboxSelected>>",self.select_dbc)
        self.srv_name = ttk.Entry(dbconn)
        self.srv_name.grid(row=1,column=1,padx=3,pady=3,sticky=('E','W'))
        self.srv_port = ttk.Entry(dbconn)
        self.srv_port.grid(row=1,column=2,padx=3,pady=3,sticky=('E','W'))
        self.db_name  = ttk.Entry(dbconn)
        self.db_name.grid(row=1,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        ttk.Label(dbconn,text='SSL Path').grid(row=2,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='SSL Key').grid(row=2,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='SSL Stash').grid(row=2,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.ssl_path = ttk.Entry(dbconn)
        self.ssl_path.grid(row=3,column=1,padx=3,pady=3,sticky=('E','W'))
        self.ssl_key  = ttk.Entry(dbconn)
        self.ssl_key.grid(row=3,column=2,padx=3,pady=3,sticky=('E','W'))
        self.ssl_stash = ttk.Entry(dbconn)
        self.ssl_stash.grid(row=3,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        ttk.Label(dbconn,text='Connect User').grid(row=4,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='Admin. User').grid(row=4,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(dbconn,text='Security User').grid(row=4,column=3,sticky=('E','W'))
        #
        self.con_usr = ttk.Entry(dbconn)
        self.con_usr.grid(row=5,column=1,padx=3,pady=3,sticky=('E','W'))
        self.adm_usr = ttk.Entry(dbconn)
        self.adm_usr.grid(row=5,column=2,padx=3,pady=3,sticky=('E','W'))
        self.sec_usr = ttk.Entry(dbconn)
        self.sec_usr.grid(row=5,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.dbc_save = tk.Button(dbconn,text='CONNECT',command=self.connect_dbc).grid(row=10,column=0,padx=3,pady=3,sticky=('E','W'))
        self.dbc_save = tk.Button(dbconn,text='SAVE',command=self.save_dbc).grid(row=10,column=1,padx=3,pady=3,sticky=('E','W'))
        self.dbc_del  = tk.Button(dbconn,text='DELETE',command=self.delete_dbc).grid(row=10,column=2,padx=3,pady=3,sticky=('E','W'))
        self.dbc_new  = tk.Button(dbconn,text='NEW',command=self.new_dbc).grid(row=10,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        ttk.Label(dbconn,text="",textvariable=self.con_info).grid(row=20,column=0,columnspan=4,padx=3,pady=3,sticky=('E','W'))
        #
        self.con_name.focus()
        self.read_dbc()

    def clear_db_screen(self):
        self.srv_name.delete(0,'end')
        self.srv_port.delete(0,'end')
        self.db_name.delete(0,'end')
        self.ssl_path.delete(0,'end')
        self.ssl_key.delete(0,'end')
        self.ssl_stash.delete(0,'end')
        self.con_usr.delete(0,'end')
        self.adm_usr.delete(0,'end')
        self.sec_usr.delete(0,'end')

    def read_dbc(self):
        self.db_con_list:list = []
        self.db_con_list = self.dbctyp.read_dbc()
        self.con_name['values'] = self.db_con_list

    def select_dbc(self,event_object):
        sel_con = event_object.widget.get()
        self.clear_db_screen()
        con_row = self.dbctyp.get_con(sel_con)
        fields = con_row.split(";")
        self.srv_name.insert(0,fields[1])
        self.srv_port.insert(0,fields[3])
        self.db_name.insert(0,fields[2])
        self.ssl_path.insert(0,fields[4])
        self.ssl_key.insert(0,fields[5])
        self.ssl_stash.insert(0,fields[6])
        self.con_usr.insert(0,fields[7])
        self.adm_usr.insert(0,fields[8])
        if fields[9][-1:] == '\n':
            self.sec_usr.insert(0,fields[9][:-1])
        else:
            self.sec_usr.insert(0,fields[9])

    def read_dbc_screen(self):
        dbc_record:str = ""
        dbc_record += self.con_name.get()+';'
        dbc_record += self.srv_name.get()+';'
        dbc_record += self.db_name.get()+';'
        dbc_record += self.srv_port.get()+';'
        dbc_record += self.ssl_path.get()+';'
        dbc_record += self.ssl_key.get()+';'
        dbc_record += self.ssl_stash.get()+';'
        dbc_record += self.con_usr.get()+';'
        dbc_record += self.adm_usr.get()+';'
        dbc_record += self.sec_usr.get()+'\n'
        return dbc_record

    def update_dbc(self,record):
        self.dbctyp.stack_update(record)

    def insert_dbc(self,record):
        self.dbctyp.stack_append(record)

    def save_dbc(self):
        dbc_record:str = ""
        dbc_record = self.read_dbc_screen()
        if len(self.con_name.get()) > 0:
            if self.con_name.get() in self.db_con_list:
                self.update_dbc(dbc_record)
            else:
                self.insert_dbc(dbc_record)
        self.dbctyp.write_dbc()
        self.read_dbc()

    def delete_dbc(self):
        del_name = self.con_name.get()
        self.dbctyp.delete_dbc(del_name)
        self.con_name.set('')
        self.clear_db_screen()
        self.save_dbc()
        self.read_dbc()

    def new_dbc(self):
        self.con_name.set('')
        self.clear_db_screen()

    def connect_dbc(self):
        tmp_ssl:str = ""
        self.conn = sec_db2.Db2()
        if self.ssl_path.get():
            if self.ssl_key.get():
                tmp_ssl += "SSLClientKeystoredb="+self.ssl_path.get()+"/"+self.ssl_key.get()+";"
            if self.ssl_stash.get():
                tmp_ssl += "SSLClientKeystash="+self.ssl_path.get()+"/"+self.ssl_stash.get()
                tmp_ssl = ";SECURITY=ssl;" + tmp_ssl
        tmp_pwd = simpledialog.askstring(title="Password",\
            prompt="PASSWORD for the CONNECT user >> "+str(self.con_usr.get())+" <<",show="*")
        if tmp_pwd:
            con_flag = self.conn.open(self.srv_name.get(),self.srv_port.get(),self.db_name.get(),tmp_ssl,self.con_usr.get(),tmp_pwd)
            if con_flag:
                tmp:str = ""
                tmp += f"Server: {self.srv_name.get()}     "
                tmp += f"Port: {self.srv_port.get()}     "
                tmp += f"Database: {self.db_name.get()}     "
                tmp += f"User: {self.con_usr.get()}     "
                self.conn.exec('SET SESSION_USER = ' + self.sec_usr.get())
                self.con_info.set(tmp)
                self.bottom()
            else:
                self.con_info.set("")
                try:
                    self.secbook.destroy()
                except:
                    pass


    # -- RBAC Tree-Select ------------------------------------------------------------
    def build_rbac_tree_select(self):
        self.treviw = tk.StringVar()
        self.tree_init = ttk.Radiobutton(self.rbactreeselect,text='USER2ROLE',variable=self.treviw,value='USR2ROL',command=self.build_usr2rol_tree)
        self.tree_init.grid(row=0,column=0,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROLE2USER',variable=self.treviw,value='ROL2USR',command=self.build_rol2usr_tree).\
            grid(row=0,column=1,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='SCHEMA2ROLE',variable=self.treviw,value='SCH2ROL',command=self.build_sch2rol_tree).\
            grid(row=1,column=0,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROLE2SCHEMA',variable=self.treviw,value='ROL2SCH',command=self.build_rol2sch_tree).\
            grid(row=1,column=1,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='TABLE2ROLE',variable=self.treviw,value='TBL2ROL',command=self.build_tbl2rol_tree).\
            grid(row=2,column=0,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROLE2TABLE',variable=self.treviw,value='ROL2TBL',command=self.build_rol2tbl_tree).\
            grid(row=2,column=1,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROUTINE2ROLE',variable=self.treviw,value='ROU2ROL',command=self.build_rou2rol_tree).\
            grid(row=3,column=0,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROLE2ROUTINE',variable=self.treviw,value='ROL2ROU',command=self.build_rol2rou_tree).\
            grid(row=3,column=1,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='SEQUENCE2ROLE',variable=self.treviw,value='SEQ2ROL',command=self.build_seq2rol_tree).\
            grid(row=4,column=0,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbactreeselect,text='ROLE2SEQUENCE',variable=self.treviw,value='ROL2SEQ',command=self.build_rol2seq_tree).\
            grid(row=4,column=1,pady=3,sticky=('E','W'))
        self.tree_init.invoke()

    def build_usr2rol_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT usr_id,usr_name,usr_start,usr_end,u2r_start,u2r_end,rol_id,\
                rol_name,rol_start,rol_end
            FROM sec.t_user left outer join sec.t_usr2rol ON usr_id = u2r_usr_id
                            left outer join sec.t_role    ON u2r_rol_id = rol_id
            WHERE usr_id > 0
            ORDER BY usr_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)
    
    def build_rol2usr_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rol_id,rol_name,rol_start,rol_end,u2r_start,u2r_end,usr_id,\
                usr_name,usr_start,usr_end
            FROM sec.t_role left outer join sec.t_usr2rol ON rol_id = u2r_rol_id
                            left outer join sec.t_user    ON u2r_usr_id = usr_id
            WHERE rol_id > 0
            ORDER BY rol_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_sch2rol_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT sch_id,sch_name,sch_start,sch_end,s2r_start,s2r_end,rol_id,\
                rol_name,rol_start,rol_end
            FROM sec.t_schema left outer join sec.t_sch2rol ON sch_id = s2r_sch_id
                              left outer join sec.t_role    ON s2r_rol_id = rol_id
            ORDER BY sch_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_rol2sch_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rol_id,rol_name,rol_start,rol_end,s2r_start,s2r_end,sch_id,\
                sch_name,sch_start,sch_end
            FROM sec.t_role left outer join sec.t_sch2rol ON rol_id = s2r_rol_id
                            left outer join sec.t_schema  ON s2r_sch_id = sch_id
            WHERE rol_id > 0
            ORDER BY rol_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)

    def build_tbl2rol_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT tbl_id,strip(tbl_schema)||'.'||strip(tbl_name) as tbl_name,\
                tbl_start,tbl_end,t2r_start,t2r_end,rol_id,rol_name,rol_start,rol_end
            FROM sec.t_table left outer join sec.t_tbl2rol ON tbl_id = t2r_tbl_id
                             left outer join sec.t_role    ON t2r_rol_id = rol_id
            ORDER BY tbl_schema,tbl_name,rol_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_rol2tbl_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rol_id,rol_name,rol_start,rol_end,t2r_start,t2r_end,tbl_id,\
                strip(tbl_schema)||'.'||strip(tbl_name) as tbl_name,tbl_start,tbl_end
            FROM sec.t_role left outer join sec.t_tbl2rol ON rol_id = t2r_rol_id
                            left outer join sec.t_table   ON t2r_tbl_id = tbl_id
            WHERE rol_id > 0
            ORDER BY rol_name,tbl_schema,tbl_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_rou2rol_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rou_id,strip(rou_schema)||'.'||strip(rou_specific) as rou_name,\
                rou_start,rou_end,r2r_start,r2r_end,rol_id,rol_name,rol_start,rol_end
            FROM sec.t_routine left outer join sec.t_rou2rol ON rou_id = r2r_rou_id
                               left outer join sec.t_role    ON r2r_rol_id = rol_id
            ORDER BY rou_schema,rou_name,rol_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_rol2rou_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rol_id,rol_name,rol_start,rol_end,r2r_start,r2r_end,rou_id,\
                strip(rou_schema)||'.'||strip(rou_name) as rou_name,rou_start,rou_end
            FROM sec.t_role left outer join sec.t_rou2rol ON rol_id = r2r_rol_id
                            left outer join sec.t_routine ON r2r_rou_id = rou_id
            WHERE rol_id > 0
            ORDER BY rol_name,rou_schema,rou_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_seq2rol_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT seq_id,strip(seq_schema)||'.'||strip(seq_name) as seq_name,\
                seq_start,seq_end,s2r_start,s2r_end,rol_id,rol_name,rol_start,rol_end
            FROM sec.t_sequence left outer join sec.t_seq2rol ON seq_id = s2r_seq_id
                                left outer join sec.t_role    ON s2r_rol_id = rol_id
            ORDER BY seq_schema,seq_name,rol_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    def build_rol2seq_tree(self):
        work:list = []
        #self.conn   = conn
        self.ctltyp = ctl_obj.CtlRbacTree(self.conn)
        sql = '''SELECT rol_id,rol_name,rol_start,rol_end,s2r_start,s2r_end,seq_id,\
                strip(seq_schema)||'.'||strip(seq_name) as seq_name,seq_start,seq_end
            FROM sec.t_role left outer join sec.t_seq2rol  ON rol_id = s2r_rol_id
                            left outer join sec.t_sequence ON s2r_seq_id = seq_id
            WHERE rol_id > 0
            ORDER BY rol_name,seq_schema,seq_name'''
        work = self.ctltyp.build(sql)
        if len(work) >= 1:
            self.build_rbac_tree(work)


    # -- RBAC Tree -------------------------------------------------------------------
    def open_rbac_tree(self):
        self.rbac_tree = ttk.Treeview(self.rbactree)
        # ---
        self.rbac_tree['columns'] = ('one','two')
        # ---
        self.rbac_tree.column('#0',width=500,minwidth=100,stretch=tk.YES)
        self.rbac_tree.column('one',width=100,minwidth=100,stretch=tk.NO)
        self.rbac_tree.column('two',width=100,minwidth=100,stretch=tk.NO)
        # ---
        self.rbac_tree.heading('#0',text='RBAC-Object',anchor=tk.W)
        self.rbac_tree.heading('one',text='Start',anchor=tk.W)
        self.rbac_tree.heading('two',text='End',anchor=tk.W)

    def close_rbac_tree(self):
        self.rbac_tree.grid(row=0,column=0,rowspan=1,columnspan=1,\
            padx=3,pady=3,sticky=('N','E','S','W'))


    def build_rbac_tree(self,work:list = []):
        self.open_rbac_tree()
        # start with the definition of the TREE-Gui
        old:str = ""
        idx:int = 1
        # start to fill the TREE-Gui with data
        for row in work:
            if row[0] is not None:
                begin = row[2].strftime("%Y-%m-%d")
                ende = row[3].strftime("%Y-%m-%d")
                if old != row[1]:
                    lvl1 = 'P'+str(row[0])+' = self.rbac_tree.insert(parent="",index='+str(idx)+',text="'+row[1]+\
                        '",values=("'+begin+'","'+ende+'"))'
                    exec(lvl1)
                    idx += 1
                    old = row[1]
                if row[4] is not None:
                    begin = row[4].strftime("%Y-%m-%d")
                    ende = row[5].strftime("%Y-%m-%d")
                    tmp = row[6]
                    try:
                        if tmp < 0:
                            tmp = tmp * -1
                    except:
                        tmp = '_'
                    # lvl2 = 'C'+str(tmp)+' = self.rbac_tree.insert(parent=P'+str(row[0])+\
                    #     ',index='+str(idx)+',text="'+row[1]+' : '+row[7]+'",values=("'+begin+'","'+ende+'"))'
                    lvl2 = f'C{tmp} = self.rbac_tree.insert(parent=P{row[0]},index={idx},text="{row[1]}:{row[7]}",values=("{begin}","{ende}"))'
                    exec(lvl2)
                    idx += 1
                if row[6] is not None:
                    begin = row[8].strftime("%Y-%m-%d")
                    ende = row[9].strftime("%Y-%m-%d")
                    lvl3 = 'self.rbac_tree.insert(parent=C'+str(tmp)+\
                        ',index='+str(idx)+',text="'+row[7]+'",values=("'+begin+'","'+ende+'"))'
                    exec(lvl3)
                    idx += 1
        self.close_rbac_tree()
        #closes the TREE-Gui after the Tree is filled with data

    def build_rbac_edit(self):
        pass

    def build_rbac_user(self):
        handle = GuiUsr(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_schema(self):
        handle = GuiSch(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_role(self):
        handle = GuiRol(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_table(self):
        handle = GuiTbl(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_routine(self):
        handle = GuiRou(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_sequence(self):
        handle = GuiSeq(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_usr2rol(self):
        handle = GuiUsr2Rol(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_sch2rol(self):
        handle = GuiSch2Rol(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_tbl2rol(self):
        handle = GuiTbl2Rol(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_rou2rol(self):
        handle = GuiRou2Rol(self.conn)
        handle.build(self.rbacedit)

    def build_rbac_seq2rol(self):
        handle = GuiSeq2Rol(self.conn)
        handle.build(self.rbacedit)

    def switch_businesstime(self):
        switch  = self.bustime.get()
        if switch == 'ON':
            self.conn.exec("SET CURRENT TEMPORAL BUSINESS_TIME = CURRENT DATE")
        else:
            self.conn.exec("SET CURRENT TEMPORAL BUSINESS_TIME = NULL")

    def run_sec_proc(self):
        self.conn.exec("CALL SEC.SECURITY2()")

    def run_err_proc(self):
        view_error = ctl_obj.CtlObj(self.conn)
        result:dict = view_error.check4error()
        tlist = result['table']
        rlist = result['routine']
        slist = result['sequence']
        #error_root = Gui()
        self.err_frm = ttk.Labelframe(self.root,text="Errors").grid(row=30,column=0,sticky=('N','E','S','W'))
        idx:int = 10
        ttk.Label(self.err_frm,text="Table does not exist").grid(row=idx,column=0,sticky=('W'))
        idx += 1
        for line in tlist:
            ttk.Label(self.err_frm,text=f"{line['TBL_SCHEMA']}.{line['TBL_NAME']}").grid(row=idx,column=0,sticky=('W'))
            idx += 1
        ttk.Separator(self.err_frm,orient='horizontal').grid(row=idx,column=0,padx=3,pady=3,sticky=('E','W'))
        idx += 1
        ttk.Label(self.err_frm,text="Routine does not exist").grid(row=idx,column=0,sticky=('W'))
        idx += 1
        for line in rlist:
            ttk.Label(self.err_frm,text=f"{line['ROU_SCHEMA']}.{line['ROU_NAME']} / {line['ROU_SPECIFIC']}").grid(row=idx,column=0,sticky=('W'))
            idx += 1
        ttk.Separator(self.err_frm,orient='horizontal').grid(row=idx,column=0,padx=3,pady=3,sticky=('E','W'))
        idx += 1
        ttk.Label(self.err_frm,text="Sequence does not exist").grid(row=idx,column=0,sticky=('W'))
        idx += 1
        for line in slist:
            ttk.Label(self.err_frm,text=f"{line['SEQ_SCHEMA']}.{line['SEQ_NAME']}").grid(row=idx,column=0,sticky=('W'))
            idx += 1



    # -- RBAC Edit-Select ------------------------------------------------------------
    def build_rbac_edit_select(self):
        self.res = tk.StringVar()
        self.bustime = tk.StringVar()
        self.edit_start = ttk.Radiobutton(self.rbaceditselect,text='USER',variable=self.res,value=0,command=self.build_rbac_user)
        self.edit_start.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='SCHEMA',variable=self.res,value=1,command=self.build_rbac_schema).\
            grid(row=1,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='ROLE',variable=self.res,value=2,command=self.build_rbac_role).\
            grid(row=2,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='TABLE',variable=self.res,value=3,command=self.build_rbac_table).\
            grid(row=3,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='ROUTINE',variable=self.res,value=4,command=self.build_rbac_routine).\
            grid(row=4,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='SEQUENCE',variable=self.res,value=5,command=self.build_rbac_sequence).\
            grid(row=5,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='USER 2 ROLE',variable=self.res,value=6,command=self.build_rbac_usr2rol).\
            grid(row=6,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='SCHEMA 2 ROLE',variable=self.res,value=7,command=self.build_rbac_sch2rol).\
            grid(row=7,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='TABLE 2 ROLE',variable=self.res,value=8,command=self.build_rbac_tbl2rol).\
            grid(row=8,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='ROUTINE 2 ROLE',variable=self.res,value=9,command=self.build_rbac_rou2rol).\
            grid(row=9,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        ttk.Radiobutton(self.rbaceditselect,text='SEQUENCE 2 ROLE',variable=self.res,value=10,command=self.build_rbac_seq2rol).\
            grid(row=10,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # --- Businesstime            
        ttk.Separator(self.rbaceditselect,orient='horizontal').grid(row=20,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.rbaceditselect,text='Businesstime').grid(row=21,column=0,padx=3,pady=3,sticky=('E','W'))
        ttk.Radiobutton(self.rbaceditselect,text='ON:',variable=self.bustime,value='ON',command=self.switch_businesstime).\
            grid(row=22,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        self.bt_start = ttk.Radiobutton(self.rbaceditselect,text='OFF:',variable=self.bustime,value='OFF',command=self.switch_businesstime)
        self.bt_start.grid(row=23,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # --- SECURITY PROCEDURE
        ttk.Separator(self.rbaceditselect,orient='horizontal').grid(row=25,column=0,padx=3,pady=3,sticky=('E','W'))
        self.sec_proc = tk.Button(self.rbaceditselect,text='SECURITY',command=self.run_sec_proc).grid(row=26,column=0,padx=3,pady=3,sticky=('E','W'))
        # --- CHECK ERROR
        #self.sec_proc = tk.Button(self.rbaceditselect,text='ERROR CHECK',command=self.run_err_proc).grid(row=27,column=0,padx=3,pady=3,sticky=('E','W'))
        # ---
        self.edit_start.invoke()
        self.bt_start.invoke()


# --------------------------------------------------------------------------------
# -- TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST --
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    #g = Gui()
    #conn = sec_db2.Db2()
    #conn.open('localhost',50000,'newsecdb','','manfred','IhMW&bue50')
    #usr = GuiUsr(conn)
    #usr.build(g)
    #rol = GuiRol(conn)
    #rol.build(g)
    #tbl = GuiTbl(conn)
    #tbl.build(g)
    #rou = GuiRou(conn)
    #rou.build(g)
    #seq = GuiSeq(conn)
    #seq.build(g)
    #u2r = GuiUsr2Rol(conn)
    #u2r.build(g)
    #s2r = GuiSch2Rol(conn)
    #s2r.build(g)
    #g.mainloop()
    # ----------------------------------------
    f = GuiFrames()
    f.build()
    f.mainloop()