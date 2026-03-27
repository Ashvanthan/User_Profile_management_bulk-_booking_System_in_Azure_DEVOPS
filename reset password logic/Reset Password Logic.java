import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.Map;

public class ResetPasswordLogic {

    // Inner class for user data
    static class User {
        String email;
        String hashedPassword;

        User(String email, String hashedPassword) {
            this.email = email;
            this.hashedPassword = hashedPassword;
        }
    }

    // User storage
    static Map<String, User> users = new HashMap<>();

    // Sample users
    static {
        users.put("ajay@gmail.com", new User("ajay@gmail.com", hashPassword("oldpass123")));
        users.put("bala@gmail.com", new User("bala@gmail.com", hashPassword("java123")));
    }

    // Method to hash password securely
    public static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();

            for (byte b : hashBytes) {
                sb.append(String.format("%02x", b));
            }

            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            return null;
        }
    }

    // Reset password method
    public static String resetPassword(String email, String otp, String newPassword) {

        // Check missing input
        if (email == null || email.trim().isEmpty()) {
            return "Error: Email is required.";
        }

        if (otp == null || otp.trim().isEmpty()) {
            return "Error: OTP is required.";
        }

        if (newPassword == null || newPassword.trim().isEmpty()) {
            return "Error: New password is required.";
        }

        // Check user exists
        if (!users.containsKey(email)) {
            return "Error: User not found.";
        }

        /*
         * Validate OTP using the previous class
         * Previous class name used here: OTPErrorHandling
         * Method used: verifyOTP(String user, String enteredOTP)
         */
        String otpResult = OTPErrorHandling.verifyOTP(email, otp);

        // If OTP verification fails, return that error
        if (!otpResult.equals("OTP verified successfully.")) {
            return otpResult;
        }

        // Hash and update new password securely
        User user = users.get(email);
        user.hashedPassword = hashPassword(newPassword);

        return "Password reset successful.";
    }

    // Login method to test updated password
    public static String login(String email, String password) {
        if (!users.containsKey(email)) {
            return "Error: User not found.";
        }

        String hashedInput = hashPassword(password);

        if (!users.get(email).hashedPassword.equals(hashedInput)) {
            return "Error: Invalid password.";
        }

        return "Login successful.";
    }

    public static void main(String[] args) {

        /*
         * This line assumes your previous OTP class already stored OTP for this user.
         * Example from previous class:
         * OTPErrorHandling.storeOTP("ajay@gmail.com", "123456", 2);
         */

        System.out.println(resetPassword("ajay@gmail.com", "123456", "newpass789"));
        System.out.println(login("ajay@gmail.com", "oldpass123"));
        System.out.println(login("ajay@gmail.com", "newpass789"));
    }
}