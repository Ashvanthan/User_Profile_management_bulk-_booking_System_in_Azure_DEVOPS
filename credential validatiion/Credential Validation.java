import java.util.HashMap;
import java.util.Map;

public class CredentialValidation {

    // Inner class for User
    static class User {
        String email;
        String password;
        String status; // ACTIVE, BLOCKED, UNVERIFIED

        User(String email, String password, String status) {
            this.email = email;
            this.password = password;
            this.status = status;
        }
    }

    // Store users
    static Map<String, User> users = new HashMap<>();

    // Add sample users
    static {
        users.put("ajay@gmail.com", new User("ajay@gmail.com", "pass123", "ACTIVE"));
        users.put("bala@gmail.com", new User("bala@gmail.com", "java123", "BLOCKED"));
        users.put("hari@gmail.com", new User("hari@gmail.com", "test123", "UNVERIFIED"));
    }

    // Validate credentials
    public static String validateLogin(String email, String password) {

        // Check missing input
        if (email == null || email.trim().isEmpty()) {
            return "Error: Email is required.";
        }

        if (password == null || password.trim().isEmpty()) {
            return "Error: Password is required.";
        }

        // Check user exists
        if (!users.containsKey(email)) {
            return "Error: User not found.";
        }

        User user = users.get(email);

        // Check account status
        if (!user.status.equals("ACTIVE")) {
            return "Error: Account is " + user.status + ".";
        }

        // Validate password
        if (!user.password.equals(password)) {
            return "Error: Invalid password.";
        }

        return "Login successful.";
    }

    public static void main(String[] args) {

        System.out.println(validateLogin("", "pass123"));
        System.out.println(validateLogin("unknown@gmail.com", "pass123"));
        System.out.println(validateLogin("bala@gmail.com", "java123"));
        System.out.println(validateLogin("ajay@gmail.com", "wrong"));
        System.out.println(validateLogin("ajay@gmail.com", "pass123"));
    }
}