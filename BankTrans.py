import sqlite3
def tras2(vec,num):
    #print(num)
    vnum=num.lower()
    veh=vec
    conn = sqlite3.connect("project1.db")
    cur = conn.cursor()
    res=cur.execute("select count(*) from vech_register where vechNumb in (:1)",{"1":str(vnum)})
    for r in res:
        res=r[0]
    #print(res)
    if res == 1:
        if veh == "Car":
            amount = 100
        elif veh == "Bus":
            amount = 150;
        elif veh=="Lorry":
            amount = 200;
        else:
            amount=0

        #print("hello")
        conn1 = sqlite3.connect("project1.db")
        cur = conn1.cursor()
        cur.execute("update BankAcc_Details a set amount=a.amount-:1 where AccNum =(select  AccNum from vech_register where vechNumb=:2) ",
            {"2": str(vnum), "1": amount})
        #print("hello1")
        conn1.commit()
        out= "Thank you and Amount:",amount,"  has been deducted"

        #return amount
    else:
        out=0
    return  out

