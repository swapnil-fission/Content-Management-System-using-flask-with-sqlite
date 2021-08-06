from flask import Flask,request,session,jsonify
import sqlite3 as sql
import re
import base64

app = Flask(__name__)
app.secret_key = 'development key'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#user will register here use regex for validation
@app.route("/saveuser",methods=['POST'])
def saveuserdata():
    try:
        if request.method == 'POST':
            re_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            re_pwd = r'\A(?=\S*?[A-Z])(?=\S*?[a-z])\S{8,}\Z'
            re_phone = r'^[0-9]{10}$'
            re_pincode = r'^[0-9]{6}$'

            userDetails = request.form
            email = userDetails['email']
            password = userDetails['password']
            fullname = userDetails['fullname']
            phone = userDetails["phone"]
            address = userDetails["address"]
            city = userDetails["city"]
            state = userDetails["state"]
            country = userDetails['country']
            pincode = userDetails['pincode']
            print(fullname)

            if (re.match(re_email, email) and re.match(re_pwd, password) and re.match(re_phone, phone) and re.match(
                    re_pincode, pincode)):
                #print("ccccccccccccccccccccccccc")
                con = sql.connect('sqlassignment.db')
                cur = con.cursor()
                #print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
                cur.execute("INSERT INTO user (email,password,fullname,phone,address,city,state,country,pincode) VALUES (?,?,?,?,?,?,?,?,?) ",(email,password,fullname,phone,address,city,state,country,pincode))
                #print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                con.commit()
                return "Data Added Successfully"
            else:
                return "Enter valid data"
        return "Error"
    except Exception as e:
        print(e)
    finally:
        print("ok")
        cur.close()
        con.close()

#login method to check user is authorize or not
@app.route("/login",methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            email=request.form['email']
            password = request.form['password']
            con = sql.connect('sqlassignment.db')
            #print("aaaaaaaaaaaaaaaaa")
            cur = con.cursor()
            cur.execute('SELECT * from user WHERE email=? AND password=?',(email,password))
            #print("bbbbbbbbbbbbbbbb")
            r=cur.fetchall()
            for i in r:
                if email == i[1] and password ==i[2]:
                    session["loggedin"]=True
                    session["email"]= email
                    return "Log in successfully"
                else:
                    return "Enter Valid Email and passsword"
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#logout method
@app.route("/logout")
def logout():
    session.clear()
    return "Logout Successfully"

#method for add content foreign key(userid) used here to maintain relationship between table
#we have to send pdf file in postman and it will store in blob format
@app.route("/addcontent",methods=['POST'])
def addcontent():
    try:
        if request.method == 'POST':
            print("start")
            #re_title="^[a-zA-Z](\s?[a-zA-Z]){,30}$"
            #re_body="^[a-zA-Z](\s?[a-zA-Z]){,300}$"
            #re_summary="^[a-zA-Z](\s?[a-zA-Z]){,60}$"
            #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            cont=request.form
            title=cont['title']
            body=cont['body']
            summary=cont['summary']
            docs=request.files['docs']
            d=docs.read()
            categories=cont['categories']
            userid=cont['userid']
            #print("qqqqqqqqqqqqqqqqqqq")

            #with open(docs,'rb') as d:
                #blob = base64.b64encode(d.read())
                #print(blob)
            #if (re.match(re_title,title) and re.match(re_body,body) and re.match(re_summary,summary)):
            if ((len(title) <= 30) and (len(body) <= 300) and (len(summary) <= 60)):
                con = sql.connect('sqlassignment.db')
                cur = con.cursor()
                cur.execute('INSERT INTO content(title,body,summary,docs,categories,userid) VALUES (?,?,?,?,?,?)',
                            (title, body, summary, d, categories, userid))
                con.commit()
                return "Data Added Successfully"
            else:
                return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#method to get single user data using cid. we can use our foreignkey i.e userid to ftch data by user
#pdf file is saved in the D drive and other data will shown in postman
@app.route("/getcontent/<int:id>",methods=["GET"])
def getcontent(id):
    try:
        if request.method == 'GET':
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM content WHERE cid=?",(id,))
            rec = cur.fetchall()
            for r in rec:
                docs = r[4]
                t=r[1]
                docspath = r"D:\\" + t + ".pdf"
                with open(docspath, 'wb') as fi:
                    fi.write(docs)
                    fi.close()
            #print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            res =[
                    dict(cid=r[0],title=r[1],body=r[2],summary=r[3],categories=r[5],userid=r[6])
                    for r in rec
                ]

            return jsonify(res)
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#method for delete content
@app.route("/deletecontent/<int:id>",methods=['DELETE'])
def deletecontent(id):
    try:
        if request.method=='DELETE':
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            cur.execute('DELETE FROM content where cid=?',(id,))
            con.commit()
            return "the content with id {} ha been deleted".format(id),200
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#method for update all content
@app.route("/updatecontent/<int:id>",methods=['PUT'])
def updateuser(id):
    try:
        if request.method == 'PUT':
            #re_title = "^[a-zA-Z](\s?[a-zA-Z]){,30}$"
            #re_body = "^[a-zA-Z](\s?[a-zA-Z]){,300}$"
            #re_summary = "^[a-zA-Z](\s?[a-zA-Z]){,60}$"
            print("aaaaaaaaaaaaaaaa")
            cont = request.form
            title = cont['title']
            body = cont['body']
            summary = cont['summary']
            docs = request.files['docs']
            d = docs.read()
            categories = cont['categories']
            print("bbbbbbbbbbbbbbbbbbbbb")
            print(len(title),len(body),len(summary))
            #if (re.match(re_title, title) and re.match(re_body, body) and re.match(re_summary, summary)):
            if((len(title)<=30) and (len(body)<=300) and (len(summary)<=60)):
                print("ccccccccccccccccccc")
                con = sql.connect('sqlassignment.db')
                cur = con.cursor()

                cur.execute("UPDATE content SET title=?,body=?,summary=?,docs=?,categories=? WHERE cid=?",(title,body,summary,d,categories,id))
                con.commit()
                return "Data updated successfully"
            else:
                return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#serch content for title
