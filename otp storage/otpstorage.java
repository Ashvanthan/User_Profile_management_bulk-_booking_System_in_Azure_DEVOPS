import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

public class OTPStorage {

    // Inner class to store OTP details
    static class OTPDetails {
        String otp;
        LocalDateTime expiryTime;

        OTPDetails(String otp, LocalDateTime expiryTime) {
            this.otp = otp;
            this.expiryTime = expiryTime;
        }
    }

    // Store OTP using user email/phone as key
    static Map<String, OTPDetails> otpStorage = new HashMap<>();

    // Method to store or overwrite OTP
    public static String storeOTP(String user, String otp, int validMinutes) {
        LocalDateTime expiryTime = LocalDateTime.now().plusMinutes(validMinutes);

        if (otpStorage.containsKey(user)) {
            otpStorage.put(user, new OTPDetails(otp, expiryTime));
            return "OTP overwritten successfully for user: " + user;
        } else {
            otpStorage.put(user, new OTPDetails(otp, expiryTime));
            return "OTP stored successfully for user: " + user;
        }
    }

    // Method to verify OTP
    public static String verifyOTP(String user, String enteredOTP) {
        if (!otpStorage.containsKey(user)) {
            return "Error: No OTP found for user.";
        }

        OTPDetails details = otpStorage.get(user);

        // Check expiry
        if (LocalDateTime.now().isAfter(details.expiryTime)) {
            otpStorage.remove(user);
            return "Error: OTP expired.";
        }

        // Check OTP match
        if (!details.otp.equals(enteredOTP)) {
            return "Error: Invalid OTP.";
        }

        // Clear OTP after successful verification
        otpStorage.remove(user);
        return "OTP verified successfully.";
    }

    // Display stored OTP data
    public static void displayStoredOTPs() {
        for (Map.Entry<String, OTPDetails> entry : otpStorage.entrySet()) {
            System.out.println("User: " + entry.getKey());
            System.out.println("OTP: " + entry.getValue().otp);
            System.out.println("Expiry Time: " + entry.getValue().expiryTime);
            System.out.println("----------------------------");
        }
    }

    public static void main(String[] args) {
        System.out.println(storeOTP("ajay@gmail.com", "123456", 2));
        System.out.println(storeOTP("ajay@gmail.com", "654321", 2)); // overwrite
        System.out.println(verifyOTP("ajay@gmail.com", "123456"));   // invalid
        System.out.println(verifyOTP("ajay@gmail.com", "654321"));   // success

        System.out.println();
        displayStoredOTPs();
    }
}