from flask import Flask, escape, request, render_template, send_from_directory, make_response
import sqlite3

#Flask App Initialisation
app=Flask(__name__)
app.config['TESTING']=False

file_css="style.css"
file_logo="logo.jpg"
fdb="C:\\FastAcc\\local.db"

#Resets database for testing
file=open(fdb, mode='w')
file.truncate(0)
file.close()

#Database fields
voterinfo=['collectorid', 'voterid', 'gender', 'first', 'middle', 'last', 'officerno', 'dob']
vaddress=['locality', 'district', 'voterid']
agricultureloan=['collectorid', 'panid', 'customername', 'loanpurpose', 'amount', 'time', 'interest', 'start_date']
civil=['collectorid','projectid','name','area','start_date','budget','constractorname','nooflaboureres']
newemployee=['employeeid','name','e_email','password','contactno','dob','collectorid']
energydept=['collectorid','customerid','customername','unitsconsumed']
cost=['home','industry','commerical','customerid']

#DB
db=sqlite3.connect(fdb)
cur=db.cursor()
cur.executescript("""
CREATE TABLE login ( collectorid INT PRIMARY KEY, password VARCHAR2(16));
CREATE TABLE voterinfo (collectorid REFERENCES login(collectorid), voterid VARCHAR2(10) PRIMARY KEY, gender VARCHAR2(1), first VARCHAR2(10), middle VARCHAR2(10), last VARCHAR2(10), officerno INT, dob DATE);
CREATE TABLE vaddress ( locality VARCHAR2(20), district VARCHAR2(20), voterid REFERENCES voterinfo(voterid));
CREATE TABLE constructionandproject (collectorid REFERENCES login(collectorid), projectid INT PRIMARY KEY, name VARCHAR2(20), area VARCHAR2(20), start_date DATE, budget DOUBLE, constractorname VARCHAR2(30), nooflaboureres INT);
CREATE TABLE laddress ( locality VARCHAR2(20), landmark VARCHAR2(20), district VARCHAR2(20), panid VARCHAR2(10) PRIMARY KEY);
CREATE TABLE agricultureloan ( collectorid REFERENCES login(collectorid), panid VARCHAR2(10) PRIMARY KEY, customername VARCHAR2(30), loanpurpose VARCHAR2(30), amount DOUBLE, time DATE, interest DOUBLE, start_date DATE);
CREATE TABLE newemployee ( employeeid INT PRIMARY KEY, name VARCHAR2(30), e_email email, password VARCHAR2(16), contactno INT(10), dob DATE, collectorid REFERENCES login(collectorid));
CREATE TABLE energydept (collectorid INT, customerid INT, customername VARCHAR2(30), unitsconsumed DOUBLE);
CREATE TABLE costperunit (home VARCHAR2(20), industry VARCHAR2(20), commerical VARCHAR2(20), customerid INT);
INSERT INTO login(collectorid, password) VALUES ("el admino","Bruh");""")
db.commit()
db.close()


@app.route("/")
def home():
	return render_template("home.html")
    
@app.route("/signup")
def signup():
    if request.method=="POST":
        newemployeeform="("+request.form['employeeid']+",'"+request.form['name']+"','"+request.form['e_email']+"','"+request.form['password']+"',"+request.form['contactno']+","+request.form['dob']+","+request.form['collectorid']+")"
        return _insertinto('newemployee',"("+','.join(newemployee)+")",newemployeeform)
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
        username=request.form['collectorid']
        password=request.form['password']
        if username== "" and password=="":
            return page_not_found("Empty form")
        else:
            db=sqlite3.connect(fdb)
            cur=db.cursor()
            cur.execute("select * from login where password='"+password+"'")
            res=cur.fetchall()
            test=username,password
            for i in res:
                if test==i:
                    req=make_response(render_template("login.html"))
                    req.set_cookie('username',value=username)
                    return "Authentication_success"
            return "Invalid Credentials"

@app.route("/login", methods=["GET"])
def login_get():
        return render_template("login.html")

@app.route("/voterid", methods=['GET','POST'])
def voterid():
    if request.method=='POST':
        voterinfoform="("+request.form['collectorid']+",'"+request.form['voterid']+"','"+request.form['gender']+"','"+request.form['first']+"','"+request.form['middle']+"','"+request.form['last']+"',"+request.form['officerno']+","+request.form['dob']+")"
        vaddressform="('"+request.form['locality']+"','"+request.form['district']+"','"+request.form['voterid']+"')"
        return _insertinto('voterinfo',"("+','.join(voterinfo)+")",voterinfoform)+"\n"+_insertinto('vaddress',"("+','.join(vaddress)+")",vaddressform)
    return render_template("voterid.html")