# we have to give search string in url
@app.route("/gettitle/<title>",methods=['GET'])
def getdatabytitle(title):
    try:
        if request.method == 'GET':
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            print("AAAAAAaaa")
            arg=['%'+title+'%']
            cur.execute("SELECT * FROM content WHERE title LIKE ?",(arg))
            print("BBBBBBBBBBBBBB")
            #for rec in cur.fetchall():
                #print(rec)
                #return "OKKKKKKKKKK"
            res=[
                    dict(cid=r[0], title=r[1], body=r[2], summary=r[3],categories=r[5],userid=r[6])
                    for r in cur.fetchall()
                ]

            return jsonify(res)
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#search content by body
@app.route("/getbody/<string>",methods=['GET'])
def getdatabybody(string):
    try:
        if request.method == 'GET':
            #print(string)
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            #print("AAAAAAaaa")
            arg=['%'+string+'%']
            cur.execute("SELECT * FROM content WHERE body LIKE ?",(arg))
            #print("BBBBBBBBBBBBBB")
            res=[
                    dict(cid=r[0], title=r[1], body=r[2], summary=r[3],categories=r[5],userid=r[6])
                    for r in cur.fetchall()
                ]

            return jsonify(res)
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#search by summary
@app.route("/getsummary/<string>",methods=['GET'])
def getdatabysummary(string):
    try:
        if request.method == 'GET':
            #print(string)
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            #print("AAAAAAaaa")
            arg=['%'+string+'%']
            cur.execute("SELECT * FROM content WHERE summary LIKE ?",(arg))
            #print("BBBBBBBBBBBBBB")
            res=[
                    dict(cid=r[0], title=r[1], body=r[2], summary=r[3],categories=r[5],userid=r[6])
                    for r in cur.fetchall()
                ]

            return jsonify(res)
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")

#search by Categories
@app.route("/getcategory/<string>",methods=['GET'])
def getdatabycategory(string):
    try:
        if request.method == 'GET':
            #print(string)
            con = sql.connect('sqlassignment.db')
            cur = con.cursor()
            #print("AAAAAAaaa")
            arg=['%'+string+'%']
            cur.execute("SELECT * FROM content WHERE categories LIKE ?",(arg))
            #print("BBBBBBBBBBBBBB")
            res=[
                    dict(cid=r[0], title=r[1], body=r[2], summary=r[3],categories=r[5],userid=r[6])
                    for r in cur.fetchall()
                ]

            return jsonify(res)
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")




if __name__ =='__main__':
    app.run(debug = True)