from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests
from textblob import TextBlob
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

class BankChatbot:
    def __init__(self):
        # Initialize banking data with enhanced information
        self.banking_data = {
            "accounts": {
                "1.1": {
                    "name": "Savings Account",
                    "definition": "A basic bank account for individuals to save money and earn interest",
                    "eligibility": "Individuals above 18 years, valid KYC documents",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Passport Size Photos (2)",
                        "KYC Form"
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
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "4.0%",
                            "min_balance": "Rs. 10,000",
                            "application_link": "https://www.hdfcbank.com/personal/save/accounts/savings-accounts"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "3.5%",
                            "min_balance": "Rs. 10,000",
                            "application_link": "https://www.icicibank.com/Personal-Banking/account-deposit/savings-account/index.page"
                        },
                        {
                            "name": "State Bank of India",
                            "interest_rate": "3.0%",
                            "min_balance": "Rs. 3,000",
                            "application_link": "https://retailbanking.sbi.co.in/retail/savings-account.htm"
                        }
                    ]
                },
                "1.2": {
                    "name": "Current Account",
                    "definition": "A bank account for businesses and professionals with high transaction volume",
                    "eligibility": "Businesses, professionals, companies, partnerships",
                    "documents": [
                        "Business Proof (Registration Certificate, GST Certificate)",
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Business Premises Proof)",
                        "Board Resolution (for companies)",
                        "Authorized Signatory List",
                        "Business PAN Card",
                        "Photographs of Signatories"
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
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "min_balance": "Rs. 25,000",
                            "transaction_limit": "Unlimited",
                            "application_link": "https://www.hdfcbank.com/personal/save/accounts/current-accounts"
                        },
                        {
                            "name": "ICICI Bank",
                            "min_balance": "Rs. 25,000",
                            "transaction_limit": "Unlimited",
                            "application_link": "https://www.icicibank.com/Personal-Banking/account-deposit/current-account/index.page"
                        },
                        {
                            "name": "Axis Bank",
                            "min_balance": "Rs. 25,000",
                            "transaction_limit": "Unlimited",
                            "application_link": "https://www.axisbank.com/retail/current-account"
                        }
                    ]
                },
                "1.3": {
                    "name": "Fixed Deposit",
                    "definition": "A term deposit with fixed interest rate and maturity period",
                    "eligibility": "Individuals, companies, trusts, societies",
                    "documents": [
                        "Identity Proof",
                        "Address Proof",
                        "PAN Card",
                        "Form 15G/15H (if applicable)"
                    ],
                    "benefits": [
                        "Higher Interest Rates (5-7% p.a.)",
                        "Flexible Tenure (7 days to 10 years)",
                        "Loan Against FD",
                        "Auto-renewal Option",
                        "Quarterly Interest Payout Option"
                    ],
                    "rules": [
                        "Minimum deposit: Rs. 1,000",
                        "Premature withdrawal charges apply",
                        "TDS applicable on interest"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "7.0%",
                            "min_deposit": "Rs. 5,000",
                            "application_link": "https://www.hdfcbank.com/personal/save/deposits/fixed-deposits"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "6.9%",
                            "min_deposit": "Rs. 10,000",
                            "application_link": "https://www.icicibank.com/Personal-Banking/account-deposit/fixed-deposits/index.page"
                        }
                    ]
                },
                "1.4": {
                    "name": "Recurring Deposit",
                    "definition": "A systematic savings scheme with fixed monthly deposits",
                    "eligibility": "Individuals, minors with guardian",
                    "documents": [
                        "Identity Proof",
                        "Address Proof",
                        "PAN Card",
                        "Passport Size Photos"
                    ],
                    "benefits": [
                        "Interest Rate: 5-7% p.a.",
                        "Flexible Deposit Amount",
                        "Tenure: 6 months to 10 years",
                        "Loan Against RD",
                        "Auto-debit Facility",
                        "Premature Withdrawal Option"
                    ],
                    "rules": [
                        "Minimum monthly deposit: Rs. 100",
                        "Fixed deposit amount",
                        "Monthly payment required"
                    ],
                    "best_banks": [
                        {
                            "name": "SBI",
                            "interest_rate": "6.5%",
                            "min_deposit": "Rs. 100",
                            "application_link": "https://retailbanking.sbi.co.in/retail/rd.htm"
                        },
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "6.7%",
                            "min_deposit": "Rs. 500",
                            "application_link": "https://www.hdfcbank.com/personal/save/deposits/recurring-deposits"
                        }
                    ]
                },
                "1.5": {
                    "name": "Salary Account",
                    "definition": "A zero-balance account for salaried individuals",
                    "eligibility": "Salaried employees with employer tie-up",
                    "documents": [
                        "Identity Proof",
                        "Address Proof",
                        "PAN Card",
                        "Salary Slip",
                        "Employer ID Card"
                    ],
                    "benefits": [
                        "Zero Balance Account",
                        "Free Debit Card",
                        "Free Cheque Book",
                        "Free RTGS/NEFT",
                        "Personal Accident Insurance",
                        "Health Insurance",
                        "Concierge Services",
                        "Special Offers on Loans"
                    ],
                    "rules": [
                        "Linked to employer",
                        "Automatic salary credit",
                        "No minimum balance required"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "features": "Comprehensive benefits",
                            "application_link": "https://www.hdfcbank.com/personal/save/accounts/salary-accounts"
                        },
                        {
                            "name": "ICICI Bank",
                            "features": "Premium benefits",
                            "application_link": "https://www.icicibank.com/Personal-Banking/account-deposit/salary-account/index.page"
                        }
                    ]
                }
            },
            "loans": {
                "2.1": {
                    "name": "Home Loan",
                    "definition": "Loan for purchasing or constructing a residential property",
                    "eligibility": "Age: 21-65 years, Stable income, Good credit score",
                    "documents": [
                        "Property Documents (Sale Agreement, Title Deed)",
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Income Proof (Salary Slips, Bank Statements)",
                        "Property Valuation Report",
                        "Cost Estimate",
                        "Builder Profile"
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
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "8.40%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.hdfc.com/home-loan"
                        },
                        {
                            "name": "SBI",
                            "interest_rate": "8.55%",
                            "processing_fee": "0.35%",
                            "application_link": "https://homeloans.sbi/"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "8.60%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.icicibank.com/home-loan/interest-rates.page"
                        }
                    ]
                },
                "2.2": {
                    "name": "Personal Loan",
                    "definition": "Unsecured loan for personal needs without collateral",
                    "eligibility": "Age: 21-60 years, Minimum income Rs. 25,000/month, Good credit score",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Income Proof (Salary Slips, Bank Statements)",
                        "ITR Returns",
                        "Form 16"
                    ],
                    "benefits": [
                        "Amount: Rs. 50,000 to Rs. 20 lakhs",
                        "Interest Rate: From 10.5%",
                        "Tenure: Up to 5 years",
                        "Quick Disbursement",
                        "No Collateral Required",
                        "Flexible EMI",
                        "Pre-closure Option",
                        "Balance Transfer"
                    ],
                    "rules": [
                        "EMI based on income",
                        "Processing fee: 1-2%",
                        "Pre-closure charges apply"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "10.50%",
                            "processing_fee": "1%",
                            "application_link": "https://www.hdfcbank.com/personal/borrow/personal-loan"
                        },
                        {
                            "name": "SBI",
                            "interest_rate": "10.75%",
                            "processing_fee": "1%",
                            "application_link": "https://bank.sbi/web/personal-banking/loans/personal-loans"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "10.90%",
                            "processing_fee": "1%",
                            "application_link": "https://www.icicibank.com/Personal-Banking/loans/personal-loan/index.page"
                        }
                    ]
                },
                "2.3": {
                    "name": "Car Loan",
                    "definition": "Loan for purchasing new or used vehicles",
                    "eligibility": "Age: 21-65 years, Stable income, Good credit score",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Income Proof (Salary Slips, Bank Statements)",
                        "Car Quotation",
                        "Driving License"
                    ],
                    "benefits": [
                        "Amount: Up to 100% of car value",
                        "Interest Rate: From 7.5%",
                        "Tenure: Up to 7 years",
                        "Zero Down Payment Option",
                        "Insurance Coverage",
                        "Quick Processing",
                        "Flexible EMI",
                        "Pre-closure Option"
                    ],
                    "rules": [
                        "EMI based on income",
                        "Processing fee: 0.5-1%",
                        "Pre-closure charges apply"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "7.50%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.hdfcbank.com/personal/borrow/car-loan"
                        },
                        {
                            "name": "SBI",
                            "interest_rate": "7.75%",
                            "processing_fee": "0.50%",
                            "application_link": "https://bank.sbi/web/personal-banking/loans/vehicle-loans"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "7.90%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.icicibank.com/Personal-Banking/loans/car-loan/index.page"
                        }
                    ]
                },
                "2.4": {
                    "name": "Education Loan",
                    "definition": "Loan for higher education in India or abroad",
                    "eligibility": "Student with admission letter, Co-applicant required",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Admission Letter",
                        "Course Fee Structure",
                        "Co-applicant Income Proof",
                        "Academic Records"
                    ],
                    "benefits": [
                        "Amount: Up to Rs. 1.5 crores",
                        "Interest Rate: From 8.5%",
                        "Tenure: Up to 15 years",
                        "Moratorium Period Available",
                        "No Collateral for loans up to Rs. 7.5 lakhs",
                        "Tax Benefits",
                        "Flexible Repayment",
                        "Coverage for all expenses"
                    ],
                    "rules": [
                        "Processing fee: 0.5-1%",
                        "Insurance premium applicable",
                        "Pre-closure charges apply"
                    ],
                    "best_banks": [
                        {
                            "name": "SBI",
                            "interest_rate": "8.50%",
                            "processing_fee": "0.50%",
                            "application_link": "https://bank.sbi/web/personal-banking/loans/education-loans"
                        },
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "8.75%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.hdfcbank.com/personal/borrow/education-loan"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "8.90%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.icicibank.com/Personal-Banking/loans/education-loan/index.page"
                        }
                    ]
                },
                "2.5": {
                    "name": "Business Loan",
                    "definition": "Loan for business expansion, working capital, or new ventures",
                    "eligibility": "Business owners, entrepreneurs, companies with 2+ years of operation",
                    "documents": [
                        "Business Proof (Registration, GST, Tax Returns)",
                        "Financial Statements",
                        "Business Plan",
                        "Bank Statements",
                        "Identity Proof",
                        "Address Proof"
                    ],
                    "benefits": [
                        "Amount: Up to Rs. 50 crores",
                        "Interest Rate: From 9.5%",
                        "Tenure: Up to 10 years",
                        "Quick Processing",
                        "Flexible Repayment",
                        "Working Capital Support",
                        "No Collateral Required",
                        "Business Advisory Services"
                    ],
                    "rules": [
                        "Processing fee: 1-2%",
                        "Business insurance required",
                        "Regular financial reporting"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "9.50%",
                            "processing_fee": "1%",
                            "application_link": "https://www.hdfcbank.com/sme/borrow/loans/business-loans"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "9.75%",
                            "processing_fee": "1%",
                            "application_link": "https://www.icicibank.com/small-business/business-loans/index.page"
                        }
                    ]
                },
                "2.6": {
                    "name": "Property Loan",
                    "definition": "Loan against property for business or personal needs",
                    "eligibility": "Property owners, Age: 21-65 years, Stable income",
                    "documents": [
                        "Property Documents",
                        "Identity Proof",
                        "Income Proof",
                        "Property Valuation Report",
                        "Bank Statements"
                    ],
                    "benefits": [
                        "Amount: Up to 70% of property value",
                        "Interest Rate: From 8.5%",
                        "Tenure: Up to 15 years",
                        "Flexible End-use",
                        "Lower Interest Rates",
                        "Longer Tenure",
                        "Balance Transfer",
                        "Top-up Facility"
                    ],
                    "rules": [
                        "Processing fee: 1-2%",
                        "Property insurance required",
                        "Regular EMI payments"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "8.50%",
                            "processing_fee": "1%",
                            "application_link": "https://www.hdfc.com/loan-against-property"
                        },
                        {
                            "name": "ICICI Bank",
                            "interest_rate": "8.75%",
                            "processing_fee": "1%",
                            "application_link": "https://www.icicibank.com/Personal-Banking/loans/loan-against-property/index.page"
                        }
                    ]
                },
                "2.7": {
                    "name": "Agricultural Loan",
                    "definition": "Loan for farming activities, equipment, and agricultural development",
                    "eligibility": "Farmers, agricultural businesses, rural entrepreneurs",
                    "documents": [
                        "Land Documents",
                        "Identity Proof",
                        "Address Proof",
                        "Farming Experience Proof",
                        "Bank Statements"
                    ],
                    "benefits": [
                        "Amount: Up to Rs. 1 crore",
                        "Interest Rate: From 7%",
                        "Tenure: Up to 10 years",
                        "Subsidy Available",
                        "Seasonal Repayment",
                        "Equipment Financing",
                        "Crop Insurance",
                        "Technical Support"
                    ],
                    "rules": [
                        "Processing fee: 0.5%",
                        "Insurance required",
                        "Regular farm visits"
                    ],
                    "best_banks": [
                        {
                            "name": "SBI",
                            "interest_rate": "7.00%",
                            "processing_fee": "0.50%",
                            "application_link": "https://bank.sbi/web/agriculture-banking/agriculture-loans"
                        },
                        {
                            "name": "HDFC Bank",
                            "interest_rate": "7.25%",
                            "processing_fee": "0.50%",
                            "application_link": "https://www.hdfcbank.com/personal/borrow/agriculture-loans"
                        }
                    ]
                }
            },
            "cards": {
                "3.1": {
                    "name": "Debit Card",
                    "definition": "Card linked to bank account for cashless transactions",
                    "eligibility": "Account holder with valid KYC",
                    "documents": [
                        "Account Details",
                        "KYC Documents (Aadhaar Card, PAN Card)",
                        "Card Application Form",
                        "Passport Size Photo"
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
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "annual_fee": "Zero",
                            "cashback": "Up to 1%",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/debit-cards"
                        },
                        {
                            "name": "ICICI Bank",
                            "annual_fee": "Zero",
                            "cashback": "Up to 1%",
                            "application_link": "https://www.icicibank.com/Personal-Banking/cards/debit-cards/index.page"
                        },
                        {
                            "name": "Axis Bank",
                            "annual_fee": "Zero",
                            "cashback": "Up to 1%",
                            "application_link": "https://www.axisbank.com/retail/cards/debit-card"
                        }
                    ]
                },
                "3.2": {
                    "name": "Credit Card",
                    "definition": "Card allowing credit-based purchases with revolving credit limit",
                    "eligibility": "Age: 21-60 years, Minimum income Rs. 3 lakhs/year, Good credit score",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Income Proof (Salary Slips, Bank Statements)",
                        "ITR Returns",
                        "Form 16"
                    ],
                    "benefits": [
                        "Credit Limit: Based on income",
                        "Interest-free Period: Up to 50 days",
                        "Reward Points Program",
                        "Travel Insurance",
                        "Lounge Access",
                        "Fuel Surcharge Waiver",
                        "EMI Options",
                        "Balance Transfer",
                        "Add-on Cards"
                    ],
                    "rules": [
                        "Annual fee: Rs. 500-5,000",
                        "Interest rate: 3-4% per month",
                        "Late payment charges apply"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "annual_fee": "Rs. 2,500",
                            "reward_rate": "2X",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/credit-cards"
                        },
                        {
                            "name": "ICICI Bank",
                            "annual_fee": "Rs. 2,500",
                            "reward_rate": "2X",
                            "application_link": "https://www.icicibank.com/Personal-Banking/cards/credit-cards/index.page"
                        },
                        {
                            "name": "Axis Bank",
                            "annual_fee": "Rs. 2,500",
                            "reward_rate": "2X",
                            "application_link": "https://www.axisbank.com/retail/cards/credit-card"
                        }
                    ]
                },
                "3.3": {
                    "name": "Prepaid Card",
                    "definition": "Card with pre-loaded amount for controlled spending",
                    "eligibility": "Anyone with valid KYC documents",
                    "documents": [
                        "Identity Proof (Aadhaar Card, PAN Card, Passport)",
                        "Address Proof (Utility Bills, Bank Statement)",
                        "Passport Size Photo"
                    ],
                    "benefits": [
                        "No Bank Account Required",
                        "Controlled Spending",
                        "Online Shopping",
                        "Bill Payments",
                        "Cash Withdrawal",
                        "Gift Option",
                        "No Credit Check",
                        "Reloadable"
                    ],
                    "rules": [
                        "Maximum balance: Rs. 2 lakhs",
                        "Reload charges apply",
                        "Validity: 3-5 years"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "annual_fee": "Rs. 500",
                            "max_balance": "Rs. 2 lakhs",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/prepaid-cards"
                        },
                        {
                            "name": "ICICI Bank",
                            "annual_fee": "Rs. 500",
                            "max_balance": "Rs. 2 lakhs",
                            "application_link": "https://www.icicibank.com/Personal-Banking/cards/prepaid-cards/index.page"
                        }
                    ]
                },
                "3.4": {
                    "name": "ATM Card",
                    "definition": "Basic card for ATM withdrawals and limited transactions",
                    "eligibility": "Account holder with valid KYC",
                    "documents": [
                        "Account Details",
                        "KYC Documents",
                        "Card Application Form"
                    ],
                    "benefits": [
                        "Zero Annual Fee",
                        "ATM Withdrawals",
                        "Balance Enquiry",
                        "Mini Statement",
                        "PIN Change",
                        "Basic Security"
                    ],
                    "rules": [
                        "Daily withdrawal limit: Rs. 25,000",
                        "PIN required",
                        "Limited to ATM usage"
                    ],
                    "best_banks": [
                        {
                            "name": "SBI",
                            "annual_fee": "Zero",
                            "withdrawal_limit": "Rs. 25,000",
                            "application_link": "https://retailbanking.sbi.co.in/retail/atm-card.htm"
                        },
                        {
                            "name": "HDFC Bank",
                            "annual_fee": "Zero",
                            "withdrawal_limit": "Rs. 25,000",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/atm-cards"
                        }
                    ]
                },
                "3.5": {
                    "name": "Virtual Card",
                    "definition": "Digital card for online transactions without physical card",
                    "eligibility": "Account holder with internet banking",
                    "documents": [
                        "Account Details",
                        "Internet Banking Access",
                        "Mobile Number"
                    ],
                    "benefits": [
                        "Instant Generation",
                        "Online Shopping",
                        "Bill Payments",
                        "Subscription Payments",
                        "Enhanced Security",
                        "Temporary Card Option",
                        "Spending Limits",
                        "Real-time Alerts"
                    ],
                    "rules": [
                        "Valid for online transactions only",
                        "Temporary validity option",
                        "Spending limits apply"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "features": "Instant generation",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/virtual-cards"
                        },
                        {
                            "name": "ICICI Bank",
                            "features": "Temporary cards",
                            "application_link": "https://www.icicibank.com/Personal-Banking/cards/virtual-cards/index.page"
                        }
                    ]
                },
                "3.6": {
                    "name": "International Card",
                    "definition": "Card for international travel and transactions",
                    "eligibility": "Account holder with valid passport",
                    "documents": [
                        "Passport",
                        "Visa (if required)",
                        "Travel Documents",
                        "KYC Documents"
                    ],
                    "benefits": [
                        "Global Acceptance",
                        "Travel Insurance",
                        "Lounge Access",
                        "Zero Foreign Currency Markup",
                        "Emergency Card Replacement",
                        "Travel Assistance",
                        "Reward Points",
                        "Currency Conversion"
                    ],
                    "rules": [
                        "Higher annual fee",
                        "Travel insurance required",
                        "International usage limits"
                    ],
                    "best_banks": [
                        {
                            "name": "HDFC Bank",
                            "annual_fee": "Rs. 3,000",
                            "features": "Global acceptance",
                            "application_link": "https://www.hdfcbank.com/personal/pay/cards/international-cards"
                        },
                        {
                            "name": "ICICI Bank",
                            "annual_fee": "Rs. 3,000",
                            "features": "Travel benefits",
                            "application_link": "https://www.icicibank.com/Personal-Banking/cards/international-cards/index.page"
                        }
                    ]
                }
            },
            "schemes": {
                "5.1": {
                    "name": "Pradhan Mantri Jan Dhan Yojana (PMJDY)",
                    "definition": "Financial inclusion scheme for providing banking services to all households",
                    "eligibility": "Any individual above 10 years of age, no income criteria",
                    "documents": [
                        "Aadhaar Card",
                        "PAN Card (if available)",
                        "Passport Size Photos",
                        "Address Proof"
                    ],
                    "benefits": [
                        "Zero Balance Account",
                        "RuPay Debit Card",
                        "Accident Insurance of Rs. 2 lakhs",
                        "Overdraft facility up to Rs. 10,000",
                        "Direct Benefit Transfer",
                        "Mobile Banking",
                        "Pension Schemes Access"
                    ],
                    "rules": [
                        "One account per family",
                        "No minimum balance required",
                        "Free mobile banking",
                        "Free ATM transactions"
                    ],
                    "best_banks": [
                        {
                            "name": "State Bank of India",
                            "features": "Wide branch network",
                            "application_link": "https://retailbanking.sbi.co.in/retail/pmjdy.htm"
                        },
                        {
                            "name": "Bank of Baroda",
                            "features": "Easy account opening",
                            "application_link": "https://www.bankofbaroda.in/personal-banking/accounts/savings-accounts/pmjdy-account"
                        }
                    ]
                },
                "5.2": {
                    "name": "Sukanya Samriddhi Yojana",
                    "definition": "Small deposit scheme for girl child education and marriage",
                    "eligibility": "Parents/guardians of girl child below 10 years",
                    "documents": [
                        "Birth Certificate of Girl Child",
                        "Aadhaar Card of Parents",
                        "Address Proof",
                        "Passport Size Photos"
                    ],
                    "benefits": [
                        "Interest Rate: 7.6% p.a.",
                        "Tax Benefits under Section 80C",
                        "Partial Withdrawal for Education",
                        "Maturity Period: 21 years",
                        "Minimum Deposit: Rs. 250",
                        "Maximum Deposit: Rs. 1.5 lakhs per year"
                    ],
                    "rules": [
                        "One account per girl child",
                        "Maximum two accounts per family",
                        "Deposit period: 14 years",
                        "Premature withdrawal allowed for education"
                    ],
                    "best_banks": [
                        {
                            "name": "State Bank of India",
                            "interest_rate": "7.6%",
                            "application_link": "https://retailbanking.sbi.co.in/retail/sukanya-samriddhi-yojana.htm"
                        },
                        {
                            "name": "Post Office",
                            "interest_rate": "7.6%",
                            "application_link": "https://www.indiapost.gov.in/Financial/Pages/Content/Sukanya-Samriddhi-Account.aspx"
                        }
                    ]
                },
                "5.3": {
                    "name": "Atal Pension Yojana (APY)",
                    "definition": "Pension scheme for unorganized sector workers",
                    "eligibility": "Age: 18-40 years, No income criteria",
                    "documents": [
                        "Aadhaar Card",
                        "Bank Account Details",
                        "Mobile Number",
                        "Nominee Details"
                    ],
                    "benefits": [
                        "Pension: Rs. 1,000 to Rs. 5,000 per month",
                        "Government Co-contribution",
                        "Tax Benefits",
                        "Guaranteed Pension",
                        "Spouse Continuation"
                    ],
                    "rules": [
                        "Monthly contribution based on age",
                        "Minimum contribution period: 20 years",
                        "Exit age: 60 years",
                        "Premature exit allowed with conditions"
                    ],
                    "best_banks": [
                        {
                            "name": "State Bank of India",
                            "features": "Wide coverage",
                            "application_link": "https://retailbanking.sbi.co.in/retail/atal-pension-yojana.htm"
                        },
                        {
                            "name": "HDFC Bank",
                            "features": "Easy enrollment",
                            "application_link": "https://www.hdfcbank.com/personal/save/accounts/atal-pension-yojana"
                        }
                    ]
                },
                "5.4": {
                    "name": "Pradhan Mantri Mudra Yojana",
                    "definition": "Loan scheme for micro enterprises",
                    "eligibility": "Small business owners, entrepreneurs, micro enterprises",
                    "documents": [
                        "Business Proof",
                        "Identity Proof",
                        "Address Proof",
                        "Project Report",
                        "Bank Statements"
                    ],
                    "benefits": [
                        "Loan up to Rs. 10 lakhs",
                        "No collateral required",
                        "Low interest rates",
                        "Quick processing",
                        "Three categories: Shishu, Kishore, Tarun"
                    ],
                    "rules": [
                        "Shishu: Up to Rs. 50,000",
                        "Kishore: Rs. 50,000 to Rs. 5 lakhs",
                        "Tarun: Rs. 5 lakhs to Rs. 10 lakhs",
                        "Processing fee: 0.5% to 1%"
                    ],
                    "best_banks": [
                        {
                            "name": "State Bank of India",
                            "interest_rate": "From 8.05%",
                            "application_link": "https://bank.sbi/web/personal-banking/loans/mudra-loans"
                        },
                        {
                            "name": "Bank of Baroda",
                            "interest_rate": "From 8.05%",
                            "application_link": "https://www.bankofbaroda.in/personal-banking/loans/mudra-loan"
                        }
                    ]
                },
                "5.5": {
                    "name": "Senior Citizen Savings Scheme (SCSS)",
                    "definition": "Retirement savings scheme for senior citizens",
                    "eligibility": "Age: 60 years or above, 55 years for retired personnel",
                    "documents": [
                        "Age Proof",
                        "Identity Proof",
                        "Address Proof",
                        "PAN Card",
                        "Retirement Proof (if applicable)"
                    ],
                    "benefits": [
                        "Interest Rate: 7.4% p.a.",
                        "Quarterly Interest Payout",
                        "Tax Benefits under Section 80C",
                        "Tenure: 5 years (extendable)",
                        "Joint Account Option"
                    ],
                    "rules": [
                        "Minimum deposit: Rs. 1,000",
                        "Maximum deposit: Rs. 15 lakhs",
                        "Premature withdrawal allowed with penalty",
                        "Extension possible for 3 years"
                    ],
                    "best_banks": [
                        {
                            "name": "State Bank of India",
                            "interest_rate": "7.4%",
                            "application_link": "https://retailbanking.sbi.co.in/retail/senior-citizen-savings-scheme.htm"
                        },
                        {
                            "name": "Post Office",
                            "interest_rate": "7.4%",
                            "application_link": "https://www.indiapost.gov.in/Financial/Pages/Content/Senior-Citizen-Savings-Scheme.aspx"
                        }
                    ]
                }
            }
        }
        
        # Common banking questions and answers
        self.qa_database = {
            "how to open account": "To open a bank account, you need:\n1. Valid ID proof (Aadhaar/PAN)\n2. Address proof\n3. Passport photos\n4. Visit any bank branch or apply online",
            "minimum balance": "Minimum balance requirements vary by bank:\n- Savings Account: Rs. 1,000 to Rs. 10,000\n- Current Account: Rs. 10,000 to Rs. 25,000\n- Zero Balance accounts available with some banks",
            "interest rates": "Current interest rates (approximate):\n- Savings Account: 2.5% to 4% p.a.\n- Fixed Deposit: 5% to 7% p.a.\n- Home Loan: 8.4% to 9% p.a.\n- Personal Loan: 10.5% to 12% p.a.",
            "documents for loan": "Common documents required for loans:\n1. ID Proof (Aadhaar/PAN)\n2. Address Proof\n3. Income Proof\n4. Bank Statements\n5. Property Documents (for home loan)",
            "online banking": "To use online banking:\n1. Register for internet banking\n2. Download bank's mobile app\n3. Set up security features\n4. Use secure networks only",
            "transfer money": "You can transfer money through:\n1. NEFT (24/7)\n2. RTGS (for high-value transfers)\n3. IMPS (instant transfers)\n4. UPI (using apps like Google Pay, PhonePe)",
            "credit card": "To get a credit card:\n1. Check eligibility (income, credit score)\n2. Choose card type\n3. Apply online/offline\n4. Submit required documents",
            "security tips": "Important banking security tips:\n1. Never share OTP/PIN\n2. Use strong passwords\n3. Enable 2FA\n4. Monitor transactions regularly\n5. Report suspicious activity immediately"
        }

        # Banking context templates
        self.context_templates = [
            "Based on your question about {topic}, here's what you should know: {answer}",
            "Regarding {topic}, the information is as follows: {answer}",
            "For {topic}, here are the details: {answer}",
            "Let me explain about {topic}: {answer}",
            "Here's what you need to know about {topic}: {answer}"
        ]

        self.location_data = {
            "4.1": {
                "bank": "HDFC Bank",
                "branch_count": 5,
                "atm_count": 12,
                "branches": [
                    {
                        "name": "HDFC Main Branch",
                        "address": "123 Main St, City",
                        "maps_link": "https://maps.google.com/?q=HDFC+Main+Branch+123+Main+St+City"
                    },
                    {
                        "name": "HDFC City Center",
                        "address": "456 Center Rd, City",
                        "maps_link": "https://maps.google.com/?q=HDFC+City+Center+456+Center+Rd+City"
                    }
                    # Add more branches as needed
                ]
            },
            "4.2": {
                "bank": "ICICI Bank",
                "branch_count": 3,
                "atm_count": 8,
                "branches": [
                    {
                        "name": "ICICI Downtown",
                        "address": "789 Downtown Ave, City",
                        "maps_link": "https://maps.google.com/?q=ICICI+Downtown+789+Downtown+Ave+City"
                    }
                    # Add more branches as needed
                ]
            }
            # Add more locations as needed
        }

        self.bank_locations = [
            {
                "bank": "HDFC Bank",
                "branch_count": 120,
                "atm_count": 350,
                "maps_branch_url": "https://www.google.com/maps/search/HDFC+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/HDFC+Bank+ATM+near+me"
            },
            {
                "bank": "ICICI Bank",
                "branch_count": 100,
                "atm_count": 300,
                "maps_branch_url": "https://www.google.com/maps/search/ICICI+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/ICICI+Bank+ATM+near+me"
            },
            {
                "bank": "State Bank of India",
                "branch_count": 200,
                "atm_count": 500,
                "maps_branch_url": "https://www.google.com/maps/search/State+Bank+of+India+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/State+Bank+of+India+ATM+near+me"
            },
            {
                "bank": "Axis Bank",
                "branch_count": 80,
                "atm_count": 220,
                "maps_branch_url": "https://www.google.com/maps/search/Axis+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/Axis+Bank+ATM+near+me"
            },
            {
                "bank": "Kotak Mahindra Bank",
                "branch_count": 60,
                "atm_count": 150,
                "maps_branch_url": "https://www.google.com/maps/search/Kotak+Mahindra+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/Kotak+Mahindra+Bank+ATM+near+me"
            },
            {
                "bank": "Punjab National Bank",
                "branch_count": 90,
                "atm_count": 210,
                "maps_branch_url": "https://www.google.com/maps/search/Punjab+National+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/Punjab+National+Bank+ATM+near+me"
            },
            {
                "bank": "Bank of Baroda",
                "branch_count": 85,
                "atm_count": 180,
                "maps_branch_url": "https://www.google.com/maps/search/Bank+of+Baroda+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/Bank+of+Baroda+ATM+near+me"
            },
            {
                "bank": "Canara Bank",
                "branch_count": 75,
                "atm_count": 160,
                "maps_branch_url": "https://www.google.com/maps/search/Canara+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/Canara+Bank+ATM+near+me"
            },
            {
                "bank": "IndusInd Bank",
                "branch_count": 50,
                "atm_count": 120,
                "maps_branch_url": "https://www.google.com/maps/search/IndusInd+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/IndusInd+Bank+ATM+near+me"
            },
            {
                "bank": "IDFC FIRST Bank",
                "branch_count": 40,
                "atm_count": 100,
                "maps_branch_url": "https://www.google.com/maps/search/IDFC+FIRST+Bank+branch+near+me",
                "maps_atm_url": "https://www.google.com/maps/search/IDFC+FIRST+Bank+ATM+near+me"
            }
        ]

    def get_ai_response(self, query):
        """Get AI-powered response for banking queries"""
        try:
            # Remove the '4' prefix if present
            if query.startswith('4'):
                query = query[1:].strip()

            # Convert query to lowercase for matching
            query = query.lower()

            # Analyze the query using TextBlob
            blob = TextBlob(query)
            
            # Extract key topics from the query
            topics = [word for word, tag in blob.tags if tag.startswith('NN')]
            
            # Check for matching keywords in the QA database
            for key, answer in self.qa_database.items():
                if key in query:
                    # Generate a contextual response
                    template = random.choice(self.context_templates)
                    topic = key.replace('_', ' ').title()
                    return template.format(topic=topic, answer=answer)

            # If no direct match, provide a contextual response
            if topics:
                topic = topics[0].title()
                return f"""I understand you're asking about {topic}. Here's what I can help you with:

1. Opening bank accounts
2. Minimum balance requirements
3. Interest rates
4. Loan documents
5. Online banking
6. Money transfers
7. Credit cards
8. Security tips

Please ask a specific question about any of these topics, and I'll provide detailed information."""
            else:
                return """I can help you with information about:
1. Opening bank accounts
2. Minimum balance requirements
3. Interest rates
4. Loan documents
5. Online banking
6. Money transfers
7. Credit cards
8. Security tips

Please ask a specific question about any of these topics."""

        except Exception as e:
            return f"I apologize, but I couldn't process your query at the moment. Please try again later. Error: {str(e)}"

    def get_real_time_rates(self, service_type):
        """Get real-time rates for banking services (mock implementation)"""
        # In a real implementation, this would fetch data from banking APIs
        rates = {
            "home_loan": {
                "HDFC": "8.40%",
                "SBI": "8.55%",
                "ICICI": "8.60%"
            },
            "personal_loan": {
                "HDFC": "10.50%",
                "SBI": "10.75%",
                "ICICI": "10.90%"
            },
            "savings_account": {
                "HDFC": "4.00%",
                "SBI": "3.00%",
                "ICICI": "3.50%"
            }
        }
        return rates.get(service_type, {})

    def display_menu(self):
        """Display the main menu with all options"""
        menu = """
Please select a category by entering the corresponding number:

1. Bank Accounts
2. Loan Services
3. Card Types
4. Bank Locations & ATMs
5. Government Schemes
6. Frequently Asked Questions (FAQ)
7. Exit

Type 'exit' to quit.
"""
        return menu

    def get_response(self, user_input):
        """Get response based on user input"""
        user_input = user_input.lower().strip()
        
        if user_input == 'hi' or user_input == 'hello':
            return self.display_menu()
            
        if user_input == 'exit' or user_input == '7':
            return "Thank you for using our banking chatbot. Goodbye!"
            
        # Handle numbered menu options
        if user_input in ['1', '2', '3', '4', '5', '6']:
            if user_input == '1':
                return """
Bank Accounts Information:
1.1 Savings Account
1.2 Current Account
1.3 Fixed Deposit (FD)
1.4 Recurring Deposit (RD)
1.5 Salary Account

Please select a specific account type (e.g., 1.1 for Savings Account) for detailed information."""
            elif user_input == '2':
                return """
Loan Services Information:
2.1 Home Loan
2.2 Personal Loan
2.3 Car Loan
2.4 Education Loan
2.5 Business Loan
2.6 Property Loan
2.7 Agricultural Loan

Please select a specific loan type (e.g., 2.1 for Home Loan) for detailed information."""
            elif user_input == '3':
                return """
Card Types Information:
3.1 Debit Card
3.2 Credit Card
3.3 Prepaid Card
3.4 ATM Card
3.5 Virtual Card
3.6 International Card

Please select a specific card type (e.g., 3.1 for Debit Card) for detailed information."""
            elif user_input == '4':
                response = "🏦 Bank Locations & ATMs:\n"
                for loc in self.bank_locations:
                    response += (
                        f"\n• {loc['bank']}\n"
                        f"  - Number of Branches: {loc['branch_count']}\n"
                        f"  - Number of ATMs: {loc['atm_count']}\n"
                        f"  - [View all branches near you]({loc['maps_branch_url']})\n"
                        f"  - [View all ATMs near you]({loc['maps_atm_url']})\n"
                    )
                return response
            elif user_input == '5':
                return """
Government Schemes Information:
5.1 Pradhan Mantri Jan Dhan Yojana (PMJDY)
5.2 Sukanya Samriddhi Yojana
5.3 Atal Pension Yojana (APY)
5.4 Pradhan Mantri Mudra Yojana
5.5 Senior Citizen Savings Scheme (SCSS)

Please select a specific scheme (e.g., 5.1 for PMJDY) for detailed information."""
            elif user_input == '6':
                return self.get_faq()
        
        # Handle sub-options
        if user_input in ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '5.1', '5.2', '5.3', '5.4', '5.5']:
            if user_input.startswith('1.'):
                return self.get_account_info(user_input)
            elif user_input.startswith('2.'):
                return self.get_loan_info(user_input)
            elif user_input.startswith('3.'):
                return self.get_card_info(user_input)
            elif user_input.startswith('5.'):
                return self.get_scheme_info(user_input)
        
        # Handle AI Q&A
        if user_input.startswith('4') or not any(user_input.startswith(str(i)) for i in range(1, 8)):
            return self.get_ai_response(user_input)
            
        return "I'm not sure I understand. Please select a valid option from the menu or type 'exit' to quit."

    def get_account_info(self, account_type):
        """Get detailed information about a specific account type"""
        account_data = self.banking_data["accounts"].get(account_type)
        if not account_data:
            return "Sorry, information for this account type is not available."
            
        response = f"""
🔹 {account_data['name']}

📝 Definition:
{account_data['definition']}

✅ Eligibility:
{account_data['eligibility']}

📋 Required Documents:
{chr(10).join(['• ' + doc for doc in account_data['documents']])}

💎 Benefits:
{chr(10).join(['• ' + benefit for benefit in account_data['benefits']])}

📌 Rules:
{chr(10).join(['• ' + rule for rule in account_data['rules']])}

🏦 Best Banks:
"""
        for bank in account_data['best_banks']:
            response += f"\n• {bank['name']}"
            for key, value in bank.items():
                if key != 'name' and key != 'application_link':
                    response += f"\n  - {key.replace('_', ' ').title()}: {value}"
            response += f"\n  - Application Link: {bank['application_link']}\n"
            
        return response

    def get_loan_info(self, loan_type):
        """Get detailed information about a specific loan type"""
        loan_data = self.banking_data["loans"].get(loan_type)
        if not loan_data:
            return "Sorry, information for this loan type is not available."
            
        response = f"""
🔹 {loan_data['name']}

📝 Definition:
{loan_data['definition']}

✅ Eligibility:
{loan_data['eligibility']}

📋 Required Documents:
{chr(10).join(['• ' + doc for doc in loan_data['documents']])}

💎 Benefits:
{chr(10).join(['• ' + benefit for benefit in loan_data['benefits']])}

📌 Rules:
{chr(10).join(['• ' + rule for rule in loan_data['rules']])}

🏦 Best Banks:
"""
        for bank in loan_data['best_banks']:
            response += f"\n• {bank['name']}"
            for key, value in bank.items():
                if key != 'name' and key != 'application_link':
                    response += f"\n  - {key.replace('_', ' ').title()}: {value}"
            response += f"\n  - Application Link: {bank['application_link']}\n"
            
        return response

    def get_card_info(self, card_type):
        """Get detailed information about a specific card type"""
        card_data = self.banking_data["cards"].get(card_type)
        if not card_data:
            return "Sorry, information for this card type is not available."
            
        response = f"""
🔹 {card_data['name']}

📝 Definition:
{card_data['definition']}

✅ Eligibility:
{card_data['eligibility']}

📋 Required Documents:
{chr(10).join(['• ' + doc for doc in card_data['documents']])}

💎 Benefits:
{chr(10).join(['• ' + benefit for benefit in card_data['benefits']])}

📌 Rules:
{chr(10).join(['• ' + rule for rule in card_data['rules']])}

🏦 Best Banks:
"""
        for bank in card_data['best_banks']:
            response += f"\n• {bank['name']}"
            for key, value in bank.items():
                if key != 'name' and key != 'application_link':
                    response += f"\n  - {key.replace('_', ' ').title()}: {value}"
            response += f"\n  - Application Link: {bank['application_link']}\n"
            
        return response

    def get_scheme_info(self, scheme_type):
        """Get detailed information about a specific government scheme"""
        scheme_data = self.banking_data["schemes"].get(scheme_type)
        if not scheme_data:
            return "Sorry, information for this scheme is not available."
            
        response = f"""
🔹 {scheme_data['name']}

📝 Definition:
{scheme_data['definition']}

✅ Eligibility:
{scheme_data['eligibility']}

📋 Required Documents:
{chr(10).join(['• ' + doc for doc in scheme_data['documents']])}

💎 Benefits:
{chr(10).join(['• ' + benefit for benefit in scheme_data['benefits']])}

📌 Rules:
{chr(10).join(['• ' + rule for rule in scheme_data['rules']])}

🏦 Participating Banks:
"""
        for bank in scheme_data['best_banks']:
            response += f"\n• {bank['name']}"
            for key, value in bank.items():
                if key != 'name' and key != 'application_link':
                    response += f"\n  - {key.replace('_', ' ').title()}: {value}"
            response += f"\n  - Application Link: {bank['application_link']}\n"
            
        return response

    def get_faq(self):
        """Get frequently asked questions and answers"""
        faq = """
🔹 Frequently Asked Questions (FAQ)

1. Account Related:
   Q: What is the minimum balance required for a savings account?
   A: It varies by bank, typically between Rs. 1,000 to Rs. 10,000. Some banks offer zero-balance accounts.

   Q: How do I open a bank account?
   A: You need valid KYC documents (Aadhaar, PAN), address proof, and passport photos. Visit any bank branch or apply online.

   Q: What is the interest rate on savings accounts?
   A: Interest rates range from 2.5% to 4% per annum, depending on the bank and account type.

2. Loan Related:
   Q: What is the minimum salary required for a personal loan?
   A: Most banks require a minimum monthly income of Rs. 25,000 to Rs. 30,000.

   Q: How long does it take to get a home loan approved?
   A: Typically 7-15 working days, subject to document verification and property valuation.

   Q: What is the maximum tenure for a car loan?
   A: Usually up to 7 years, depending on the car value and your income.

3. Card Related:
   Q: What should I do if my card is lost?
   A: Immediately call the bank's 24/7 helpline to block the card and request a replacement.

   Q: Are there charges for using ATMs of other banks?
   A: Yes, after the free transactions limit (usually 3-5 per month), charges apply.

   Q: How do I activate my new debit/credit card?
   A: You can activate it through the bank's mobile app, internet banking, or by visiting an ATM.

4. General Banking:
   Q: What is NEFT/RTGS/IMPS?
   A: These are electronic fund transfer systems:
      - NEFT: National Electronic Funds Transfer (24/7)
      - RTGS: Real Time Gross Settlement (for high-value transfers)
      - IMPS: Immediate Payment Service (instant transfers)

   Q: How can I check my account balance?
   A: Through mobile banking, internet banking, ATM, SMS banking, or by visiting a branch.

   Q: What is the process for updating KYC?
   A: Visit your bank branch with original documents or update online through the bank's website/app.

5. Security Related:
   Q: How can I protect my online banking?
   A: Use strong passwords, enable 2FA, never share OTPs, and regularly update your contact details.

   Q: What should I do if I notice unauthorized transactions?
   A: Immediately report to the bank's helpline and block your card/account if necessary.

   Q: How often should I change my banking passwords?
   A: It's recommended to change passwords every 3-6 months.

For more specific questions, please use the AI Q&A session (Option 4) or select a specific banking service from the menu.
"""
        return faq

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # TODO: Add actual authentication logic here
        session['user'] = username  # For now, just store the username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
            
        # TODO: Add actual registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    chatbot_response = get_chatbot_response(user_input)
    return jsonify({'response': chatbot_response})

def get_chatbot_response(user_input):
    chatbot = BankChatbot()
    return chatbot.get_response(user_input)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)