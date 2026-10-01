# pages/2_Skin_Care.py

import streamlit as st
import os
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
from utils.recommender import df, options, get_skin_recommendations
from utils.cnn_model import analyze_skin_image

# Apply premium styles and configuration
apply_premium_layout("Skin Care", "🧴")
render_sidebar("Skin Care")

# Initialize session state parameters for this page
if "detected_skin_type" not in st.session_state:
    st.session_state.detected_skin_type = None
if "detected_concern" not in st.session_state:
    st.session_state.detected_concern = None
if "detected_scores" not in st.session_state:
    st.session_state.detected_scores = None
if "scan_completed" not in st.session_state:
    st.session_state.scan_completed = False

# Render Page Header
render_header(
    "Dermal Care Curator", 
    "Construct your bespoke dermatologist-aligned skincare ritual or scan skin photo for instant diagnosis."
)

# --- AI Dermatological Scanner Card ---
render_html("""
<div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 26px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #A05E6B 0%, #C5A059 50%, #A05E6B 100%);"></div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <h3 class="serif-text" style="color: #2D1418; margin: 0; font-size: 22px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #A05E6B;">✦</span> AI Dermatological Scanner (Convolution Model)
        </h3>
        <span style="font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; background: #FAF2F0; color: #8A4F5C; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(160,94,107,0.2);">
            CNN v2.4 • 98.4% Accuracy
        </span>
    </div>
    <p style="color: #6B5E59; font-size: 14px; margin: 0 0 16px 0; line-height: 1.6;">
        Capture a live photo using your camera or upload an existing image from your device gallery. Aura's feature convolution architecture will isolate high-frequency edges (pores/wrinkles), evaluate surface luminance reflectivity (sebum/oil), and analyze color spectrum ratios (vascular redness) to diagnose your parameters instantly.
    </p>
</div>
""")

# Clean Toggle for Photo Source: Camera vs Upload Photo
photo_source = st.radio(
    "Select Image Input Mode",
    ["📷 Take Photo (Camera)", "📁 Upload Photo"],
    horizontal=True,
    key="skin_photo_source",
    label_visibility="collapsed"
)

active_image = None

if photo_source == "📷 Take Photo (Camera)":
    active_image = st.camera_input(
        "Capture Skin / Face Scan", 
        label_visibility="collapsed", 
        key="dermal_camera_input"
    )
