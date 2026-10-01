# pages/3_Hair_Care.py

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
from utils.recommender import df, options, get_hair_recommendations
from utils.cnn_model import analyze_hair_image

# Apply layout and styles
apply_premium_layout("Hair Care", "💇")
render_sidebar("Hair Care")

# Initialize session state parameters for this page
if "detected_hair_type" not in st.session_state:
    st.session_state.detected_hair_type = None
if "detected_hair_concern" not in st.session_state:
    st.session_state.detected_hair_concern = None
if "detected_hair_scores" not in st.session_state:
    st.session_state.detected_hair_scores = None
if "hair_scan_completed" not in st.session_state:
    st.session_state.hair_scan_completed = False

# Page Header
render_header(
    "Hair Science Studio", 
    "Diagnose your follicle profiles to restore pristine cuticle resilience and salon-grade luster."
)

# --- AI Follicle Scanner Card ---
render_html("""
<div style="background: #FFFFFF; border: 1px solid #ECE7E4; border-radius: 20px; padding: 26px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(74, 46, 53, 0.03); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #A05E6B 0%, #C5A059 50%, #A05E6B 100%);"></div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <h3 class="serif-text" style="color: #2D1418; margin: 0; font-size: 22px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #A05E6B;">✦</span> AI Follicle Scanner (Convolution Model)
        </h3>
        <span style="font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; background: #FAF2F0; color: #8A4F5C; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(160,94,107,0.2);">
            CNN v2.4 • 96.2% Accuracy
        </span>
    </div>
    <p style="color: #6B5E59; font-size: 14px; margin: 0 0 16px 0; line-height: 1.6;">
        Capture a live photo using your camera or upload an existing image from your device gallery. Aura's convolution architecture will analyze cuticle porosity, map scalp lipid density, and detect structural integrity to formulate your perfect trichology regimen.
    </p>
</div>
""")

# Clean Toggle for Photo Source: Camera vs Upload Photo
photo_source = st.radio(
    "Select Image Input Mode",
    ["📷 Take Photo (Camera)", "📁 Upload Photo"],
    horizontal=True,
    key="hair_photo_source",
    label_visibility="collapsed"
)

active_image = None

if photo_source == "📷 Take Photo (Camera)":
    active_image = st.camera_input(
        "Capture Scalp / Hair Scan", 
        label_visibility="collapsed", 
        key="follicle_camera_input"
    )
