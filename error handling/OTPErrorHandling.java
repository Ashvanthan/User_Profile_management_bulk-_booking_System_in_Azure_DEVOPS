import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

public class OTPErrorHandling {

    // Inner class to store OTP data
    static class OTPData {
        String otp;
        LocalDateTime expiryTime;

        OTPData(String otp, LocalDateTime expiryTime) {
            this.otp = otp;
            this.expiryTime = expiryTime;
        }
    }

    // OTP storage
    static Map<String, OTPData> otpStore = new HashMap<>();

    // Store OTP
    public static String storeOTP(String user, String otp, int validMinutes) {
        LocalDateTime expiryTime = LocalDateTime.now().plusMinutes(validMinutes);
        otpStore.put(user, new OTPData(otp, expiryTime));
        return "OTP stored successfully.";
    }

    // Verify OTP with error handling
    public static String verifyOTP(String user, String enteredOTP) {

        // Check if OTP exists
        if (!otpStore.containsKey(user)) {
            return "Error: No OTP found for this user.";
        }

        OTPData data = otpStore.get(user);

        // Check expiry
        if (LocalDateTime.now().isAfter(data.expiryTime)) {
            otpStore.remove(user);
            return "Error: OTP has expired.";
        }

        // Check incorrect OTP
        if (!data.otp.equals(enteredOTP)) {
            return "Error: Incorrect OTP.";
        }

        // Success case
        otpStore.remove(user);
        return "OTP verified successfully.";
    }

    public static void main(String[] args) {
        // Store OTP
        System.out.println(storeOTP("ajay@gmail.com", "123456", 1));

        // Incorrect OTP
        System.out.println(verifyOTP("ajay@gmail.com", "111111"));

        // Correct OTP
        System.out.println(verifyOTP("ajay@gmail.com", "123456"));

        // No OTP found after removal
        System.out.println(verifyOTP("ajay@gmail.com", "123456"));
    }
}