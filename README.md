# 🤖 Prompt Engineering Chatbot

A Python chatbot demonstrating lessons from a Prompt Engineering course: Summarization, Transformation, Expansion, Inference, and Chatting with LLMs.

---

## 🔹 Features

- **LLMs & Prompting Principles**: Explains types of LLMs and effective prompting techniques.  
- **Iterative Prompt Development**: Shows step-by-step prompt refinement.  
- **Summarization**: Converts long text into bullets, one line, or detailed summary.  
- **Inferring**: Extracts sentiment, topics, and possible intent.  
- **Transforming**: Changes tone, style, or translates text (e.g., Formal → Casual, English → Telugu).  
- **Expanding**: Expands short text into detailed outputs like emails or stories.  
- **Chatbot (Capstone)**: Combines all lessons into one chatbot interface.

---

## 🔹 Tech Stack

- Python 3.11+  
- Streamlit for UI  
- OpenAI API (GPT-4o-mini / GPT-3.5-turbo)  
- Python-dotenv for environment variables  

---

## 🔹 Installation

1. **Clone the repo:**

```bash
git clone https://github.com/Haritha4170/prompt-engineering-chatbot.git
cd prompt-engineering-chatbot

## 🔹 2.Create & activate virtual environment (Windows):

bash
Copy code
python -m venv .venv
.venv\Scripts\activate.bat
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file with your OpenAI API key:

ini
Copy code
OPENAI_API_KEY=sk-your_api_key_here
Run the App:

bash
Copy code
streamlit run app.py
Open your browser at http://localhost:8501 to interact with the chatbot.

🔹 Usage
Summarize: Short or detailed summaries of long text.

Transform: Change tone, style, or language.

Expand: Turn short text into long-form outputs.

Infer: Detect sentiment, topics, and intent.

Chat: Interactive chatbot for any query.



🔹 Skills Learned
Prompt engineering with LLMs

Summarization, inference, transformation, expansion

Streamlit app development

OpenAI API integration

Deploying Python apps