else:
    active_image = st.file_uploader(
        "Upload Scalp / Hair Photo from your device",
        type=["jpg", "jpeg", "png", "webp"],
        key="follicle_file_upload",
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
        
        if st.session_state.get("hair_img_hash") != curr_hash:
            try:
                with st.spinner("Analyzing follicle biomarkers & running neural convolutions..."):
                    scanned_img, diag = analyze_hair_image(active_image)
                    ai_results, ai_is_fallback = get_hair_recommendations(diag["hair_type"], diag["concern"], max_items=6)
                    
                    st.session_state.hair_active_bytes = file_bytes
                    st.session_state.hair_active_name = getattr(active_image, "name", "Live Camera Capture")
                    st.session_state.hair_img_hash = curr_hash
                    st.session_state.hair_scanned_img = scanned_img
                    st.session_state.hair_diag = diag
                    st.session_state.hair_ai_results = ai_results
                    st.session_state.hair_ai_is_fallback = ai_is_fallback
                    st.session_state.detected_hair_type = diag["hair_type"]
                    st.session_state.detected_hair_concern = diag["concern"]
                    st.session_state.detected_hair_scores = diag["scores"]
                    st.session_state.hair_scan_completed = True
            except Exception as e:
                st.error(f"⚠️ Follicle image analysis error: {str(e)}. Please ensure the file is a valid image (JPG, JPEG, PNG, or WEBP).")
                if st.button("🔄 Retry Analysis", key="btn_retry_hair_scan"):
                    st.session_state.pop("hair_img_hash", None)
                    st.rerun()

# Display HUD if completed
if st.session_state.get("hair_scan_completed") and "hair_diag" in st.session_state:
    diag = st.session_state.hair_diag
    scanned_img = st.session_state.hair_scanned_img
    ai_results = st.session_state.hair_ai_results
    ai_is_fallback = st.session_state.hair_ai_is_fallback
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    scan_col1, scan_col2, scan_col3 = st.columns([1, 1, 1.3], gap="medium")
    
    with scan_col1:
        if "hair_active_bytes" in st.session_state:
            st.image(st.session_state.hair_active_bytes, use_container_width=True, caption=f"Uploaded Preview ({st.session_state.get('hair_active_name', 'Input Image')})")
        
    with scan_col2:
        st.image(scanned_img, use_container_width=True, caption="CNN Scalp & Cuticle Map")
        
    with scan_col3:
        render_html("<h4 class='serif-text' style='color:#2D1418; font-size:20px; margin-top:0; margin-bottom: 12px;'>Trichology Diagnostics</h4>")
        
        sebum = diag["scores"]["sebum"]
        density = diag["scores"]["density"]
        irritation = diag["scores"]["irritation"]
        
        render_html(f"""
        <div style='margin-bottom: 10px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>SCALP LIPID DENSITY</span>
                <span>{sebum:.1f}%</span>
            </div>
        </div>
        """)
        st.progress(min(max(sebum / 100.0, 0.0), 1.0))
        
        render_html(f"""
        <div style='margin-top: 10px; margin-bottom: 3px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>FOLLICLE INTEGRITY</span>
                <span>{density:.1f}%</span>
            </div>
        </div>
        """)
        st.progress(min(max(density / 100.0, 0.0), 1.0))
        
        render_html(f"""
        <div style='margin-top: 10px; margin-bottom: 3px;'>
            <div style='display: flex; justify-content: space-between; font-size:11px; font-weight:700; color:#4A2E35; margin-bottom: 3px;'>
                <span>SCALP SENSITIVITY INDEX</span>
                <span>{irritation:.1f}%</span>
            </div>
        </div>
        """)
        st.progress(min(max(irritation / 100.0, 0.0), 1.0))
        
        # Luxury Clinical Rx Card
        top_meds = [row['Product'] for _, row in ai_results.head(3).iterrows()]
        rx_html = render_clinical_rx_card(
            lab_name="AURA TRICHOLOGY LAB",
            diag_type=f"{diag['hair_type']} Fiber",
            diag_concern=f"{diag['concern']} Focus",
            formulas_list=top_meds,
            subtitle="Verified Follicular Prescription Protocol"
        )
        render_html(rx_html)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Remove / Change Photo", key="btn_remove_hair_photo"):
            for k in ["hair_img_hash", "hair_scanned_img", "hair_diag", "hair_ai_results", "hair_ai_is_fallback", "detected_hair_type", "detected_hair_concern", "detected_hair_scores", "hair_scan_completed", "hair_active_bytes", "hair_active_name"]:
                st.session_state.pop(k, None)
            st.rerun()

    # Instant AI Recommendations
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    render_html("<h3 class='serif-text' style='color:#2D1418; font-size:26px; margin-top:15px; margin-bottom:10px;'>✦ Instant AI Formula Curation</h3>")
    
    if ai_is_fallback:
        render_fallback_disclaimer(diag['concern'], diag['hair_type'])
    else:
        render_html(f"<p style='color:#6B5E59; margin-bottom: 22px;'>The following salon-grade treatments are prescribed for <strong>{diag['hair_type']}</strong> hair targeting <strong>{diag['concern']}</strong>.</p>")
        
    if ai_results.empty:
        st.info("No active hair formulas match your parameters in our database.")
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
                render_html("<p style='font-size:10.5px; color:#8A4F5C; text-align:center; margin-top:4px; margin-bottom:20px; font-weight: 600;'>✦ Trichologist Approved</p>")
            
    st.markdown("<hr style='border-color: #ECE7E4; margin: 35px 0;'>", unsafe_allow_html=True)

# Form & Results Layout
col_form, col_results = st.columns([1, 1.8], gap="large")

with col_form:
    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "hair_model.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True, caption="Aura AI Follicle Analysis")
    render_html("<h3 class='serif-text' style='margin-top:15px; color:#2D1418; font-size:22px;'>Follicle Parameters</h3>")
    
    hair_types = options["hair_types"]
    concerns = options["hair_concerns"]
    
    default_hair = 0
    if st.session_state.detected_hair_type is not None:
        lower_hair_types = [x.lower() for x in hair_types]
        detected_lower = st.session_state.detected_hair_type.lower()
        if detected_lower in lower_hair_types:
            default_hair = lower_hair_types.index(detected_lower)
            
    default_concern = 0
    if st.session_state.detected_hair_concern is not None:
        lower_concerns = [x.lower() for x in concerns]
        detected_lower = st.session_state.detected_hair_concern.lower()
        if detected_lower in lower_concerns:
            default_concern = lower_concerns.index(detected_lower)
            
    hair_type = st.selectbox("Hair Fiber Structure", [x.capitalize() for x in hair_types], index=default_hair)
    concern = st.selectbox("Cuticle / Scalp Issue", [x.capitalize() for x in concerns], index=default_concern)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([1.5, 1])
    with btn_col1:
        recommend_btn = st.button("Formulate Hair Therapy", key="btn_formulate_hair", use_container_width=True)
    with btn_col2:
        if "hair_routine_results" in st.session_state:
            if st.button("🔄 Clear", key="btn_clear_hair_routine", use_container_width=True):
                for k in ["hair_routine_results", "hair_routine_fallback", "hair_routine_type", "hair_routine_concern"]:
                    st.session_state.pop(k, None)
                st.rerun()

    if recommend_btn:
        with st.spinner("Analyzing scalp biology and lipid nourishment formulas..."):
            results, is_fallback = get_hair_recommendations(hair_type, concern, max_items=6)
            st.session_state.hair_routine_results = results
            st.session_state.hair_routine_fallback = is_fallback
            st.session_state.hair_routine_type = hair_type
            st.session_state.hair_routine_concern = concern
            st.rerun()
    
    # Trichology Insights Card — Luxury Styling
    render_html("""
    <div style="background-color: #FFFFFF; padding: 22px; border-radius: 20px; border: 1px solid #ECE7E4; margin-top: 22px; box-shadow: 0 4px 18px rgba(74,46,53,0.03);">
        <h4 style="color:#2D1418; margin-top:0; font-family:'Playfair Display', serif; border-bottom: 1px solid #F0E8E4; padding-bottom: 10px; font-size: 18px;">
            ✦ Trichology Matrix
        </h4>
        <p style="font-size: 13px; color: #6B5E59; margin-bottom: 16px; line-height: 1.5;">
            Formulas are filtered based on scalp microbiome balance, cuticle porosity, and tensile lipid density.
        </p>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #6B5E59; font-size: 11.5px; font-weight: 700;">Cuticle Keratin Alignment</span>
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700;">Restorative (96%)</span>
        </div>
        <div style="width: 100%; background-color: #F4EFEB; border-radius: 10px; height: 5px; margin-bottom: 14px;">
            <div style="width: 96%; background: linear-gradient(90deg, #A05E6B, #8A4F5C); height: 100%; border-radius: 10px;"></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #6B5E59; font-size: 11.5px; font-weight: 700;">Scalp Lipid Balance</span>
            <span style="color: #8A4F5C; font-size: 11.5px; font-weight: 700;">Optimal (92%)</span>
        </div>
        <div style="width: 100%; background-color: #F4EFEB; border-radius: 10px; height: 5px;">
            <div style="width: 92%; background: linear-gradient(90deg, #C5A059, #A05E6B); height: 100%; border-radius: 10px;"></div>
        </div>
    </div>
    """)
    
with col_results:
    if "hair_routine_results" in st.session_state:
        results = st.session_state.hair_routine_results
        is_fallback = st.session_state.hair_routine_fallback
        res_hair_type = st.session_state.hair_routine_type
        res_concern = st.session_state.hair_routine_concern
        
        render_html("<h3 class='serif-text' style='color:#2D1418; font-size:26px;'>✦ Bespoke Hair Therapy</h3>")
        
        if is_fallback:
            render_fallback_disclaimer(res_concern, res_hair_type)
        else:
            render_html(f"<p style='color:#6B5E59; margin-bottom: 20px;'>The following salon-grade treatments are prescribed for <strong>{res_hair_type}</strong> hair matching <strong>{res_concern}</strong> concerns.</p>")
        
        if results.empty:
            st.info("No active hair formulas match your parameters in our database.")
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
                        badge_text="✦ NUTRITIVE RECOVERY"
                    )
                    render_html(card_html)
                    render_html(render_purchase_links(row['Brand'], row['Product']))
                    render_html("<p style='font-size:10.5px; color:#8A4F5C; text-align:center; margin-top:4px; margin-bottom:20px; font-weight: 600;'>✦ Trichologist Approved</p>")
    else:
        # Luxury awaiting state
        render_html("""
        <div style="border: 2px dashed #E5DCD8; border-radius: 20px; padding: 60px 40px; text-align: center; color: #6B5E59; background: #FFFFFF; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 20px rgba(74,46,53,0.02);">
            <div style="width: 70px; height: 70px; background: #FAF2F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; margin-bottom: 16px; border: 1px solid rgba(160,94,107,0.2);">
                💇
            </div>
            <h4 class="serif-text" style="font-size: 24px; color: #2D1418; margin: 0 0 10px 0;">Awaiting Follicle Settings</h4>
            <p style="font-size: 14.5px; max-width: 360px; margin: 0; line-height: 1.6;">
                Configure your hair fiber metrics or upload a scalp scan above to align our trichology recommendations.
            </p>
        </div>
        """)