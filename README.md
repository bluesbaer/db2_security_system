# db2_security_system

This is a rolebased user administration tool for Db2 databases.  
1. Prerequisites:  
Python3.7  
tkinter  
ibm_db (Db2 Python Driver: pip install ibm_db)

2. install_security.py
This program connects to the database and  
Creates bufferpool and tablespaces for the Security-System  
Creates tables, indexes and views for the data used in the Security-System
Creates an procedure to activate or deactivate user permissions in the database  
**Run the installation**  
    *python install_security.py*
    The program comes up with an screen where you have to fill in:   
    - servername of the database
    - portnumber of the database
    - name of the database
    - connect user (user with password known to the database server)
    - administration user (virtual user)
    - security user (virtual user)
    Only if you use SSL (optional)
    - path to the SSL-Files
    - SSL-Key
    - SSL-Stash  
    
    **VIRTUAL USER**  
    In the Security-System only the CONNECT-User is alowed to connect to the database.  
    But he is not allowed to maintain data or maintain database objects.  
    But he is allowed to become an other user like the ADMINISTRATION-User or the SECURITY-User.  
    *SET SESSION_USER = administration-user*   
    *SET SESSION_USER = security-user*   
    The ADMINISTRATION-User is not allowed to connect to the database.  
    And he is not allowed to GRANT or REVOKE user permissions.  
    But he is allowed to maintain database objects.  
    The SECURITY-User is also not allowed to connect to the database.  
    And he is also not allowed to maintain any database objects.  
    But he is allowed to GRENT or REVOKE user permissions.  
    So the CONNECT-User is an user known to your server with an passwor.  
    The ADMINISTRATOR- and the SECURITY-User could be any name that you want not known to the server and without any password.  
    Therfore they are called VIRTUAL-User and only the CONNECT-User is able to become the VIRTUAL-User.
    
3. mandant.py  
If you want to have SCHEMA-Security (per schema an ADMINISTRATION- and SECURITY-USER)  
Therefore you have to have the Security-System installed.
Then you run the mandant-program  
*python mandant.py*
In the first run you have to INITIALIZE the Security-System.  
Then you have to run the program for every schema (ADD CLIENT) you want to use the Security-System.  

4. execute_security.py  
If you have installed the Security-System (with or withoutSCHEMA-Security) this is the program to administrate user access.  
In the first screen you may store your connection data to connect to the database.
As soon as you've been connected to the database you will see:  
On the left side the 'Tree View' for you user permissions. This could be which role is attached to which user USER2ROLE.
Or the other way round ROLE2USER. 
You are also able to see TABLE2ROLE (TABLE = Table or View), ROUTINE2ROLE (ROUTINE = Function or Procedure) and SEQUENCE2ROLE.  
On the right side you see you will see the 'Edit View Select'.  
Here you may select what you want to maintain USER, ROLE or USER2ROLE or ...  
The 'Edit View' will change as you select an othe option in the 'Edit View Select'.  
Every entry in the Security-System has an START- and an END-Date which might reflect from which date to which date the permission is active.  
The radiobutton 'Businesstime' could be set to ON or OFF. Then the 'Tree View' shows only activ permissions or all permissions.  
To activate or deactivate permissions you have to run the Security-Procedure.  
Therefore an scheduler should run the Security-Procedure 'SEC.SECURITY2()' or you run it manualy 'CALL SEC.SECURITY2()'.  
If you have any problems with the Security-System then just go to the database server.  
Connect as the apropriate CONNECTION-User switch to the SECURITY-User and the type:
*db2 SET SERVEROUTPUT ON*  
*db2 "CALL SEC.SECURITY2()*  
This will show you the ERROR-Message and WHere in the Security-Procedure the Error hapened.  

5. migrate_2_multi.py  
If you started the Security-System without SCHEMA-Security and now you will activate the SCHEMA-Security.
Here you have to edit the program. You will find the codeline 'maintain this section'.  
Type in the servername, portnumber, etc. and start the program.  
The program creates per schema some CSV-Files and one IMPORT-File.  
Copy these files to the database server and connect for each schema as the corresponding CONNECT-User.  
Then switch to the corresponding SECURITY-User and run the IMPORT-File for your schema.  
**ATTENTION: The SECURITY-User needs LOAD-Permission**

If you have any problems you may contact me:
info@manfred-wagner.at