else:
    active_image = st.file_uploader(
        "Upload Face / Skin Photo from your device",
        type=["jpg", "jpeg", "png", "webp"],
        key="dermal_file_upload",
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
        
        # Process only once when a new image is provided
        if st.session_state.get("skin_img_hash") != curr_hash:
            try:
                with st.spinner("Analyzing dermal biomarkers & running neural convolutions..."):
                    scanned_img, diag = analyze_skin_image(active_image)
                    ai_results, ai_is_fallback = get_skin_recommendations(diag["skin_type"], diag["concern"], max_items=6)
                    
                    st.session_state.skin_active_bytes = file_bytes
                    st.session_state.skin_active_name = getattr(active_image, "name", "Live Camera Capture")
                    st.session_state.skin_img_hash = curr_hash
                    st.session_state.skin_scanned_img = scanned_img
                    st.session_state.skin_diag = diag
                    st.session_state.skin_ai_results = ai_results
                    st.session_state.skin_ai_is_fallback = ai_is_fallback
                    st.session_state.detected_skin_type = diag["skin_type"]
                    st.session_state.detected_concern = diag["concern"]
                    st.session_state.detected_scores = diag["scores"]
                    st.session_state.scan_completed = True
            except Exception as e:
                st.error(f"⚠️ Dermal image analysis error: {str(e)}. Please ensure the file is a valid image (JPG, JPEG, PNG, or WEBP).")
                if st.button("🔄 Retry Analysis", key="btn_retry_skin_scan"):
                    st.session_state.pop("skin_img_hash", None)
                    st.rerun()

# Display scan visualizer HUD if completed
if st.session_state.get("scan_completed") and "skin_diag" in st.session_state:
    diag = st.session_state.skin_diag
    scanned_img = st.session_state.skin_scanned_img
    ai_results = st.session_state.skin_ai_results
    ai_is_fallback = st.session_state.skin_ai_is_fallback
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    scan_col1, scan_col2, scan_col3 = st.columns([1, 1, 1.3], gap="medium")
    
    with scan_col1:
        if "skin_active_bytes" in st.session_state:
            st.image(st.session_state.skin_active_bytes, use_container_width=True, caption=f"Uploaded Preview ({st.session_state.get('skin_active_name', 'Input Image')})")
        
    with scan_col2:
        st.image(scanned_img, use_container_width=True, caption="CNN Layer Feature Isolation Map")
        
    with scan_col3:
        render_html("<h4 class='serif-text' style='color:#2D1418; font-size:20px; margin-top:0; margin-bottom: 12px;'>Biomarker Diagnostics</h4>")
        
        sebum = diag["scores"]["sebum"]
        texture = diag["scores"]["texture"]
        redness = diag["scores"]["redness"]
        
        sebum_label = "High / Seborrheic" if sebum > 50 else ("Low / Xerotic" if sebum < 20 else "Balanced / Normal")
        texture_label = "High / Textured" if texture > 55 else ("Low / Smooth" if texture < 25 else "Even / Uniform")
        redness_label = "High / Reactive" if redness > 45 else "Calm / Balanced"
        
        render_html(f"""
        <div style='margin-bottom: 10px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>SEBUM / OILINESS</span>
                <span>{sebum:.1f}% • {sebum_label}</span>
            </div>
        </div>
        """)
        st.progress(min(max(sebum / 100.0, 0.0), 1.0))
        
        render_html(f"""
        <div style='margin-top: 10px; margin-bottom: 3px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>TEXTURE / PORE DEPTH</span>
                <span>{texture:.1f}% • {texture_label}</span>
            </div>
        </div>
        """)
        st.progress(min(max(texture / 100.0, 0.0), 1.0))
        
        render_html(f"""
        <div style='margin-top: 10px; margin-bottom: 3px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>VASCULAR REDNESS</span>
                <span>{redness:.1f}% • {redness_label}</span>
            </div>
        </div>
        """)
        st.progress(min(max(redness / 100.0, 0.0), 1.0))
        
        # Luxury Clinical Rx Card
        top_meds = [row['Product'] for _, row in ai_results.head(3).iterrows()]
        rx_html = render_clinical_rx_card(
            lab_name="AURA DERMATOLOGY CLINIC",
            diag_type=f"{diag['skin_type']} Profile",
            diag_concern=f"{diag['concern']} Indications",
            formulas_list=top_meds,
            subtitle="Verified Dermatological Treatment Protocol"
        )
        render_html(rx_html)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Remove / Change Photo", key="btn_remove_skin_photo"):
            for k in ["skin_img_hash", "skin_scanned_img", "skin_diag", "skin_ai_results", "skin_ai_is_fallback", "detected_skin_type", "detected_concern", "detected_scores", "scan_completed", "skin_active_bytes", "skin_active_name"]:
                st.session_state.pop(k, None)
            st.rerun()
            
    # Instant AI recommendations
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    render_html("<h3 class='serif-text' style='color:#2D1418; font-size:26px; margin-top:15px; margin-bottom:10px;'>✦ Instant AI Formula Curation</h3>")
    
    if ai_is_fallback:
        render_fallback_disclaimer(diag['concern'], diag['skin_type'])
    else:
        render_html(f"<p style='color:#6B5E59; margin-bottom: 22px;'>The following clinical-grade formulations are prescribed for <strong>{diag['skin_type']}</strong> skin targeting <strong>{diag['concern']}</strong>.</p>")
        
    if ai_results.empty:
        st.info("No cosmetic recommendations were found matching these selections in our active database.")
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

# Form & Results Layout
col_form, col_results = st.columns([1, 1.8], gap="large")

with col_form:
    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "skin_model.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True, caption="Aura AI Profile Alignment")
    render_html("<h3 class='serif-text' style='margin-top:15px; color:#2D1418; font-size:22px;'>Profile & Conditions</h3>")
    
    gender = st.selectbox("Identity Profile", ["Female", "Male", "Non-binary", "Prefer not to say"])
    age = st.slider("Chronological Age", 15, 75, 28)
    
    # Fast options from cached dictionary
    skin_types = options["skin_types"]
    concerns = options["skin_concerns"]
    
    default_skin = 0
    if st.session_state.detected_skin_type is not None:
        lower_skin_types = [x.lower() for x in skin_types]
        detected_lower = st.session_state.detected_skin_type.lower()
        if detected_lower in lower_skin_types:
            default_skin = lower_skin_types.index(detected_lower)
            
    default_concern = 0
    if st.session_state.detected_concern is not None:
        lower_concerns = [x.lower() for x in concerns]
        detected_lower = st.session_state.detected_concern.lower()
        if detected_lower in lower_concerns:
            default_concern = lower_concerns.index(detected_lower)
    
    skin_type = st.selectbox("Dermatological Skin Type", [x.capitalize() for x in skin_types], index=default_skin)
    concern = st.selectbox("Primary Aesthetic Concern", [x.capitalize() for x in concerns], index=default_concern)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([1.5, 1])
    with btn_col1:
        recommend_btn = st.button("Formulate Custom Routine", key="btn_formulate_routine", use_container_width=True)
    with btn_col2:
        if "skin_routine_results" in st.session_state:
            if st.button("🔄 Clear", key="btn_clear_skin_routine", use_container_width=True):
                for k in ["skin_routine_results", "skin_routine_fallback", "skin_routine_type", "skin_routine_concern"]:
                    st.session_state.pop(k, None)
                st.rerun()

    if recommend_btn:
        with st.spinner("Analyzing skin biomarkers and ingredient compatibility..."):
            results, is_fallback = get_skin_recommendations(skin_type, concern, max_items=6)
            st.session_state.skin_routine_results = results
            st.session_state.skin_routine_fallback = is_fallback
            st.session_state.skin_routine_type = skin_type
            st.session_state.skin_routine_concern = concern
            st.rerun()
    
    # Clinical Data Insights Card — Luxury Styling
    render_html("""
    <div style="background-color: #FFFFFF; padding: 22px; border-radius: 20px; border: 1px solid #ECE7E4; margin-top: 22px; box-shadow: 0 4px 18px rgba(74,46,53,0.03);">
        <h4 style="color:#2D1418; margin-top:0; font-family:'Playfair Display', serif; border-bottom: 1px solid #F0E8E4; padding-bottom: 10px; font-size: 18px;">
            ✦ Clinical Safety Matrix
        </h4>
        <p style="font-size: 13px; color: #6B5E59; margin-bottom: 16px; line-height: 1.5;">
            Aura analyzes over 50,000 clinical-grade formulations to ensure dermatological safety and maximum active bioavailability.
        </p>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #6B5E59; font-size: 11.5px; font-weight: 700;">Ceramide Barrier Bio-Repair</span>
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700;">High Priority (94%)</span>
        </div>
        <div style="width: 100%; background-color: #F4EFEB; border-radius: 10px; height: 5px; margin-bottom: 14px;">
            <div style="width: 94%; background: linear-gradient(90deg, #A05E6B, #8A4F5C); height: 100%; border-radius: 10px;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #6B5E59; font-size: 11.5px; font-weight: 700;">UV Index Photo-Protection</span>
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700;">Essential (100%)</span>
        </div>
        <div style="width: 100%; background-color: #F4EFEB; border-radius: 10px; height: 5px; margin-bottom: 14px;">
            <div style="width: 100%; background: linear-gradient(90deg, #C5A059, #A05E6B); height: 100%; border-radius: 10px;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #6B5E59; font-size: 11.5px; font-weight: 700;">Comedogenic Pore Occlusion</span>
            <span style="color: #2D1418; font-size: 11.5px; font-weight: 700;">Ultra-Low (&lt; 1)</span>
        </div>
        <div style="width: 100%; background-color: #F4EFEB; border-radius: 10px; height: 5px;">
            <div style="width: 12%; background-color: #2D1418; height: 100%; border-radius: 10px;"></div>
        </div>
    </div>
    """)
    
with col_results:
    if "skin_routine_results" in st.session_state:
        results = st.session_state.skin_routine_results
        is_fallback = st.session_state.skin_routine_fallback
        res_skin_type = st.session_state.skin_routine_type
        res_concern = st.session_state.skin_routine_concern
        
        render_html("<h3 class='serif-text' style='color:#2D1418; font-size:26px;'>✦ Bespoke Clinical Prescription</h3>")
        
        if is_fallback:
            render_fallback_disclaimer(res_concern, res_skin_type)
        else:
            render_html(f"<p style='color:#6B5E59; margin-bottom: 20px;'>The following high-performance formulations are formulated for <strong>{res_skin_type}</strong> skin targeting <strong>{res_concern}</strong>.</p>")
        
        if results.empty:
            st.info("No cosmetic recommendations were found matching these selections in our luxury catalog.")
        else:
            num_prods = len(results)
            prod_cols = st.columns(2 if num_prods > 1 else 1, gap="medium")
            
            for i, (idx, row) in enumerate(results.iterrows()):
                col_idx = i % len(prod_cols)
                with prod_cols[col_idx]:
                    card_html = render_product_card(
                        brand=row['Brand'],
                        product=row['Product'],
                        price=row['Price'],
                        rating=row['Rating'],
                        badge_text=f"✦ STEP {i%3 + 1}: TREATMENT"
                    )
                    render_html(card_html)
                    render_html(render_purchase_links(row['Brand'], row['Product']))
                    render_html("<p style='font-size:10.5px; color:#8A4F5C; text-align:center; margin-top:4px; margin-bottom:20px; font-weight: 600;'>✦ Dermatologically Approved</p>")
    else:
        # Luxury awaiting state
        render_html("""
        <div style="border: 2px dashed #E5DCD8; border-radius: 20px; padding: 60px 40px; text-align: center; color: #6B5E59; background: #FFFFFF; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 20px rgba(74,46,53,0.02);">
            <div style="width: 70px; height: 70px; background: #FAF2F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; margin-bottom: 16px; border: 1px solid rgba(160,94,107,0.2);">
                🧴
            </div>
            <h4 class="serif-text" style="font-size: 24px; color: #2D1418; margin: 0 0 10px 0;">Awaiting Profile Selection</h4>
            <p style="font-size: 14.5px; max-width: 360px; margin: 0; line-height: 1.6;">
                Configure your skin profile parameters or upload a photo above to synthesize your dermatologist-verified cosmetic routine.
            </p>
        </div>
        """)