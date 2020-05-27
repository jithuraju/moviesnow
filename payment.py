#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
import os, sys
import imp

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
import random

cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader
global gs_value,gs_key,custid
print("Content-type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields


#user_updateddate= form_data["user_updated_date"].value


#print(firstname)

import pymysql
from pymysql.err import MySQLError


conn = pymysql.connect(
    db='pyb82_gp2',
    user='pyb82-gp2',
    passwd='Av0I8hEC',
    host='localhost')
c = conn.cursor()
try:
   # Execute the SQL command
   #c.execute(sql)
   name= form_data["name"].value
   card_no= form_data["cardnumber"].value
   exp_dm= form_data["expdm"].value
   sql = 'select global_settings_key,global_settings_val from globalmaster'
   print(sql)
   c.execute(sql)
   data=c.fetchone()
   gs_key,gs_value=data[0],data[1]
   print(gs_value)
   print(gs_key)
   sql1 = 'select email from signup where first_name ="%s"' %(name)
   print(sql1)
   c.execute(sql1)
   data1=c.fetchone()
   emailid=data1[0]
   print(emailid)
   sql2='select customerprofileid from paymentinfo where email="%s"' %(emailid)
   c.execute(sql2)
   data2=c.fetchone()
   custid=data2[0]
   print(custid)
   conn.commit()
   merchantAuth = apicontractsv1.merchantAuthenticationType()
   merchantAuth.name = gs_value
   merchantAuth.transactionKey = gs_key
   creditCard = apicontractsv1.creditCardType()
   creditCard.cardNumber = card_no
   creditCard.expirationDate =exp_dm
   payment = apicontractsv1.paymentType()
   payment.creditCard = creditCard
   billTo = apicontractsv1.customerAddressType()
   billTo.firstName = name
   profile = apicontractsv1.customerPaymentProfileType()
   profile.payment = payment
   profile.billTo = billTo
   createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
   createCustomerPaymentProfile.merchantAuthentication = merchantAuth
   createCustomerPaymentProfile.paymentProfile = profile
   createCustomerPaymentProfile.customerProfileId = str(custid)
   controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
   controller.execute()
   response = controller.getresponse()
   print(response.customerPaymentProfileId)
   payid=response.customerPaymentProfileId

   
   # Execute the SQL command
   #c.execute(sql)
   sql3 = 'update paymentinfo set paymentprofileid = "%s" where email="%s" ' %(payid,emailid)  
   print(sql3)
   #c.execute('insert into user values("%s", "%s","%s", "%s","%s", "%s")' % \
           #  (id, name,address,mobile,pwd,salt1))
   # Commit your changes in the database
   c.execute(sql3)
   conn.commit()


   #if (response.messages.resultCode=="Ok"):
   # print("Successfully created a customer payment profile with id: %s" % response.customerPaymentProfileId)
   #else:
   # print("Failed to create customer payment profile %s" % response.messages.message[0]['text'].text)
   #print(response)
   #payid=response.customerPaymentProfileId
   

except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 



env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('output.html')
output_from_parsed_template = template.render(firstname=name)

try:
   fh = open("output2.html", "w")
   fh.write(output_from_parsed_template)
except IOError:
   print ("<br>Error: can't find file or read data")
else:
   print ("Written content in the file successfully")

print("Content-type:text/html\n\n")
redirectURL = "http://pyb82-gp2.specind.net/home2.html"
print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print ("</html>")
