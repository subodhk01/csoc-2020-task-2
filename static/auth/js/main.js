function loginformsubmit(){
    $('.error').html("...");
    username = document.getElementById("inputUsername").value.trim();
    password = document.getElementById("inputPassword").value;
    if(username==="" || password===""){
        setInterval(
            function(){
                $('.error').html("No fields should be empty");
            }
            ,500);
        console.log('empty fields.')
    }else {
        $('form').submit();
    }
}
function signupformsubmit(){
    $('.error').html("...");
    username = document.getElementById("inputUsername").value.trim();
    firstname = document.getElementById("inputFirstname").value.trim();
    lastname = document.getElementById("inputLastname").value.trim();
    email = document.getElementById("inputEmail").value.trim();
    password1 = document.getElementById("inputPassword1").value;
    password2 = document.getElementById("inputPassword2").value;
    if(username==="" || password1==="" || password2==="" || email==="" || firstname==="" || lastname===""){
        setInterval(
            function(){
                $('.error').html("No fields should be empty");
            }
            ,500);
        console.log('empty fields.')
    }else {
            $('form').submit();
        }
}