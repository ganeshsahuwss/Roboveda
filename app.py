from __future__ import print_function
import json
from flask import Flask,render_template,jsonify,Response,request
from flask_mongoengine import MongoEngine
import razorpay

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

app=Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'db': 'roboveda','host': 'localhost','port': 27017}

db=MongoEngine()
db.init_app(app)

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

#

#register table
class register(db.Document):
    id = db.StringField(primary_key=True)
    name=db.StringField(max_length=50)
    mobile=db.StringField(max_length=10)
    emailid=db.StringField(max_length=50)
    ticket=db.StringField(max_length=100)

    def to_json(self):
        return {"id":self.id,
                "name":self.name,
                "mobile":self.mobile,
                "emailid":self.emailid,
                "ticket":self.ticket
                }





#register APi

#get data
@app.route('/show',methods=["GET"])
def get():
    user = register.objects().to_json()
    return Response(user,mimetype="application/json")

#post
@app.route('/addrecord', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    user = register(id=record["id"],
                 name=record["name"],
                 mobile=record["mobile"],
                 emailid=record["emailid"],
                 ticket=record["ticket"])

    user.save()
    response = {
                'status': 'success',
                'message': 'record add successfully',
                'data':[]
            }
    
    return jsonify(user.to_json(),response)

#update
@app.route("/edit/<id>",methods=["PUT"])
def editview(id):
   
    record=json.loads(request.data)
    register.objects.get(id=id).update(**record)

    
    return jsonify({'status': 'success','message': ' edit successfully',})

#delete
@app.route("/delete/<id>",methods=["DELETE"])
def deleteview(id):
    register.objects.get(id=id).delete()
    
    return jsonify({'status': 'success','message': 'delete successfully'}) 


# create an instance of the API class
api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
create_contact = sib_api_v3_sdk.CreateContact(email="ganesh@gmail.com") # CreateContact | Values to create a contact

try:
    # Create a contact
    api_response = api_instance.create_contact(create_contact)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->create_contact: %s\n" % e)




@app.route("/index")
def index():
    return render_template('index.html')




if __name__=="__main__":
    app.run(debug=True)