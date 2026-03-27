import java.util.HashMap;
import java.util.Map;

public class LoginErrorHandling {

    // Store username and password
    static Map<String, String> users = new HashMap<>();

    // Add sample users
    static {
        users.put("ajay", "pass123");
        users.put("abinash", "java123");
        users.put("admin", "admin@123");
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

        // Check user existence
        if (!users.containsKey(username)) {
            return "Error: Invalid username.";
        }

        // Check password
        if (!users.get(username).equals(password)) {
            return "Error: Invalid password.";
        }

        return "Login successful.";
    }

    public static void main(String[] args) {
        System.out.println(login("", "pass123"));
        System.out.println(login("ajay", ""));
        System.out.println(login("hari", "pass123"));
        System.out.println(login("ajay", "wrongpass"));
        System.out.println(login("ajay", "pass123"));
    }
}