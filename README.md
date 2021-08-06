# Content-Management-System-using-flask-with-sqlite

1) insatall package like flask and sqlite3
2)run db.py file to create table in your sqlite db
3)run the flask app with main.py

4)@app.route("/saveuser",methods=['POST'])

in that method send data for the following field
email,password,fullname,phone,address,city,state,country,pincode

5)@app.route("/login",methods=['POST'])

send data email and password to authenticate user

6)@app.route("/addcontent",methods=['POST'])
 send below data
 
 title--text
 body--text
 summary--text
 docs==send pdf file here
 categorie--text
 userid--text it is foreign key with user(userid)
 
 7)@app.route("/getcontent/<int:id>",methods=["GET"])
 
 send content cid here in the url 
 
 in that title,body,summary,categories,userid will get data in postman 
 and
 docs pdf will save in D drive with title.pdf(above title field name) name
 
 8)@app.route("/deletecontent/<int:id>",methods=['DELETE'])
 
 send content cid here in the url
 
 9)@app.route("/updatecontent/<int:id>",methods=['PUT'])
 
 in url send content(cid) for the update
 
 and send below data
 
 title--text
 body--text
 summary--text
 docs==send pdf file here
 categorie--text
 
 10)@app.route("/gettitle/<title>",methods=['GET'])
 @app.route("/getbody/<string>",methods=['GET'])
 @app.route("/getsummary/<string>",methods=['GET'])
 @app.route("/getcategory/<string>",methods=['GET'])
 
 in the above method we have to send string in url and we will get all data 
 
 
 
 
