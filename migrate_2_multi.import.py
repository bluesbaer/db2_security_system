#!/dev/usr python
import os

schema = 'USR2'

def get_working_list():
    working_list:list = []
    files = os.listdir('.')
    for file in files:
        part = file.split('.')
        if str(part[-1]).upper() == 'CSV':
            part = file.split('_')
            if str(part[0]).upper() == schema.upper():
                working_list.append(file)
    return working_list

def cr_import_statement(working_list):
    sql = 'db2 "IMPORT FROM §file§ OF DEL MODIFIED BY COLDEL; IMPLICITLYHIDDENMISSING INSERT INTO sec.t_§table§"'
    for file in working_list:
        schema = file.split('_')[0]
        table = file.split('_')[1].split('.')[0]
        tmp_sql = sql.replace('§file§',file)
        tmp_sql = tmp_sql.replace('§table§',table)
        print(f"{tmp_sql}")


if __name__ == '__main__':
    working_list:list = []
    working_list = get_working_list()
    cr_import_statement(working_list)