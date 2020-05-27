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
global gs_value,gs_key
print("Content-type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields

#userid= form_data["uid"].value
firstname = form_data["fname"].value
lastname = form_data["lname"].value
mobile_number = form_data["contact"].value
email= form_data["email"].value
password = form_data["pswd"].value
#userstatus= form_data["user_status"].value
#user_createddate= form_data["user_created_date"].value
#user_updateddate= form_data["user_updated_date"].value


print(firstname)

import pymysql
from pymysql.err import MySQLError
# password1 = form_data["pwd"].value
# salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
# pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
#                                 salt, 100000)
# print('pwd',pwdhash)
# pwdhash = binascii.hexlify(pwdhash)
# pwdhash1= pwdhash

def hash_password(password):
  salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
  pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
  pwdhash = binascii.hexlify(pwdhash)
  return (salt + pwdhash).decode('ascii')
new_password = hash_password(password)
salt = new_password[:64]



conn = pymysql.connect(
    db='pyb82_gp2',
    user='pyb82-gp2',
    passwd='Av0I8hEC',
    host='localhost')
c = conn.cursor()

password= new_password

salt1 = salt

try:
   # Execute the SQL command
   #c.execute(sql)
   sql = 'insert into signup(first_name,last_name,email,contact,pswd,salt) values ("%s", "%s", "%s", "%s","%s","%s")' %(firstname,lastname,email,mobile_number,password,salt1)
   print(sql)
   #c.execute('insert into user values("%s", "%s","%s", "%s","%s", "%s")' % \
           #  (id, name,address,mobile,pwd,salt1))
   # Commit your changes in the database
   c.execute(sql)
   conn.commit()

except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 

try:
    sql = 'select global_settings_val,global_settings_key from globalmaster ' 
    print(sql)
    c.execute(sql)
    data1=c.fetchone()
    gs_value,gs_key=data1[0],data1[1]
    print(gs_value)
    print(gs_key)
    c.execute(sql)
    conn.commit()

    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = gs_value
    merchantAuth.transactionKey = gs_key
    createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
    createCustomerProfile.merchantAuthentication = merchantAuth
    createCustomerProfile.profile = apicontractsv1.customerProfileType(firstname, lastname, email)
    controller = createCustomerProfileController(createCustomerProfile)
    controller.execute()
    response = controller.getresponse()  
    print(response.customerProfileId)
    custid=response.customerProfileId
except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 

try:
   # Execute the SQL command
   #c.execute(sql)
   sql = 'insert into paymentinfo(email,customerprofileid) values ("%s", "%s")' %(email,custid)
   print(sql)
   #c.execute('insert into user values("%s", "%s","%s", "%s","%s", "%s")' % \
           #  (id, name,address,mobile,pwd,salt1))
   # Commit your changes in the database
   c.execute(sql)
   conn.commit()

except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 



env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('output.html')
output_from_parsed_template = template.render(firstname=firstname)

try:
   fh = open("output.html", "w")
   fh.write(output_from_parsed_template)
except IOError:
   print ("<br>Error: can't find file or read data")
else:
   print ("Written content in the file successfully")

print("Content-type:text/html\n\n")
redirectURL = "http://pyb82-gp2.specind.net/signin.html"
print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print ("</html>")
