# utils/layout.py

import streamlit as st
import os
import urllib.parse
import textwrap
from functools import lru_cache

def render_html(html_str):
    """
    Renders pure HTML cleanly without markdown indentation interference.
    Strips leading indentation and uses st.html() when available.
    """
    cleaned = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)

@lru_cache(maxsize=2048)
def render_purchase_links(brand, product):
    """
    Returns HTML for multiple shopping website purchase links with LRU memoization.
    Styled with a cohesive, ultra-luxury high-fashion aesthetic.
    """
    query = urllib.parse.quote_plus(f"{brand} {product}")
    brand_query = urllib.parse.quote_plus(f"{brand} {product} official site")
    amazon_url = f"https://www.amazon.in/s?k={query}"
    flipkart_url = f"https://www.flipkart.com/search?q={query}"
    nykaa_url = f"https://www.nykaa.com/search/result/?q={query}"
    myntra_url = f"https://www.myntra.com/{query}"
    purplle_url = f"https://www.purplle.com/search?q={query}"
    own_store_url = "http://localhost:8000/#shop" 
    official_brand_url = f"https://www.google.com/search?q={brand_query}"
    
    return f"""
    <div class="purchase-links-block" style="margin-top: 14px;">
        <a href="{own_store_url}" target="_blank" style="text-decoration: none; display: block; margin-bottom: 8px;">
            <div class="aura-buy-btn">
                <span>✨</span> Buy on Aura Official Store
            </div>
        </a>
        <a href="{official_brand_url}" target="_blank" style="text-decoration: none; display: block; margin-bottom: 10px;">
            <div class="brand-portal-btn">
                <span>🌐</span> {brand} Official Website
            </div>
        </a>
        <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #8C7B83; margin-bottom: 6px; text-align: center;">Verified Retail Partners</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
            <a href="{nykaa_url}" target="_blank" class="partner-chip" title="Buy on Nykaa">
                <span style="color: #FF0E7A; font-weight: 800;">N</span> Nykaa
            </a>
            <a href="{purplle_url}" target="_blank" class="partner-chip" title="Buy on Purplle">
                <span style="color: #6A2C91; font-weight: 800;">P</span> Purplle
            </a>
            <a href="{amazon_url}" target="_blank" class="partner-chip" title="Buy on Amazon">
                <span style="color: #FF9900; font-weight: 800;">a</span> Amazon
            </a>
            <a href="{flipkart_url}" target="_blank" class="partner-chip" title="Buy on Flipkart">
                <span style="color: #2874F0; font-weight: 800;">f</span> Flipkart
            </a>
        </div>
    </div>
    """

@st.cache_data(show_spinner=False)
def get_cached_css():
    css_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "assets", 
        "style.css"
    )
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def apply_premium_layout(page_title="AURA", page_icon="✨"):
    """
    Sets the page configuration and injects the centralized premium CSS stylesheet.
    """
    try:
        st.set_page_config(
            page_title=f"AURA • {page_title}",
            page_icon=page_icon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except st.errors.StreamlitAPIException:
        pass

    css_content = get_cached_css()
    if css_content:
        render_html(f"<style>{css_content}</style>")


def draw_stars(rating):
    """
    Returns a stylized star rating string.
    """
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.4 else 0
    stars = "★" * full_stars + ("½" if half_star else "") + "☆" * (5 - full_stars - half_star)
    return stars


def render_sidebar(current_page=""):
    """
    Renders the consistent sidebar elements including AURA branding,
    a custom premium navigation menu, information box, and side image.
    """
    with st.sidebar:
        # Luxury Brand Lockup
        render_html("""
        <div class="sidebar-brand-card">
            <div class="brand-emblem-seal">
                <span>✧</span>
            </div>
            <div class="brand-monogram-title">AURA</div>
            <div class="brand-monogram-sub">HAUTE BIOTECH BEAUTY • PARIS</div>
            <div class="brand-accent-glow"></div>
        </div>
        
        <div class="sidebar-status-pill">
            <span class="status-live-dot"></span>
            <span class="status-live-text">NEURAL ENGINE ACTIVE</span>
            <span class="status-live-ver">v2.4</span>
        </div>
        """)
        
        # VIP Flagship Storefront Invite Card
        render_html("""
        <a href="http://localhost:8000" target="_blank" style="text-decoration: none; display: block; margin-bottom: 20px;">
            <div class="boutique-invite-card">
                <div class="boutique-card-top">
                    <span class="boutique-tag">FLAGSHIP BOUTIQUE</span>
                    <span class="boutique-badge">VIP ACCESS</span>
                </div>
                <div class="boutique-title">Aura Boutique & Cart</div>
                <div class="boutique-desc">Explore 500+ official clinical products with instant secure checkout.</div>
                <div class="boutique-cta">
                    <span>Enter Flagship Boutique</span>
                    <span class="boutique-arrow">→</span>
                </div>
            </div>
        </a>
        """)
        
        nav_items = {
            "Home": ("✦  01 • Home Portal", "pages/1_Home.py"),
            "Skin Care": ("🧴  02 • Dermal Care", "pages/2_Skin_Care.py"),
            "Hair Care": ("💆  03 • Follicle Care", "pages/3_Hair_Care.py"),
            "Makeup": ("💄  04 • Makeup Studio", "pages/4_Makeup.py"),
            "Data Analysis": ("📊  05 • Clinical Analytics", "pages/5_Data_Analysis.py")
        }
        
        render_html("""
        <div class="nav-section-label">
            <span>CLINICAL MODULES</span>
            <span class="nav-count">05</span>
        </div>
        """)
        
        for key, (label, path) in nav_items.items():
            is_active = (current_page == key)
            st.markdown(f"<div class='nav-item-container {'active' if is_active else ''}'>", unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}"):
                if not is_active:
                    st.switch_page(path)
            st.markdown("</div>", unsafe_allow_html=True)
            
        render_html("""
        <div class="sidebar-diagnostic-card">
            <div class="diagnostic-card-title">
                <span style="color: #C5A059;">◈</span> CLINICAL RIG STATUS
            </div>
            <div class="diagnostic-stat-row">
                <span class="diag-label">Match Precision</span>
                <span class="diag-val" style="color: #E5C2C4;">98.4% Clinically Aligned</span>
            </div>
            <div class="diagnostic-stat-row">
                <span class="diag-label">Active Archive</span>
                <span class="diag-val">50,000+ Formulas</span>
            </div>
            <div class="diagnostic-stat-row">
                <span class="diag-label">Safety Clearance</span>
                <span class="diag-val" style="color: #C5A059;">100% Dermatologist Vetted</span>
            </div>
        </div>
        """)
        
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "assets", 
            "sidebar_model.png"
        )
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.image(
                "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80",
                use_container_width=True
            )
            
        render_html("""
        <div class="sidebar-editorial-caption">
            "Where molecular chemistry meets timeless elegance."
        </div>
        <div class="sidebar-footer">
            <div>© 2026 AURA BIOTECH CLINIC</div>
            <div>PARIS • GENEVA • NEW YORK</div>
        </div>
        """)


