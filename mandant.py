#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import datetime
import sec_db2 as driver

class Gui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.error_msg = tk.StringVar()
        self.sel_cmd = ''
        self.root = self
        self.root.title('self.multitenancy for the Database Security System by M.Wagner')
        self.db2 = driver.Db2()
        self.db_con = ''
        pass
        
    def build(self):
        self.multi = ttk.LabelFrame(self.root,text='Database Connections')
        self.multi.grid(row=0,column=0,padx=3,pady=3,sticky=('N','E','S','W'))
        # 
        ttk.Label(self.multi,text='Server').grid(row=0,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='Port').grid(row=0,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='Database').grid(row=0,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.srv_name = ttk.Entry(self.multi)
        self.srv_name.grid(row=1,column=1,padx=3,pady=3,sticky=('E','W'))
        self.srv_port = ttk.Entry(self.multi)
        self.srv_port.grid(row=1,column=2,padx=3,pady=3,sticky=('E','W'))
        self.db_name  = ttk.Entry(self.multi)
        self.db_name.grid(row=1,column=3,padx=3,pady=3,sticky=('E','W'))
        # 
        ttk.Label(self.multi,text='SSL-PATH').grid(row=2,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='SSL-KEY').grid(row=2,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='SSL-Stash').grid(row=2,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.ssl_path = ttk.Entry(self.multi)
        self.ssl_path.grid(row=3,column=1,padx=3,pady=3,sticky=('E','W'))
        self.ssl_key = ttk.Entry(self.multi)
        self.ssl_key.grid(row=3,column=2,padx=3,pady=3,sticky=('E','W'))
        self.ssl_stash  = ttk.Entry(self.multi)
        self.ssl_stash.grid(row=3,column=3,padx=3,pady=3,sticky=('E','W'))
        # 
        ttk.Label(self.multi,text='Connection-User').grid(row=4,column=1,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='Administration-User').grid(row=4,column=2,padx=3,pady=3,sticky=('E','W'))
        ttk.Label(self.multi,text='Security-User').grid(row=4,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.con_usr = ttk.Entry(self.multi)
        self.con_usr.grid(row=5,column=1,padx=3,pady=3,sticky=('E','W'))
        self.adm_usr = ttk.Entry(self.multi)
        self.adm_usr.grid(row=5,column=2,padx=3,pady=3,sticky=('E','W'))
        self.sec_usr  = ttk.Entry(self.multi)
        self.sec_usr.grid(row=5,column=3,padx=3,pady=3,sticky=('E','W'))
        #
        ttk.Label(self.multi,text='Action').grid(row=6,column=1,columnspan=3,padx=3,pady=3,sticky=('E','W'))
        #
        self.action = ttk.Combobox(self.multi)
        self.action.grid(row=7,column=1,columnspan=3,padx=3,pady=3,sticky=('E','W'))
        self.action.bind("<<ComboboxSelected>>",self.select_action)
        self.action['values'] = ['INITIALIZE','ADD CLIENT']
        #
        self.srv_name.focus()
        
    def select_action(self,event_object):
        #
        self.inner_multi = ttk.Frame(self.multi)
        self.inner_multi.grid(row=10,column=1,columnspan=3,padx=3,pady=3,sticky=('N','E','S','W'))
        #
        self.sel_cmd = event_object.widget.get()
        if event_object.widget.get() == 'INITIALIZE':
            pass
        if event_object.widget.get() == 'ADD CLIENT':
            #
            ttk.Label(self.inner_multi,text='Schema-Name').grid(row=1,column=1,padx=3,pady=3,sticky=('E','W'))
            #
            self.sch_name = ttk.Entry(self.inner_multi)
            self.sch_name.grid(row=2,column=1,columnspan=3,padx=3,pady=3,sticky=('E','W'))
            #
            ttk.Label(self.inner_multi,text='Schema-Connection-User').grid(row=8,column=1,padx=3,pady=3,sticky=('E','W'))
            ttk.Label(self.inner_multi,text='Schema-Administration-User').grid(row=8,column=2,padx=3,pady=3,sticky=('E','W'))
            ttk.Label(self.inner_multi,text='Schema-Security-User').grid(row=8,column=3,padx=3,pady=3,sticky=('E','W'))
            #
            self.sch_con_usr = ttk.Entry(self.inner_multi)
            self.sch_con_usr.grid(row=9,column=1,padx=3,pady=3,sticky=('E','W'))
            self.sch_adm_usr = ttk.Entry(self.inner_multi)
            self.sch_adm_usr.grid(row=9,column=2,padx=3,pady=3,sticky=('E','W'))
            self.sch_sec_usr  = ttk.Entry(self.inner_multi)
            self.sch_sec_usr.grid(row=9,column=3,padx=3,pady=3,sticky=('E','W'))
            #
        ttk.Button(self.inner_multi, text='EXECUTE', command=self.execute).grid(row=10,column=1,columnspan=3,padx=3,pady=3,sticky=('E','W'))
        self.error_label = ttk.Label(self.inner_multi, text="", textvariable=self.error_msg)
        self.error_label.grid(row=11,column=1,columnspan=3,padx=3,pady=3,sticky=('E','W'))

    def execute(self):
        if self.check_main() == True:
            if self.sel_cmd == 'ADD CLIENT':
                if self.check_sub() == True:
                    self.add_client()
            else:
                self.init_multi()
            
    
    def check_main(self):
        status:bool = False
        if self.srv_name.get():
            if self.srv_port.get():
                if self.db_name.get():
                    if self.con_usr.get():
                        if self.adm_usr.get():
                            if self.sec_usr.get():
                                status = True
                                self.error_msg.set('')
                            else:
                                self.error_msg.set('Secure-User fehlt')
                        else:
                            self.error_msg.set('Admin-User fehlt')
                    else:
                        self.error_msg.set('Connection-User fehlt')
                else:
                    self.error_msg.set('Datenbankname fehlt')
            else:
                self.error_msg.set('Portnummer fehlt')
        else:
            self.error_msg.set('Servername fehlt')
        return status

    def check_sub(self):
        status:bool = False
        if self.sch_con_usr.get():
            if self.sch_adm_usr.get():
                if self.sch_sec_usr.get():
                    if self.sch_name.get():
                        self.error_msg.set('')
                        status = True
                    else:
                        self.error_msg.set('Schema-Name fehlt')
                else:
                    self.error_msg.set('Schema Secure-User fehlt')
            else:
                self.error_msg.set('Schema Admin-User fehlt')
        else:
            self.error_msg.set('Schema Connection-User fehlt')
        return status

    def init_multi(self):
        self.log_file = open('INIT.log','a')
        self.log_file.write(f"BEGIN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.connect_to_db()
        # check security-system
        if self.check_secsys():
            # check multi-client
            if self.check_multi():
                self.error_msg.set('MULTI-CLIENT CAPABILITY ALREADY EXISTS')
                self.log_file.write('### MULTI-CLIENT CAPABILITY ALREADY EXISTS\n')
            else:
                self.log_file.write('### INITIALIZE MULTI-CLIENT CAPABILITY!\n')
                self.implement_multi()
                self.log_file.close()
        else:
            self.error_msg.set('You need to install the SECUSRITY-SYSTEM first')
            self.log_file.write('### You need to install the SECUSRITY-SYSTEM first\n')
        print('INITIALIZE MULTI-CLIENT CAPABILITY!')
        pass
    
    def add_client(self):
        log_name = self.sch_name.get().upper()
        self.log_file = open(f'{log_name}.log','a')
        self.log_file.write(f"BEGIN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.db_con = self.connect_to_db()
        # check security-system
        if self.check_secsys():
            # check multi-client
            if self.check_multi():
                self.log_file.write('### ADD CLIENT TO SECURITY-SYSTEM!\n')
                self.add_schema_client()
                self.log_file.close()
            else:
                self.error_msg.set('You need to initialize the multi-client capability')
                self.log_file.write('### You need to initialize the multi-client capability\n')
        else:
             self.error_msg.set('You need to install the SECUSRITY-SYSTEM first')
             self.log_file.write('### You need to install the SECUSRITY-SYSTEM first\n')
        print('ADD CLIENT TO SECURITY-SYSTEM!')
        pass

    def check_secsys(self):
        flag:bool = False
        val:dict = {}
        # Bufferpool: BPSEC04K ? => 1
        bp_sql = "SELECT count(*) AS anzahl FROM syscat.bufferpools WHERE bpname = 'BPSEC04K'"
        # Tablespace: SECDAT04K, SECIDX04K ? => 2
        ts_sql = "SELECT count(*) AS anzahl FROM syscat.tablespaces WHERE tbspace IN ('SECDAT04K','SECIDX04K')"
        # Schema:     SEC => 1
        sc_sql = "SELECT count(*) AS anzahl FROM syscat.schemata WHERE schemaname = 'SEC'"
        # TABLE:      T_USER, T_ROLE, T_TABLE => 3
        tb_sql = "SELECT count(*) AS anzahl FROM syscat.tables WHERE tabname IN ('T_USER','T_ROLE','T_TABLE')"
        # Procedure:  SECURITY2 => 1
        pr_sql = "SELECT count(*) AS anzahl FROM syscat.routines WHERE specificname = 'SECURITY2'"
        self.log_file.write(f"### (bp_sql):{bp_sql}\n")
        self.db2.exec(bp_sql)
        val = self.db2.fetch()
        if val['ANZAHL'] == 1:
            self.log_file.write(f"### (ts_sql):{ts_sql}\n")
            self.db2.exec(ts_sql)
            val = self.db2.fetch()
            if val['ANZAHL'] == 2:
                self.log_file.write(f"### (sc_sql):{sc_sql}\n")
                self.db2.exec(sc_sql)
                val = self.db2.fetch()
                if val['ANZAHL'] == 1:
                    self.log_file.write(f"### (tb_sql):{tb_sql}\n")
                    self.db2.exec(tb_sql)
                    val = self.db2.fetch()
                    if val['ANZAHL'] == 3:
                        self.log_file.write(f"### (sql):{pr_sql}\n")
                        self.db2.exec(pr_sql)
                        val = self.db2.fetch()
                        if val['ANZAHL'] == 1:
                            flag = True
        return flag

    def check_multi(self):
        flag:bool = False
        val:dict = {}
        # SECURITYPOLICIES = SECRULE => 1
        s1_sql = "SELECT count(*) AS anzahl FROM syscat.securitypolicies WHERE secpolicyname = 'SECRULE'"
        # SECURITYLABELCOMPONENTS = SEC_LEVEL => 1
        s2_sql = "SELECT count(*) AS anzahl FROM syscat.securitylabelcomponents WHERE compname = 'SEC_LEVEL'"
        # SECURITYLABELS = SEC_ROOT => 1
        s3_sql = "SELECT count(*) AS anzahl FROM syscat.securitylabels WHERE seclabelname = 'SEC_ROOT'"
        self.log_file.write(f"### (s1_sql):{s1_sql}\n")
        self.db2.exec(s1_sql)
        val = self.db2.fetch()
        if val['ANZAHL'] == 1:
            self.log_file.write(f"### (s2_sql):{s2_sql}\n")
            self.db2.exec(s2_sql)
            val = self.db2.fetch()
            if val['ANZAHL'] == 1:
                self.log_file.write(f"### (s3_sql):{s3_sql}\n")
                self.db2.exec(s3_sql)
                val = self.db2.fetch()
                if val['ANZAHL'] == 1:
                    flag = True
        return flag

    def implement_multi(self):
        # Erstellen der LBAC COMPONENT
        i1_sql = "CREATE SECURITY LABEL COMPONENT sec_level TREE ('ROOT' ROOT)"
        # Erstellen der LBAC POLICY
        i2_sql = "CREATE SECURITY POLICY secrule COMPONENTS sec_level WITH DB2LBACRULES"
        # Erstellen des LBAC LABEL
        i3_sql = "CREATE SECURITY LABEL secrule.sec_root COMPONENT sec_level 'ROOT'"
        # Zuweisen des LABEL zum USER
        i4_sql = f"GRANT SECURITY LABEL secrule.sec_root TO USER $user$"
        # Datenbankverbindung abbrechen
        # Der Instance-User meldet sich an der Datenbank an
        # Zuweisen des LABEL zum USER
        i5_sql = f"GRANT SECURITY LABEL secrule.sec_root TO USER $ins_usr$"
        #
        self.log_file.write(f"### (i1_sql):{i1_sql}\n")
        self.db2.exec(i1_sql)
        tmp_sql:str = ""
        self.log_file.write(f"### (i2_sql):{i2_sql}\n")
        self.db2.exec(i2_sql)
        self.log_file.write(f"### (i3_sql):{i3_sql}\n")
        self.db2.exec(i3_sql)
        # Get the Name of the Instance-User
        self.ins_usr = simpledialog.askstring(title="INSTANZ-USER",\
            prompt="Input name for instanceuser:")
        # SEC_USER => INSTANCE_USER
        self.connect_to_db(self.ins_usr)
        # GRANT LABEL ... TO USER SEC_USER
        tmp_sql = i4_sql.replace('$user$',self.sec_usr.get().upper())
        self.log_file.write(f"### (tmp_sql):{tmp_sql}\n")
        self.db2.exec(tmp_sql)
        # INSTANCE_USER => SEC_USER
        self.connect_to_db()
        # GRANT LABEL ... TO USER INSTANCE_USER
        tmp_sql = i4_sql.replace('$user$',self.ins_usr)
        self.log_file.write(f"### (tmp_sql):{tmp_sql}\n")
        self.db2.exec(tmp_sql)
        # ADD SECURITY POLICY & LABEL TO Tables
        # SEC_USER => INSTANCE_USER
        self.connect_to_db(self.ins_usr)
        obj_list = ['T_USER','T_ROLE','T_SCHEMA','T_TABLE','T_ROUTINE','T_SEQUENCE','T_USR2ROL','T_SCH2ROL','T_TBL2ROL','T_ROU2ROL','T_SEQ2ROL']
        for obj in obj_list:
            self.db2.exec(f"ALTER TABLE SEC.{obj} ADD SECURITY POLICY SECRULE")
            self.log_file.write(f"### (add_pol) ALTER TABLE SEC.{obj} ADD SECURITY POLICY SECRULE\n")
            self.db2.exec(f"ALTER TABLE SEC.{obj} ADD COLUMN LBL DB2SECURITYLABEL IMPLICITLY HIDDEN")
            self.log_file.write(f"### (add_lbl) ALTER TABLE SEC.{obj} ADD COLUMN LBL DB2SECURITYLABEL IMPLICITLY HIDDEN\n")
        self.log_file.write('### Die Datenbank is nun Initialisiert\n')
        pass

    def add_schema_client(self):
        # GRANT DB-AUTH
        a1_sql = f"GRANT CONNECT ON DATABASE TO USER {self.sch_con_usr.get().upper()}"
        #a2_sql = f"GRANT SCHEMAADM WITHOUT DATAACCESS WITHOUT ACCESSCTRL ON DATABASE TO USER {self.sch_adm_usr.get().upper()}"
        a2_sql = f"GRANT ALTERIN,CREATEIN,DROPIN ON SCHEMA {self.sch_name.get().upper()} TO USER {self.sch_adm_usr.get().upper()}"
        a3_sql = f"GRANT SECADM ON DATABASE TO USER {self.sch_sec_usr.get().upper()}"
        a4_sql = f"GRANT SETSESSIONUSER ON USER {self.sch_adm_usr.get().upper()} TO USER {self.sch_con_usr.get().upper()}"
        a5_sql = f"GRANT SETSESSIONUSER ON USER {self.sch_sec_usr.get().upper()} TO USER {self.sch_con_usr.get().upper()}"
        # GRANT TABLE-AUTH
        tabname:str = ""
        g1_sql = f"SELECT tabname FROM syscat.tables WHERE tabschema = 'SEC' AND type = 'T'"
        x1_sql = f"GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE SEC.$tabname$ TO USER {self.sch_sec_usr.get().upper()}"
        g2_sql = f"SELECT tabname FROM syscat.tables WHERE tabschema = 'SEC' AND type = 'V'"
        x2_sql = f"GRANT SELECT ON TABLE SEC.$tabname$ TO USER {self.sch_sec_usr.get().upper()}"
        # CREATE AND GRANT LABEL
        l1_sql = f"ALTER SECURITY LABEL COMPONENT sec_level ADD ELEMENT '{self.sch_name.get().upper()}' UNDER 'ROOT'"
        l2_sql = f"CREATE SECURITY LABEL secrule.sec_{self.sch_name.get().upper()} COMPONENT sec_level '{self.sch_name.get().upper()}'"
        l3_sql = f"GRANT SECURITY LABEL secrule.sec_{self.sch_name.get().upper()} TO USER {self.sch_sec_usr.get().upper()}"
        # CHECK LABEL, COMPONENTS & ELEMENTS
        c1_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabelcomponents WHERE compname = 'SEC_LEVEL'"
        c2_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabelcomponentelements WHERE elementvalue = '{self.sch_name.get().upper()}'"
        c3_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabels WHERE seclabelname = 'SEC_{self.sch_name.get().upper()}'"
        # Execute GRANTS a1 - a5
        for x_sql in [a1_sql, a2_sql, a3_sql, a4_sql, a5_sql]:
            self.log_file.write(f"### (x_sql):{x_sql}\n")
            self.db2.exec(x_sql)
        # Execute GRANTS g1 - g2 & x1 - x2
        tmp_g = [g1_sql, g2_sql]
        tmp_x = [x1_sql, x2_sql]
        sql_list:list = []
        for g_sql, x_sql in zip(tmp_g, tmp_x):
            self.log_file.write(f"### (g_sql):{g_sql}\n")
            self.db2.exec(g_sql)
            row = self.db2.fetch()
            while row != False:
                tmp_sql:str = ""
                tmp_sql = x_sql.replace("$tabname$",row['TABNAME'])
                self.log_file.write(f"### (tmp_sql):{tmp_sql}\n")
                sql_list.append(tmp_sql)
                row = self.db2.fetch()
        for x_sql in sql_list:
            self.log_file.write(f"### (x_sql):{x_sql}\n")
            self.db2.exec(x_sql)
        # check securitylabelcomponent
        self.log_file.write(f"### (c1_sql):{c1_sql}\n")
        self.db2.exec(c1_sql)
        flag = self.db2.fetch()
        if flag['ANZAHL'] >= 1:
            # check securitylabelcomponentelement
            self.log_file.write(f"### (c2_sql):{c2_sql}\n")
            self.db2.exec(c2_sql)
            flag = self.db2.fetch()
            if flag['ANZAHL'] == 0:
                self.log_file.write(f"### (l1_sql):{l1_sql}\n")
                self.db2.exec(l1_sql)
            # check security_label
            self.log_file.write(f"### (c3_sql):{c3_sql}\n")
            self.db2.exec(c3_sql)
            flag = self.db2.fetch()
            if flag['ANZAHL'] == 0:
                self.log_file.write(f"### (l2_sql):{l2_sql}\n")
                self.db2.exec(l2_sql)
            # grant label
            self.log_file.write(f"### (l3_sql):{l3_sql}\n")
            self.log_file.write(f'### Der User:{self.sch_sec_usr.get().upper()} für das Schema:{self.sch_name.get().upper()} ist nun in der Datenbank aktiviert\n')
            self.db2.exec(l3_sql)
            # get the last number for an security-user
            id_sql = "SELECT MIN(USR_ID) AS ID FROM SEC.T_USER"
            self.db2.exec(id_sql)
            usr_id = self.db2.fetch()
            # get the last number for an security-role
            id_sql = "SELECT MIN(ROL_ID) AS ID FROM SEC.T_ROLE"
            self.db2.exec(id_sql)
            rol_id = self.db2.fetch()
            # connect as the new connect-user
            self.connect_to_db(self.sch_con_usr.get().upper())
            # become the new security-user
            set_sql = f"SET SESSION_USER = {self.sch_sec_usr.get().upper()}"
            self.db2.exec(set_sql)
            # get the activation date
            tmp_date = datetime.now()
            now = tmp_date.strftime('%Y-%m-%d')
            # insert ADM & SEC into T_USER
            sec_sql1 = f"INSERT INTO SEC.T_USER (USR_ID,USR_NAME,USR_CONNECT,USR_START,USR_END,USR_MARK) VALUES "
            sec_sql1 += f"({usr_id['ID'] - 1},'{self.sch_adm_usr.get().upper()}','{self.sch_con_usr.get().upper()}','{now}','2999-12-31','A')"
            self.db2.exec(sec_sql1)
            sec_sql2 = f"INSERT INTO SEC.T_USER (USR_ID,USR_NAME,USR_CONNECT,USR_START,USR_END,USR_MARK) VALUES "
            sec_sql2 += f"({usr_id['ID'] - 2},'{self.sch_sec_usr.get().upper()}','{self.sch_con_usr.get().upper()}','{now}','2999-12-31','S')"
            self.db2.exec(sec_sql2)
            # insert SCHEMA into T_SCHEMA
            sec_sql3 = f"INSERT INTO SEC.T_SCHEMA (SCH_NAME,SCH_START,SCH_END) VALUES ('{self.sch_name.get().upper()}','{now}','2999-12-31')"
            self.db2.exec(sec_sql3)
            # insert ROLE into T_ROLE
            sec_sql4 = f"INSERT INTO SEC.T_ROLE (ROL_ID,ROL_NAME,ROL_START,ROL_END,ROL_TYPE) VALUES "
            sec_sql4 += f"({rol_id['ID'] - 1},'{self.sch_name.get().upper()}_CONNECT','{now}','2999-12-31','R')"
            self.db2.exec(sec_sql4)
            sec_sql4 = f"INSERT INTO SEC.T_ROLE (ROL_ID,ROL_NAME,ROL_START,ROL_END,ROL_TYPE) VALUES "
            sec_sql4 += f"({rol_id['ID'] - 2},'{self.sch_name.get().upper()}_LOAD','{now}','2999-12-31','R')"
            self.db2.exec(sec_sql4)
            # insert Relation into T_SCH2ROL
            sec_sql5 = f"SELECT SCH_ID FROM SEC.T_SCHEMA WHERE SCH_NAME = '{self.sch_name.get().upper()}'"
            self.db2.exec(sec_sql5)
            sch_id = self.db2.fetch()
            sec_sql6 = f"SELECT ROL_ID FROM SEC.T_ROLE WHERE ROL_NAME = '{self.sch_name.get().upper()}_CONNECT'"
            self.db2.exec(sec_sql6)
            rol_id = self.db2.fetch()
            sec_sql7 = f"INSERT INTO SEC.T_SCH2ROL (S2R_ROL_ID,S2R_SCH_ID,S2R_SCHADM,S2R_SCHSEC,S2R_START,S2R_END) "
            sec_sql7 += f"VALUES ({rol_id['ROL_ID']},{sch_id['SCH_ID']},'N','N','{now}','2999-12-31')"
            self.db2.exec(sec_sql7)
        pass
    
    def connect_to_db(self, instance_user=""):
        tmp_ssl:str = ""
        if self.ssl_path.get():
            if self.ssl_key.get():
                tmp_ssl += "SSLClientKeystoredb="+self.ssl_path.get()+"/"+self.ssl_key.get()+";"
            if self.ssl_stash.get():
                tmp_ssl += "SSLClientKeystash="+self.ssl_path.get()+"/"+self.ssl_stash.get()
                tmp_ssl = ";SECURITY=ssl;" + tmp_ssl
        if instance_user == "":
            tmp_pwd = simpledialog.askstring(title="Password",\
                prompt="Input password for user >> "+str(self.con_usr.get())+" <<",show="*")
            if tmp_pwd:
                con_flag = self.db2.open(self.srv_name.get(),self.srv_port.get(),self.db_name.get(),tmp_ssl,self.con_usr.get(),tmp_pwd)
                if con_flag:
                    tmp:str = ""
                    tmp += f"Server: {self.srv_name.get()}     "
                    tmp += f"Port: {self.srv_port.get()}     "
                    tmp += f"Database: {self.db_name.get()}     "
                    tmp += f"User: {self.con_usr.get()}     "
                    self.db2.exec('SET SESSION_USER = ' + self.sec_usr.get())
                    self.error_msg.set(tmp)
                else:
                    self.error_msg.set("")
        else:
            tmp_pwd = simpledialog.askstring(title="Password",\
                prompt="Input password for user >> "+str(instance_user)+" <<",show="*")
            if tmp_pwd:
                con_flag = self.db2.open(self.srv_name.get(),self.srv_port.get(),self.db_name.get(),tmp_ssl,instance_user,tmp_pwd)
                if con_flag:
                    tmp:str = ""
                    tmp += f"Server: {self.srv_name.get()}     "
                    tmp += f"Port: {self.srv_port.get()}     "
                    tmp += f"Database: {self.db_name.get()}     "
                    tmp += f"User: {instance_user}     "
                    self.error_msg.set(tmp)
                else:
                    self.error_msg.set("")

if __name__ == '__main__':
    window = Gui()
    window.build()
    window.mainloop()

