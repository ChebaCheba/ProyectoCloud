#!flask/bin/python
import json
import os
import pandas as pd
import pymysql
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from mock import data

load_dotenv('.env')

host=os.getenv("HOST_PC")
port=int(os.getenv("PORT_PC"))
dbname=os.getenv("DBNAME_PC")
user=os.getenv("USER_PC")
password=os.getenv("PASS_PC")

conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
app = Flask(__name__)

#print(pd.read_sql('show tables;', con=conn))

# END-POINTS

#GET {service_url}/user/{id}
@app.route('/<service>/user/<int:user_id>', methods=['GET'])
def get_user(service, user_id):
    response = {"userId":user_id}
    users = data["users"]
    for user in users:
        if user["userId"]==user_id:
            response["name"] = user["name"]
            response["email"] = user["email"]
            break
    return response

#GET {service_url}/user/{id}/classes
@app.route('/<service>/user/<int:user_id>/classes', methods=['GET'])
def get_user_classes(service, user_id):
    classes_id = None
    response = {"userId":user_id, "classes": []}
    users = data["users"]
    classes = data["classes"]
    for user in users:
        if user["userId"]==user_id:
            classes_id = user["classes"]
            break
    for class_id in classes_id:
        for c in classes:
            if c["classId"]==class_id and service==c["service"]:
                response["classes"].append({"classId":class_id, "name":c["name"]})
                break
    return response

#GET {service_url}/user/{id}/classes/{class_id}/assignments
@app.route('/<service>/user/<int:user_id>/classes/<int:class_id>/assignments', methods=['GET'])
def get_user_class_assignments(service, user_id, class_id):
    response = {"classId":class_id, "assignments":[]}
    assignments = data["assignments"]
    for assign in assignments:
        if assign["class"]==class_id:
            response["assignments"].append({"assigmentId": assign["assignmentId"]})
            break
    return response

#GET {service_url}/user/{id}/classes/{class_id}/assignments/{assignment_id}
@app.route('/<service>/user/<int:user_id>/classes/<int:class_id>/assignments/<int:assignment_id>', methods=['GET'])
def get_user_class_assignment(service, user_id, class_id, assignment_id):
    response = {"assignmentId": assignment_id}
    assignments = data["assignments"]
    for assign in assignments:
        if assign["assignmentId"]==assignment_id:
            response["title"] = assign["title"]
            response["dueDate"] = assign["dueDate"]
            response["type"] = assign["type"]
            response["URL"] = assign["URL"]
            break
    return response
#GET {service_url}/user/{id}/classes/{class_id}/messages
@app.route('/<service>/user/<int:user_id>/classes/<int:class_id>/messages', methods=['GET'])
def get_user_class_messages(service, user_id, class_id):
    response = {"classId":class_id, "messages":[]}
    messages = data["messages"]
    for message in messages:
        if message["class"]==class_id:
            response["messages"].append({"messageId": message["messageId"]})
            break
    return response
#GET {service_url}/user/{id}/classes/{class_id}/messages/{message_id}
@app.route('/<service>/user/<int:user_id>/classes/<int:class_id>/messages/<int:message_id>', methods=['GET'])
def get_user_class_message(service, user_id, class_id, message_id):
    response = {"messageId": message_id}
    messages = data["messages"]
    for message in messages:
        if message["messageId"]==message_id:
            response["title"] = message["title"]
            response["content"] = message["content"]
            break
    return response

#GET user/{id}
@app.route('/user/<int:user_id>', methods=['GET'])
def db_get_user(user_id):
    query = 'select * from User where userId='+str(user_id)+';'
    user = pd.read_sql(query, con=conn).to_json(orient='records')
    return user
#GET user/{id}/services
@app.route('/user/<int:user_id>/services', methods=['GET'])
def db_get_user_services(user_id):
    query = 'SELECT S.name FROM Tokens T JOIN Services S ON S.serviceId=T.serviceId WHERE T.userId = '+str(user_id)+';'
    services = pd.read_sql(query, con=conn).to_json(orient='records')
    return services

#GET user/{id}/classes
@app.route('/user/<int:user_id>/classes', methods=['GET'])
def db_get_user_classes(user_id):
    query = 'SELECT C.name FROM User_Class UC JOIN Class C ON C.classId=UC.classId WHERE UC.userId = '+str(user_id)+';'
    classes = pd.read_sql(query, con=conn).to_json(orient='records')
    return classes
#GET user/{id}/classes/{class_id}/assignments
@app.route('/user/<int:user_id>/classes/<int:class_id>/assignments', methods=['GET'])
def db_get_user_class_assignments(user_id, class_id):
    query = 'SELECT A.assignmentId FROM Assignment A WHERE A.classId='+str(class_id)+';'
    assignments = pd.read_sql(query, con=conn).to_json(orient='records')
    return assignments
#GET user/{id}/classes/{class_id}/assignments/{assignment_id}
@app.route('/user/<int:user_id>/classes/<int:class_id>/assignments/<int:assignment_id>', methods=['GET'])
def db_get_user_class_assignment(user_id, class_id,assignment_id):
    query = 'SELECT A.assignmentId, A.title, A.dueDate, A.URL FROM Assignment A WHERE A.assignmentId='+str(assignment_id)+';'
    assignment = pd.read_sql(query, con=conn).to_json(orient='records')
    return assignment
#GET user/{id}/classes/{class_id}/messages
@app.route('/user/<int:user_id>/classes/<int:class_id>/messages', methods=['GET'])
def db_get_user_class_messages(user_id, class_id):
    query = 'SELECT M.messageId FROM Message M WHERE M.classId='+str(class_id)+';'
    messages = pd.read_sql(query, con=conn).to_json(orient='records')
    return messages
#GET user/{id}/classes/{class_id}/messages/{message_id}
@app.route('/user/<int:user_id>/classes/<int:class_id>/messages/<int:message_id>', methods=['GET'])
def db_get_user_class_message(user_id, class_id,message_id):
    query = 'SELECT M.messageId, M.title, M.content FROM Message M WHERE M.messageId='+str(message_id)+';'
    message = pd.read_sql(query, con=conn).to_json(orient='records')
    return message

if __name__ == '__main__':
    app.run(debug=True) 
"""

GET user/{id}
GET user/{id}/services
GET user/{id}/classes
GET user/{id}/classes/{class_id}/assignments
GET user/{id}/classes/{class_id}/assignments/{assignment_id}
GET user/{id}/classes/{class_id}/messages
GET user/{id}/classes/{class_id}/messages/{message_id}

POST user
POST user/{id}/services
POST user/{id}/classes
POST user/{id}/classes/{class_id}/assignments
POST user/{id}/classes/{class_id}/messages

"""

