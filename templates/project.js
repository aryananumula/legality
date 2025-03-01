document.getElementById("validatebutton").addEventListener("click", validation);
function validation()
{
  validateUserName(document.getElementById("name"));
  validatePhone(document.getElementById("phone")) ;
  validateEmail(document.getElementById("email"));
  validateMessage(document.getElementById("message"))
}
function validateUserName(myInput)
{
  if((myInput.value.length)==0)
 alert("please enter a name");
  else if ((myInput.value.length)<3&&(myInput.value.length)>0)
  alert("please enter a name more than 3 letters");

}
function validatePhone(myInput)
{
    if((myInput.value.length)==0)
 alert("please enter phone number");
  else if ((myInput.value.length)<11&&(myInput.value.length)>0)
  alert("please enter a phone number more than 10 digits ");

}

function validateEmail(myInput )
{
    var regex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
 if (myInput.value.match(regex)){ 
 }
 
 else
alert("Enter a valid email ");
}

function validateMessage(myInput)
{
    if((myInput.value.length)==0)
 alert("please enter a message");
  else if ((myInput.value.length)<60&&(myInput.value.length)>0)
  alert("please enter a message more than 60 letters ");

}
