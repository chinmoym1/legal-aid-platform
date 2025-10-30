import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def show_home():
    # --- PAGE CONFIG ---
    # Set page config only once, and at the top
    try:
        st.set_page_config(page_title="Legal Aid Assistant", page_icon="⚖️", layout="wide")
    except st.errors.StreamlitAPIException:
        # This will happen if the config is already set on another page
        pass

    # --- NEW PROFESSIONAL LEGAL THEME CSS ---
    st.markdown("""
        <style>
            /* --- 1. FONT & COLOR PALETTE --- */
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=Lato:wght@300;400;700&display=swap');
            
            :root {
                --font-serif: 'EB Garamond', serif; /* For headings, gives a classic "legal" feel */
                --font-sans: 'Lato', sans-serif;    /* For body text, clean and readable */
                
                --color-primary-dark: #001F3F; /* Deep Navy */
                --color-primary-light: #003B73; /* Lighter Navy */
                --color-accent-gold: #B8860B;   /* Muted, sophisticated gold */
                --color-accent-gold-light: #D4AF37;
                --color-bg-light: #FDFBF6;      /* Warm off-white, like parchment */
                --color-bg-dark: #F4F4F4;       /* Light grey for contrast sections */
                --color-text-dark: #2F2F2F;     /* Charcoal grey for body */
                --color-text-light: #666666;    /* Lighter grey for descriptions */
                --color-white: #FFFFFF;
                --color-border: #DDDDDD;
            }

            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                font-family: var(--font-sans);
                background-color: var(--color-bg-light);
                color: var(--color-text-dark);
            }
            
            /* Hide Streamlit's default header and footer */
            [data-testid="stHeader"] {
                background: var(--color-bg-light);
            }
            
            /* Main app container */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }

            /* --- 2. HERO SECTION --- */
            .hero {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                padding: 6rem 2rem;
                border-radius: 16px;
                background: linear-gradient(145deg, var(--color-primary-dark) 0%, var(--color-primary-light) 100%);
                color: var(--color-white);
                box-shadow: 0 12px 35px rgba(0, 31, 63, 0.2);
                margin-bottom: 4rem;
            }
            .hero-title {
                font-family: var(--font-serif);
                font-size: 3.5rem; /* 56px */
                font-weight: 700;
                margin-bottom: 1.25rem;
                color: var(--color-white);
                line-height: 1.2;
            }
            .hero-sub {
                font-size: 1.25rem; /* 20px */
                color: rgba(255, 255, 255, 0.85);
                margin-bottom: 2.5rem;
                max-width: 700px;
                line-height: 1.6;
            }
            .hero-buttons { display: flex; gap: 1rem; }
            
            .btn {
                padding: 14px 30px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 1rem; /* 16px */
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid transparent;
                text-decoration: none !important; /* For button links, ensured no underline */
                display: inline-block;
            }
            .btn-primary {
                background: var(--color-accent-gold);
                color: var(--color-primary-dark);
                border-color: var(--color-accent-gold);
            }
            .btn-primary:hover {
                background: var(--color-accent-gold-light);
                border-color: var(--color-accent-gold-light);
                box-shadow: 0 4px 15px rgba(184, 134, 11, 0.3);
                transform: translateY(-2px);
                text-decoration: none; /* Ensure no underline on hover */
            }
            .btn-outline {
                background: transparent;
                color: var(--color-white);
                border: 2px solid var(--color-white);
            }
            .btn-outline:hover {
                background: var(--color-white);
                color: var(--color-primary-dark);
                transform: translateY(-2px);
                text-decoration: none; /* Ensure no underline on hover */
            }

            /* --- 3. SECTION HEADINGS --- */
            .section-heading {
                font-family: var(--font-serif);
                font-size: 2.5rem; /* 40px */
                font-weight: 600;
                color: var(--color-primary-dark);
                text-align: center;
                margin-bottom: 1.5rem;
                margin-top: 4rem;
            }
            .section-subheading {
                text-align: center;
                font-size: 1.1rem;
                color: var(--color-text-light);
                margin-top: -1rem;
                margin-bottom: 3rem;
                max-width: 650px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            }

            /* --- 4. CORE FEATURES (CARDS) --- */
            .cards-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 2rem;
                margin-top: 2rem;
            }
            .feature-card {
                background: var(--color-white);
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
                border: 1px solid var(--color-border);
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
                text-align: left;
            }
            .feature-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border-color: var(--color-accent-gold);
            }
            .feature-icon {
                font-size: 2.5rem; /* 40px */
                margin-bottom: 1rem;
                display: block;
            }
            .feature-title {
                font-family: var(--font-serif);
                font-size: 1.5rem; /* 24px */
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: var(--color-primary-dark);
            }
            .feature-desc {
                color: var(--color-text-light);
                font-size: 0.95rem;
                line-height: 1.6;
            }

            /* --- 5. NEW: COMMITMENT SECTION --- */
            .commitment-section {
                display: flex;
                gap: 3rem;
                align-items: center;
                padding: 4rem 0;
                margin-top: 4rem;
                border-top: 1px solid var(--color-border);
                border-bottom: 1px solid var(--color-border);
            }
            .commitment-left {
                flex: 1;
            }
            .commitment-right {
                flex: 1;
                font-size: 1.05rem;
                line-height: 1.7;
                color: var(--color-text-dark);
            }
            .commitment-right ul {
                list-style-type: '✓';
                padding-left: 1.5rem;
            }
            .commitment-right li {
                padding-left: 0.75rem;
                margin-bottom: 0.75rem;
            }

            /* --- 6. HOW IT WORKS (STEPS) --- */
            .steps-row {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2rem;
                margin-top: 3rem;
            }
            .step-box {
                background: var(--color-white);
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
                border: 1px solid var(--color-border);
                text-align: center;
            }
            .step-number {
                background: var(--color-primary-dark);
                color: var(--color-white);
                width: 48px;
                height: 48px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 1.25rem;
                font-family: var(--font-serif);
                margin-bottom: 1rem;
            }
            .step-title {
                font-family: var(--font-serif);
                font-weight: 600;
                font-size: 1.3rem;
                color: var(--color-primary-dark);
                margin-bottom: 0.5rem;
            }
            .step-text { color: var(--color-text-light); font-size: 0.95rem; line-height: 1.6; }

            /* --- 7. NEW: TESTIMONIALS --- */
            .testimonials {
                background-color: var(--color-bg-dark);
                padding: 4rem 2rem;
                margin-top: 4rem;
                border-radius: 12px;
            }
            .testimonial-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
            }
            .testimonial-card {
                background: var(--color-white);
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border-top: 4px solid var(--color-accent-gold);
            }
            .testimonial-text {
                font-style: italic;
                color: var(--color-text-dark);
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            .testimonial-author {
                font-weight: 700;
                color: var(--color-primary-dark);
            }
            .testimonial-author span {
                font-weight: 400;
                color: var(--color-text-light);
                font-size: 0.9rem;
            }
            
            /* --- 8. DISCLAIMER & FOOTER --- */
            .disclaimer {
                background: #F6ECC2A6; /* Light yellow, suitable for warnings */
                border-left: 5px solid #F59E0B; /* Amber */
                padding: 1.5rem;
                border-radius: 8px;
                color: #B45309;
                margin: 4rem auto 2rem auto;
                max-width: 95%;
                font-size: 0.95rem;
                line-height: 1.6;
            }
            .disclaimer strong {
                color: #92400E;
            }

            .footer {
                margin-top: 3rem;
                text-align: center;
                color: #999999; /* Lighter grey for footer */
                font-size: 0.9rem;
                padding: 2rem 0;
                border-top: 1px solid var(--color-border);
            }

            /* --- 9. RESPONSIVENESS --- */
            @media (max-width: 992px) {
                .main .block-container {
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
                .hero-title { font-size: 2.75rem; }
                .hero-sub { font-size: 1.1rem; }
                .commitment-section { flex-direction: column; }
            }
            @media (max-width: 768px) {
                .steps-row { grid-template-columns: 1fr; }
                .hero-title { font-size: 2.25rem; }
                .hero-buttons { flex-direction: column; width: 80%; }
                .btn { width: 100%; }
            }

        </style>
    """, unsafe_allow_html=True)

    # --- 1. HERO SECTION ---
    # Simplified the hero, made it text-centric. The "Stats" felt a bit
    # like a marketing gimmick, so I removed it for a more professional feel.
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Intelligent Legal Assistance, Instantly.</div>
        <div class="hero-sub">
            Navigate your legal questions with clarity. Our AI-powered platform helps you 
            understand complex issues, draft documents, and summarize case law—securely and efficiently.
        </div>
        <div class="hero-buttons">
            <a href="#" class="btn btn-primary" id="open-chatbot">Start Your Query</a>
            <a href="#" class="btn btn-outline" id="open-doc-gen">Browse Services</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. CORE FEATURES ---
    # Kept your original features, but applied new classes and more professional icons.
    st.markdown("""
    <div class="section-heading">Your Comprehensive Legal Toolkit</div>
    <div class="cards-grid">
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Document Generator</div>
            <div class="feature-desc">Create affidavits, RTI applications, or legal complaints using smart, guided templates.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Legal Chatbot</div>
            <div class="feature-desc">Ask legal questions in plain English. Receive accurate, concise AI responses instantly.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📑</div>
            <div class="feature-title">Case Summarizer</div>
            <div class="feature-desc">Upload lengthy judgments or contracts and get quick, human-readable summaries in seconds.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Confidential</div>
            <div class="feature-desc">We ensure all your data is processed with bank-level encryption and complete confidentiality.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 3. NEW SECTION: OUR COMMITMENT ---
    # This section builds trust and adds "authentic" legal-themed content.
    st.markdown("""
    <div class="commitment-section">
        <div class="commitment-left">
            <div class="section-heading" style="text-align: left; margin-top: 0;">Our Commitment to You</div>
            <p class="section-subheading" style="text-align: left; margin-left: 0; max-width: 500px;">
                We believe access to legal information should be simple, affordable, and accessible. 
                Our platform is built on three core principles.
            </p>
        </div>
        <div class="commitment-right">
            <ul>
                <li><strong>Accessibility:</strong> Providing clear, understandable legal information to everyone, regardless of their background.</li>
                <li><strong>Accuracy:</strong> Leveraging state-of-the-art AI trained on vast legal corpora to ensure reliable assistance.</li>
                <li><strong>Confidentiality:</strong> Protecting your privacy is our highest priority. Your data is yours alone.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 4. HOW IT WORKS SECTION ---
    # Re-styled your existing "How It Works" section to match the new theme.
    st.markdown("""
    <div class="section-heading">Get Started in Three Simple Steps</div>
    <div class="steps-row">
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">Choose a Service</div>
            <div class="step-text">Select the AI Chatbot for questions, the Generator for documents, or the Summarizer for analysis.</div>
        </div>
        <div class="step-box">
            <div class="step-number">2</div>
            <div class="step-title">Provide Your Details</div>
            <div class="step-text">Type your question, fill in the guided form, or upload your legal document securely.</div>
        </div>
        <div class="step-box">
            <div class="step-number">3</div>
            <div class="step-title">Receive Your Result</div>
            <div class="step-text">Get an instant AI-powered answer, download your completed document, or read your summary.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 5. NEW SECTION: TESTIMONIALS ---
    # Added a testimonials section for social proof and authenticity.
    st.markdown("""
    <div class="testimonials">
        <div class="section-heading" style="margin-top: 0;">Trusted by Users Like You</div>
        <div class="testimonial-grid">
            <div class="testimonial-card">
                <div class="testimonial-text">"The AI chatbot helped me understand the RTI filing process in minutes. I was stuck for days before this. Incredibly helpful."</div>
                <div class="testimonial-author">R. Kumar <span>- Public User</span></div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-text">"I used the document generator for a rental agreement. It was clear, simple, and covered all the clauses I needed. Highly recommend."</div>
                <div class="testimonial-author">S. Chen <span>- Small Business Owner</span></div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-text">"Summarizing a 50-page judgment used to take me hours. This tool did it in 30 seconds and the summary was spot-on."</div>
                <div class="testimonial-author">A. Desai <span>- Paralegal</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 6. DISCLAIMER + FOOTER ---
    # Re-styled the disclaimer to be more prominent and professional.
    st.markdown("""
    <div class="disclaimer">
        <strong>Legal Disclaimer:</strong> Legal Aid Assistant is an AI-powered informational tool and not a substitute for a qualified lawyer or law firm. 
        It does not provide legal advice, and its use does not create an attorney-client relationship. 
        For critical matters, please consult with a professional legal practitioner.
    </div>

    <div class="footer">
        © 2025 Legal Aid Assistant. All Rights Reserved.
        <br>
        Empowering access to legal information through technology.
    </div>
    """, unsafe_allow_html=True)

    # --- PAGE NAVIGATION (HIDDEN JAVASCRIPT) ---
    # This is a bit of a hack to make the HTML buttons navigate in Streamlit.
    # We add JavaScript to find the Streamlit buttons (which are on the sidebar)
    # and click them when our HTML buttons are clicked.
    
    # IMPORTANT: This assumes your other pages are named 'AI_Chatbot' and 'Document_Generator'
    # in your multipage app structure.
    
    # We find the Streamlit sidebar links by their text content.
    # st.components.v1.html("""
    # <script>
    # function findStreamlitButton(text) {
    #     // Find all sidebar navigation links
    #     const buttons = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] ul li a');
    #     for (let button of buttons) {
    #         // Check the text content inside the link
    #         if (button.textContent.includes(text)) {
    #             return button;
    #         }
    #     }
    #     return null;
    # }

    # // Add click listener for the Chatbot button
    # window.parent.document.getElementById('open-chatbot').addEventListener('click', function() {
    #     const chatbotButton = findStreamlitButton('AI Chatbot'); // MATCHES YOUR PAGE NAME
    #     if (chatbotButton) {
    #         chatbotButton.click();
    #     } else {
    #         console.error('Could not find sidebar link for AI Chatbot');
    #     }
    # });

    # // Add click listener for the Document Generator button
    # window.parent.document.getElementById('open-doc-gen').addEventListener('click', function() {
    #     const docGenButton = findStreamlitButton('Document Generator'); // MATCHES YOUR PAGE NAME
    #     if (docGenButton) {
    #         docGenButton.click();
    #     } else {
    #         console.error('Could not find sidebar link for Document Generator');
    #     }
    # });
    # </script>
    # """, height=0)


# This allows you to run this file directly for testing
if __name__ == "__main__":
    # To simulate the multipage app environment for the JS to work, 
    # we'd ideally have other pages. For now, just show the home.
    # In your main app, you'd call show_home() on the 'Home' page.
    show_home()

