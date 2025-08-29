# Banking Chatbot

A web-based banking chatbot that provides information about various banking services, including accounts, cards, loans, and general banking queries. The chatbot uses OpenAI's GPT model for dynamic responses to custom queries.

## Features

- Interactive web interface
- Comprehensive banking information
- AI-powered Q&A session
- Quick menu options
- Responsive design
- Real-time chat experience

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bank_chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. The chatbot will greet you with a welcome message and main menu options.
2. You can either:
   - Click on the quick menu buttons (Accounts, Cards, Loans, FAQ, AI Q&A)
   - Type your query directly in the input box
3. The chatbot will respond with relevant information based on your query.
4. For custom queries, use the AI Q&A option or type your question directly.

## Menu Options

1. Types of Accounts
   - Savings Account
   - Current Account
   - Fixed Deposit
   - Recurring Deposit
   - Salary Account

2. Types of Cards
   - Debit Card
   - Credit Card
   - Prepaid Card
   - ATM Card
   - Virtual Card
   - International Card

3. Loan Services
   - Home Loan
   - Personal Loan
   - Car/Vehicle Loan
   - Education Loan
   - Property Loan
   - Business Loan
   - Agricultural Loan

4. FAQ
   - Common banking questions and answers

5. AI Q&A Session
   - Ask any banking-related question

## Contributing

Feel free to submit issues and enhancement requests! 