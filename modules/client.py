from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd


def get_details(email):
    global name, location, gen, clicid
    q = f'select CName,CLocation,CGender,CID from mydb.client where CEmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    name = d[0][0]
    location = d[0][1]
    gen = d[0][2]
    clicid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


# ---------------------------------------------Apply a Job---------------------------------------------------
def apply(table):
    # fetch cid,jid from treeview that is in available jobs function
    # code
    selectedindex = table.focus()     # that will return number index
    # that will return list of values with columns=['JID','JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification','MinExp', 'Salary']
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    chkquery = f'SELECT * from mydb.application where cid={clicid} and jid={ajid}'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(chkquery)
    tempbuff = cur.fetchall()
    mycon.close()
    if(tempbuff):
        messagebox.showinfo(
            'Oops', 'It seems like you have already applied to this job')
    else:
        queryapplyjob = f'Insert into application values(NULL,(select rid from mydb.job where job.jid={ajid}),{ajid},{clicid})'
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(queryapplyjob)
        mycon.commit()
        mycon.close()
        messagebox.showinfo('Thanks', 'Your application has been submitted')

# ----------------------------------------------Delete A Job -----------------------------------


def delet(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    aaid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'delete from mydb.application where aid={aaid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your application has been Deleted')
    myapp()


# -------------------------------------------- Sort Queries --------------------------------------------------------
def sort_alljobs(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(
            f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid order by {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1


def sort_myapplications(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute(
            f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid} order by {criteria}')
        jobs = cur.fetchall()
        mycon.close()
        i = 0
        for r in jobs:
            table.insert('', i, text="", values=(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
            i += 1

# ----------------------------------------------Show all Jobs-----------------------------------------------


def showalljobs(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select job.JID,job.JobRole,job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.Qualification, job.MinExp, job.Salary from mydb.job JOIN mydb.recruiter ON job.rid=recruiter.rid')
    jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in jobs:
        table.insert('', i, text="", values=(
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        i += 1

# ----------------------------------------------Show my Applications-----------------------------------------------------


def show_myapplications(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT application.aid,job.JobRole, job.JobType, recruiter.CompanyName, recruiter.CompanyLocation, job.qualification, job.minexp, job.salary FROM application JOIN recruiter ON application.rid=recruiter.rid JOIN job ON application.jid=job.jid where application.CID={clicid}')
    applications = cur.fetchall()
    mycon.close()
    print(applications)
    i = 0
    for x in applications:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
        i += 1


# ----------------------------------------------Available Jobs----------------------------------------------------

def available():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_alljobs(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    apl = Button(rt, text="Apply", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: apply(table))
    apl.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11),  rowheight=30)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set, style='mystyle.Treeview')
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text='CompanyName')
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=100, anchor=CENTER)
    table.column("JobRole", width=150, anchor=CENTER)
    table.column("JobType", width=150, anchor=CENTER)
    table.column("CompanyName", width=150, anchor=CENTER)
    table.column("CompanyLocation", width=150, anchor=CENTER)
    table.column("Qualification", width=100, anchor=CENTER)
    table.column("MinExp", width=100, anchor=CENTER)
    table.column("Salary", width=150, anchor=CENTER)
    showalljobs(table)
    table.pack(fill="both", expand=1)
    mycon.close()


# -----------------------------------------My Applictions----------------------------------------------------------------
def myapp():
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=('normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType', 'CompanyLocation')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="#00b9ed",
                    fg="#ffffff", command=lambda: sort_myapplications(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)

    search = Button(rt, text="Sort", font=('normal', 12, 'bold'), bg="#00b9ed",
                    fg="#ffffff", command=lambda: sort_myapplications(table))

    dlt = Button(rt, text="Delete", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: delet(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11),  rowheight=30)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    table = ttk.Treeview(tab, columns=('AID', 'JobRole', 'JobType', 'CompanyName', 'CompanyLocation', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set, style='mystyle.Treeview')

    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("AID", text="AID")
    table.heading("JobRole", text="JobRole")
    table.heading("JobType", text="JobType")
    table.heading("CompanyName", text='CompanyName')
    table.heading("CompanyLocation", text="CompanyLocation")
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")
    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("AID", width=50, anchor=CENTER)
    table.column("JobRole", width=150, anchor=CENTER)
    table.column("JobType", width=150, anchor=CENTER)
    table.column("CompanyName", width=150, anchor=CENTER)
    table.column("CompanyLocation", width=150, anchor=CENTER)
    table.column("Qualification", width=100, anchor=CENTER)
    table.column("MinExp", width=100, anchor=CENTER)
    table.column("Salary", width=150, anchor=CENTER)
    show_myapplications(table)
    table.pack(fill="both", expand=1)
    mycon.close()


# ---------------------------------------------------------------------------------------------------------------------------
def cli(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    get_details(email)

    bg.load = PhotoImage(file=f'elements\\bg{gen}.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # Navbar
    nm = Label(root, text=f'{name}', font=(
        'normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{location}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=('normal', 20),
                bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=240)
    ep = Button(lf, text="Edit Profile", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: client_edit(root))

    ep.grid(row=0, column=0, padx=60, pady=30)
    pj = Button(lf, text="Available Jobs", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=available)
    pj.grid(row=1, column=0, padx=60, pady=30)
    ap = Button(lf, text="My Applications", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=myapp)
    ap.grid(row=2, column=0, padx=60, pady=30)

    # Right
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)

def client_edit(root):

    q = f'SELECT CAge, CLocation, CGender, CExp, CSkills, CQualification from mydb.client where CEmail="{email}";'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    cAge = d[0][0]
    cLocation = d[0][1]
    cGender = d[0][2]
    cExp = d[0][3]
    cSkills = d[0][4]
    cQualification = d[0][5]


    print("hello ", name, ", Edit your profile")
    r3 = Frame(root, height=700, width=1050)
    r3.place(x=0, y=0)
    r3.render = PhotoImage(file="elements/edit_bg.png")
    img = Label(r3, image=r3.render)
    img.place(x=0, y=0)

    global gender, age, loc, workxp, qualification, skills
    gender = StringVar()

    style = ttk.Style(r3)
    style.configure("TRadiobutton", background="#329DF3",
                    foreground="#000000", font=("arial", 16, "bold"))

    gender_l = Label(r3, text="Gender : ", bg='#329DF3', fg="#FFDE59",
                     font=('normal', 20, 'bold'))
    gender_l.place(x=600, y=200)
    ttk.Radiobutton(r3, text="Male", value="M", variable=gender).place(
        x=800, y=200)
    ttk.Radiobutton(r3, text="Female", value="F", variable=gender).place(
        x=900, y=200)
    gender.set(cGender)

    age_l = Label(r3, text="Age : ", bg='#329DF3', fg="#FFDE59",
                  font=('normal', 20, 'bold'))
    age_l.place(x=600, y=250)
    age = Entry(r3, placeholder='Age', width=20)
    age.insert(cAge)
    age.place(x=790, y=250)

    loc_l = Label(r3, text="Location : ", bg='#329DF3', fg="#FFDE59",
                  font=('normal', 20, 'bold'))
    loc_l.place(x=600, y=300)
    loc = Entry(r3, placeholder='Location', width=20)
    loc.insert(cLocation)
    loc.place(x=790, y=300)

    workxp_l = Label(r3, text="Experience : ", bg='#329DF3', fg="#FFDE59",
                     font=('normal', 20, 'bold'))
    workxp_l.place(x=600, y=350)
    workxp = Entry(r3, placeholder='Work Experience(yrs)', width=20)
    workxp.insert(cExp)
    workxp.place(x=790, y=350)

    qualification_l = Label(r3, text="Qualification : ",
                            bg='#329DF3', fg="#FFDE59", font=('normal', 20, 'bold'))
    qualification_l.place(x=600, y=400)
    qualification = Entry(r3, placeholder='Btech/BE...', width=20)
    qualification.insert(cQualification)
    qualification.place(x=790, y=400)

    skills_l = Label(r3, text="Skills : ", bg='#329DF3',
                     fg="#FFDE59", font=('normal', 20, 'bold'))
    skills_l.place(x=600, y=450)
    skills = Entry(r3, placeholder='separated by comma', width=20)
    skills.insert(cSkills)
    skills.place(x=790, y=450)

    r3.bn = PhotoImage(file="elements\\update.png")
    btn = Button(r3, image=r3.bn, bg='#329DF3', bd=0,
                 activebackground="#ffffff", command=lambda: client_submit(root))
    btn.place(x=820, y=550)

    r3.bn2 = PhotoImage(file="elements\\back.png")
    btn2 = Button(r3, image=r3.bn2, bg='#329DF3', bd=0,
                 activebackground="#ffffff", command=lambda: cli(root, email))
    btn2.place(x=620, y=550)


def client_submit(root):
    global gender1, age1, loc1, workxp1, qualification1, skills1
    gender1 = gender.get()
    age1 = age.get()
    loc1 = loc.get()
    workxp1 = workxp.get()
    qualification1 = qualification.get()
    skills1 = skills.get()
    print(name, email, gender1, age1, loc1, workxp1, qualification1, skills1)
    if gender1 and age1 and loc1 and workxp1:
        exe1 = f'UPDATE mydb.Client SET CAge = {age1}, CLocation = "{loc1}", CGender = "{gender1}", CExp = {workxp1}, CSkills = "{skills1}", CQualification = "{qualification1}" WHERE CName = "{name}";'
        try:
            mycon = sql.connect(host='localhost', user='root',
                                passwd=user_pwd, database='mydb')
            cur = mycon.cursor()

            cur.execute(exe1)
            messagebox.showinfo('SUCCESS!', 'Profile Updated')
            cli(root, email)
            name.delete(0, END)
            email.delete(0, END)
            gender.delete(0, END)
            loc.delete(0, END)
            age.delete(0, END)
            workxp.delete(0, END)
            qualification.delete(0, END)
            skills.delete(0, END)
            mycon.commit()
            mycon.close()
            logi(root)
        except:
            pass

    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS MUST BE FILLED')
