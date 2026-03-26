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
    page_title="Automotive Concept AI",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #080818; color: #f0f0f0; }
.stApp { background-color: #080818; }

.hero {
    width: 100%;
    height: 460px;
    border-radius: 24px;
    overflow: hidden;
    position: relative;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4px;
    margin-bottom: 2rem;
}
.hero-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.55) saturate(1.2);
}
.hero-overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(8,8,24,0.05) 0%, rgba(8,8,24,0.82) 100%);
    z-index: 1;
    border-radius: 24px;
}
.hero-content {
    position: absolute;
    bottom: 0; left: 0;
    width: 100%;
    z-index: 2;
    text-align: center;
    padding: 2rem;
}
.logo {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 6px;
    text-transform: uppercase;
    background: linear-gradient(135deg, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.main-title {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.main-title span {
    background: linear-gradient(135deg, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.main-sub {
    font-size: 0.82rem;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.examples {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 1.5rem;
}
.example {
    font-size: 0.73rem;
    color: #555;
    border: 1px solid #1e1e3a;
    border-radius: 20px;
    padding: 5px 14px;
    background: #0f0f24;
    font-family: 'Inter', sans-serif;
}
.section-header {
    font-size: 0.68rem;
    font-weight: 600;
    background: linear-gradient(135deg, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e3a;
}
.description-box {
    background: #0f0f24;
    border: 1px solid #1e1e3a;
    border-radius: 14px;
    padding: 1.5rem;
    color: #888;
    font-size: 0.9rem;
    line-height: 1.9;
    margin-bottom: 1rem;
}
.description-box ul { padding-left: 1.2rem; margin: 0; }
.description-box ul li { margin-bottom: 0.6rem; color: #999; }
.description-box ul li strong { color: #ccc; }
.spec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 1rem; }
.spec-item { background: #0f0f24; border: 1px solid #1e1e3a; border-radius: 10px; padding: 12px 14px; }
.spec-label { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 1.5px; color: #444; margin-bottom: 4px; }
.spec-value { font-size: 0.92rem; font-weight: 500; color: #ccc; }
.rating-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #0d0d20; }
.rating-label { font-size: 0.72rem; color: #444; text-transform: uppercase; letter-spacing: 1px; }
.stars { background: linear-gradient(135deg, #38bdf8, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 2px; }
.badge { display: inline-block; background: #0f0f24; border: 1px solid #1e1e3a; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; color: #444; margin: 2px; }
.image-frame { border: 1px solid #1e1e3a; border-radius: 16px; overflow: hidden; }
hr { border: none; border-top: 1px solid #1e1e3a; margin: 2rem 0; }

/* Refinement Panel */
.refine-panel {
    background: #0a0a1f;
    border: 1px solid #1e1e3a;
    border-radius: 18px;
    padding: 1.4rem;
    margin-top: 1.2rem;
}
.refine-title {
    font-size: 0.68rem;
    font-weight: 600;
    background: linear-gradient(135deg, #f472b6, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e3a;
}
.refine-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #444;
    margin-bottom: 0.4rem;
    margin-top: 0.8rem;
}
.refine-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 0.5rem;
}
.refine-chip {
    font-size: 0.7rem;
    color: #38bdf8;
    border: 1px solid #1a3a4a;
    border-radius: 20px;
    padding: 4px 12px;
    background: #050d14;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
}

div[data-testid="stTextInput"] > div > div > input {
    background-color: #0f0f24 !important;
}
div[data-testid="stTextInput"] > div > div > div {
    display: none !important;
}
div[data-testid="stTextInput"] > div > div {
    border: none !important;
    box-shadow: none !important;
    border: 1.5px solid #1e1e3a !important;
    border-radius: 50px !important;
    color: #f0f0f0 !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.8rem !important;
    height: 58px !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: #38bdf8 !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #2a2a4a !important;
}
div[data-testid="stTextInput"] label { display: none !important; }
div[data-testid="stTextInput"] small { display: none !important; }
[data-testid="InputInstructions"] { display: none !important; }
.st-emotion-cache-1aq44bt { display: none !important; }
iframe { border: none !important; }
div[class*="InputInstructions"] { display: none !important; }
p[class*="instructions"] { display: none !important; }

.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #f472b6) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.9 !important; }

/* Selectbox and slider dark styling */
div[data-testid="stSelectbox"] > div > div {
    background-color: #0f0f24 !important;
    border: 1px solid #1e1e3a !important;
    color: #ccc !important;
    border-radius: 10px !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(135deg, #38bdf8, #f472b6) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <img class="hero-img" src="https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80"/>
    <img class="hero-img" src="https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&q=80"/>
    <img class="hero-img" src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80"/>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="logo">Automotive Concept AI</div>
        <div class="main-title">Design any car. <span>Instantly.</span></div>
        <div class="main-sub">Describe your dream car and let AI bring it to life</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    prompt = st.text_input("", placeholder="e.g. A futuristic blue hypercar with gull-wing doors...", label_visibility="collapsed")

st.markdown("""
<div class="examples">
    <span class="example">Futuristic hypercar</span>
    <span class="example">Italian sports car</span>
    <span class="example">Cyberpunk SUV</span>
    <span class="example">British luxury sedan</span>
    <span class="example">Japanese coupe</span>
</div>
""", unsafe_allow_html=True)

col_x, col_y, col_z = st.columns([1, 2, 1])
with col_y:
    generate = st.button("Generate Concept")

st.markdown("<hr>", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def stars(n):
    try:
        return "★" * int(n) + "☆" * (5 - int(n))
    except:
        return "★★★★☆"

def clean(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def format_description(text):
    if isinstance(text, list):
        text = "\n".join([str(i) for i in text])
    text = str(text)
    lines = [l.strip() for l in text.replace("**", "").split("\n") if l.strip()]
    items = ""
    for line in lines:
        line = line.lstrip("-•*123456789.").strip()
        if ":" in line:
            parts = line.split(":", 1)
            items += f"<li><strong>{parts[0].strip()}:</strong> {parts[1].strip()}</li>"
        elif line:
            items += f"<li>{line}</li>"
    return f"<ul>{items}</ul>" if items else f"<p>{text}</p>"

def build_image_prompt(base_prompt, color=None, style=None, time_of_day=None, background=None, mood=None, extra=None):
    """Build an enriched image prompt from base + refinement options."""
    parts = [base_prompt]
    if color and color != "Original":
        parts.append(f"{color.lower()} color")
    if style and style != "Original":
        parts.append(style.lower())
    if time_of_day and time_of_day != "Original":
        parts.append(f"{time_of_day.lower()} lighting")
    if background and background != "Original":
        parts.append(f"{background.lower()} background")
    if mood and mood != "Original":
        parts.append(f"{mood.lower()} mood")
    if extra and extra.strip():
        parts.append(extra.strip())
    refined = ", ".join(parts)
    return (
        f"RAW photo, {refined}, "
        f"automotive photography, shot on Canon EOS R5, 85mm lens, "
        f"natural lighting, real car, hyperrealistic, photographic, "
        f"8k uhd, dslr, high quality, film grain, Fujifilm XT3, "
        f"sharp focus, realistic skin texture, no CGI, no illustration"
    )

def call_hf_image(image_prompt):
    """Call HuggingFace SDXL and return PIL Image or None."""
    hf_response = requests.post(
        "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": image_prompt, "wait_for_model": True},
        timeout=120
    )
    if hf_response.status_code == 200:
        try:
            return Image.open(BytesIO(hf_response.content))
        except Exception:
            return None
    return None

def generate_pdf(prompt, description, blueprint, engineering, specs, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 12, "AUTOMOTIVE CONCEPT AI", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "Generative Design Studio", ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(56, 189, 248)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    for section_title, content in [
        ("Concept Prompt", prompt),
        ("Description", description),
        ("Technical Blueprint", blueprint),
        ("Engineering Notes", engineering),
    ]:
        if content:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(56, 189, 248)
            pdf.cell(0, 9, section_title, ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, clean(content))
            pdf.ln(3)
    if specs:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(56, 189, 248)
        pdf.cell(0, 9, "Specifications", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        for k, v in specs.items():
            pdf.cell(70, 7, clean(k))
            pdf.cell(0, 7, clean(v), ln=True)
        pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 9, "Visual Concept", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name)
        pdf.image(tmp.name, x=10, w=190)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf.output(tmp_pdf.name)
        return tmp_pdf.name


# ── Session state init ────────────────────────────────────────────────────────
for key in ["generated_image", "description", "blueprint", "engineering", "specs",
            "base_prompt", "ratings", "show_refine", "current_image_prompt", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "show_refine" not in st.session_state:
    st.session_state.show_refine = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Chat-based prompt refinement via Groq ─────────────────────────────────────
def refine_prompt_via_chat(original_prompt, current_image_prompt, chat_history, user_message):
    """Ask LLaMA to intelligently update the image prompt based on user's chat message."""
    history_text = ""
    if chat_history:
        history_text = "\n".join([
            f"User: {m['user']}\nUpdated prompt: {m['refined_prompt']}"
            for m in chat_history[-5:]  # last 5 turns for context
        ])

    system_msg = """You are an expert automotive image prompt engineer.
You are given:
1. The original car concept from the user
2. The current image generation prompt being used
3. The conversation history of refinements so far
4. A new refinement request from the user

Your job is to return ONLY an updated image generation prompt string — no explanation, no JSON, no markdown, just the raw prompt text.

Rules:
- Always keep: "RAW photo, automotive photography, shot on Canon EOS R5, 85mm lens, natural lighting, real car, hyperrealistic, photographic, 8k uhd, dslr, high quality, film grain, Fujifilm XT3, sharp focus, realistic skin texture, no CGI, no illustration"
- Intelligently apply the user's change (colour, style, mood, setting, details)
- Build on ALL previous refinements, don't reset them
- Keep the core car concept intact"""

    user_content = f"""Original car concept: {original_prompt}

Current image prompt: {current_image_prompt}

Previous refinements:
{history_text if history_text else "None yet"}

New user request: {user_message}

Return ONLY the updated prompt string."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()


# ── Initial Generation ────────────────────────────────────────────────────────
if generate:
    if not prompt:
        st.warning("Please type your car concept in the search bar above!")
    else:
        st.session_state.base_prompt = prompt
        st.session_state.show_refine = False
        st.session_state.chat_history = []
        st.session_state.current_image_prompt = build_image_prompt(prompt)

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_right:
            st.markdown('<div class="section-header">Visual Concept</div>', unsafe_allow_html=True)
            with st.spinner("Rendering visual..."):
                img = call_hf_image(st.session_state.current_image_prompt)
                if img:
                    st.session_state.generated_image = img
                    st.markdown('<div class="image-frame">', unsafe_allow_html=True)
                    st.image(img, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.session_state.show_refine = True
                else:
                    st.error("Image generation failed. Please try again.")

        with col_left:
            st.markdown('<div class="section-header">AI Description</div>', unsafe_allow_html=True)
            with st.spinner("Thinking..."):
                system_msg = """You are the world's most renowned automotive concept designer and chief engineer, combining the vision of Pininfarina, the precision of AMG, and the innovation of Tesla.

When given a car concept, you MUST respond ONLY with a valid JSON object. No extra text, no markdown, no explanation — ONLY JSON.

{
  "description": "Write exactly 6 bullet points, each on a new line starting with '- Label: description'. Labels must be: Design, Exterior, Interior, Performance, Technology, Feel. Each point must be vivid, technical and inspiring — 2 sentences each.",
  "blueprint": "Write exactly 5 bullet points, each on a new line starting with '- Label: description'. Labels must be: Chassis, Suspension, Drivetrain, Aerodynamics, Frame. Be precise with materials and engineering terms.",
  "engineering": "Write exactly 5 bullet points, each on a new line starting with '- Label: description'. Labels must be: Brakes, Steering, Cooling, Tyres, Safety. Include specific technical details.",
  "performance_rating": <integer 1-5>,
  "design_rating": <integer 1-5>,
  "tech_rating": <integer 1-5>,
  "comfort_rating": <integer 1-5>,
  "value_rating": <integer 1-5>,
  "top_speed": "specific value with unit e.g. 342 km/h",
  "acceleration": "specific value e.g. 0-100 in 2.4s",
  "range": "specific value e.g. 720 km",
  "power": "specific value e.g. 850 HP",
  "torque": "specific value e.g. 1,100 Nm",
  "weight": "specific value e.g. 1,680 kg",
  "dimensions": "L x W x H x Wheelbase e.g. 4,920 x 2,080 x 1,280 x 2,950 mm",
  "price_estimate": "specific range e.g. $240,000 - $290,000",
  "target_audience": "specific description e.g. Ultra-high-net-worth performance enthusiasts aged 35-55"
}"""

                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=1500
                )

                raw = response.choices[0].message.content.strip()
                try:
                    raw = raw[raw.find("{"):raw.rfind("}")+1]
                    data = json.loads(raw)
                except:
                    data = {"description": raw}

                st.session_state.description = data.get("description", "")
                st.session_state.blueprint = data.get("blueprint", "")
                st.session_state.engineering = data.get("engineering", "")
                st.session_state.specs = {
                    "Top Speed": data.get("top_speed", "N/A"),
                    "0-100 km/h": data.get("acceleration", "N/A"),
                    "Range": data.get("range", "N/A"),
                    "Power": data.get("power", "N/A"),
                    "Torque": data.get("torque", "N/A"),
                    "Weight": data.get("weight", "N/A"),
                    "Dimensions": data.get("dimensions", "N/A"),
                    "Price": data.get("price_estimate", "N/A"),
                }
                st.session_state.ratings = {
                    "Performance": data.get("performance_rating", 4),
                    "Design": data.get("design_rating", 4),
                    "Technology": data.get("tech_rating", 4),
                    "Comfort": data.get("comfort_rating", 3),
                    "Value": data.get("value_rating", 3),
                }

                st.markdown(f'<div class="description-box">{format_description(st.session_state.description)}</div>', unsafe_allow_html=True)

                st.markdown('<div class="section-header" style="margin-top:1.5rem">Specifications</div>', unsafe_allow_html=True)
                spec_html = "".join([
                    f'<div class="spec-item"><div class="spec-label">{k}</div><div class="spec-value">{v}</div></div>'
                    for k, v in st.session_state.specs.items()
                ])
                st.markdown(f'<div class="spec-grid">{spec_html}</div>', unsafe_allow_html=True)

                st.markdown('<div class="section-header" style="margin-top:1.5rem">Ratings</div>', unsafe_allow_html=True)
                rating_html = "".join([
                    f'<div class="rating-row"><span class="rating-label">{k}</span><span class="stars">{stars(v)}</span></div>'
                    for k, v in st.session_state.ratings.items()
                ])
                st.markdown(f'<div class="description-box" style="padding:0.5rem 1rem">{rating_html}</div>', unsafe_allow_html=True)

                if st.session_state.blueprint:
                    st.markdown('<div class="section-header" style="margin-top:1.5rem">Technical Blueprint</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="description-box">{format_description(st.session_state.blueprint)}</div>', unsafe_allow_html=True)

                if st.session_state.engineering:
                    st.markdown('<div class="section-header" style="margin-top:1.5rem">Engineering Notes</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="description-box">{format_description(st.session_state.engineering)}</div>', unsafe_allow_html=True)

                tags = [prompt[:30]]
                tag_html = "".join([f'<span class="badge">{t}</span>' for t in tags])
                st.markdown(f'<div style="margin-top:1rem">{tag_html}</div>', unsafe_allow_html=True)


# ── Persistent result display (after generation, on re-renders) ───────────────
if st.session_state.generated_image and not generate:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_right:
        st.markdown('<div class="section-header">Visual Concept</div>', unsafe_allow_html=True)
        st.markdown('<div class="image-frame">', unsafe_allow_html=True)
        st.image(st.session_state.generated_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_left:
        if st.session_state.description:
            st.markdown('<div class="section-header">AI Description</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="description-box">{format_description(st.session_state.description)}</div>', unsafe_allow_html=True)
        if st.session_state.specs:
            st.markdown('<div class="section-header" style="margin-top:1.5rem">Specifications</div>', unsafe_allow_html=True)
            spec_html = "".join([
                f'<div class="spec-item"><div class="spec-label">{k}</div><div class="spec-value">{v}</div></div>'
                for k, v in st.session_state.specs.items()
            ])
            st.markdown(f'<div class="spec-grid">{spec_html}</div>', unsafe_allow_html=True)
        if st.session_state.ratings:
            st.markdown('<div class="section-header" style="margin-top:1.5rem">Ratings</div>', unsafe_allow_html=True)
            rating_html = "".join([
                f'<div class="rating-row"><span class="rating-label">{k}</span><span class="stars">{stars(v)}</span></div>'
                for k, v in st.session_state.ratings.items()
            ])
            st.markdown(f'<div class="description-box" style="padding:0.5rem 1rem">{rating_html}</div>', unsafe_allow_html=True)
        if st.session_state.blueprint:
            st.markdown('<div class="section-header" style="margin-top:1.5rem">Technical Blueprint</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="description-box">{format_description(st.session_state.blueprint)}</div>', unsafe_allow_html=True)
        if st.session_state.engineering:
            st.markdown('<div class="section-header" style="margin-top:1.5rem">Engineering Notes</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="description-box">{format_description(st.session_state.engineering)}</div>', unsafe_allow_html=True)


# ── Chat Refinement Window ────────────────────────────────────────────────────
if st.session_state.show_refine and st.session_state.generated_image:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 Refine Your Visual</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#444; font-size:0.8rem; margin-bottom:1rem;">'
        'Chat to update the image — specs stay the same. '
        'Try: <em>"make it more aggressive"</em>, <em>"change to red"</em>, <em>"put it on a racetrack at night"</em>'
        '</p>',
        unsafe_allow_html=True
    )

    chat_col, img_col = st.columns([1, 1], gap="large")

    with chat_col:
        # Display chat history
        if st.session_state.chat_history:
            for turn in st.session_state.chat_history:
                st.markdown(
                    f'<div style="background:#0f0f24; border:1px solid #1e1e3a; border-radius:12px; '
                    f'padding:10px 14px; margin-bottom:8px;">'
                    f'<div style="font-size:0.7rem; color:#38bdf8; text-transform:uppercase; '
                    f'letter-spacing:1px; margin-bottom:4px;">You</div>'
                    f'<div style="color:#ccc; font-size:0.88rem;">{turn["user"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div style="background:#050510; border:1px solid #1a1a30; border-radius:12px; '
                    f'padding:10px 14px; margin-bottom:12px;">'
                    f'<div style="font-size:0.7rem; color:#f472b6; text-transform:uppercase; '
                    f'letter-spacing:1px; margin-bottom:4px;">AI Applied</div>'
                    f'<div style="color:#666; font-size:0.8rem; font-style:italic;">✓ Image updated</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # Chat input
        chat_input = st.text_input(
            "chat",
            placeholder='e.g. "make it black", "add a spoiler", "put it on a mountain road at sunset"',
            label_visibility="collapsed",
            key="chat_input"
        )
        send_btn = st.button("✦ Apply", key="chat_send")

        if send_btn and chat_input and chat_input.strip():
            with st.spinner("Understanding your request..."):
                refined_prompt = refine_prompt_via_chat(
                    st.session_state.base_prompt,
                    st.session_state.current_image_prompt,
                    st.session_state.chat_history,
                    chat_input.strip()
                )
            with img_col:
                st.markdown('<div class="section-header">Updated Visual</div>', unsafe_allow_html=True)
                with st.spinner("Re-rendering..."):
                    new_img = call_hf_image(refined_prompt)
                    if new_img:
                        st.session_state.generated_image = new_img
                        st.session_state.current_image_prompt = refined_prompt
                        st.session_state.chat_history.append({
                            "user": chat_input.strip(),
                            "refined_prompt": refined_prompt
                        })
                        st.markdown('<div class="image-frame">', unsafe_allow_html=True)
                        st.image(new_img, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.success("✓ Image updated — specs unchanged")
                    else:
                        st.error("Refinement failed. Please try again.")
        else:
            with img_col:
                if st.session_state.generated_image:
                    st.markdown('<div class="section-header">Current Visual</div>', unsafe_allow_html=True)
                    st.markdown('<div class="image-frame">', unsafe_allow_html=True)
                    st.image(st.session_state.generated_image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)


# ── PDF Download ──────────────────────────────────────────────────────────────
if st.session_state.description and st.session_state.generated_image:
    st.markdown("<hr>", unsafe_allow_html=True)
    col_x, col_y, col_z = st.columns([1, 2, 1])
    with col_y:
        pdf_path = generate_pdf(
            st.session_state.base_prompt or "",
            st.session_state.description,
            st.session_state.blueprint,
            st.session_state.engineering,
            st.session_state.specs,
            st.session_state.generated_image
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="DOWNLOAD PDF REPORT",
                data=f,
                file_name="automotive_concept.pdf",
                mime="application/pdf"
            )
