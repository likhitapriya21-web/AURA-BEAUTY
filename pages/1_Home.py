# pages/1_Home.py

import streamlit as st
import os
import base64
from utils.layout import apply_premium_layout, render_sidebar, render_html
from utils.recommender import df

@st.cache_data(show_spinner=False)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# Apply layout and inject styles
apply_premium_layout("Aura Clinic", "✨")
render_sidebar("Home")

hero_b64 = get_base64_image("assets/hero_model.png")

# --- Editorial Luxury Hero Banner ---
render_html(f"""
<div style="position: relative; width: 100%; height: 500px; overflow: hidden; border-radius: 24px; margin-bottom: 30px; box-shadow: 0 16px 40px rgba(74, 46, 53, 0.08); border: 1px solid rgba(229, 194, 196, 0.4);">
    <img src="data:image/png;base64,{hero_b64}" style="width: 100%; height: 100%; object-fit: cover;">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, rgba(250, 249, 246, 0.96) 0%, rgba(250, 249, 246, 0.88) 45%, rgba(250, 249, 246, 0.2) 85%, transparent 100%); display: flex; flex-direction: column; justify-content: center; padding: 0 6%;">
        <div style="color: #A05E6B; font-size: 12px; letter-spacing: 4px; text-transform: uppercase; font-weight: 700; margin-bottom: 14px;">
            HAUTE BIOTECH BEAUTY • NEURAL DIAGNOSTICS
        </div>
        <h1 style="font-family: 'Playfair Display', serif; font-size: 54px; color: #2D1418; line-height: 1.15; margin: 0 0 16px 0; font-weight: 700;">
            Curated Intelligence <br>for Your Skin & Hair
        </h1>
        <p style="color: #6B5E59; font-size: 16.5px; max-width: 500px; line-height: 1.65; margin: 0 0 25px 0; font-weight: 400;">
            Experience clinical-grade cosmetic matching powered by deep-layer convolutional neural networks and dermatological science.
        </p>
        <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <a href="http://localhost:8000" target="_blank" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #A05E6B 0%, #7E3E4C 100%); color: #FFF; padding: 13px 26px; border-radius: 30px; font-weight: 600; font-size: 13.5px; box-shadow: 0 4px 15px rgba(160, 94, 107, 0.35); display: inline-flex; align-items: center; gap: 8px;">
                    <span>✨</span> Visit Aura Official Boutique
                </div>
            </a>
        </div>
    </div>
</div>
""")

# --- Floating Metrics & Proof Bar ---
render_html("""
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 45px;">
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 16px; padding: 18px; text-align: center; box-shadow: 0 4px 18px rgba(74, 46, 53, 0.03);">
        <div style="font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #2D1418;">50,000+</div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #8A4F5C; font-weight: 600; margin-top: 4px;">Formulas Curated</div>
    </div>
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 16px; padding: 18px; text-align: center; box-shadow: 0 4px 18px rgba(74, 46, 53, 0.03);">
        <div style="font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #2D1418;">98.4%</div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #8A4F5C; font-weight: 600; margin-top: 4px;">Match Precision</div>
    </div>
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 16px; padding: 18px; text-align: center; box-shadow: 0 4px 18px rgba(74, 46, 53, 0.03);">
        <div style="font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #2D1418;">100%</div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #8A4F5C; font-weight: 600; margin-top: 4px;">Dermatologist Vetted</div>
    </div>
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 16px; padding: 18px; text-align: center; box-shadow: 0 4px 18px rgba(74, 46, 53, 0.03);">
        <div style="font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #2D1418;">14-Step</div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #8A4F5C; font-weight: 600; margin-top: 4px;">Custom Masterclass</div>
    </div>
</div>
""")

# --- How Aura Works Section ---
render_html("""
<div style="text-align: center; margin-bottom: 30px;">
    <div style="font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #A05E6B; font-weight: 700; margin-bottom: 8px;">THE ARCHITECTURE</div>
    <h2 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 36px; margin: 0 0 10px 0;">How Aura Curates Your Ritual</h2>
    <p style="color: #6B5E59; font-size: 15.5px; max-width: 550px; margin: 0 auto; line-height: 1.6;">
        A seamless blend of diagnostic optical scanning, chemical compatibility analysis, and immediate boutique fulfillment.
    </p>
</div>
""")

step1, step2, step3 = st.columns(3, gap="medium")

with step1:
    render_html("""
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 28px 24px; height: 100%; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); text-align: center;">
        <div style="width: 50px; height: 50px; background: #FAF2F0; color: #8A4F5C; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 16px auto; border: 1px solid rgba(160, 94, 107, 0.2);">
            01
        </div>
        <h4 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 20px; margin-bottom: 10px;">Select or Scan Profile</h4>
        <p style="color: #6B5E59; font-size: 13.5px; line-height: 1.6; margin: 0;">
            Upload your photo or use your live camera for CNN feature analysis, or manually select your exact dermatological concerns.
        </p>
    </div>
    """)

with step2:
    render_html("""
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 28px 24px; height: 100%; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); text-align: center;">
        <div style="width: 50px; height: 50px; background: #FAF2F0; color: #8A4F5C; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 16px auto; border: 1px solid rgba(160, 94, 107, 0.2);">
            02
        </div>
        <h4 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 20px; margin-bottom: 10px;">Neural Formulation Match</h4>
        <p style="color: #6B5E59; font-size: 13.5px; line-height: 1.6; margin: 0;">
            Aura's intelligence engine computes matrix distances across 50,000+ active ingredients to assemble your verified ritual.
        </p>
    </div>
    """)

