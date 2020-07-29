import csv
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
import vehicle as v
import PIL
import sqlite3
import cx_Oracle
import BankTrans as bt
import numberread as nr
import os


def register_user():
    name_info=name.get()
    rc_info=rcnumber.get()
    vec_info=vecnum.get()
    acc_info=AccNum.get()
    phn_info=phoneNum.get()
    #conn = sqlite3.connect('example.db')

    conn = sqlite3.connect("project1.db")
    cur = conn.cursor()
    cur.execute("insert into vech_register(name,RC,vechNumb,AccNum,phnenumber) values(:1,:2,:3,:4,:5) ",{"1":str(name_info),"2":str(rc_info),"3":str(vec_info),"4":str(acc_info),"5":str(phn_info)})
    conn.commit()

    name_entry.delete(0,END)
    rc_entry.delete(0,END)
    Vnum_entry.delete(0,END)
    BNum_entry.delete(0,END)
    PNum_entry.delete(0,END)

    Label(screen1,text="Registration Success",bg="green",width="300",height="2",font=("calibri,13")).pack()

#**********************************************************************************************************************************************************

def register():
    global screen1
    screen1=Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("400x350")
    global name
    global rcnumber
    global vecnum
    global AccNum,phoneNum
    global name_entry,rc_entry,Vnum_entry,BNum_entry,PNum_entry
    name=StringVar()
    rcnumber=StringVar()
    vecnum=StringVar()
    AccNum=StringVar()
    phoneNum=StringVar()
    Label(screen1, text="*******Registration Form********",bg="OliveDrab4",width="300",height="2",font=("calibri,13")).pack()
    screen1.config(bg="OliveDrab4")
    Label(screen1, text="",bg="OliveDrab4").pack()
    #Name
    Label(screen1,text="NameOfPerson *",bg="OliveDrab4").pack()
    name_entry=Entry(screen1,textvariable = name)
    name_entry.pack()
    #RCNumber
    Label(screen1,text="RCNumber*",bg="OliveDrab4").pack()
    rc_entry=Entry(screen1,textvariable = rcnumber)
    #rc_entry.set(rc_entry.get()[:5])
    rc_entry.pack()
    #VehicleNUmber
    Label(screen1, text="VehicleNumber(lowercase) *",bg="OliveDrab4").pack()
    Vnum_entry = Entry(screen1, textvariable=vecnum)
    Vnum_entry.pack()
    #AccNum
    Label(screen1, text="BankAccountNumber*",bg="OliveDrab4").pack()
    BNum_entry = Entry(screen1, textvariable=AccNum)
    BNum_entry.pack()
    #phonenumber
    Label(screen1, text="PhoneNumber*", bg="OliveDrab4").pack()
    PNum_entry = Entry(screen1, textvariable=phoneNum)
    PNum_entry.pack()
    Label(screen1, text="",bg="OliveDrab4").pack()
    Button(screen1,text="register",width="10",height="1",command=register_user).pack()

#********************************************************************************************************************************************************************************
def open_file():
    global screen4
    res=filedialog.askopenfilename(initialdir="E:\\Final_prjt-2020-2\\LicPlateImages\\correct_pred",title="selectFile",filetype=(("Png files",".png"),("all files",".*")))
    #res=nr.num_read()
    #print(res)
    vechile=v.test_single_image(res)
    numbers=nr.num_read(res)
    print(vechile,numbers.lower())
    resu=bt.tras2(vechile,numbers)
    #output="vechile Number:",numbers,"has passed by tollgate",resu,"at",current_time
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    with open('loggingData.csv', mode='a', newline='') as log_file:
        employee_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([numbers, vechile, current_time])
    print("******Done**********")
    if resu ==0:
        output="vechile Number:" + numbers +" Is Not Register Plz collect fare"
    else:
        output = "vechile Number:" + numbers + " has passed by tollgate " + " at " + str(current_time) + str(resu)
    Label(screen3, text=output, bg="red", width="500", height="2", font=("calibri,05")).pack()
    #Label(screen3, text=output_final, bg="red", width="500", height="2", font=("calibri,05")).pack()


def log_user():
    global screen3
    name_user=username.get()
    pass_user=password.get()
    conn = sqlite3.connect("project1.db")
    cur = conn.cursor()
    cur.execute("select count(*) from authentication where name =:1 and password=:2",{"1":str(name_user),"2":str(pass_user)})
    for row in cur:
        res=row[0]
    if res == 0:
        Label(screen2, text="Login Failed", bg="red", width="300", height="2", font=("calibri,13")).pack()
    else:
        screen3 = Toplevel(screen)
        screen3.title("ABCtollgate")
        screen3.geometry("500x500")
        Label(screen3, text="******* WelCome To ABC-Tollgate ********", bg="pink", width="300", height="2",
              font=("calibri,13")).pack()
        screen3.config(bg="pink")
        Label(screen3, text="",bg="pink").pack()
        Label(screen3, text="****Upload An Image****",bg="pink",width="200",height="2").pack()
        Label(screen3, text="",bg="pink").pack()
        Button(screen3, text="UpLoadImage", width="20", bg="powder blue",height="1", command=open_file).pack()
        screen3.mainloop()

#**********************************************************************************************************************************************************************************

def login():
    global screen2
    screen2=Toplevel(screen)
    screen2.title("Auth_Login")
    screen2.geometry("400x350")
    global username
    global password
    global username_entry,password_entry
    username=StringVar()
    password=StringVar()
    Label(screen2, text="*******Login For Auth********", bg="sandy brown", width="300", height="2",
          font=("calibri,13")).pack()
    screen2.config(bg="sandy brown")
    Label(screen2, text="",bg="sandy brown").pack()
    # Name
    Label(screen2, text="UserName *",bg="sandy brown").pack()
    username_entry = Entry(screen2, textvariable=username)
    username_entry.pack()
    #password
    Label(screen2, text="Password *",bg="sandy brown").pack()
    #password_entry = Entry(screen2, textvariable=password)
    #password_entry.pack()
    #Label(screen2, text="",bg="sandy brown").pack()
    passEntry = Entry(screen2, textvariable=password, show='*').pack()
    Button(screen2, text="LogIN", width="10", height="1",bg="powder blue", command=log_user).pack()

#***********************************************************************************************************************************************************************************

def main_screen():
    global screen
    screen=Tk()
    screen.geometry("300x250",)
    screen.title("TollGate Fare-Register")
    Label(text="TollGate Fare-Register",bg="dark slate gray",width="300",font=Font(size=16),height="2").pack()
    screen.config(bg="dark slate gray")
    Label(screen, text="",bg="dark slate gray").pack()
    Button(text="Login",height="2",width="30",bg="powder blue",command=login).pack()
    Label(text="",bg="dark slate gray").pack()
    Button(text="VehicleRegister", height="2" ,width="30",bg="powder blue",command=register).pack()
    screen.mainloop()

if __name__ == "__main__":
    main_screen()




