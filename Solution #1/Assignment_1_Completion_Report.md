# Kwan Ju

## Finished Task

### Assignment #1

#### Detail Contents

**Project Overview:**
Successfully implemented a comprehensive bank account management system using Python object-oriented programming principles. The system supports multiple account types with specific business rules and constraints.

**Key Features Implemented:**

1. **BankAccount Class Design:**
   - Created a robust `BankAccount` class with proper encapsulation using private attributes
   - Implemented automatic unique ID generation for each account instance
   - Added random bank account number generation (8-digit format)
   - Integrated timestamp tracking for account creation and transaction history

2. **Account Types Supported:**
   - **D/W Account (Deposit/Withdrawal):** Standard checking account with immediate withdrawal capability
   - **Saving Account:** Time-restricted account requiring 1-year maturity period before withdrawals
   - **Minus Account (Overdraft):** Account allowing negative balance up to -500,000 limit

3. **Core Functionality:**
   - **Deposit Method:** Validates positive amounts and updates account balance
   - **Withdrawal Method:** Implements account-specific withdrawal rules with password verification
   - **Account Information Display:** Comprehensive account details presentation
   - **Balance Management:** Secure balance retrieval and modification

4. **Security Features:**
   - Password-protected withdrawal operations
   - Input validation for deposit and withdrawal amounts
   - Encapsulated account data with private attributes

5. **Business Logic Implementation:**
   - **D/W Account:** Standard balance verification before withdrawal
   - **Saving Account:** 365-day maturity period enforcement with date calculation
   - **Minus Account:** -500,000 overdraft limit validation
   - **Error Handling:** Comprehensive error messages for invalid operations

6. **Technical Implementation:**
   - Used `datetime` module for time-based calculations
   - Implemented `random` module for unique account number generation
   - Applied proper Python class inheritance and encapsulation
   - Included destructor method for account cleanup

**Testing and Validation:**
- Created comprehensive test cases demonstrating all account types
- Verified deposit and withdrawal operations with various scenarios
- Tested account-specific business rules and constraints
- Validated error handling for invalid inputs and operations

**Code Quality:**
- Well-documented code with detailed docstrings
- Consistent naming conventions and code structure
- Proper separation of concerns and modular design
- Clean and maintainable codebase following Python best practices

**Deliverables:**
- Complete `assignment_1.py` file with fully functional bank account system
- Comprehensive test cases demonstrating all features
- Proper documentation and code comments
- Error handling and validation mechanisms

**Learning Outcomes:**
- Mastered Python object-oriented programming concepts
- Implemented real-world business logic in software systems
- Applied proper data encapsulation and security practices
- Developed understanding of banking system requirements and constraints 