import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import tempfile
import json

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
HF_API_KEY = os.getenv("HF_API_KEY")

st.set_page_config(
    page_title="Automotive Concept Visualizer",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0a;
    color: #f0f0f0;
}
.stApp { background-color: #0a0a0a; }
.main-hero {
    text-align: center;
    padding: 3rem 0 1rem 0;
}
.main-title {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #E8401C, #ff6b47);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.main-subtitle {
    font-size: 1.1rem;
    color: #888;
    margin-bottom: 2rem;
}
.config-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.config-title {
    font-size: 1rem;
    font-weight: 600;
    color: #E8401C;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.section-header {
    font-size: 1.2rem;
    font-weight: 600;
    color: #E8401C;
    border-bottom: 1px solid #222;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.description-box {
    background: #141414;
    border: 1px solid #222;
    border-radius: 12px;
    padding: 1.5rem;
    color: #ccc;
    font-size: 0.92rem;
    line-height: 1.8;
}
.spec-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}
.spec-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #1e1e1e;
    font-size: 0.9rem;
    color: #ccc;
}
.spec-table td:first-child {
    color: #888;
    width: 40%;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stars { color: #E8401C; font-size: 1rem; }
.badge {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #aaa;
    margin: 2px;
}
.stButton>button {
    background: linear-gradient(135deg, #E8401C, #c0320f);
    color: white;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.7rem 2rem;
    border: none;
    width: 100%;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #ff5533, #E8401C);
    transform: translateY(-1px);
}
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    color: #888 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
}
.divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-hero">
    <div class="main-title">AUTOMOTIVE CONCEPT AI</div>
    <div class="main-subtitle">Transform your vision into stunning concept designs using Generative AI</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown('<div class="config-card"><div class="config-title">Configure Your Concept</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    body_type = st.selectbox("Body Type", ["Sports Car", "SUV", "Sedan", "Hypercar", "Pickup Truck", "Convertible", "Coupe", "Electric Van"])
    era = st.selectbox("Design Era", ["Futuristic 2050", "Neo-Retro", "Modern 2025", "Cyberpunk", "Classic Revival", "Concept Show Car"])

with col2:
    color_theme = st.selectbox("Color Theme", ["Midnight Black", "Arctic White", "Deep Red", "Electric Blue", "Matte Gray", "Champagne Gold", "Neon Green"])
    fuel_type = st.selectbox("Powertrain", ["Full Electric", "Hydrogen Fuel Cell", "Hybrid", "V8 Petrol", "V12 Supercharged", "Solar Assisted EV"])

with col3:
    mood = st.selectbox("Design Mood", ["Aggressive & Sporty", "Luxury & Elegant", "Rugged & Tough", "Minimalist & Clean", "Futuristic & Bold", "Classic & Timeless"])
    brand_style = st.selectbox("Brand Inspiration", ["Original Design", "German Precision", "Italian Passion", "Japanese Minimalism", "American Muscle", "British Luxury"])

st.markdown('</div>', unsafe_allow_html=True)

extra_prompt = st.text_input("Additional Details (optional)", placeholder="e.g. gull-wing doors, transparent hood, holographic dashboard...")

generate = st.button("Generate Concept")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

def stars(n):
    return "★" * n + "☆" * (5 - n)

def generate_pdf(prompt, description, specs, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 12, "AUTOMOTIVE CONCEPT AI", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Powered by Generative AI", ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(232, 64, 28)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 9, "Concept Configuration", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, prompt)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 9, "AI Description", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    clean = description.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean)
    pdf.ln(4)
    if specs:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(232, 64, 28)
        pdf.cell(0, 9, "Specifications", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        for key, val in specs.items():
            pdf.cell(60, 7, str(key), border=0)
            pdf.cell(0, 7, str(val), border=0, ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(232, 64, 28)
    pdf.cell(0, 9, "Visual Concept", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name)
        pdf.image(tmp.name, x=10, w=190)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf.output(tmp_pdf.name)
        return tmp_pdf.name

if generate:
    full_prompt = f"{body_type} | {era} | {color_theme} | {fuel_type} | {mood} | {brand_style}"
    if extra_prompt:
        full_prompt += f" | Extra: {extra_prompt}"

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<p class="section-header">AI Description</p>', unsafe_allow_html=True)
        with st.spinner("Generating concept..."):
            system_msg = """You are a world-class automotive concept designer and engineer. 
When given a car concept configuration, you must respond ONLY with a valid JSON object in this exact format:
{
  "description": "A detailed 150-200 word description of the car concept covering design language, exterior, interior, and overall feel",
  "performance_rating": <number 1-5>,
  "design_rating": <number 1-5>,
  "tech_rating": <number 1-5>,
  "comfort_rating": <number 1-5>,
  "value_rating": <number 1-5>,
  "top_speed": "e.g. 320 km/h",
  "acceleration": "e.g. 0-100 in 2.8s",
  "range": "e.g. 650 km",
  "power": "e.g. 750 HP",
  "price_estimate": "e.g. $180,000 - $220,000",
  "target_audience": "e.g. Performance enthusiasts aged 30-45"
}
Return ONLY the JSON, no extra text."""

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Design a concept car: {full_prompt}"}
                ],
                temperature=0.8,
                max_tokens=1000
            )

            raw = response.choices[0].message.content.strip()
            try:
                raw = raw[raw.find("{"):raw.rfind("}")+1]
                data = json.loads(raw)
            except:
                data = {"description": raw}

            description = data.get("description", "")
            st.markdown(f'<div class="description-box">{description}</div>', unsafe_allow_html=True)

            st.markdown('<p class="section-header" style="margin-top:1.5rem">Specifications</p>', unsafe_allow_html=True)
            specs = {
                "Top Speed": data.get("top_speed", "N/A"),
                "Acceleration": data.get("acceleration", "N/A"),
                "Range / Tank": data.get("range", "N/A"),
                "Power Output": data.get("power", "N/A"),
                "Estimated Price": data.get("price_estimate", "N/A"),
                "Target Audience": data.get("target_audience", "N/A"),
            }
            rows = "".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in specs.items()])

            ratings = {
                "Performance": data.get("performance_rating", 4),
                "Design": data.get("design_rating", 4),
                "Technology": data.get("tech_rating", 4),
                "Comfort": data.get("comfort_rating", 3),
                "Value": data.get("value_rating", 3),
            }
            rating_rows = "".join([
                f'<tr><td>{k}</td><td><span class="stars">{stars(int(v))}</span></td></tr>'
                for k, v in ratings.items()
            ])

            st.markdown(f"""
            <table class="spec-table">
                {rows}
                <tr><td colspan="2" style="padding-top:12px; color:#E8401C; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.5px;">Ratings</td></tr>
                {rating_rows}
            </table>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            tags = [body_type, era, fuel_type, mood]
            tag_html = "".join([f'<span class="badge">{t}</span>' for t in tags])
            st.markdown(tag_html, unsafe_allow_html=True)

    with col_right:
        st.markdown('<p class="section-header">Visual Concept</p>', unsafe_allow_html=True)
        with st.spinner("Rendering visual..."):
            image_prompt = (
                f"A stunning photorealistic concept car design, {body_type}, {era} design style, "
                f"{color_theme} color, {mood} aesthetic, {brand_style} influence, "
                f"professional automotive photography, studio lighting, clean background, "
                f"ultra detailed, 8k quality, showroom render"
            )
            if extra_prompt:
                image_prompt += f", {extra_prompt}"

            hf_response = requests.post(
                "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={"inputs": image_prompt, "wait_for_model": True}
            )
            if hf_response.status_code == 200:
                generated_image = Image.open(BytesIO(hf_response.content))
                st.image(generated_image, use_container_width=True)
            else:
                st.error(f"Image generation failed: {hf_response.text}")
                generated_image = None

    if description and generated_image:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Export</p>', unsafe_allow_html=True)
        pdf_path = generate_pdf(full_prompt, description, specs, generated_image)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="automotive_concept.pdf",
                mime="application/pdf"
            )