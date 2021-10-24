from flask import Flask,Response,request

from application_services.UsersResource.user_service import UserResource
from application_services.UsersResource.address_service import AddressResource
import json


app = Flask(__name__)

null=None

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/users',methods=['GET','POST'])
def get_or_post_users():
    # search all users information
    if request.method=='GET':
        res = UserResource.get_user_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    # insert a user to database
    elif request.method == 'POST':
        template=request.form
        res = UserResource.post_user_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/users/<id>',methods=['GET','PUT','DELETE'])
def process_single_user(id):
    if request.method=='GET':
        template={'ID':id}
        res = UserResource.get_user_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        template=request.form
        res = UserResource.put_user_by_id(template,id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'DELETE':
        res = UserResource.delete_user_by_id(id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/addresses',methods=['GET','POST'])
def get_or_post_address():
    # search all addresses information
    if request.method=='GET':
        res = AddressResource.get_address_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    # insert an address to database
    elif request.method == 'POST':
        template=request.form
        res = AddressResource.post_address_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/addresses/<id>',methods=['GET','PUT','DELETE'])
def process_single_address(id):
    if request.method=='GET':
        template={'ID':id}
        res = AddressResource.get_address_by_template(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        template=request.form
        res = AddressResource.put_address_by_id(template, id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'DELETE':
        res = AddressResource.delete_address_by_id(id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/users/<userid>/addresses',methods=['GET'])
def get_user_adress(userid):
    if request.method=='GET':
        template = {'ID': userid}
        res=AddressResource.get_address_by_userid(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/addresses/<addressid>/users',methods=['GET'])
def get_address_users(addressid):
    if request.method=='GET':
        template = {'addressID': addressid}
        res=AddressResource.get_users_by_addressid(template)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0")
