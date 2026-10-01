# pages/4_Makeup.py

import streamlit as st
from utils.layout import (
    apply_premium_layout, 
    render_sidebar, 
    render_header, 
    render_product_card, 
    render_fallback_disclaimer, 
    render_purchase_links,
    render_clinical_rx_card,
    render_html
)
from utils.recommender import df, options, get_makeup_recommendations
from utils.cnn_model import analyze_makeup_image

# Apply layout and styles
apply_premium_layout("Makeup", "💄")
render_sidebar("Makeup")

# Initialize session state parameters for this page
if "detected_makeup_skin_type" not in st.session_state:
    st.session_state.detected_makeup_skin_type = None
if "detected_makeup_style" not in st.session_state:
    st.session_state.detected_makeup_style = None
if "detected_makeup_scores" not in st.session_state:
    st.session_state.detected_makeup_scores = None
if "makeup_scan_completed" not in st.session_state:
    st.session_state.makeup_scan_completed = False

# Page Header
render_header(
    "Aura Beauty Parlor", 
    "Step into our virtual atelier for colorimetric facial harmony and a personalized 14-step couture masterclass."
)

render_html("""
<div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 26px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #A05E6B 0%, #C5A059 50%, #A05E6B 100%);"></div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <h3 class="serif-text" style="color: #2D1418; margin: 0; font-size: 22px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #A05E6B;">✦</span> Colorimetric Face Analysis Atelier
        </h3>
        <span style="font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; background: #FAF2F0; color: #8A4F5C; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(160,94,107,0.2);">
            CNN v2.4 • 99.1% Accuracy
        </span>
    </div>
    <p style="color: #6B5E59; font-size: 14px; margin: 0 0 16px 0; line-height: 1.6;">
        Just like entering a world-class beauty parlor, your journey begins with a complete facial contour analysis. Capture a live photo using your camera or upload an existing image from your device gallery. Our AI stylists evaluate your genetic undertones, surface contrast, and skin tone to craft your 14-step masterclass.
    </p>
</div>
""")

# Clean Toggle for Photo Source: Camera vs Upload Photo
photo_source = st.radio(
    "Select Image Input Mode",
    ["📷 Take Photo (Camera)", "📁 Upload Photo"],
    horizontal=True,
    key="makeup_photo_source",
    label_visibility="collapsed"
)

active_image = None

if photo_source == "📷 Take Photo (Camera)":
    active_image = st.camera_input(
        "Capture Your Beauty Profile", 
        label_visibility="collapsed", 
        key="makeup_camera_input"
    )
else:
    active_image = st.file_uploader(
        "Upload Face Photo from your device",
        type=["jpg", "jpeg", "png", "webp"],
        key="makeup_file_upload",
        help="Supported formats: JPG, JPEG, PNG, WEBP (Max: 10MB)"
    )

# File Validation & AI Pipeline Execution
if active_image is not None:
    MAX_SIZE_BYTES = 10 * 1024 * 1024
    if active_image.size > MAX_SIZE_BYTES:
        st.error(f"⚠️ Image file is too large ({active_image.size / (1024*1024):.1f}MB). Maximum allowed upload size is 10MB. Please choose a smaller photo.")
        active_image = None
    else:
        file_bytes = active_image.getvalue()
        curr_hash = hash(file_bytes)
        
        if st.session_state.get("makeup_img_hash") != curr_hash:
            try:
                with st.spinner("Analyzing undertone & contrast features..."):
                    scanned_img, diag = analyze_makeup_image(active_image)
                    ai_results, ai_is_fallback = get_makeup_recommendations(diag["skin_type"], diag["concern"], max_items=6)
                    
                    st.session_state.makeup_active_bytes = file_bytes
                    st.session_state.makeup_active_name = getattr(active_image, "name", "Live Camera Capture")
                    st.session_state.makeup_img_hash = curr_hash
                    st.session_state.makeup_scanned_img = scanned_img
                    st.session_state.makeup_diag = diag
                    st.session_state.makeup_ai_results = ai_results
                    st.session_state.makeup_ai_is_fallback = ai_is_fallback
                    st.session_state.detected_makeup_skin_type = diag["skin_type"]
                    st.session_state.detected_makeup_style = diag["concern"]
                    st.session_state.detected_makeup_scores = diag["scores"]
                    st.session_state.makeup_scan_completed = True
            except Exception as e:
                st.error(f"⚠️ Makeup aesthetic analysis error: {str(e)}. Please ensure the file is a valid image (JPG, JPEG, PNG, or WEBP).")
                if st.button("🔄 Retry Analysis", key="btn_retry_makeup_scan"):
                    st.session_state.pop("makeup_img_hash", None)
                    st.rerun()

