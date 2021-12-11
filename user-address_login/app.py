from flask import Flask,Response,request,render_template,redirect,url_for

from application_services.UsersResource.user_service import UserResource
from application_services.UsersResource.address_service import AddressResource
from flask_dance.contrib.google import google,make_google_blueprint
import json
import os


app = Flask(__name__)

null=None

os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']='1'
app.secret_key="some secret"

blueprint = make_google_blueprint(
    client_id='1027342541063-p5o91gkgoot1q6466c3tesm3gtlpce0j.apps.googleusercontent.com',
    client_secret='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',
    reprompt_consent=True,
    scope=["profile","email"]
)

app.register_blueprint(blueprint,url_prefix="/login")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/getid')
def get_id():
    user_info_endpoint = 'oauth2/v2/userinfo'
    if google.authorized:
        google_data=google.get(user_info_endpoint).json()
        return google_data
    else:
        return 'please login in!'

@app.route('/login')
def login():
    google_data=None
    user_info_endpoint='oauth2/v2/userinfo'
    if google.authorized:
        google_data=google.get(user_info_endpoint).json()
        #print(google_data)
        return "You are {email} on Google".format(email=google_data["email"])
    else:
        return redirect(url_for("google.login"))


@app.route('/users',methods=['GET','POST'])
def get_or_post_users():
    # search all users information
    if request.method=='GET':
        qs = request.query_string
        if qs:
            qs_dict={}
            for q in str(qs,'utf-8').split('&'):
                q=q.split('=')
                qs_dict[q[0]]=q[1]
        else:
            qs_dict=None
        if qs_dict and 'limit' in qs_dict.keys():
            res = UserResource.get_user_by_template_limit(qs_dict)
            self_url=request.url
            limit_value = qs_dict['limit']
            next_url = self_url
            pre_url = self_url
            if 'offset' in qs_dict.keys():
                next_url=next_url[:-1]+str(int(next_url[-1])+int(limit_value))
                pre_url=pre_url[:-1]+str(max(int(pre_url[-1])-int(limit_value),0))
            else:
                next_url = next_url + '&offset='+limit_value
                pre_url= pre_url + '&offset=0'
            new_res={}
            new_res['data']=res
            links=[
                {
                    "ref": "self",
                    "href": self_url
                },
                {
                    "ref": "pre",
                    "href": pre_url
                },
                {
                    "ref": "next",
                    "href": next_url
                }
            ]
            new_res['link']=links
            res=new_res
        else:
            res = UserResource.get_user_by_template(qs_dict)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    # insert a user to database
    elif request.method == 'POST':
        template=request.form
        email=template['email']
        if '@' not in email:
            res='Bad Data'
            rsp = Response(json.dumps(res, default=str), status=400, content_type="application/json")
            return rsp
        res = UserResource.post_user_by_template(template)
        if res==1:
            res='created'
            url='users/'+str(template['ID'])
            rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json",headers={'location':url})
        elif res=='integrity error':
            rsp = Response(json.dumps(res, default=str), status=422, content_type="application/json")
        return rsp

@app.route('/users/<id>',methods=['GET','PUT','DELETE'])
def process_single_user(id):
    if request.method=='GET':
        template={'ID':id}
        res = UserResource.get_user_by_template(template)
        if not res:
            res='404 not found'
            rsp = Response(json.dumps(res, default=str), status=404, content_type="application/json")
        else:
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        template=request.form
        res = UserResource.put_user_by_id(template,id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == 'DELETE':
        res = UserResource.delete_user_by_id(id)
        if res==1:
            res='Deleted'
        rsp = Response(json.dumps(res, default=str), status=204, content_type="text")
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
    app.run(host="0.0.0.0", port=5000)
