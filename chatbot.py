import os
import json
import openai
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Load policy data
def load_policies():
    with open('data/policies.json', 'r') as f:
        return pd.read_json(f)

# Simple intent detection (expand as needed)
def detect_intent(message):
    message = message.lower()
    if 'policy' in message and ('number' in message or 'details' in message):
        return 'fetch_policy'
    if 'claim' in message:
        return 'claim_process'
    return 'general'

# Fetch policy details by policy number
def get_policy_details(policy_number):
    policies = load_policies()
    match = policies[policies['policy_number'] == policy_number]
    if not match.empty:
        return match.iloc[0].to_dict()
    return None

# Generate response using OpenAI GPT
def generate_response(message, context=None):
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    client = openai.OpenAI()
    prompt = f"You are an insurance assistant. {message}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Main chatbot handler
def chatbot_reply(message):
    try:
        intent = detect_intent(message)
        if intent == 'fetch_policy':
            # Try to extract policy number (simple approach)
            import re
            match = re.search(r'pol\d+', message, re.IGNORECASE)
            if match:
                policy_number = match.group(0).upper()
                details = get_policy_details(policy_number)
                if details:
                    return f"Policy Details for {policy_number}: Holder: {details['holder_name']}, Type: {details['type']}, Coverage: {details['coverage']}, Valid Till: {details['valid_till']}"
                else:
                    return f"Sorry, I couldn't find details for policy number {policy_number}."
            else:
                return "Please provide a valid policy number."
        elif intent == 'claim_process':
            return "To file a claim, please provide your policy number and a brief description of the incident. Our team will guide you through the next steps."
        else:
            # General insurance queries
            return generate_response(message)
    except Exception as e:
        import openai
        if isinstance(e, openai.AuthenticationError):
            return "Error: Invalid OpenAI API key. Please check your .env file."
        elif isinstance(e, openai.OpenAIError):
            return f"Error: OpenAI service error: {str(e)}"
        else:
            return f"Error: Unexpected server error: {str(e)}" 