import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import tempfile

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HF_API_KEY = os.getenv("HF_API_KEY")

st.set_page_config(
    page_title="Automotive Concept Visualizer",
    page_icon="",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #E8401C;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #E8401C;
        border-bottom: 2px solid #E8401C;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
    .description-box {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        color: #f0f0f0;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    .stButton>button {
        background-color: #E8401C;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #c0320f;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title"> Automotive Concept Visualizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Transform your car ideas into stunning visuals and detailed descriptions using Generative AI</p>', unsafe_allow_html=True)

st.markdown("---")

col_input, col_btn = st.columns([4, 1])
with col_input:
    prompt = st.text_input("", placeholder="e.g. A futuristic electric sports car with sleek aerodynamic design")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("Generate ")

st.markdown("---")

def generate_pdf(prompt, description, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 15, "Automotive Concept Visualizer", ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Powered by Generative AI", ln=True, align="C")
    pdf.ln(5)
    pdf.set_draw_color(232, 64, 28)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 10, "Concept Prompt", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 7, prompt)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 10, "AI Description", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    clean_description = description.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_description)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 10, "Visual Concept", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name)
        pdf.image(tmp.name, x=10, w=190)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf.output(tmp_pdf.name)
        return tmp_pdf.name

if generate:
    if prompt:
        col1, col2 = st.columns(2)
        description = ""
        generated_image = None

        with col1:
            st.markdown('<p class="section-header">AI Description</p>', unsafe_allow_html=True)
            with st.spinner("Generating description..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert automotive designer. When given a car concept, describe it in detail covering design, performance, features and target audience."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                description = response.choices[0].message.content
                st.markdown(f'<div class="description-box">{description}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<p class="section-header">Visual Concept</p>', unsafe_allow_html=True)
            with st.spinner("Generating image..."):
                image_prompt = f"A highly detailed, photorealistic concept car design: {prompt}, studio lighting, professional automotive photography"
                hf_response = requests.post(
                    "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
                    headers={"Authorization": f"Bearer {HF_API_KEY}"},
                    json={"inputs": image_prompt, "wait_for_model": True}
                )
                if hf_response.status_code == 200:
                    generated_image = Image.open(BytesIO(hf_response.content))
                    st.image(generated_image, caption=prompt, use_container_width=True)
                else:
                    st.error(f"Image generation failed: {hf_response.text}")

        if description and generated_image:
            st.markdown("---")
            st.markdown("### Export your Concept")
            pdf_path = generate_pdf(prompt, description, generated_image)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f,
                    file_name="automotive_concept.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("Please enter a car concept first!")