def render_header(title, subtitle=None):
    """
    Renders a premium Playfair Display title and subtitle header block with luxury styling.
    """
    sub = f"<p class='header-subtitle'>{subtitle}</p>" if subtitle else ""
    render_html(f"""
    <div class="header-container">
        <h1 class='serif-text header-title'>{title}</h1>
        {sub}
        <div class="header-accent-line"></div>
    </div>
    """)


def render_product_card(brand, product, price, rating, step_number=None, badge_text=None):
    """
    Returns the HTML snippet for a premium styled product card.
    """
    stars = draw_stars(rating)
    badge_html = ""
    if badge_text:
        badge_html = f'<div class="recommend-badge">{badge_text}</div>'
    elif step_number is not None:
        badge_html = f'<div class="recommend-badge"><span>✦</span> STEP {step_number} • CLINICAL MATCH</div>'
        
    return f"""
    <div class="product-card">
        <div>
            {badge_html}
            <div class="brand-badge">{brand}</div>
            <div class="product-title">{product}</div>
        </div>
        <div class="product-meta">
            <div>
                <span class="product-price-label">Price</span>
                <div class="product-price">₹{int(price):,}</div>
            </div>
            <div style="text-align: right;">
                <div class="product-rating">{stars}</div>
                <div class="product-score-badge">{rating} / 5.0 Rating</div>
            </div>
        </div>
    </div>
    """


def render_stat_card(value, label, icon="✦"):
    """
    Returns the HTML snippet for a luxury statistics/metrics box.
    """
    return f"""
    <div class="stat-card">
        <div class="stat-icon-pill">{icon}</div>
        <div class="stat-number">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def render_fallback_disclaimer(concern, skin_type):
    """
    Renders a luxury warning fallback disclaimer box.
    """
    render_html(f"""
    <div class="fallback-disclaimer">
        <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; margin-bottom: 4px; color: #8A4F5C;">
            <span>✦</span> Clinical Archival Note
        </div>
        <div>
            An exact formulation specifically categorized under <strong>{concern}</strong> for <strong>{skin_type}</strong> skin is currently undergoing replenishment in our active archive. Below is the synthesized, dermatologist-approved ritual optimized for your <strong>{skin_type}</strong> profile.
        </div>
    </div>
    """)


def render_clinical_rx_card(lab_name, diag_type, diag_concern, formulas_list, subtitle=None):
    """
    Renders a high-end luxury clinical diagnosis & treatment protocol certificate.
    """
    items_html = ""
    for i, item in enumerate(formulas_list):
        items_html += f"""
        <div class="rx-item">
            <span class="rx-item-num">0{i+1}</span>
            <div class="rx-item-content">
                <strong>Formula {i+1}:</strong> {item}
            </div>
        </div>
        """
        
    sub_text = f"<p style='color: #6B5E59; font-size: 12px; margin: 4px 0 0 0;'>{subtitle}</p>" if subtitle else ""

    return f"""
    <div class="clinical-rx-card">
        <div class="rx-header">
            <div>
                <div class="rx-seal">AURA LAB CERTIFIED</div>
                <div class="rx-title">{lab_name}</div>
                {sub_text}
            </div>
            <div class="rx-badge">[ ⚚ Rx PROTOCOL ]</div>
        </div>
        
        <div class="rx-diagnosis-row">
            <div>
                <span class="rx-label">CLINICAL PROFILE</span>
                <div class="rx-val">{diag_type}</div>
            </div>
            <div>
                <span class="rx-label">TARGET INDICATION</span>
                <div class="rx-val">{diag_concern}</div>
            </div>
        </div>
        
        <div class="rx-protocol-header">PRESCRIBED FORMULATION REGIMEN</div>
        <div class="rx-items-list">
            {items_html}
        </div>
        
        <div class="rx-footer">
            <span>Verified by AI Convolution Biomarker Engine</span>
            <span>Batch: AUR-{abs(hash(diag_type + diag_concern)) % 100000:05d}</span>
        </div>
    </div>
    """
