const form =
document.getElementById("login-form");


const errorMsg =
document.getElementById("error");



form.addEventListener(
"submit",
async(e)=>{


e.preventDefault();



const email =
document.getElementById("email").value;


const password =
document.getElementById("password").value;



try{


const response =
await fetch(
"http://127.0.0.1:8000/login",
{

method:"POST",

headers:{
"Content-Type":
"application/x-www-form-urlencoded"
},

body:
new URLSearchParams({

username:email,
password:password

})

}

);



if(!response.ok){

throw new Error(
"Credenciales incorrectas"
);

}



const data =
await response.json();



localStorage.setItem(
"token",
data.access_token
);



redirectByRole();



}
catch(error){


errorMsg.textContent =
error.message;


}



});