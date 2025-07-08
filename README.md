# Insurance Query Resolution Chatbot

A simple FastAPI-based chatbot that answers insurance-related queries, fetches policy details, and guides users through claim processes using NLP (OpenAI GPT).

## Features

- Ask insurance-related questions
- Fetch policy details from sample data
- Guide users through claim processes

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
3. Run the app:
   ```bash
   uvicorn app:app --reload
   ```

## API Usage

- POST `/chat` with JSON `{ "message": "your question" }`
- Response: `{ "response": "chatbot reply" }`

## Sample Data

- Edit `data/policies.json` to add or modify insurance policy data.
