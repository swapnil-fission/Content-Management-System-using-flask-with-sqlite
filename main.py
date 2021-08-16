from flask import Flask, request, session, jsonify
import sqlite3 as sql
import re
from dbConnection import openConn
import os

app = Flask(__name__)
app.secret_key = 'development key'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/user", methods=['POST'])
def userData():
    try:
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

        if (re.match(re_email, email) and re.match(re_pwd, password) and re.match(re_phone, phone) and re.match(
                re_pincode, pincode)):
            con = openConn()
            con.execute(
                "INSERT INTO user (email,password,fullname,phone,address,city,state,country,pincode) VALUES (?,?,?,?,?,?,?,?,?) ",
                (email, password, fullname, phone, address, city, state, country, pincode))
            con.commit()
            return "Data Added Successfully"
        else:
            return "Enter valid data"
    except Exception as err:
        print(err)
    finally:
        con.close()
        print("ok")


@app.route("/login", methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        con = openConn()
        cur = con.cursor()
        cur.execute('SELECT * from user WHERE email=? AND password=?', (email, password))
        if (len(list(cur)) == 1):
            session["loggedin"] = True
            session["email"] = email
            return "Log in successfully"
        else:
            return "Enter Valid Email and passsword"
    except Exception as err:
        print(err)
    finally:
        cur.close()
        con.close()
        print("ok")


@app.route("/logout")
def logout():
    session.clear()
    return "Logout Successfully"


@app.route("/content", methods=['POST'])
def addContent():
    try:
        cont = request.form
        title = cont['title']
        body = cont['body']
        summary = cont['summary']
        docs = request.files['docs']
        data = docs.read()
        categories = cont['categories']
        userid = cont['userid']
        if ((len(title) <= 30) and (len(body) <= 300) and (len(summary) <= 60)):
            con = openConn()
            cur = con.cursor()
            cur.execute('INSERT INTO content(title,body,summary,docs,categories,userid) VALUES (?,?,?,?,?,?)',
                        (title, body, summary, data, categories, userid))
            con.commit()
            return "Data Added Successfully"
        else:
            return "Error"
    except Exception as err:
        print(err)
    finally:
        cur.close()
        con.close()
        print("ok")


@app.route("/content/<int:id>", methods=["GET"])
def getContent(id):
    try:
        con = openConn()
        cur = con.cursor()
        path = os.getcwd()
        cur.execute("SELECT * FROM content WHERE cid=?", (id,))
        for result in cur.fetchall():
            docs = result[4]
            title = result[1]
            docspath = path + "\\" + title + ".pdf"
            with open(docspath, 'wb') as file:
                file.write(docs)
                file.close()
        return {
            'cid': result[0],
            'title': result[1],
            'body': result[2],
            'summary': result[3],
            'categories': result[5],
            'userid': result[6]
        }
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        print("ok")


@app.route("/content/<int:id>", methods=['DELETE'])
def deleteContent(id):
    try:
        if request.method == 'DELETE':
            con = openConn()
            con.execute('DELETE FROM content where cid=?', (id,))
            con.commit()
            return "the content with id {} ha been deleted".format(id), 200
        else:
            return "Error"
    except Exception as e:
        print(e)
    finally:
        con.close()
        print("ok")


@app.route("/content/<int:id>", methods=['PUT'])
def updateContent(id):
    try:
        cont = request.form
        title = cont['title']
        body = cont['body']
        summary = cont['summary']
        docs = request.files['docs']
        d = docs.read()
        categories = cont['categories']
        if ((len(title) <= 30) and (len(body) <= 300) and (len(summary) <= 60)):
            con = openConn()
            con.execute("UPDATE content SET title=?,body=?,summary=?,docs=?,categories=? WHERE cid=?",
                        (title, body, summary, d, categories, id))
            con.commit()
            return "Data updated successfully"
        else:
            return "Error"
    except Exception as err:
        print(err)
    finally:
        con.close()
        print("ok")


@app.route("/search/<data_field>", methods=['GET'])
def searchContent(data_field):
    try:
        #data_field = request.args.get('field')
        string_search = request.args.get('string')
        con = openConn()
        cur = con.cursor()
        arg = ['%' + string_search + '%']
        sub_query = data_field + ' LIKE '
        query = 'SELECT * FROM content WHERE ' + sub_query + '?'
        cur.execute(query, (arg))
        path = os.getcwd()
        alist = []
        for result in cur.fetchall():
            title = result[1]
            docs = result[4]
            adict = {'cid': result[0], 'title': result[1], 'body': result[2], 'summary': result[3],
                     'categories': result[5], 'userid': result[6]}
            alist.append(adict)
            docspath = path + "\\" + title + ".pdf"
            with open(docspath, 'wb') as file:
                file.write(docs)
                file.close()
        return jsonify(alist)
    except Exception as err:
        print(err)
    finally:
        cur.close()
        con.close()
        print("ok")


if __name__ == '__main__':
    app.run(debug=True)
