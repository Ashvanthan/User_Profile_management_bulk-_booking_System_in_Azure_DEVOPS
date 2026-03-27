import java.util.HashSet;
import java.util.Set;

public class UniqueCheck {

    // Store existing emails and phone numbers
    static Set<String> emails = new HashSet<>();
    static Set<String> phones = new HashSet<>();

    // Method to register user
    public static String registerUser(String email, String phone) {

        // Check email uniqueness
        if (emails.contains(email)) {
            return "Error: Email already exists.";
        }

        // Check phone uniqueness
        if (phones.contains(phone)) {
            return "Error: Phone number already exists.";
        }

        // Prevent duplicates by adding only unique values
        emails.add(email);
        phones.add(phone);

        return "User registered successfully.";
    }

    // Main method for testing
    public static void main(String[] args) {

        System.out.println(registerUser("ajay@gmail.com", "9876543210"));
        System.out.println(registerUser("ajay@gmail.com", "9123456780"));
        System.out.println(registerUser("bala@gmail.com", "9876543210"));
        System.out.println(registerUser("hari@gmail.com", "9999999999"));
    }
}