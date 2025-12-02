# Configuration File Documentation

This document provides comprehensive information regarding the structure and various types of blocks within the configuration files used in this project.

## Structure Explanation
Configuration files are structured as plain text files, typically consisting of several key sections identifying different functionalities.

## Block Types
The configuration files support the following block types:

1. **REQUEST**: This block defines the HTTP request parameters such as method, headers, and endpoint.
   ```
   REQUEST {
       METHOD: "GET"
       HEADER: {
           "Authorization": "Bearer token"
       }
       URL: "/api/data"
   }
   ```

2. **PARSE**: This block is used to specify how to parse the response data from requests.
   ```
   PARSE {
       RESULT: "data.result"
   }
   ```

3. **KEY CHECK**: This block contains conditions to check the validity of keys within the application.
   ```
   KEY CHECK {
       DATABASE_KEY: "ABC123"
   }
   ```

4. **FUNCTION**: Defines reusable functions or methods that can be called within the configs.
   ```
   FUNCTION {
       addNumbers(a, b) {
           return a + b;
       }
   }
   ```

5. **UTILITY**: This block is intended for utility functionalities that can aid in the operations of other blocks.
   ```
   UTILITY {
       LOG_LEVEL: "DEBUG"
   }
   ```

## Variable Replacement Syntax
Variable replacement utilizes the `$` sign followed by the variable name. For instance:
```
/${VARIABLE_NAME}/
``` 
This allows dynamic values to be injected into requests and functions.

## Complete Examples
### Example Configuration
```plaintext
REQUEST {
    METHOD: "POST"
    HEADER: { "Content-Type": "application/json" }
    URL: "/api/submit"
}

PARSE {
    RESULT: "data.message"
}

KEY CHECK {
    API_KEY: "xyz456"
}

FUNCTION {
    formatResponse(data) {
        return JSON.stringify(data);
    }
}

UTILITY {
    TIMEOUT: "30"
}
```

## Cookie Format Examples
Cookies must be formatted as follows:
```
Set-Cookie: cookieName=cookieValue; Path=/; HttpOnly; Secure
```

## Troubleshooting Guide
- **Issue:** Request fails with status 404.
  **Solution:** Check that the URL and method specified in the REQUEST block are correct.
- **Issue:** Response parsing error.
  **Solution:** Ensure that the PARSE block accurately reflects the response structure.

## Best Practices for Creating Custom Configs
- Always comment blocks for clarity.
- Validate the structure before applying configurations.
- Use ENV variables for sensitive information.
- Keep requests organized by functionality.

Refer to this document whenever you create or modify config files to ensure accuracy and consistency throughout the project.