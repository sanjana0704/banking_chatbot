import openai
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class BankChatbot:
    def __init__(self):
        # Initialize OpenAI API key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Initialize banking data
        self.banking_data = {
            "accounts": {
                "1.1": {
                    "name": "Savings Account",
                    "definition": "A basic bank account for individuals to save money and earn interest",
                    "eligibility": "Individuals above 18 years, valid KYC documents",
                    "documents": [
                        "1.1.1 Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "1.1.2 Address Proof (Utility Bills, Bank Statement)",
                        "1.1.3 Passport Size Photos (2)",
                        "1.1.4 KYC Form"
                    ],
                    "benefits": [
                        "Interest Rate: 4% per annum",
                        "Minimum Balance: Rs. 1000",
                        "Zero Balance Option Available",
                        "Online Banking Access",
                        "Mobile Banking App",
                        "ATM Card with Contactless Payment",
                        "Cheque Book Facility",
                        "Fund Transfer (NEFT/RTGS/IMPS)",
                        "Bill Payments",
                        "Standing Instructions"
                    ],
                    "rules": [
                        "Minimum balance maintenance required",
                        "Limited free ATM transactions",
                        "Interest calculated on daily balance"
                    ]
                },
                "1.2": {
                    "name": "Current Account",
                    "definition": "A bank account for businesses and professionals with high transaction volume",
                    "eligibility": "Businesses, professionals, companies, partnerships",
                    "documents": [
                        "1.2.1 Business Proof (Registration Certificate, GST Certificate)",
                        "1.2.2 Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "1.2.3 Address Proof (Business Premises Proof)",
                        "1.2.4 Board Resolution (for companies)",
                        "1.2.5 Authorized Signatory List",
                        "1.2.6 Business PAN Card",
                        "1.2.7 Photographs of Signatories"
                    ],
                    "benefits": [
                        "Unlimited Transactions",
                        "Overdraft Facility",
                        "Business Banking Services",
                        "Multi-location Access",
                        "Bulk Payment Facility",
                        "Payroll Management",
                        "Tax Payment Services",
                        "Customized Cheque Books"
                    ],
                    "rules": [
                        "Minimum Balance: Rs. 10,000",
                        "No interest on balance",
                        "Transaction charges apply"
                    ]
                }
            },
            "loans": {
                "2.1": {
                    "name": "Home Loan",
                    "definition": "Loan for purchasing or constructing a residential property",
                    "eligibility": "Age: 21-65 years, Stable income, Good credit score",
                    "documents": [
                        "2.1.1 Property Documents (Sale Agreement, Title Deed)",
                        "2.1.2 Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "2.1.3 Income Proof (Salary Slips, Bank Statements)",
                        "2.1.4 Property Valuation Report",
                        "2.1.5 Cost Estimate",
                        "2.1.6 Builder Profile"
                    ],
                    "benefits": [
                        "Amount: Up to Rs. 5 crores",
                        "Interest Rate: From 8.4%",
                        "Tenure: Up to 30 years",
                        "Pre-approval Available",
                        "Balance Transfer",
                        "Top-up Loan",
                        "Part Prepayment",
                        "Tax Benefits"
                    ],
                    "rules": [
                        "EMI based on income",
                        "Property insurance required",
                        "Pre-closure charges apply"
                    ]
                }
            },
            "cards": {
                "3.1": {
                    "name": "Debit Card",
                    "definition": "Card linked to bank account for cashless transactions",
                    "eligibility": "Account holder with valid KYC",
                    "documents": [
                        "3.1.1 Account Details",
                        "3.1.2 KYC Documents (Aadhaar Card, PAN Card)",
                        "3.1.3 Card Application Form",
                        "3.1.4 Passport Size Photo"
                    ],
                    "benefits": [
                        "Annual Fee: Zero",
                        "Daily ATM Limit: Rs. 50,000",
                        "Online Shopping Limit: Rs. 1 lakh",
                        "Contactless Payment",
                        "International Usage",
                        "Cashback Offers",
                        "Reward Points",
                        "Insurance Coverage",
                        "Lost Card Protection"
                    ],
                    "rules": [
                        "PIN required for transactions",
                        "Daily withdrawal limits apply",
                        "International usage charges"
                    ]
                }
            }
        }

    def get_ai_response(self, query):
        """Get AI-powered response for banking queries"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful banking assistant. Provide accurate and concise information about banking services."},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I couldn't process your query at the moment. Please try again later. Error: {str(e)}"

    def display_menu(self):
        """Display the main menu"""
        print("\n🏦 Welcome to Banking Services Chatbot!")
        print("\nPlease select a category:")
        print("1️⃣ Bank Accounts")
        print("2️⃣ Loan Services")
        print("3️⃣ Card Types")
        print("4️⃣ AI Q&A Session")
        print("5️⃣ Exit")

    def display_accounts_menu(self):
        """Display accounts submenu"""
        print("\n📋 Bank Accounts:")
        print("1.1 Savings Account")
        print("1.2 Current Account")
        print("1.3 Fixed Deposit (FD)")
        print("1.4 Recurring Deposit (RD)")
        print("1.5 Salary Account")
        print("1.6 Back to Main Menu")

    def display_loans_menu(self):
        """Display loans submenu"""
        print("\n💰 Loan Services:")
        print("2.1 Home Loan")
        print("2.2 Personal Loan")
        print("2.3 Car Loan")
        print("2.4 Education Loan")
        print("2.5 Business Loan")
        print("2.6 Property Loan")
        print("2.7 Agricultural Loan")
        print("2.8 Back to Main Menu")

    def display_cards_menu(self):
        """Display cards submenu"""
        print("\n💳 Card Types:")
        print("3.1 Debit Card")
        print("3.2 Credit Card")
        print("3.3 Prepaid Card")
        print("3.4 ATM Card")
        print("3.5 Virtual Card")
        print("3.6 International Card")
        print("3.7 Back to Main Menu")

    def display_service_details(self, category, service_id):
        """Display detailed information about a specific service"""
        if category in self.banking_data and service_id in self.banking_data[category]:
            service = self.banking_data[category][service_id]
            print(f"\n📌 {service['name']} Details:")
            print(f"\nDefinition: {service['definition']}")
            print(f"\nEligibility: {service['eligibility']}")
            print("\nRequired Documents:")
            for doc in service['documents']:
                print(f"- {doc}")
            print("\nBenefits:")
            for benefit in service['benefits']:
                print(f"- {benefit}")
            print("\nRules:")
            for rule in service['rules']:
                print(f"- {rule}")
        else:
            print("Service information not available.")

    def start_chat(self):
        """Start the chatbot interaction"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-5): ")

            if choice == "1":
                while True:
                    self.display_accounts_menu()
                    sub_choice = input("\nEnter your choice (1.1-1.6): ")
                    if sub_choice == "1.6":
                        break
                    elif sub_choice in self.banking_data["accounts"]:
                        self.display_service_details("accounts", sub_choice)
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "2":
                while True:
                    self.display_loans_menu()
                    sub_choice = input("\nEnter your choice (2.1-2.8): ")
                    if sub_choice == "2.8":
                        break
                    elif sub_choice in self.banking_data["loans"]:
                        self.display_service_details("loans", sub_choice)
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "3":
                while True:
                    self.display_cards_menu()
                    sub_choice = input("\nEnter your choice (3.1-3.7): ")
                    if sub_choice == "3.7":
                        break
                    elif sub_choice in self.banking_data["cards"]:
                        self.display_service_details("cards", sub_choice)
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "4":
                print("\n🤖 AI Q&A Session (Type 'back' to return to main menu)")
                while True:
                    query = input("\nAsk your banking question: ")
                    if query.lower() == 'back':
                        break
                    response = self.get_ai_response(query)
                    print(f"\nAI: {response}")

            elif choice == "5":
                print("\nThank you for using our Banking Services Chatbot! Goodbye! 👋")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    chatbot = BankChatbot()
    chatbot.start_chat() 