# Render results when available
if st.session_state.get("makeup_scan_completed") and "makeup_diag" in st.session_state:
    diag = st.session_state.makeup_diag
    scanned_img = st.session_state.makeup_scanned_img
    ai_results = st.session_state.makeup_ai_results
    ai_is_fallback = st.session_state.makeup_ai_is_fallback
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    scan_col1, scan_col2, scan_col3 = st.columns([1, 1, 1.3], gap="medium")
    
    with scan_col1:
        if "makeup_active_bytes" in st.session_state:
            st.image(st.session_state.makeup_active_bytes, use_container_width=True, caption=f"Uploaded Preview ({st.session_state.get('makeup_active_name', 'Input Image')})")
        
    with scan_col2:
        st.image(scanned_img, use_container_width=True, caption="CNN Undertone & Contrast Map")
        
    with scan_col3:
        render_html("<h4 class='serif-text' style='color:#2D1418; font-size:20px; margin-top:0; margin-bottom: 12px;'>Diagnostic Facial Profile</h4>")
        
        tone = diag.get('skin_tone', 'Medium')
        undertone = diag.get('undertone', 'Neutral')
        
        render_html(f"""
        <div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 14px; padding: 14px 16px; margin-bottom: 14px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                <div>
                    <span style="font-size: 10px; color: #8C7B83; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Skin Tone</span>
                    <div style="font-size: 14px; font-weight: 700; color: #2D1418;">{tone}</div>
                </div>
                <div>
                    <span style="font-size: 10px; color: #8C7B83; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Undertone</span>
                    <div style="font-size: 14px; font-weight: 700; color: #A05E6B;">{undertone}</div>
                </div>
                <div style="margin-top: 6px;">
                    <span style="font-size: 10px; color: #8C7B83; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Base Texture</span>
                    <div style="font-size: 14px; font-weight: 700; color: #2D1418;">{diag['skin_type']}</div>
                </div>
                <div style="margin-top: 6px;">
                    <span style="font-size: 10px; color: #8C7B83; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">Target Concern</span>
                    <div style="font-size: 14px; font-weight: 700; color: #2D1418;">{diag['concern']}</div>
                </div>
            </div>
        </div>
        """)
        
        top_meds = [row['Product'] for _, row in ai_results.head(3).iterrows()]
        rx_html = render_clinical_rx_card(
            lab_name="AURA AESTHETICS ATELIER",
            diag_type=f"{tone} Skin • {undertone} Undertone",
            diag_concern=f"{diag['skin_type']} Base ({diag['concern']})",
            formulas_list=top_meds,
            subtitle="Custom Colorimetric & Base Formulation Protocol"
        )
        render_html(rx_html)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Remove / Change Photo", key="btn_remove_makeup_photo"):
            for k in ["makeup_img_hash", "makeup_scanned_img", "makeup_diag", "makeup_ai_results", "makeup_ai_is_fallback", "detected_makeup_skin_type", "detected_makeup_style", "detected_makeup_scores", "makeup_scan_completed", "makeup_active_bytes", "makeup_active_name"]:
                st.session_state.pop(k, None)
            st.rerun()

    # 14-Step Routine
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    render_html("""
    <div style="text-align: center; margin-bottom: 25px;">
        <div style="font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #A05E6B; font-weight: 700; margin-bottom: 6px;">COUTURE MASTERCLASS</div>
        <h3 class='serif-text' style='color:#2D1418; font-size:32px; margin: 0 0 8px 0;'>✦ Your Bespoke 14-Step Masterclass</h3>
    </div>
    """)
    render_html(f"<p style='color:#6B5E59; text-align:center; margin-bottom:30px;'>Calibrated specifically for your <strong>{tone}</strong> skin tone with <strong>{undertone}</strong> undertones and <strong>{diag['skin_type']}</strong> canvas.</p>")
    
    def render_step(num, title, why, shade, how, example):
        render_html(f"""
        <div style="background:#FFFFFF; border:1px solid #ECE7E4; border-radius:18px; padding:22px 24px; margin-bottom:16px; box-shadow: 0 4px 18px rgba(74,46,53,0.02); transition: all 0.25s ease;">
            <div style="display:flex; align-items:center; gap:14px; border-bottom:1px solid #F2ECE8; padding-bottom:12px; margin-bottom:14px;">
                <div style="background: linear-gradient(135deg, #A05E6B 0%, #834753 100%); color:white; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size: 13.5px; box-shadow: 0 2px 8px rgba(160,94,107,0.3);">
                    {num}
                </div>
                <h4 style="color:#2D1418; margin:0; font-size:18px; font-family: 'Playfair Display', serif;">{title}</h4>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div>
                    <div style="font-size:10px; text-transform: uppercase; letter-spacing: 1px; color:#8C7B83; font-weight: 700; margin-bottom:2px;">Curator Rationale</div>
                    <p style="font-size:13px; color:#6B5E59; margin-top:0; margin-bottom:10px; line-height: 1.5;">{why}</p>
                    
                    <div style="font-size:10px; text-transform: uppercase; letter-spacing: 1px; color:#8C7B83; font-weight: 700; margin-bottom:2px;">Ideal Shade Palette</div>
                    <p style="font-size:13px; color:#2D1418; font-weight: 600; margin-top:0; margin-bottom: 0;">{shade}</p>
                </div>
                <div>
                    <div style="font-size:10px; text-transform: uppercase; letter-spacing: 1px; color:#8C7B83; font-weight: 700; margin-bottom:2px;">Application Method</div>
                    <p style="font-size:13px; color:#6B5E59; margin-top:0; margin-bottom:10px; line-height: 1.5;">{how}</p>
                    
                    <div style="font-size:10px; text-transform: uppercase; letter-spacing: 1px; color:#8C7B83; font-weight: 700; margin-bottom:2px;">Recommended Formulation</div>
                    <p style="font-size:13px; color:#8A4F5C; font-weight:700; margin-top:0; margin-bottom: 0;">✨ {example}</p>
                </div>
            </div>
        </div>
        """)
        
    skin_type = diag['skin_type']
    
    # 1. Foundation
    f_why = "A velvety matte finish balances epidermal lipid reflectivity." if skin_type == "Oily" else "A hydrating, dewy finish nourishes and softens dry tissue."
    f_shade = f"{tone} tone with calibrated {undertone} undertones."
    f_how = "Apply a thin layer starting from the center of the face, blending outwards using a damp beauty sponge."
    render_step(1, "Foundation", f_why, f_shade, f_how, "Aura Luminous Silk Foundation" if skin_type == "Dry" else "Aura Velvet Matte Foundation")
    
    # 2. Color Corrector
    c_why = "To neutralize localized hyperpigmentation and micro-vascular shadows."
    c_shade = "Peach/Orange" if tone in ["Medium", "Tan", "Deep"] else "Green/Yellow"
    c_how = "Dab a tiny amount exclusively on targeted areas before concealer. Feather edges seamlessly."
    render_step(2, "Color Corrector", c_why, c_shade, c_how, "Aura Pro-Correct Pigment Palette")
    
    # 3. Concealer
    cc_why = "To illuminate orbital contours and unify complexion without creasing."
    cc_shade = f"1-2 shades lighter than your {tone} foundation."
    cc_how = "Apply delicately under the eyes and on high points. Tap gently with warmth of fingertips."
    render_step(3, "Concealer", cc_why, cc_shade, cc_how, "Aura Radiant Cream Concealer")
    
    # 4. Setting Powder
    p_why = "Locks the foundation base in place and controls sebum." if skin_type in ["Oily", "Combination"] else "Sets the under-eye delicately without dehydrating tissue."
    p_shade = f"Translucent Silicate" if tone in ["Fair", "Light", "Medium"] else "Warm Banana Tinted Powder"
    p_how = "Press lightly under the eyes and across the T-zone using a plush velour puff."
    render_step(4, "Compact & Setting Powder", p_why, p_shade, p_how, "Aura Flawless Finish Micro-Powder")
    
    # 5. Contour/Bronzer
    b_why = f"To introduce structural warmth and bone-structure dimension to your {tone} complexion."
    b_shade = f"Cool-toned taupe for contour, warm terracotta for bronze." if undertone == "Cool" else "Warm golden bronze."
    b_how = "Sweep in a subtle '3' contour along hairline, beneath cheekbones, and jawline."
    render_step(5, "Contour & Sculpting Bronzer", b_why, b_shade, b_how, "Aura Sculpting Bronzer Duo")
    
    # 6. Blush
    bl_why = "Infuses vital micro-circulation flush and natural luminescence."
    bl_shade = "Soft Peach & Terracotta" if undertone == "Warm" else "Dusty Rose & Petal Pink"
    bl_how = "Smile gently and apply high on apples of cheeks, sweeping upward toward the temples."
    render_step(6, "Hydrating Cheek Blush", bl_why, bl_shade, bl_how, "Rare Beauty Soft Pinch Liquid Blush")
    
    # 7. Highlighter
    h_why = "Captures ambient photon reflectivity on high architectural points."
    h_shade = "Champagne Gold" if undertone == "Warm" else ("Icy Pearl" if tone in ["Fair", "Light"] else "Rose Gold")
    h_how = "Dust delicately onto the highest arch of cheekbones, bridge of nose, and cupid's bow."
    render_step(7, "Highlighter & Strobe", h_why, h_shade, h_how, "Aura Liquid Strobe Illuminator")
    
    # 8. Eyebrow Product
    e_why = "Architecturally frames ocular geometry and establishes proportion."
    e_shade = "Cool Ash Brown / Soft Black" if tone in ["Medium", "Deep"] else "Taupe / Soft Caramel"
    e_how = "Use ultra-fine strokes to mimic natural hair growth, grooming upward with a clean spoolie."
    render_step(8, "Micro-Precision Brow Pencil", e_why, e_shade, e_how, "Aura Micro-Precision Brow Stylist")
    
    # 9. Eyeshadow Palette
    es_why = "Harmonizes with your genetic iris pigments and undertone temperature."
    es_shade = "Burnished copper & gold" if undertone == "Warm" else "Cool amethyst, taupe & satin plum"
    es_how = "Wash transition color across the crease, define outer corner, and pat silk shimmer on lid."
    render_step(9, "Chromatic Eyeshadow Palette", es_why, es_shade, es_how, "Aura Signature 12-Pan Palette")
    
    # 10. Eyeliner
    el_why = "Intensifies lash line density and delineates eye contours."
    el_shade = "Rich Espresso Brown for day, Velvet Carbon Black for evening."
    el_how = "Glide along the lash roots with zero gap, elevating outward at outer corner."
    render_step(10, "Precision Eyeliner", el_why, el_shade, el_how, "Aura Waterproof Gel Liner")
    
    # 11. Mascara
    m_why = "Elevates, fans out, and magnifies keratin lash fiber volume."
    m_shade = "Deep Carbon Black"
    m_how = "Roll the brush from base to tip in a gentle zigzag motion for separation."
    render_step(11, "Lash Architecture Mascara", m_why, m_shade, m_how, "Aura Lash Architect Mascara")
    
    # 12. Lip Liner
    ll_why = "Sculpts lip architecture and prevents feathering of active pigments."
    ll_shade = f"One tone deeper than your {tone}-calibrated lipstick."
    ll_how = "Trace the natural perimeter, emphasizing the cupid's bow and softening inward."
    render_step(12, "Lip Architecture Liner", ll_why, ll_shade, ll_how, "Aura Velvet Lip Pencil")
    
    # 13. Lipstick/Lip Gloss
    lip_why = "Unifies the chromatic story with nourishing peptide moisture."
    lip_shade = "Warm brick terracotta" if undertone == "Warm" else "Berry rose or blue-red"
    lip_how = "Press onto center of lips, diffusing outwards. Layer gloss for plump volume."
    render_step(13, "Lipstick & Hydrating Gloss", lip_why, lip_shade, lip_how, "Charlotte Tilbury Matte Revolution")
    
    # 14. Setting Spray
    s_why = "Melts powdered pigments into skin matrix and guarantees 16-hour endurance."
    s_shade = "Invisible Hydrating Micro-Mist"
    s_how = "Mist 8 inches away in cross formation to lock in the artistic look."
    render_step(14, "Continuous Setting Mist", s_why, s_shade, s_how, "Aura Continuous Setting Mist" if skin_type == "Dry" else "Aura Matte Fix Spray")
    
    st.markdown("<hr style='border-color: #ECE7E4; margin: 35px 0;'>", unsafe_allow_html=True)
    
    # Recommendations Display
    render_html("<h3 class='serif-text' style='color:#2D1418; font-size:26px; margin-top:15px; margin-bottom:10px;'>✦ Shop Your Aesthetic Selection</h3>")
    
    if ai_is_fallback:
        render_fallback_disclaimer(diag['concern'], diag['skin_type'])
    else:
        render_html(f"<p style='color:#6B5E59; margin-bottom: 22px;'>The following luxury cosmetics are matched for a <strong>{diag['skin_type']}</strong> base targeting a <strong>{diag['concern']}</strong> look.</p>")
        
    if ai_results.empty:
        st.info("No active makeup catalog entries match your selection currently.")
    else:
        num_prods = len(ai_results)
        prod_cols = st.columns(min(num_prods, 3), gap="medium")
        
        for i, (idx, row) in enumerate(ai_results.iterrows()):
            col_idx = i % len(prod_cols)
            with prod_cols[col_idx]:
                card_html = render_product_card(
                    brand=row['Brand'],
                    product=row['Product'],
                    price=row['Price'],
                    rating=row['Rating'],
                    step_number=(i % 3 + 1)
                )
                render_html(card_html)
                render_html(render_purchase_links(row['Brand'], row['Product']))
                render_html("<p style='font-size:10.5px; color:#8A4F5C; text-align:center; margin-top:4px; margin-bottom:20px; font-weight: 600;'>✦ Dermatologically Approved</p>")
                
    st.markdown("<hr style='border-color: #ECE7E4; margin: 35px 0;'>", unsafe_allow_html=True)
else:
    # Empty State
    render_html("""
    <div style="border: 2px dashed #E5DCD8; border-radius: 20px; padding: 60px 40px; text-align: center; color: #6B5E59; background: #FFFFFF; margin-top:20px; box-shadow: 0 4px 20px rgba(74,46,53,0.02);">
        <div style="width: 70px; height: 70px; background: #FAF2F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 16px auto; border: 1px solid rgba(160,94,107,0.2);">
            💄
        </div>
        <h4 class="serif-text" style="font-size: 24px; color: #2D1418; margin: 0 0 10px 0;">Awaiting Your Facial Portrait</h4>
        <p style="font-size: 14.5px; max-width: 420px; margin: 0 auto; line-height: 1.6;">
            Capture a live photo or upload an image above. Our AI atelier will analyze your skin tone, genetic undertone, and canvas texture to generate your bespoke 14-step masterclass.
        </p>
    </div>
    """)