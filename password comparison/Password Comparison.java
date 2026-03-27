import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.Map;

public class PasswordComparison {

    // Inner class for user data
    static class User {
        String username;
        String hashedPassword;

        User(String username, String hashedPassword) {
            this.username = username;
            this.hashedPassword = hashedPassword;
        }
    }

    // Store users
    static Map<String, User> users = new HashMap<>();

    // Method to hash password using SHA-256
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

    // Add sample users
    static {
        users.put("ajay", new User("ajay", hashPassword("pass123")));
        users.put("abinash", new User("abinash", hashPassword("java123")));
        users.put("admin", new User("admin", hashPassword("admin@123")));
    }

    // Login method
    public static String login(String username, String password) {

        // Check missing input
        if (username == null || username.trim().isEmpty()) {
            return "Error: Username is required.";
        }

        if (password == null || password.trim().isEmpty()) {
            return "Error: Password is required.";
        }

        // Check user exists
        if (!users.containsKey(username)) {
            return "Error: User not found.";
        }

        User user = users.get(username);

        // Hash entered password
        String hashedInputPassword = hashPassword(password);

        // Compare hashed password
        if (!user.hashedPassword.equals(hashedInputPassword)) {
            return "Error: Invalid password.";
        }

        return "Login successful.";
    }

    public static void main(String[] args) {
        System.out.println(login("", "pass123"));
        System.out.println(login("ajay", ""));
        System.out.println(login("hari", "pass123"));
        System.out.println(login("ajay", "wrong123"));
        System.out.println(login("ajay", "pass123"));
    }
}