@app.route("/agricultureloan")
def agricultureloan():
    if request.method=="POST":
        agricultureloanform="("+request.form['collectorid']+","+request.form['panid']+","+request.form['customername']+","+request.form['loanpurpose']+","+request.form['amount']+","+request.form['time']+","+request.form['interest']+request.form['start_date']+")"
        return _insertinto('agricultureloan',"("+','.join(agricultureloan)+")",agricultureloanform)
    return render_template("agricultureloan.html")

@app.route("/civil")
def civil():
    if request.method=="POST":
        civilform="("+request.form['collectorid']+","+request.form['projectid']+","+request.form['name']+","+request.form['area']+","+request.form['start_date']+","+request.form['constractorname']+","+request.form['nooflaboureres']+")"
        return _insertinto('constructionandproject',"("+','.join(civil)+")",civilform)
    return render_template("civil.html")

@app.route("/energy")
def energy():
    if request.method=="POST":
        energydeptform="("+","+request.form['collectorid']+","+request.form['customerid']+","+request.form['customername']+","+request.form['unitsconsumed']+")"
        return _insertinto('energydept',"("+','.join(energydept)+")",enegydeptform)
    return render_template("energy.html")

@app.route("/costperunit",methods=["GET"])
def costperunit_get():
    dbd=sqlite3.connect(fdb)
    cur=dbd.cursor()
    cur.execute("select * from costperunit")
    res=cur.fetchall()
    return str(res)

@app.route("/setcostperunit",methods=["POST"])
def costperunit_post():
    if login()=="Authentication_success":
        costperunitform="("+","+request.form['home']+","+request.form['industry']+","+request.form['commerical']+","+request.form['customerid']+")"
        return _insertinto('costperunit',"("+','.join(costperunit)+")",costperunitform)
    else:
        return "Error 403"

@app.route("/setcostperunit",methods=["POST"])
def costperunit():
    return render_template("cost.html")

@app.route("/favicon.ico")
def favicon():
    return "C"

@app.route("/viewdata", methods=["POST"])
def viewdata_post():
    dbd=sqlite3.connect(fdb)
    cur=dbd.cursor()
    if request.form['tablename'].isspace():
        return "Invalid table name or entry."
    if login()=="Authentication_success":
        cur.execute("SELECT * FROM "+request.form['tablename'])
        return str(cur.fetchall())
    elif request.form['tablename']=="login":
        return "Error 403"
    else:
        cur.execute("SELECT * FROM "+request.form['tablename']+" WHERE "+request.form['entry'])
        return _tablise(request.form['tablename'],cur.fetchall())

@app.route("/viewdata", methods=["GET"])
def viewdata_get():
    return render_template("viewdata.html")
    
@app.route("/"+file_logo)
def logo():
    print("/"+file_logo)
    return send_from_directory("D:\\Sem F2020\\DBMS\\perojeckt",file_logo)

@app.route("/"+file_css)
def css():
    print("/"+file_css)
    return send_from_directory("/",file_css)

@app.errorhandler(404)
def page_not_found(i):
    return i

@app.errorhandler(403)
def not_allowed(i):
    return i

#Internal functions
def _insertinto(tablename, sequence, values):
    dbd=sqlite3.connect(fdb)
    cur=dbd.cursor()
    cur.execute("insert into "+tablename+sequence+" values "+values)
    dbd.commit()
    dbd.close()
    return "Value inserted"+values
base="""
<!DOCTYPE html>
<html>
<head>
	<title>Agricultural Loan</title>
	<style>
		body{background-color: Lightblue;
			color:Black;
			background-size: cover;
		    }
		h1{
			text-align: center;
			font-family:Lucida Handwritting; 
			position: absolute;
            left: 400px;
            top: 30px;
		}
		h4{
			position: absolute;
            left: 400px;
            top: 100px;
		}
		table, th {
			border: 1px solid black;
		}
		table{
			background-color: White;
		}
		

     </style>
</head>
<body>
	<h1><strong>Data View</strong></h1>

"""
def _tablise(table, table_entries):
    tab=[]
    for i in table:
        tab.append("<td>"+"</td><td>".join(i)+"</td>")
    thable='</tr><tr>'.join(tab)
    thable=base+"<table><th>"+"</th><th>".join(table_entries)+"</th>"+table+"</table>"
    print("Tablise")
    print(thable)
    return thable

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