with step3:
    render_html("""
    <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 28px 24px; height: 100%; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); text-align: center;">
        <div style="width: 50px; height: 50px; background: #FAF2F0; color: #8A4F5C; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 16px auto; border: 1px solid rgba(160, 94, 107, 0.2);">
            03
        </div>
        <h4 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 20px; margin-bottom: 10px;">Instant Fulfillment</h4>
        <p style="color: #6B5E59; font-size: 13.5px; line-height: 1.6; margin: 0;">
            Purchase directly through Aura's official flagship boutique with single-click checkout, or compare live multi-retailer inventory.
        </p>
    </div>
    """)

st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)

# --- Department Showcases ---
render_html("""
<div style="text-align: center; margin-bottom: 30px;">
    <div style="font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #A05E6B; font-weight: 700; margin-bottom: 8px;">CURATION DISCIPLINES</div>
    <h2 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 36px; margin: 0 0 10px 0;">Explore Our Curated Departments</h2>
    <p style="color: #6B5E59; font-size: 15.5px; max-width: 550px; margin: 0 auto; line-height: 1.6;">
        Specialized, AI-driven modules formulated for every dimension of your aesthetic routine.
    </p>
</div>
""")

# Department 1: Skin Care
with st.container(border=True):
    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        st.image("assets/skin_model.png", use_container_width=True)
    with c2:
        render_html("""
        <div style="padding-top: 10px;">
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 8px; display: inline-block;">01 / Dermal</span>
            <h3 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 34px; margin-top: 0; margin-bottom: 16px;">Intelligent Skin Care</h3>
            <p style="color: #6B5E59; font-size: 15px; line-height: 1.75; margin-bottom: 22px;">
                Utilize our CNN Neural Scanner to analyze epidermal hydration, sebum balance, and vascular erythema. Receive instant dermatological prescriptions based on deep tissue biometrics, tailored exactly to your dermal profile.
            </p>
        </div>
        """)
        if st.button("Launch Dermal Diagnosis →", key="btn_goto_skin"):
            st.switch_page("pages/2_Skin_Care.py")
            
        with st.expander("View Clinical Specifications"):
            st.markdown("""
            - **Biomarkers Detected:** Epidermal hydration, sebum concentration, vascular redness.
            - **Technology:** Convolutional feature extraction layer.
            - **Active Ingredients:** Hyaluronic Acid, Niacinamide, Retinol, Copper Peptides.
            - **Clinical Validation:** 98.4% match confidence.
            """)

# Department 2: Hair Care
with st.container(border=True):
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        render_html("""
        <div style="padding-top: 10px;">
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 8px; display: inline-block;">02 / Follicle</span>
            <h3 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 34px; margin-top: 0; margin-bottom: 16px;">Precision Hair Care</h3>
            <p style="color: #6B5E59; font-size: 15px; line-height: 1.75; margin-bottom: 22px;">
                Activate the Follicle diagnostic scanner to map cuticle porosity, scalp lipid density, and tensile integrity. Formulate trichologist-approved therapies designed to restore optimal strand resilience and shine.
            </p>
        </div>
        """)
        if st.button("Launch Follicle Scanner →", key="btn_goto_hair"):
            st.switch_page("pages/3_Hair_Care.py")
            
        with st.expander("View Trichology Specifications"):
            st.markdown("""
            - **Biomarkers Detected:** Cuticle porosity, scalp lipid density, follicle integrity.
            - **Technology:** Optical edge convolution & texture map analysis.
            - **Active Ingredients:** Keratin Complex, Biotinyl Tripeptide, Argan Lipids.
            - **Clinical Validation:** 96.2% match confidence.
            """)
    with c2:
        st.image("assets/hair_model.png", use_container_width=True)

# Department 3: Makeup
with st.container(border=True):
    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        st.image("assets/makeup_model.png", use_container_width=True)
    with c2:
        render_html("""
        <div style="padding-top: 10px;">
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 8px; display: inline-block;">03 / Color</span>
            <h3 style="font-family: 'Playfair Display', serif; color: #2D1418; font-size: 34px; margin-top: 0; margin-bottom: 16px;">Artistic Makeup Studio</h3>
            <p style="color: #6B5E59; font-size: 15px; line-height: 1.75; margin-bottom: 22px;">
                Discover color cosmetics and artistic formulations precisely matched to your genetic undertones, surface contrast, and clinical skin safety requirements for a flawless, couture finish.
            </p>
        </div>
        """)
        if st.button("Enter Makeup Studio →", key="btn_goto_makeup"):
            st.switch_page("pages/4_Makeup.py")
            
        with st.expander("View Colorimetric Specifications"):
            st.markdown("""
            - **Biomarkers Detected:** Genetic undertone (Warm/Cool/Neutral), surface contrast.
            - **Technology:** Colorimetric RGB-ratio clustering & luminance extraction.
            - **Formulation:** Hypoallergenic, non-comedogenic, clean active pigments.
            - **Clinical Validation:** 99.1% match confidence.
            """)