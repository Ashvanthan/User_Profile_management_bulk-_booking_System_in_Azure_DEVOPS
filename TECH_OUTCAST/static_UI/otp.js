function submitOTP() {

    // Get OTP digits from input fields
    const otp = 
        document.getElementById("otp1").value +
        document.getElementById("otp2").value +
        document.getElementById("otp3").value +
        document.getElementById("otp4").value +
        document.getElementById("otp5").value +
        document.getElementById("otp6").value;

    if(otp.length < 6){
        document.getElementById("error").innerText = "Please enter all 6 digits";
        return;
    }

    // Send OTP to backend
    fetch("http://127.0.0.1:8000/verify-otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ otp: otp, email: "test@gmail.com" }) // include email or session ID
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            document.getElementById("error").style.color = "green";
            document.getElementById("error").innerText = data.message;
            // Redirect after success
            setTimeout(() => {
                window.location.href = "resetpassword.html"; 
            }, 1000);
        } else {
            document.getElementById("error").style.color = "red";
            document.getElementById("error").innerText = data.message;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("error").innerText = "Server error";
    });
}