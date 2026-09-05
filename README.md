# AI-Email-Generator
# ✉️ AI Email Assistant

An AI-powered email drafting and enhancement web application built with **Streamlit** and **Groq Cloud API**. This application helps users construct fresh emails, modify existing drafts, correct grammar, and adjust tones seamlessly using fast language model inference.

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
