from bottle import route, run, template, static_file, get, post, delete, request
import bottle
import os
from sys import argv
import json
import pymysql

bottle.TEMPLATE_PATH.insert(0,os.path.dirname(os.path.abspath(__file__)))

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='', (ENTER PASSWORD)
                             db='users_4s1',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

@get("/admin")
def admin_portal():
	return template("pages/admin.html")



@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


if __name__ == "__main__":
    run(host='localhost', port=7001, debug=True)