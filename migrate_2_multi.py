#!/dev/usr python

## Db2 Security-System
## Version 1.0
## Manfred Wagner
## info@manfred-wagner.at


import sec_db2

server = 'db2amdmt'
port = 60220
db = 'amdmt'
ssl = ''
user = 'dbconusr'
pwd = 'dbconusr'

#server = 'db2dr01t'
#port = 60380
#db = 'dr01t'
#ssl = ''
#user = 'db2dr01t'
#pwd = 'K7zP5w&'

database = sec_db2.Db2()
database.open(server,port,db,'',user,pwd)
database.exec('SET SESSION_USER = dbsecusr')

schema_list:list = []
table_list:list = []
routine_list:list = []
sequence_list:list = []
role_list:list = []
dbuser_list:list = []
tbl2rol_list:list = []
rou2rol_list:list = []
seq2rol_list:list = []
usr2rol_list:list = []

sql_init = "SELECT schemaname FROM syscat.schemata WHERE schemaname NOT LIKE 'SYS%' AND schemaname NOT IN ('NULLID','SQLJ','SEC')"
sql_table = "SELECT * FROM sec.t_table WHERE tbl_schema = '§schema§'"
sql_tbl2rol = "SELECT * FROM sec.t_tbl2rol WHERE t2r_tbl_id = §id§"
sql_role = "SELECT * FROM sec.t_role WHERE rol_id = §id§"
sql_routine = "SELECT * FROM sec.t_routine WHERE rou_schema = '§schema§'"
sql_rou2rol = "SELECT * FROM sec.t_rou2rol WHERE r2r_rou_id = §id§"
sql_sequence = "SELECT * FROM sec.t_sequence WHERE seq_schema = '§schema§'"
sql_seq2rol = "SELECT * FROM sec.t_seq2rol WHERE s2r_seq_id = §id§"
sql_usr2rol = "SELECT * FROM sec.t_usr2rol WHERE u2r_rol_id = §id§"
sql_user = "SELECT * FROM sec.t_user WHERE usr_id = §id§"

def get_schema():
    database.exec(sql_init)
    row = database.fetch()
    while row != False:
        schema_list.append(row['SCHEMANAME'].strip())
        row = database.fetch()
    pass

def get_table(schema):
    sql = sql_table.replace('§schema§',schema)
    database.exec(sql)
    row = database.fetch()
    while row != False:
        table_list.append(row)
        row = database.fetch()
    pass

def get_tbl2rol(id):
    sql = sql_tbl2rol.replace('§id§',str(id))
    database.exec(sql)
    row = database.fetch()
    while row != False:
        tbl2rol_list.append(row)
        row = database.fetch()
    pass

def get_role():
    tmp_role_list:list = []
    for rol_id in tbl2rol_list:
        tmp_role_list.append(rol_id['T2R_ROL_ID'])
    for rol_id in rou2rol_list:
        tmp_role_list.append(rol_id['R2R_ROL_ID'])
    for rol_id in seq2rol_list:
        tmp_role_list.append(rol_id['S2R_ROL_ID'])
    tmp_role_list = set(tmp_role_list)
    for id in tmp_role_list:
        sql = sql_role.replace('§id§',str(id))
        database.exec(sql)
        row = database.fetch()
        while row != False:
            role_list.append(row)
            row = database.fetch()
    pass

def get_routine(schema):
    sql = sql_routine.replace('§schema§',schema)
    database.exec(sql)
    row = database.fetch()
    while row != False:
        routine_list.append(row)
        row = database.fetch()
    pass

def get_rou2rol(id):
    sql = sql_rou2rol.replace('§id§',str(id))
    database.exec(sql)
    row = database.fetch()
    while row != False:
        rou2rol_list.append(row)
        row = database.fetch()
    pass

def get_sequence(schema):
    sql = sql_sequence.replace('§schema§',schema)
    database.exec(sql)
    row = database.fetch()
    while row != False:
        sequence_list.append(row)
        row = database.fetch()
    pass

def get_seq2rol(id):
    sql = sql_seq2rol.replace('§id§',str(id))
    database.exec(sql)
    row = database.fetch()
    while row != False:
        seq2rol_list.append(row)
        row = database.fetch()
    pass

def get_usr2rol(id):
    sql = sql_usr2rol.replace('§id§',str(id))
    database.exec(sql)
    row = database.fetch()
    while row != False:
        usr2rol_list.append(row)
        row = database.fetch()
    pass

def get_user(id):
    sql = sql_user.replace('§id§',str(id))
    database.exec(sql)
    row = database.fetch()
    while row != False:
        dbuser_list.append(row)
        row = database.fetch()
    pass

def write_data(schema):
    with open(f'{schema}_IMPORT.sql','w+') as cover:
        cover.write(f'--#SET TERMINATOR @\n')
        if dbuser_list:
            write_routine(f'{schema}_USER.csv',dbuser_list)
            cover.write(f'IMPORT FROM {schema}_USER OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_user\n')
        if role_list:
            write_routine(f'{schema}_ROLE.csv',role_list)
            cover.write(f'IMPORT FROM {schema}_ROLE OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_role\n')
        if table_list:
            write_routine(f'{schema}_TABLE.csv',table_list)
            cover.write(f'IMPORT FROM {schema}_TABLE OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_table\n')
        if routine_list:
            write_routine(f'{schema}_ROUTINE.csv',routine_list)
            cover.write(f'IMPORT FROM {schema}_ROUTINE OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_routine\n')
        if sequence_list:
            write_routine(f'{schema}_SEQUENCE.csv',sequence_list)
            cover.write(f'IMPORT FROM {schema}_SEQUENCE OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_sequence\n')
        if usr2rol_list:
            write_routine(f'{schema}_USR2ROL.csv',usr2rol_list)
            cover.write(f'IMPORT FROM {schema}_USR2ROL OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_usr2rol\n')
        if tbl2rol_list:
            write_routine(f'{schema}_TBL2ROL.csv',tbl2rol_list)
            cover.write(f'IMPORT FROM {schema}_TBL2ROL OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_tbl2rol\n')
        if rou2rol_list:
            write_routine(f'{schema}_ROU2ROL.csv',rou2rol_list)
            cover.write(f'IMPORT FROM {schema}_ROU2ROL OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_rou2rol\n')
        if seq2rol_list:
            write_routine(f'{schema}_SEQ2ROL.csv',seq2rol_list)
            cover.write(f'IMPORT FROM {schema}_SEQ2ROL OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_seq2rol\n')
        cover.close()
    pass

def write_routine(item,item_list):
    with open(item,'w+') as file:
        for line in item_list:
            record:str = ''
            for key in line.keys():
                record += f'{str(line[key]).strip()};'
            #print(record[:-1])
            file.write(f'{record[:-1]}\n')
        file.close()
    # --------------------------------------------------
    pass

get_schema()
for schema in schema_list:
    get_table(schema)
    for id in table_list:
        get_tbl2rol(id['TBL_ID'])
    get_routine(schema)
    for id in routine_list:
        get_rou2rol(id['ROU_ID'])
    get_sequence(schema)
    for id in sequence_list:
        get_seq2rol(id['SEQ_ID'])
    get_role()
    for id in role_list:
        get_usr2rol(id['ROL_ID'])
    for id in usr2rol_list:
        get_user(id['U2R_USR_ID'])
    print("--------------------------------------------------------------------------------")
    print(f"Schema:{schema}")
    write_data(schema)
    table_list, routine_list, sequence_list = [], [], []
    tbl2rol_list, rou2rol_list, seq2rol_list = [], [], []
    role_list, usr2rol_list, dbuser_list = [], [], []






