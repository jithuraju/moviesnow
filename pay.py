#!/usr/bin/python3
import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *

print("Content-type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields
#userid= form_data["uid"].value

#userstatus= form_data["user_status"].value
#user_createddate= form_data["user_created_date"].value
#user_updateddate= form_data["user_updated_date"].value

import pymysql
from pymysql.err import MySQLError
# password1 = form_data["pwd"].value
# salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
# pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
#                                 salt, 100000)
# print('pwd',pwdhash)
# pwdhash = binascii.hexlify(pwdhash)
# pwdhash1= pwdhash





conn = pymysql.connect(
    db='pyb82_gp2',
    user='pyb82-gp2',
    passwd='Av0I8hEC',
    host='localhost')
c = conn.cursor()

#userid= form_data["uid"].value
#userstatus= form_data["user_status"].value
#user_createddate= form_data["user_created_date"].value
#user_updateddate= form_data["user_updated_date"].value
try:
   # Execute the SQL command
   #c.execute(sql)
    # fetch from global_master_table
    customer_id = form_data["cid"].value
    payment_id = form_data["pid"].value

    sqlfetch = 'select global_settings_key,global_settings_val from globalmaster'
    c.execute(sqlfetch)
    data = c.fetchone()
    transactionKey,apiLoginId = data[0],data[1]
    conn.commit()

        # API to initiate payment
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = apiLoginId
    merchantAuth.transactionKey = transactionKey

    # create a customer payment profile
    profileToCharge = apicontractsv1.customerProfilePaymentType()
    profileToCharge.customerProfileId = customer_id
    profileToCharge.paymentProfile = apicontractsv1.paymentProfile()
    profileToCharge.paymentProfile.paymentProfileId = payment_id

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = 2000
    transactionrequest.profile = profileToCharge

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "728180"

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()
    if response is not None:
      if response.messages.resultCode == "Ok":
        if hasattr(response.transactionResponse, 'messages') == True:
                    print ('Successfully created transaction with Transaction ID: %s' % response.transactionResponse.transId)
                    print ('Transaction Response Code: %s' % response.transactionResponse.responseCode)
                    print ('Message Code: %s' % response.transactionResponse.messages.message[0].code)
                    print ('Description: %s' % response.transactionResponse.messages.message[0].description)
        else:
          print ('Failed Transaction.')
          if hasattr(response.transactionResponse, 'errors') == True:
            print ('Error Code:  %s' % str(response.transactionResponse.errors.error[0].errorCode))
            print ('Error message: %s' % response.transactionResponse.errors.error[0].errorText)
          else:
            print ('Failed Transaction.')
            if hasattr(response, 'transactionResponse') == True and hasattr(response.transactionResponse, 'errors') == True:
              print ('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode))
              print ('Error message: %s' % response.transactionResponse.errors.error[0].errorText)
            else:
              print ('Error Code: %s' % response.messages.message[0]['code'].text)
              print ('Error message: %s' % response.messages.message[0]['text'].text)
    else:
      print ('Null Response.')
except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))



# output.html file
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('output.html')
output_from_parsed_template = template.render(data=data)



