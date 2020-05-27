function validateName() {
  var x = document.forms["form1"]["fname"].value;
  if (x =="") {
    alert("Name must be filled out");
    return false;
}
  var chr=/^[A-Z]/;
  if(x.match(chr))
  {
    return true;
  }
  else
  {
    alert("first letter of name must be in caps...")
    return false;
  }
  
}

function ValidateMail() 
{ 
  var f = document.forms["form1"]["email"].value;	
  if (f.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/))
  {
    return (true)
  }
  else:
  {
    alert("You have entered an invalid email address!")
    return (false)
  }
}



function validatePhone(){
  var z = document.forms["form1"]["contact"].value;
  if(z.match(/^[0-9]{10}$/)){
    return true;
  }
  else{
    alert("invalid phoneno:..");
    return false;
  }
}



function validatePass(){
  var y = document.forms["form1"]["pswd"].value;
  if(y.match(/[a-zA-Z0-9@#$*!]{6,}/)){
    if(y.match(/[@#$%&*!]{1,}/)){
      if(y.match(/[A-Z]{1,}/)){
        return true;

      }
      else
      {
        alert("password must include a cap letter....");
        return false;
      }
      return true;
    }
    else
    {
      alert("password must include special character...");
      return false;
    }
    return true;
  }
  else
  {
    alert("Invalid password.A password must have atleast 1 cap letter,a special char and min length of 6....");
    return false;
  }
}

