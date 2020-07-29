import sqlite3

conn=sqlite3.connect("project1.db")
c=conn.cursor()
#c.execute("create table BankAcc_Details(AccNum number(20),amount number(20),foreign key(AccNum) references vech_register(AccNum))")
c.execute("INSERT INTO BankAcc_Details VALUES(543210,1000)")
conn.commit()

