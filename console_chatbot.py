import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the OpenAI API key
openai.api_key = "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"

# Banking information database
banking_info = {
    "accounts": {
        "savings": {
            "info": """Savings Account Information:
- Interest Rate: 4% per annum
- Minimum Balance: Rs. 1000
- Zero Balance Option Available
- Online Banking Access
- Mobile Banking App
- ATM Card with Contactless Payment
- Cheque Book Facility
- Fund Transfer (NEFT/RTGS/IMPS)
- Bill Payments
- Standing Instructions""",
            "documents": """Documents Required:
1. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport
   - Voter ID
   - Driving License

2. Address Proof:
   - Aadhaar Card
   - Passport
   - Utility Bills
   - Bank Statement with Cheque
   - Rental Agreement

3. Additional Documents:
   - Passport Size Photographs (2)
   - Income Proof (if required)
   - KYC Form (filled and signed)""",
            "eligibility": """Eligibility:
- Indian Resident
- Age: 18+ years
- Valid KYC Documents
- No existing account with us (if zero balance)"""
        },
        "current": {
            "info": """Current Account Information:
- For: Businesses and Professionals
- Minimum Balance: Rs. 10,000
- Unlimited Transactions
- Overdraft Facility
- Business Banking Services
- Multi-location Access
- Bulk Payment Facility
- Payroll Management
- Tax Payment Services
- Customized Cheque Books""",
            "documents": """Documents Required:
1. Business Proof:
   - Registration Certificate
   - GST Certificate
   - Shop Act License
   - Partnership Deed
   - Memorandum of Association

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport
   - Director's ID (for companies)

3. Address Proof:
   - Business Premises Proof
   - Utility Bills
   - Property Documents

4. Additional Documents:
   - Board Resolution (for companies)
   - Authorized Signatory List
   - Business PAN Card
   - Photographs of Signatories""",
            "eligibility": """Eligibility:
- Registered Business Entity
- Valid Business Documents
- Minimum Turnover (varies)
- Business Vintage (if applicable)"""
        },
        "fd": {
            "info": """Fixed Deposit Information:
- Interest Rate: 5.5% to 7% (based on tenure)
- Tenure: 7 days to 10 years
- Minimum Amount: Rs. 10,000
- Auto-renewal Option
- Loan Against FD
- Premature Withdrawal Facility
- Monthly/Quarterly Interest Payout
- Senior Citizen Benefits
- Tax Benefits""",
            "documents": """Documents Required:
1. Existing Account Details
2. KYC Documents:
   - Aadhaar Card
   - PAN Card
   - Address Proof

3. Additional Documents:
   - FD Application Form
   - Nomination Form
   - Cancelled Cheque""",
            "eligibility": """Eligibility:
- Existing Account Holder
- Valid KYC Documents
- Minimum Age: 18 years
- NRIs (with additional documents)"""
        },
        "rd": {
            "info": """Recurring Deposit Information:
- Interest Rate: Up to 6.5%
- Minimum Monthly Deposit: Rs. 500
- Tenure: 6 months to 10 years
- Auto-debit Facility
- Premature Closure Option
- Loan Against RD
- Monthly Interest Calculation
- Senior Citizen Benefits""",
            "documents": """Documents Required:
1. Existing Account Details
2. KYC Documents:
   - Aadhaar Card
   - PAN Card
   - Address Proof

3. Additional Documents:
   - RD Application Form
   - Auto-debit Mandate
   - Nomination Form""",
            "eligibility": """Eligibility:
- Existing Account Holder
- Valid KYC Documents
- Regular Income Source
- Minimum Age: 18 years"""
        },
        "salary": {
            "info": """Salary Account Information:
- Zero Balance Account
- Salary Credit Facility
- Free ATM Transactions
- Online Banking Access
- Mobile Banking App
- Debit Card
- Cheque Book
- Bill Payments
- Insurance Coverage
- Special Offers""",
            "documents": """Documents Required:
1. Company Documents:
   - Company ID Card
   - Salary Slip
   - Appointment Letter
   - Company PAN Card

2. Personal Documents:
   - Aadhaar Card
   - PAN Card
   - Address Proof
   - Passport Size Photos""",
            "eligibility": """Eligibility:
- Salaried Employee
- Company Tie-up Required
- Valid Employment Proof
- Minimum Age: 18 years"""
        }
    },
    "cards": {
        "debit": {
            "info": """Debit Card Information:
- Annual Fee: Zero
- Daily ATM Limit: Rs. 50,000
- Online Shopping Limit: Rs. 1 lakh
- Contactless Payment
- International Usage
- Cashback Offers
- Reward Points
- Insurance Coverage
- Lost Card Protection""",
            "documents": """Documents Required:
1. Account Details
2. KYC Documents:
   - Aadhaar Card
   - PAN Card

3. Additional Documents:
   - Card Application Form
   - Passport Size Photo""",
            "eligibility": """Eligibility:
- Account Holder
- Valid KYC Documents
- Minimum Age: 18 years
- Active Account Status"""
        },
        "credit": {
            "info": """Credit Card Information:
- Credit Limit: Based on income
- Interest-free Period: Up to 50 days
- Reward Points Program
- Travel Insurance
- Lounge Access
- Fuel Surcharge Waiver
- EMI Options
- Balance Transfer
- Add-on Cards""",
            "documents": """Documents Required:
1. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns
   - Form 16

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

3. Address Proof:
   - Utility Bills
   - Rental Agreement
   - Property Documents""",
            "eligibility": """Eligibility:
- Minimum Income: Rs. 25,000/month
- Good Credit Score
- Employment History
- Age: 21-60 years"""
        },
        "prepaid": {
            "info": """Prepaid Card Information:
- Load Limit: Rs. 2 lakhs
- Validity: 3 years
- Online Shopping
- Bill Payments
- Mobile Recharge
- Gift Option
- Reload Facility
- Transaction Alerts
- Lost Card Protection""",
            "documents": """Documents Required:
1. KYC Documents:
   - Aadhaar Card
   - PAN Card
   - Address Proof

2. Additional Documents:
   - Application Form
   - Passport Photo""",
            "eligibility": """Eligibility:
- Age: 18+ years
- Valid KYC Documents
- Indian Resident"""
        },
        "atm": {
            "info": """ATM Card Information:
- Daily Withdrawal Limit: Rs. 50,000
- Balance Inquiry
- Mini Statement
- Fund Transfer
- Mobile Recharge
- Bill Payments
- PIN Change
- Card Blocking""",
            "documents": """Documents Required:
1. Account Details
2. KYC Documents:
   - Aadhaar Card
   - PAN Card""",
            "eligibility": """Eligibility:
- Account Holder
- Valid KYC Documents
- Active Account Status"""
        },
        "virtual": {
            "info": """Virtual Card Information:
- For Online Transactions Only
- Temporary Card Numbers
- Set Spending Limits
- One-time Use Option
- Instant Generation
- 24/7 Availability
- Transaction Alerts
- Secure Shopping""",
            "documents": """Documents Required:
1. Account Details
2. KYC Documents:
   - Aadhaar Card
   - PAN Card""",
            "eligibility": """Eligibility:
- Account Holder
- Valid KYC Documents
- Active Account Status"""
        },
        "international": {
            "info": """International Card Information:
- For Foreign Transactions
- Global Acceptance
- Travel Insurance
- Emergency Assistance
- Currency Conversion
- Lost Card Protection
- Lounge Access
- Reward Points""",
            "documents": """Documents Required:
1. Travel Documents:
   - Passport
   - Visa
   - Travel Tickets

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

3. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns""",
            "eligibility": """Eligibility:
- Account Holder
- Travel History
- Good Credit Score
- Minimum Income: Rs. 50,000/month"""
        }
    },
    "loans": {
        "home": {
            "info": """Home Loan Information:
- Amount: Up to Rs. 5 crores
- Interest Rate: From 8.4%
- Tenure: Up to 30 years
- Pre-approval Available
- Balance Transfer
- Top-up Loan
- Part Prepayment
- Tax Benefits""",
            "documents": """Documents Required:
1. Property Documents:
   - Sale Agreement
   - Title Deed
   - NOC from Society
   - Approved Plan

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

3. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns
   - Form 16

4. Additional Documents:
   - Property Valuation Report
   - Cost Estimate
   - Builder Profile""",
            "eligibility": """Eligibility:
- Age: 21-65 years
- Minimum Income: Rs. 25,000/month
- Good Credit Score
- Property Location"""
        },
        "personal": {
            "info": """Personal Loan Information:
- Amount: Rs. 50,000 to Rs. 20 lakhs
- Interest Rate: From 10.5%
- Tenure: Up to 5 years
- Quick Disbursement
- No Collateral
- Flexible EMI
- Pre-closure Option
- Balance Transfer""",
            "documents": """Documents Required:
1. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

2. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns
   - Form 16

3. Address Proof:
   - Utility Bills
   - Rental Agreement
   - Property Documents""",
            "eligibility": """Eligibility:
- Age: 21-60 years
- Minimum Income: Rs. 15,000/month
- Good Credit Score
- Employment History"""
        },
        "car": {
            "info": """Car Loan Information:
- Amount: Up to 85% of vehicle value
- Interest Rate: From 8.75%
- Tenure: Up to 7 years
- Quick Approval
- Insurance Cover
- Roadside Assistance
- Balance Transfer
- Top-up Option""",
            "documents": """Documents Required:
1. Vehicle Documents:
   - Quotation
   - Registration Certificate
   - Insurance Papers
   - Road Tax Receipt

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Driving License

3. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns""",
            "eligibility": """Eligibility:
- Age: 21-65 years
- Minimum Income: Rs. 20,000/month
- Good Credit Score
- Valid Driving License"""
        },
        "education": {
            "info": """Education Loan Information:
- Amount: Up to Rs. 50 lakhs
- Interest Rate: From 8.5%
- Moratorium Period: Course duration + 6 months
- No Collateral (up to Rs. 7.5 lakhs)
- Tax Benefits
- Top-up Option
- Balance Transfer""",
            "documents": """Documents Required:
1. Academic Documents:
   - Admission Letter
   - Course Details
   - Fee Structure
   - Previous Marksheets

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

3. Income Proof:
   - Parent's/Guardian's Income
   - Bank Statements
   - ITR Returns""",
            "eligibility": """Eligibility:
- Indian National
- Admission in Recognized Institution
- Good Academic Record
- Co-applicant Required"""
        },
        "property": {
            "info": """Property Loan Information:
- Amount: Up to Rs. 10 crores
- Interest Rate: From 9%
- Tenure: Up to 20 years
- Pre-approval Available
- Balance Transfer
- Top-up Loan
- Part Prepayment
- Tax Benefits""",
            "documents": """Documents Required:
1. Property Documents:
   - Sale Agreement
   - Title Deed
   - NOC from Society
   - Approved Plan

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport

3. Income Proof:
   - Salary Slips
   - Bank Statements
   - ITR Returns
   - Form 16""",
            "eligibility": """Eligibility:
- Age: 21-65 years
- Minimum Income: Rs. 30,000/month
- Good Credit Score
- Property Location"""
        },
        "business": {
            "info": """Business Loan Information:
- Amount: Up to Rs. 1 crore
- Interest Rate: From 11%
- Tenure: Up to 5 years
- Quick Disbursement
- No Collateral (up to limit)
- Flexible Usage
- Top-up Option
- Balance Transfer""",
            "documents": """Documents Required:
1. Business Proof:
   - Registration Certificate
   - GST Certificate
   - Shop Act License
   - Partnership Deed

2. Financial Documents:
   - Bank Statements
   - ITR Returns
   - Balance Sheet
   - Profit & Loss Statement

3. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Passport""",
            "eligibility": """Eligibility:
- Business Vintage: 2+ years
- Minimum Turnover
- Good Credit Score
- Business Location"""
        },
        "agricultural": {
            "info": """Agricultural Loan Information:
- Amount: Up to Rs. 50 lakhs
- Interest Rate: From 7%
- Tenure: Up to 15 years
- Subsidy Available
- Crop Insurance
- Kisan Credit Card
- Top-up Option
- Moratorium Period""",
            "documents": """Documents Required:
1. Land Documents:
   - Land Records
   - Title Deed
   - Survey Number
   - Cultivation Proof

2. Identity Proof:
   - Aadhaar Card
   - PAN Card
   - Voter ID

3. Income Proof:
   - Bank Statements
   - Crop Details
   - Previous Loan Details""",
            "eligibility": """Eligibility:
- Farmer with Land
- Cultivation History
- Good Credit History
- Land Location"""
        }
    },
    "faq": {
        "common": """Frequently Asked Questions:

1. What is the minimum balance for a savings account?
   Answer: Rs. 1000 (Zero balance option available)

2. How can I apply for a credit card?
   Answer: Visit any branch or apply online with required documents

3. What is the interest rate for home loans?
   Answer: Starting from 8.4% (varies based on profile)

4. How to open a new account?
   Answer: Visit branch with Aadhaar, PAN, address proof, and photos

5. What are the ATM withdrawal limits?
   Answer: Rs. 50,000 per day

6. How to apply for a loan?
   Answer: Visit branch with required documents and income proof

7. What is the process for FD renewal?
   Answer: Auto-renewal option available or visit branch before maturity

8. How to update KYC?
   Answer: Visit branch with latest documents or use online banking

9. What are the charges for NEFT/RTGS?
   Answer: Free for savings account, nominal charges for current account

10. How to block a lost card?
    Answer: Call 24x7 helpline or use mobile banking app"""
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\nWelcome to Banking Chatbot!")
    print("\nMain Menu:")
    print("1. Types of Accounts")
    print("2. Types of Cards")
    print("3. Loan Services")
    print("4. FAQ")
    print("5. Ask a Query")
    print("0. Exit")
    print("\nPlease select an option (0-5): ")

def print_accounts_menu():
    print("\nTypes of Accounts:")
    print("1. Savings Account")
    print("2. Current Account")
    print("3. Fixed Deposit (FD)")
    print("4. Recurring Deposit (RD)")
    print("5. Salary Account")
    print("0. Back to Main Menu")
    print("\nPlease select an option (0-5): ")

def print_cards_menu():
    print("\nTypes of Cards:")
    print("1. Debit Card")
    print("2. Credit Card")
    print("3. Prepaid Card")
    print("4. ATM Card")
    print("5. Virtual Card")
    print("6. International Card")
    print("0. Back to Main Menu")
    print("\nPlease select an option (0-6): ")

def print_loans_menu():
    print("\nLoan Services:")
    print("1. Home Loan")
    print("2. Personal Loan")
    print("3. Car/Vehicle Loan")
    print("4. Education Loan")
    print("5. Property Loan")
    print("6. Business Loan")
    print("7. Agricultural Loan")
    print("0. Back to Main Menu")
    print("\nPlease select an option (0-7): ")

def get_ai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a helpful banking assistant. 
Provide detailed, accurate information about banking services including:
- Account types and features
- Card services and benefits
- Loan products and eligibility
- Documentation requirements
- Application procedures
- Interest rates and charges
- Security measures
- Customer support options"""},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"""I apologize, but I encountered an error: {str(e)}

To fix this:
1. Make sure you have a valid OpenAI API key
2. Check your internet connection
3. Ensure you have sufficient credits in your OpenAI account

You can still use the regular chatbot features by selecting options 1-4 from the main menu."""

def main():
    while True:
        clear_screen()
        print_menu()
        choice = input().strip()

        if choice == "0":
            print("\nThank you for using our Banking Chatbot! Have a great day!")
            break

        elif choice == "1":
            while True:
                clear_screen()
                print_accounts_menu()
                account_choice = input().strip()

                if account_choice == "0":
                    break
                elif account_choice == "1":
                    print("\n" + banking_info['accounts']['savings']['info'])
                    print("\n" + banking_info['accounts']['savings']['documents'])
                    print("\n" + banking_info['accounts']['savings']['eligibility'])
                elif account_choice == "2":
                    print("\n" + banking_info['accounts']['current']['info'])
                    print("\n" + banking_info['accounts']['current']['documents'])
                    print("\n" + banking_info['accounts']['current']['eligibility'])
                elif account_choice == "3":
                    print("\n" + banking_info['accounts']['fd']['info'])
                    print("\n" + banking_info['accounts']['fd']['documents'])
                    print("\n" + banking_info['accounts']['fd']['eligibility'])
                elif account_choice == "4":
                    print("\n" + banking_info['accounts']['rd']['info'])
                    print("\n" + banking_info['accounts']['rd']['documents'])
                    print("\n" + banking_info['accounts']['rd']['eligibility'])
                elif account_choice == "5":
                    print("\n" + banking_info['accounts']['salary']['info'])
                    print("\n" + banking_info['accounts']['salary']['documents'])
                    print("\n" + banking_info['accounts']['salary']['eligibility'])
                else:
                    print("\nInvalid choice. Please try again.")
                
                input("\nPress Enter to continue...")

        elif choice == "2":
            while True:
                clear_screen()
                print_cards_menu()
                card_choice = input().strip()

                if card_choice == "0":
                    break
                elif card_choice == "1":
                    print("\n" + banking_info['cards']['debit']['info'])
                    print("\n" + banking_info['cards']['debit']['documents'])
                    print("\n" + banking_info['cards']['debit']['eligibility'])
                elif card_choice == "2":
                    print("\n" + banking_info['cards']['credit']['info'])
                    print("\n" + banking_info['cards']['credit']['documents'])
                    print("\n" + banking_info['cards']['credit']['eligibility'])
                elif card_choice == "3":
                    print("\n" + banking_info['cards']['prepaid']['info'])
                    print("\n" + banking_info['cards']['prepaid']['documents'])
                    print("\n" + banking_info['cards']['prepaid']['eligibility'])
                elif card_choice == "4":
                    print("\n" + banking_info['cards']['atm']['info'])
                    print("\n" + banking_info['cards']['atm']['documents'])
                    print("\n" + banking_info['cards']['atm']['eligibility'])
                elif card_choice == "5":
                    print("\n" + banking_info['cards']['virtual']['info'])
                    print("\n" + banking_info['cards']['virtual']['documents'])
                    print("\n" + banking_info['cards']['virtual']['eligibility'])
                elif card_choice == "6":
                    print("\n" + banking_info['cards']['international']['info'])
                    print("\n" + banking_info['cards']['international']['documents'])
                    print("\n" + banking_info['cards']['international']['eligibility'])
                else:
                    print("\nInvalid choice. Please try again.")
                
                input("\nPress Enter to continue...")

        elif choice == "3":
            while True:
                clear_screen()
                print_loans_menu()
                loan_choice = input().strip()

                if loan_choice == "0":
                    break
                elif loan_choice == "1":
                    print("\n" + banking_info['loans']['home']['info'])
                    print("\n" + banking_info['loans']['home']['documents'])
                    print("\n" + banking_info['loans']['home']['eligibility'])
                elif loan_choice == "2":
                    print("\n" + banking_info['loans']['personal']['info'])
                    print("\n" + banking_info['loans']['personal']['documents'])
                    print("\n" + banking_info['loans']['personal']['eligibility'])
                elif loan_choice == "3":
                    print("\n" + banking_info['loans']['car']['info'])
                    print("\n" + banking_info['loans']['car']['documents'])
                    print("\n" + banking_info['loans']['car']['eligibility'])
                elif loan_choice == "4":
                    print("\n" + banking_info['loans']['education']['info'])
                    print("\n" + banking_info['loans']['education']['documents'])
                    print("\n" + banking_info['loans']['education']['eligibility'])
                elif loan_choice == "5":
                    print("\n" + banking_info['loans']['property']['info'])
                    print("\n" + banking_info['loans']['property']['documents'])
                    print("\n" + banking_info['loans']['property']['eligibility'])
                elif loan_choice == "6":
                    print("\n" + banking_info['loans']['business']['info'])
                    print("\n" + banking_info['loans']['business']['documents'])
                    print("\n" + banking_info['loans']['business']['eligibility'])
                elif loan_choice == "7":
                    print("\n" + banking_info['loans']['agricultural']['info'])
                    print("\n" + banking_info['loans']['agricultural']['documents'])
                    print("\n" + banking_info['loans']['agricultural']['eligibility'])
                else:
                    print("\nInvalid choice. Please try again.")
                
                input("\nPress Enter to continue...")

        elif choice == "4":
            clear_screen()
            print(banking_info['faq']['common'])
            input("\nPress Enter to continue...")

        elif choice == "5":
            clear_screen()
            print("\nAsk your banking-related question:")
            user_query = input().strip()
            response = get_ai_response(user_query)
            print("\n" + response)
            input("\nPress Enter to continue...")

        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 