function login(event) {
    event.preventDefault(); // prevent default form submission

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(email === "" || password === ""){
        document.getElementById("message").innerText = "Please enter email and password";
        return;
    }

    fetch("http://127.0.0.1:8000/login", { // Your FastAPI login endpoint
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            document.getElementById("message").innerText = "Login successful!";
            // Redirect to dashboard page after 1 second
            setTimeout(() => {
                window.location.href = "dashboard.html"; 
            }, 1000);
        } else {
            document.getElementById("message").innerText = data.message;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("message").innerText = "Server error";
    });
}