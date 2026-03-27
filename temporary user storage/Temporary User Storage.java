import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.Map;

public class TemporaryUserStorage {

    // Inner class to store user details
    static class User {
        String name;
        String email;
        String phone;
        String hashedPassword;
        String status; // UNVERIFIED or ACTIVE

        User(String name, String email, String phone, String hashedPassword, String status) {
            this.name = name;
            this.email = email;
            this.phone = phone;
            this.hashedPassword = hashedPassword;
            this.status = status;
        }
    }

    // Temporary user storage
    static Map<String, User> temporaryUsers = new HashMap<>();

    // Method to hash password
    public static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashedBytes = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hashedBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            return null;
        }
    }

    // Register user in temporary storage
    public static String registerTemporaryUser(String name, String email, String phone, String password) {
        if (temporaryUsers.containsKey(email)) {
            return "Error: User already exists in temporary storage.";
        }

        String hashedPassword = hashPassword(password);
        User user = new User(name, email, phone, hashedPassword, "UNVERIFIED");
        temporaryUsers.put(email, user);

        return "User stored temporarily as UNVERIFIED.";
    }

    // Prevent login for unverified users
    public static String loginUser(String email, String password) {
        if (!temporaryUsers.containsKey(email)) {
            return "Error: User not found.";
        }

        User user = temporaryUsers.get(email);
        String hashedPassword = hashPassword(password);

        if (!user.hashedPassword.equals(hashedPassword)) {
            return "Error: Invalid password.";
        }

        if (user.status.equals("UNVERIFIED")) {
            return "Access denied: Account not activated yet.";
        }

        return "Login successful.";
    }

    // Activate user account
    public static String activateUser(String email) {
        if (!temporaryUsers.containsKey(email)) {
            return "Error: User not found.";
        }

        User user = temporaryUsers.get(email);
        user.status = "ACTIVE";

        return "User account activated successfully.";
    }

    // Display temporary stored users
    public static void displayUsers() {
        for (User user : temporaryUsers.values()) {
            System.out.println("Name: " + user.name);
            System.out.println("Email: " + user.email);
            System.out.println("Phone: " + user.phone);
            System.out.println("Status: " + user.status);
            System.out.println("--------------------------");
        }
    }

    public static void main(String[] args) {
        System.out.println(registerTemporaryUser("Ajay", "ajay@gmail.com", "9876543210", "pass123"));
        System.out.println(loginUser("ajay@gmail.com", "pass123")); // blocked
        System.out.println(activateUser("ajay@gmail.com"));
        System.out.println(loginUser("ajay@gmail.com", "pass123")); // success

        System.out.println();
        displayUsers();
    }
}