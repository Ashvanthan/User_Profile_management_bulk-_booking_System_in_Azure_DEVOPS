import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class InputValidation {

    // Regex pattern for email validation
    private static final Pattern EMAIL_PATTERN =
            Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");

    // Regex pattern for phone validation (10 digits)
    private static final Pattern PHONE_PATTERN =
            Pattern.compile("^[0-9]{10}$");

    // Method to validate all inputs
    public static List<String> validateInput(String name, String email, String phone) {
        List<String> errors = new ArrayList<>();

        // Check required fields
        if (name == null || name.trim().isEmpty()) {
            errors.add("Name is required.");
        }

        if (email == null || email.trim().isEmpty()) {
            errors.add("Email is required.");
        }

        if (phone == null || phone.trim().isEmpty()) {
            errors.add("Phone number is required.");
        }

        // Check email format
        if (email != null && !email.trim().isEmpty()) {
            if (!EMAIL_PATTERN.matcher(email).matches()) {
                errors.add("Invalid email format.");
            }
        }

        // Check phone format
        if (phone != null && !phone.trim().isEmpty()) {
            if (!PHONE_PATTERN.matcher(phone).matches()) {
                errors.add("Invalid phone number. It must contain exactly 10 digits.");
            }
        }

        return errors;
    }

    // Main method for testing
    public static void main(String[] args) {
        String name = "";
        String email = "abcgmail.com";
        String phone = "12345";

        List<String> validationErrors = validateInput(name, email, phone);

        if (validationErrors.isEmpty()) {
            System.out.println("Validation successful.");
        } else {
            System.out.println("Validation failed with following errors:");
            for (String error : validationErrors) {
                System.out.println(error);
            }
        }
    }
}