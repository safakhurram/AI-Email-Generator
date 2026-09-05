# ✉️ AI Email Assistant

An AI-powered email drafting and enhancement web application built with **Streamlit** and **Groq Cloud API**. This application helps users construct fresh emails, modify existing drafts, correct grammar, and adjust tones seamlessly using fast language model inference.

🔗 **Live Demo:** [https://ai-email-generator12.streamlit.app/](https://ai-email-generator12.streamlit.app/)

---

## 🚀 Features

* **Create Fresh Emails:** Generate structured emails based on recipient, context, talking points, and additional info.
* **Email Refinement:** Modify existing drafts by making them shorter, formal, friendly, or grammatically correct.
* **Tone Control:** Support for various tones including Professional, Casual, Friendly, and Auto-detect.
* **Fast Processing:** Powered by Groq's high-speed LLM infrastructure.
* **Dynamic UI:** Intuitive layout built with Streamlit.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend/UI:** Streamlit
* **LLM Engine:** Groq API (`groq/compound` model)
* **Environment Management:** `python-dotenv`

---

## 📂 Project Structure

```text
ai_email/
│── app.py             # Main Streamlit application
│── requirements.txt   # Required Python libraries
│── .gitignore         # Ignores .env and virtual environment files
└── README.md          # Project documentation
🔧 Installation & Local Setup
1. Clone the Repository
Bash
git clone [https://github.com/YOUR_USERNAME/ai-email-assistant.git](https://github.com/YOUR_USERNAME/ai-email-assistant.git)
cd ai-email-assistant
2. Create and Activate Virtual Environment
Bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root directory and add your Groq API key:

Code snippet
GROQ_API_KEY=gsk_your_groq_api_key_here
5. Run the Streamlit App
Bash
streamlit run app.py
