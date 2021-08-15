# Content-Management-System-using-flask-with-sqlite

 In the Content-Management-System user can create itself and then login. User will doing CRUD operation for our data. And also performing search operation according to its requirement

## Installation

This project need following Tools/Application/Ide
1) Python--pycharam,spyder,etc
2) SQLite--SQLitestudio
3) Postman (for testing)
4) virtualenv

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

import sqlite3

conn=sqlite3.connect("sqlassignment.db")

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









