function forgotPassword() {

    const email = document.getElementById("email").value;

    if(email === ""){
        document.getElementById("message").innerText = "Please enter your email";
        return;
    }

    fetch("http://127.0.0.1:8000/forgot-password", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email
        })

    })
    .then(response => response.json())
    .then(data => {

        document.getElementById("message").innerText = data.message;

    })
    .catch(error => {

        document.getElementById("message").innerText = "Server error";

    });

}