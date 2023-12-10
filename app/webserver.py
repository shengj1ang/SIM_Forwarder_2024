# This webserver.py is for test only
from functions.database import db
from flask import Flask, request, render_template, send_from_directory, redirect

db=db(db_path="database/mydatabase.db", phonenum="008615961485300", timezone=0)
