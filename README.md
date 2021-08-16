# Content-Management-System-using-flask-with-sqlite

 In the Content-Management-System user can create itself and then login. User will doing CRUD operation for our data. And also performing search operation according to its requirement
 
 ● The system will have 1 user role, i.e author.
 
 ● Author should be able to register and login using name &amp; password to the CMS
 
 ● Author can create, view, edit and delete contents created by him.
 
 ● Users should search content by matching terms in title, body, summary and categories.

## Installation

This project need following Tools/Technology/framework
1) Python
2) SQLite
3) Postman
4) virtualenv
5) Flask

## Create a project folder

mkdir myproject
cd myproject

## Create a virtual environment

    python -m venv flask_env

## Activate the environment

    venv\Scripts\activate

## Add requirements.txt file

    pip install -r requirements.txt

## Database Connectivity to sqlite

Setup with sqlite Database

  Tables Created
    1)user
    2)content
    
       1)user schema
           CREATE TABLE IF NOT EXISTS user (
           userid INTEGER PRIMARY KEY AUTOINCREMENT, 
           email TEXT NOT NULL, 
           password TEXT NOT NULL, 
           fullname TEXT NOT NULL, 
           phone TEXT NOT NULL, 
           address TEXT, 
           city TEXT, 
           state TEXT, 
           country TEXT, 
           pincode TEXT NOT NULL
           )
       2)content schema
           CREATE TABLE IF NOT EXISTS content(
           cid INTEGER PRIMARY KEY AUTOINCREMENT, 
           title TEXT NOT NULL, 
           body TEXT NOT NULL, 
           summary TEXT NOT NULL, 
           docs BLOB NOT NULL, 
           categories TEXT NOT NULL, 
           userid INTEGER,
           CONSTRAINT fk_user FOREIGN KEY (userid) REFERENCES user(userid)
           )
## Run below file

For database and table creation 
--python db.py 

For project run
--python main.py


# API's

Register User-- http://localhost:5000/user

Login User-- http://localhost:5000/login

Logout User-- http://localhost:5000/logout

Add Content --  http://localhost:5000/content

Get Content -- http://localhost:5000/content/     (pass id here after /)

Delete Content -- http://localhost:5000/content/     (pass id here after /)

Update Content -- http://localhost:5000/content/     (pass id here after /)

Search Content -- http://localhost:5000/search









