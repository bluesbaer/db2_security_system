#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, simpledialog
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
        self.connect_to_db()
        print('INITIALIZE MULTI-CLIENT CAPABILITY!')
        # check security-system
        if self.check_secsys():
            # check multi-client
            if self.check_multi():
                self.error_msg.set('MULTI-CLIENT CAPABILITY ALREADY EXISTS')
            else:
                self.implement_multi()
        else:
            self.error_msg.set('You need to install the SECUSRITY-SYSTEM first')
        pass
    
    def add_client(self):
        self.db_con = self.connect_to_db()
        print('ADD CLIENT TO SECURITY-SYSTEM!')
        # check security-system
        if self.check_secsys():
            # check multi-client
            if self.check_multi():
                self.add_schema_client()
            else:
                self.error_msg.set('You need to initialize the multi-client capability')
        else:
             self.error_msg.set('You need to install the SECUSRITY-SYSTEM first')
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
        self.db2.exec(bp_sql)
        val = self.db2.fetch()
        if val['ANZAHL'] == 1:
            self.db2.exec(ts_sql)
            val = self.db2.fetch()
            if val['ANZAHL'] == 2:
                self.db2.exec(sc_sql)
                val = self.db2.fetch()
                if val['ANZAHL'] == 1:
                    self.db2.exec(tb_sql)
                    val = self.db2.fetch()
                    if val['ANZAHL'] == 3:
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
        self.db2.exec(s1_sql)
        val = self.db2.fetch()
        if val['ANZAHL'] == 1:
            self.db2.exec(s2_sql)
            val = self.db2.fetch()
            if val['ANZAHL'] == 1:
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
        i4_sql = f"GRANT SECURITY LABEL secrule.sec_root TO USER $ins_usr$"
        # Datenbankverbindung abbrechen
        # Der Instance-User meldet sich an der Datenbank an
        # Zuweisen des LABEL zum USER
        i5_sql = f"GRANT SECURITY LABEL secrule.sec_root TO USER $ins_usr$"
        #
        if self.db2.exec(i1_sql):
            tmp_sql:str = ""
            if self.db2.exec(i2_sql):
                if self.db2.exec(i3_sql):
                    # Get the Name of the Instance-User
                    ins_usr = simpledialog.askstring(title="INSTANZ-USER",\
                        prompt="Input name for instanceuser:")
                    tmp_sql = i4_sql.replace('$ins_usr$',ins_usr)
                    if self.db2.exec(tmp_sql):
                        tmp_usr = self.con_usr.get()
                        self.con_usr.set(ins_usr)
                        self.connect_to_db()
                        self.con_usr.set(tmp_usr)
                        tmp_sql = i4_sql.replace('$ins_usr$',tmp_usr)
                        if self.db2.exec(tmp_sql):
                            self.connect_to_db()
                            ins_usr = tmp_usr
                            if self.db2.exec(i5_sql):
                                self.err_msg.set('Die Datenbank is nun Initialisiert')
        pass

    def add_schema_client(self):
        # GRANT DB-AUTH
        a1_sql = f"GRANT CONNECT ON DATABASE TO USER {self.sch_con_usr.get()}"
        a2_sql = f"GRANT DBADM WITHOUT DATAACCESS WITHOUT ACCESSCTRL ON DATABASE TO USER {self.sch_adm_usr.get()}"
        a3_sql = f"GRANT SECADM ON DATABASE TO USER {self.sch_sec_usr.get()}"
        a4_sql = f"GRANT SETSESSIONUSER ON USER {self.sch_adm_usr.get()} TO USER {self.sch_con_usr.get()}"
        a5_sql = f"GRANT SETSESSIONUSER ON USER {self.sch_sec_usr.get()} TO USER {self.sch_con_usr.get()}"
        # GRANT TABLE-AUTH
        tabname:str = ""
        g1_sql = f"SELECT tabname FROM syscat.tables WHERE tabschema = 'SEC' AND type = 'T'"
        x1_sql = f"GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE SEC.$tabname$ TO USER {self.sch_sec_usr.get()}"
        g2_sql = f"SELECT tabname FROM syscat.tables WHERE tabschema = 'SEC' AND type = 'V'"
        x2_sql = f"GRANT SELECT ON TABLE SEC.$tabname$ TO USER {self.sch_sec_usr.get()}"
        # CREATE AND GRANT LABEL
        l1_sql = f"ALTER SECURITY LABEL COMPONENT sec_level ADD ELEMENT '{self.sch_name.get()}' UNDER 'ROOT'"
        l2_sql = f"CREATE SECURITY LABEL secrule.sec_{self.sch_name.get()} COMPONENT sec_level '{self.sch_name.get()}'"
        l3_sql = f"GRANT SECURITY LABEL secrule.sec_{self.sch_name.get()} TO USER {self.sch_sec_usr.get()}"
        # CHECK LABEL, COMPONENTS & ELEMENTS
        c1_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabelcomponents WHERE compname = 'SEC_LEVEL'"
        c2_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabelcomponentelements WHERE elementvalue = '{self.sch_name.get()}'"
        c3_sql = f"SELECT count(*) AS anzahl FROM syscat.securitylabels WHERE seclabelname = 'SEC_{self.sch_name.get()}'"
        #
        for x_sql in [a1_sql, a2_sql, a3_sql, a4_sql, a5_sql]:
            self.db2.exec(x_sql)
        tmp_g = [g1_sql, g2_sql]
        tmp_x = [x1_sql, x2_sql]
        sql_list:list = []
        for g_sql, x_sql in zip(tmp_g, tmp_x):
            self.db2.exec(g_sql)
            row = self.db2.fetch()
            while row != False:
                tmp_sql:str = ""
                tmp_sql = x_sql.replace("$tabname$",row['TABNAME'])
                print(f"### tmp_sql:{tmp_sql} ###")
                sql_list.append(tmp_sql)
                row = self.db2.fetch()
        for x_sql in sql_list:
            self.db2.exec(x_sql)
        # check securitylabelcomponent
        self.db2.exec(c1_sql)
        flag = self.db2.fetch()
        if flag['ANZAHL'] >= 1:
            # check securitylabelcomponentelement
            self.db2.exec(c2_sql)
            flag = self.db2.fetch()
            if flag['ANZAHL'] == 0:
                self.db2.exec(l1_sql)
            # check security_label
            self.db2.exec(c3_sql)
            flag = self.db2.fetch()
            if flag['ANZAHL'] == 0:
                self.db2.exec(l2_sql)
            # grant label
            self.db2.exec(l3_sql)
        pass
    
    def connect_to_db(self):
        tmp_ssl:str = ""
        if self.ssl_path.get():
            if self.ssl_key.get():
                tmp_ssl += "SSLClientKeystoredb="+self.ssl_path.get()+"/"+self.ssl_key.get()+";"
            if self.ssl_stash.get():
                tmp_ssl += "SSLClientKeystash="+self.ssl_path.get()+"/"+self.ssl_stash.get()
                tmp_ssl = ";SECURITY=ssl;" + tmp_ssl
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


if __name__ == '__main__':
    window = Gui()
    window.build()
    window.mainloop()

