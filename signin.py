#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader

print("Content-type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields

#userid= form_data["uid"].value
#firstname = form_data["fname"].value
#lastname = form_data["lname"].value
#mobile_number = form_data["contact"].value
email= form_data["email1"].value
password = form_data["password"].value
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

def hash_password(password,salt):
  pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt.encode('ascii'), 100000)
  pwdhash = binascii.hexlify(pwdhash)
  print("hashed pswd",pwdhash)
  return pwdhash.decode('ascii')


def authentication(pswd,new_password):
  pswd=pswd[64:]
  print("Stored password",pswd)
  print("Hashed Password",new_password)
  if(new_password==pswd):
    print("Content-type:text/html\n\n")
    redirectURL = "http://pyb82-gp2.specind.net/home2.html"
    print("<html>")
    print("<head>")
    print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
    print("</head>")
    print ("</html>")
  else:
    print("Content-type:text/html\n\n")
    redirectURL = "http://pyb82-gp2.specind.net/signinerror.html"
    print("<html>")
    print("<head>")
    print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
    print("</head>")
    print ("</html>")


conn = pymysql.connect(
    db='pyb82_gp2',
    user='pyb82-gp2',
    passwd='Av0I8hEC',
    host='localhost')
c = conn.cursor()

#userid= form_data["uid"].value
#name = form_data["fname"].value
#username = form_data["uname"].value
#mobile_number = form_data["mnumber"].value
#email= form_data["email"].value
#password= new_password
#userstatus= form_data["user_status"].value
#user_createddate= form_data["user_created_date"].value
#user_updateddate= form_data["user_updated_date"].value
#salt1 = salt

try:
   # Execute the SQL command
   #c.execute(sql)
   sql = 'select pswd,salt from signup where email = "%s" ' %(email)
   print(sql)
   c.execute(sql)
   data=c.fetchone()
   pswd,salt=data[0],data[1]
   #c.execute('insert into user values("%s", "%s","%s", "%s","%s", "%s")' % \
           #  (id, name,address,mobile,pwd,salt1))
   # Commit your changes in the database
   print("password: ",pswd,"salt: ",salt)
   
   conn.commit()
   new_password = hash_password(password,salt)
   authentication(pswd,new_password)


except MySQLError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0])) 



env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('output1.html')
output_from_parsed_template = template.render(email=email)

try:
   fh = open("output.html", "w")
   fh.write(output_from_parsed_template)
except IOError:
   print ("<br>Error: can't find file or read data")
else:
   print ("Written content in the file successfully")


