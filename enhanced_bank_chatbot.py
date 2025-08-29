import os
import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from dotenv import load_dotenv

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize transformers pipeline for text classification
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load banking knowledge base
class BankingKnowledgeBase:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.vectorizer = TfidfVectorizer()
        self._prepare_vectorizer()
    
    def _load_knowledge_base(self):
        # Load banking knowledge from JSON file
        try:
            with open('banking_knowledge.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to basic knowledge base
            return {
                "account_types": {
                    "savings": "A savings account is a basic type of bank account that allows you to deposit money, keep it safe, and withdraw funds, all while earning interest.",
                    "checking": "A checking account is a deposit account that allows you to easily access your money for daily transactions.",
                    "fixed_deposit": "A fixed deposit is an investment instrument offered by banks which provides investors a higher rate of interest than a regular savings account."
                },
                "loan_types": {
                    "personal": "A personal loan is an unsecured loan that can be used for any purpose, with fixed interest rates and monthly payments.",
                    "home": "A home loan is a secured loan taken to purchase a property, with the property itself serving as collateral.",
                    "car": "A car loan is a secured loan taken to purchase a vehicle, with the vehicle serving as collateral."
                },
                "cards": {
                    "credit": "A credit card allows you to borrow money up to a certain limit to make purchases, with the obligation to pay back the borrowed amount.",
                    "debit": "A debit card allows you to spend money by drawing on funds you have deposited at the bank."
                }
            }
    
    def _prepare_vectorizer(self):
        # Prepare TF-IDF vectorizer with all knowledge base entries
        all_texts = []
        for category in self.knowledge_base.values():
            for text in category.values():
                all_texts.append(text)
        self.vectorizer.fit(all_texts)
    
    def find_similar_questions(self, query, threshold=0.3):
        # Convert query to vector
        query_vec = self.vectorizer.transform([query])
        
        # Compare with all knowledge base entries
        similarities = {}
        for category, items in self.knowledge_base.items():
            for key, text in items.items():
                text_vec = self.vectorizer.transform([text])
                similarity = cosine_similarity(query_vec, text_vec)[0][0]
                if similarity > threshold:
                    similarities[f"{category}.{key}"] = similarity
        
        return sorted(similarities.items(), key=lambda x: x[1], reverse=True)

class BankingChatbot:
    def __init__(self):
        self.knowledge_base = BankingKnowledgeBase()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        # Tokenize and remove stopwords
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)
    
    def extract_entities(self, text):
        # Extract named entities using spaCy
        doc = nlp(text)
        entities = {
            'account_types': [],
            'loan_types': [],
            'card_types': [],
            'other': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['other'].append(ent.text)
        
        # Check for specific banking terms
        text_lower = text.lower()
        for account_type in self.knowledge_base.knowledge_base['account_types'].keys():
            if account_type in text_lower:
                entities['account_types'].append(account_type)
        
        for loan_type in self.knowledge_base.knowledge_base['loan_types'].keys():
            if loan_type in text_lower:
                entities['loan_types'].append(loan_type)
        
        for card_type in self.knowledge_base.knowledge_base['cards'].keys():
            if card_type in text_lower:
                entities['card_types'].append(card_type)
        
        return entities
    
    def classify_intent(self, text):
        # Classify the intent of the user's query
        result = classifier(text)[0]
        return result['label'], result['score']
    
    def generate_response(self, user_input):
        # Preprocess input
        processed_input = self.preprocess_text(user_input)
        
        # Extract entities
        entities = self.extract_entities(user_input)
        
        # Classify intent
        intent, confidence = self.classify_intent(user_input)
        
        # Find similar questions
        similar_questions = self.knowledge_base.find_similar_questions(processed_input)
        
        # Generate response based on analysis
        if similar_questions:
            best_match = similar_questions[0]
            category, key = best_match[0].split('.')
            response = self.knowledge_base.knowledge_base[category][key]
            
            # Add context based on entities
            if entities['account_types']:
                response += f"\n\nWould you like to know more about {', '.join(entities['account_types'])} accounts?"
            elif entities['loan_types']:
                response += f"\n\nWould you like to know more about {', '.join(entities['loan_types'])} loans?"
            elif entities['card_types']:
                response += f"\n\nWould you like to know more about {', '.join(entities['card_types'])} cards?"
            
            return response
        
        # Fallback response
        return """I'm not sure I understand your question completely. Could you please:
1. Be more specific about your banking query
2. Check if your question relates to:
   - Account types (savings, checking, fixed deposit)
   - Loan types (personal, home, car)
   - Card types (credit, debit)
3. Try rephrasing your question"""

# Initialize chatbot
chatbot = BankingChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        response = chatbot.generate_response(user_input)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 