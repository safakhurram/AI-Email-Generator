import os
import re
import json
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from dotenv import load_dotenv

# --------------------------------------------------
# ENVIRONMENT CONFIGURATION
# --------------------------------------------------
load_dotenv(override=True)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Email Generator | Write Better Emails in Seconds",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""
if "generation_metadata" not in st.session_state:
    st.session_state.generation_metadata = {}

# Retrieve API key from environment variable (never hardcode)
api_key = os.environ.get("GROQ_API_KEY", "").strip()
if not api_key and "session_api_key" in st.session_state:
    api_key = st.session_state.session_api_key

# --------------------------------------------------
# MODERN SAAS DESIGN SYSTEM (CSS)
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Clean Streamlit Defaults */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    div[data-testid="stToolbar"] { display: none; }
    div[data-testid="stDecoration"] { display: none; }

    /* Page Container */
    .block-container {
        max-width: 1180px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Top Navigation Header */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 14px 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-logo-badge {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: white;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
    }
    .brand-title {
        font-size: 19px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.015em;
        line-height: 1.2;
    }
    .brand-tagline {
        font-size: 12px;
        font-weight: 500;
        color: #64748b;
    }
    .nav-badge {
        background: #eef2ff;
        color: #4f46e5;
        border: 1px solid #c7d2fe;
        font-size: 12px;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px 16px 8px 16px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f1f5f9;
        color: #4338ca;
        border: 1px solid #e0e7ff;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0f172a;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 16.5px;
        color: #475569;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.55;
        font-weight: 400;
    }

    /* SaaS Cards */
    .saas-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 24px 26px;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04), 0 4px 16px -4px rgba(15, 23, 42, 0.03);
        height: 100%;
        margin-bottom: 20px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .saas-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.06);
    }
    .card-header-box {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    .card-header-icon {
        width: 36px;
        height: 36px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .card-header-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .card-header-desc {
        font-size: 12px;
        color: #64748b;
        margin-top: 2px;
    }

    /* Form Inputs */
    label, div[data-testid="stWidgetLabel"] p {
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #334155 !important;
        margin-bottom: 4px !important;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        font-size: 14px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        font-size: 14.5px !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    /* Large Premium Generate Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        height: 52px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.38) !important;
        filter: brightness(1.04) !important;
    }

    /* Download & Action Buttons */
    div.stDownloadButton > button {
        background: #ffffff !important;
        color: #4f46e5 !important;
        border: 1px solid #c7d2fe !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 44px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.15s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: #f5f3ff !important;
        border-color: #818cf8 !important;
        color: #3730a3 !important;
    }

    /* Email Preview Card */
    .email-preview-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08);
        overflow: hidden;
        margin-top: 24px;
        margin-bottom: 20px;
    }
    .email-preview-topbar {
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .window-dots {
        display: flex;
        gap: 6px;
    }
    .dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
    }
    .dot-red { background: #ef4444; }
    .dot-yellow { background: #f59e0b; }
    .dot-green { background: #10b981; }

    .preview-client-label {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .preview-status-pill {
        background: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
    }

    /* Email Meta Rows */
    .email-meta-container {
        padding: 18px 24px 14px 24px;
        background: #ffffff;
        border-bottom: 1px solid #f1f5f9;
    }
    .meta-row {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .meta-label {
        font-weight: 600;
        color: #64748b;
        min-width: 65px;
    }
    .meta-val-subject {
        font-weight: 700;
        color: #0f172a;
        font-size: 16px;
    }
    .meta-pill {
        display: inline-flex;
        align-items: center;
        background: #f1f5f9;
        color: #334155;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 13px;
        font-weight: 500;
    }
    .meta-pill-tone {
        background: #ede9fe;
        color: #6d28d9;
        font-weight: 600;
    }

    /* Email Body */
    .email-body-content {
        padding: 24px 28px;
        font-size: 15px;
        line-height: 1.7;
        color: #1e293b;
        white-space: pre-wrap;
        background: #ffffff;
        min-height: 200px;
    }

    /* Footer */
    .saas-footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
        margin-top: 40px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
    }

    /* Configuration Banner */
    .config-banner {
        background: #fefce8;
        border: 1px solid #fef08a;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TOP NAVIGATION HEADER
# --------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="brand-group">
        <div class="brand-logo-badge">✉️</div>
        <div>
            <div class="brand-title">AI Email Generator</div>
            <div class="brand-tagline">Smart AI Writing Assistant for Fast, Professional Emails</div>
        </div>
    </div>
    <div class="nav-badge">
        <span>⚡</span>
        <span>Groq • openai/gpt-oss-20b</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span>✨</span> Next-Gen AI Email Suite
    </div>
    <div class="hero-title">
        Write better emails in seconds.
    </div>
    <div class="hero-subtitle">
        Turn bullet points or rough drafts into compelling, clear, and perfectly toned emails tailored for any recipient.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# API KEY VALIDATION & SAAS CONFIGURATION
# --------------------------------------------------
if not api_key:
    with st.container():
        st.markdown("""
        <div class="config-banner">
            <div style="font-weight: 700; color: #854d0e; font-size: 14.5px; margin-bottom: 4px;">
                🔑 Groq API Key Setup
            </div>
            <div style="font-size: 13.5px; color: #713f12; line-height: 1.5;">
                We could not detect a <code>GROQ_API_KEY</code> in your environment or <code>.env</code> file. 
                You can enter your API key below for this session:
            </div>
        </div>
        """, unsafe_allow_html=True)
        session_key_input = st.text_input(
            "Enter Groq API Key (starts with gsk_)",
            type="password",
            placeholder="gsk_...",
            help="Your key is stored safely in memory for this session."
        )
        if session_key_input.strip():
            st.session_state.session_api_key = session_key_input.strip()
            st.rerun()


# --------------------------------------------------
# MAIN WORKSPACE: TWO-COLUMN LAYOUT
# --------------------------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

# LEFT COLUMN: EMAIL DETAILS
with col_left:
    st.markdown("""
    <div class="saas-card">
        <div class="card-header-box">
            <div class="card-header-icon">⚙️</div>
            <div>
                <h3 class="card-header-title">Email Details</h3>
                <div class="card-header-desc">Set your goal, recipient, context, and tone</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    action = st.selectbox(
        "What do you want to do?",
        [
            "Create Email",
            "Improve Email",
            "Correct Grammar",
            "Make Formal",
            "Make Friendly",
            "Make Shorter"
        ],
        help="Select the AI writing action to apply."
    )

    recipient = st.text_input(
        "👤 Recipient Name",
        placeholder="e.g. Miss Ahmed / Dr. Sarah Jenkins",
        help="The person or team who will receive the email."
    )

    sender = st.text_input(
        "✍️ Your Name",
        placeholder="e.g. Safa / Alex Morgan",
        help="Your name as it should appear in the closing."
    )

    event = st.text_input(
        "📌 Event / Context",
        placeholder="e.g. Assignment extension request",
        help="The primary topic or context for this email."
    )

    tone = st.selectbox(
        "🎨 Email Tone",
        [
            "Auto",
            "Professional",
            "Friendly",
            "Casual"
        ],
        help="Desired tone for the email communication."
    )

    extra_info = st.text_input(
        "📚 Additional Information",
        placeholder="e.g. CS-261, Section B, deadline Monday",
        help="Any specifics, requirements, or constraints."
    )

    st.markdown("</div>", unsafe_allow_html=True)


# RIGHT COLUMN: YOUR MESSAGE
with col_right:
    st.markdown("""
    <div class="saas-card">
        <div class="card-header-box">
            <div class="card-header-icon">📝</div>
            <div>
                <h3 class="card-header-title">Your Message</h3>
                <div class="card-header-desc">Provide raw talking points or draft email content</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if action == "Create Email":
        content = st.text_area(
            "What should the email say?",
            placeholder=(
                "Example:\n"
                "Ask my teacher for an extension because I need "
                "more time to complete the assignment.\n"
                "- Mention I finished parts 1 and 2\n"
                "- Request until Wednesday evening"
            ),
            height=300,
            help="Describe key points or talking points."
        )
    else:
        content = st.text_area(
            "Paste your existing email",
            placeholder="Paste your email here to refine, shorten, or format...",
            height=300,
            help="Paste the email you'd like AI to improve."
        )

    st.markdown("""
        <div style="font-size: 12px; color: #64748b; margin-top: 8px; display: flex; align-items: center; gap: 6px;">
            <span>💡</span> <span>Tip: Specific context and tone choices yield the most accurate results.</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
generate = st.button(
    "✨ Generate Email",
    use_container_width=True
)

if generate:
    active_key = api_key or os.environ.get("GROQ_API_KEY", "").strip()

    if not active_key:
        st.error("❌ Groq API key was not found. Please provide your API key in the configuration section above or set the `GROQ_API_KEY` environment variable.")
    elif not content.strip():
        st.warning("⚠️ Please enter some information in the 'Your Message' field first.")
    else:
        # Exact prompt structure preserved
        prompt = f"""
You are an expert AI Email Writing Assistant.

Action:
{action}

Recipient:
{recipient}

Sender:
{sender}

Event / Context:
{event}

Tone:
{tone}

User Content:
{content}

Additional Information:
{extra_info}

Instructions:

- Follow the selected action exactly.
- Correct grammar and spelling.
- Improve clarity and sentence structure.
- Keep the original meaning when modifying an email.
- Make the email natural and human-like.
- If tone is Auto, choose the most appropriate tone based on the context.
- Professional means respectful and formal.
- Friendly means warm and polite.
- Casual means relaxed and natural.
- Include the recipient name if provided.
- Include useful class, section, deadline or event information.
- Include the sender name in the closing if provided.
- For Make Shorter, remove unnecessary words.
- For Make Formal, make the email professional.
- For Make Friendly, make the email warm and polite.
- For Correct Grammar, focus mainly on grammar and spelling.
- For Improve Email, improve clarity, grammar and structure.
- Return ONLY the finished email.
- Do not explain what you changed.
- Include a suitable subject.

Use this format:

Subject: <subject>

<email body>

<closing>,
{sender}
"""

        try:
            client = Groq(api_key=active_key)
            with st.spinner("✨ Creating your email with Groq..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert email writing assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5
                )

                generated_text = response.choices[0].message.content.strip()
                st.session_state.generated_email = generated_text
                st.session_state.generation_metadata = {
                    "action": action,
                    "recipient": recipient if recipient else "Not specified",
                    "sender": sender if sender else "You",
                    "tone": tone
                }

        except Exception as e:
            error_msg = str(e)
            if "invalid_api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                st.error("❌ Authentication Error: The provided Groq API key is invalid. Please check your key and try again.")
            else:
                st.error(f"❌ Something went wrong while generating the email:\n\n{error_msg}")


# --------------------------------------------------
# RESULT SECTION: EMAIL PREVIEW CARD
# --------------------------------------------------
if st.session_state.generated_email:
    email_text = st.session_state.generated_email
    meta = st.session_state.generation_metadata

    # Parse Subject line and Body
    subject_match = re.search(r"^Subject:\s*(.+)$", email_text, flags=re.MULTILINE | re.IGNORECASE)
    if subject_match:
        extracted_subject = subject_match.group(1).strip()
        body_display = re.sub(r"^Subject:\s*.+\n*", "", email_text, count=1, flags=re.MULTILINE | re.IGNORECASE).strip()
    else:
        extracted_subject = f"Email re: {meta.get('action', 'Generated Email')}"
        body_display = email_text

    st.markdown("""
        <div style="margin-top: 36px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em;">
                    Your AI-Generated Email
                </h2>
                <div style="font-size: 14px; color: #64748b; margin-top: 2px;">
                    Review your ready-to-send email below or copy and download it directly.
                </div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="nav-badge" style="background: #f0fdf4; color: #166534; border-color: #bbf7d0;">
                    ✓ Ready to Send
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Authentic Email Preview Card
    st.markdown(f"""
    <div class="email-preview-card">
        <div class="email-preview-topbar">
            <div class="window-dots">
                <div class="dot dot-red"></div>
                <div class="dot dot-yellow"></div>
                <div class="dot dot-green"></div>
            </div>
            <div class="preview-client-label">
                <span>📬</span> Email Client Preview
            </div>
            <div class="preview-status-pill">
                AI Formatted
            </div>
        </div>
        <div class="email-meta-container">
            <div class="meta-row">
                <span class="meta-label">Subject:</span>
                <span class="meta-val-subject">{extracted_subject}</span>
            </div>
            <div class="meta-row" style="margin-bottom: 0;">
                <span class="meta-label">Details:</span>
                <span class="meta-pill">To: {meta.get('recipient', 'Recipient')}</span>
                <span class="meta-pill">From: {meta.get('sender', 'Sender')}</span>
                <span class="meta-pill meta-pill-tone">Tone: {meta.get('tone', 'Auto')}</span>
            </div>
        </div>
        <div class="email-body-content">{body_display}</div>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar: Download & Copy
    btn_col1, btn_col2 = st.columns([1, 1], gap="medium")

    with btn_col1:
        st.download_button(
            label="📥 Download Email (.txt)",
            data=email_text,
            file_name="generated_email.txt",
            mime="text/plain",
            use_container_width=True
        )

    with btn_col2:
        if st.button("📋 Copy Email to Clipboard", use_container_width=True):
            st.toast("✅ Email copied to clipboard!")
            components.html(
                f"""
                <script>
                navigator.clipboard.writeText({json.dumps(email_text)});
                </script>
                """,
                height=0,
                width=0
            )

    # Accessible Raw/Editable View
    with st.expander("✏️ View / Edit Raw Text", expanded=False):
        st.text_area(
            "Full email text with subject",
            value=email_text,
            height=250,
            help="You can copy or make quick manual edits here."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="saas-footer">
    ✉️ AI Email Generator • Powered by Groq
</div>
""", unsafe_allow_html=True)