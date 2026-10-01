# utils/recommender.py

import os
import pandas as pd
import streamlit as st

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "data", 
    "products.csv"
)

@st.cache_data(show_spinner=False)
def load_and_preprocess_dataset():
    """
    Loads products dataset, pre-normalizes lowercase columns for fast indexing,
    and sorts by rating descending so top-tier items are recommended first.
    """
    if os.path.exists(CSV_PATH):
        dataset = pd.read_csv(CSV_PATH)
    else:
        # Fallback dummy data if file is missing
        data = {
            "Category": ["Skin", "Skin", "Hair", "Hair", "Makeup", "Makeup"],
            "Skin_Type": ["Oily", "Dry", "Combination", "Sensitive", "Oily", "Dry"],
            "Hair_Type": ["", "", "Dry", "Oily", "", ""],
            "Concern": ["Acne", "Dryness", "Frizz", "Dandruff", "Daily Makeup", "Party Makeup"],
            "Product": ["Salicylic Cleanser", "Hydrating Cream", "Argan Serum", "Tea Tree Shampoo", "Matte Foundation", "Glow Primer"],
            "Brand": ["CeraVe", "CeraVe", "Moroccanoil", "Paul Mitchell", "Fenty Beauty", "MAC"],
            "Price": [1200, 1500, 3200, 2400, 3600, 4200],
            "Rating": [4.6, 4.8, 4.7, 4.5, 4.8, 4.9]
        }
        dataset = pd.DataFrame(data)

    # Clean & normalize for fast indexed querying
    dataset["Rating"] = pd.to_numeric(dataset["Rating"], errors="coerce").fillna(4.0)
    dataset["Price"] = pd.to_numeric(dataset["Price"], errors="coerce").fillna(0)
    dataset = dataset.sort_values(by="Rating", ascending=False).reset_index(drop=True)

    dataset["_cat_lower"] = dataset["Category"].fillna("").astype(str).str.lower().str.strip()
    dataset["_skin_lower"] = dataset["Skin_Type"].fillna("").astype(str).str.lower().str.strip()
    dataset["_hair_lower"] = dataset["Hair_Type"].fillna("").astype(str).str.lower().str.strip()
    dataset["_concern_lower"] = dataset["Concern"].fillna("").astype(str).str.lower().str.strip()

    return dataset

# Global df reference for backward compatibility
df = load_and_preprocess_dataset()

# Fast cached unique values
@st.cache_data(show_spinner=False)
def get_unique_options():
    skin_mask = df["_cat_lower"] == "skin"
    hair_mask = df["_cat_lower"] == "hair"
    makeup_mask = df["_cat_lower"] == "makeup"

    skin_types = sorted([x.strip() for x in df[skin_mask]["Skin_Type"].dropna().unique() if str(x).strip()])
    skin_concerns = sorted([x.strip() for x in df[skin_mask]["Concern"].dropna().unique() if str(x).strip()])
    hair_types = sorted([x.strip() for x in df[hair_mask]["Hair_Type"].dropna().unique() if str(x).strip()])
    hair_concerns = sorted([x.strip() for x in df[hair_mask]["Concern"].dropna().unique() if str(x).strip()])
    makeup_styles = sorted([x.strip() for x in df[makeup_mask]["Concern"].dropna().unique() if str(x).strip()])

    return {
        "skin_types": skin_types,
        "skin_concerns": skin_concerns,
        "hair_types": hair_types,
        "hair_concerns": hair_concerns,
        "makeup_styles": makeup_styles
    }

options = get_unique_options()

# Recommendation functions with caching & limit
@st.cache_data(show_spinner=False)
def get_skin_recommendations(skin_type, concern, max_items=12):
    s_type = str(skin_type).lower().strip()
    s_concern = str(concern).lower().strip()

    mask_exact = (
        (df["_cat_lower"] == "skin") &
        (df["_skin_lower"] == s_type) &
        (df["_concern_lower"] == s_concern)
    )
    results = df[mask_exact]
    is_fallback = False

    if results.empty:
        mask_fallback = (
            (df["_cat_lower"] == "skin") &
            (df["_skin_lower"] == s_type)
        )
        results = df[mask_fallback]
        is_fallback = True

    if max_items and len(results) > max_items:
        results = results.head(max_items)

    return results, is_fallback

@st.cache_data(show_spinner=False)
def get_hair_recommendations(hair_type, concern, max_items=12):
    h_type = str(hair_type).lower().strip()
    h_concern = str(concern).lower().strip()

    mask_exact = (
        (df["_cat_lower"] == "hair") &
        (df["_hair_lower"] == h_type) &
        (df["_concern_lower"] == h_concern)
    )
    results = df[mask_exact]
    is_fallback = False

    if results.empty:
        mask_fallback = (
            (df["_cat_lower"] == "hair") &
            (df["_hair_lower"] == h_type)
        )
        results = df[mask_fallback]
        is_fallback = True

    if max_items and len(results) > max_items:
        results = results.head(max_items)

    return results, is_fallback

@st.cache_data(show_spinner=False)
def get_makeup_recommendations(skin_type, style, max_items=12):
    s_type = str(skin_type).lower().strip()
    s_style = str(style).lower().strip()

    mask_exact = (
        (df["_cat_lower"] == "makeup") &
        (df["_skin_lower"] == s_type) &
        (df["_concern_lower"] == s_style)
    )
    results = df[mask_exact]
    is_fallback = False

    if results.empty:
        mask_fallback = (
            (df["_cat_lower"] == "makeup") &
            (df["_skin_lower"] == s_type)
        )
        results = df[mask_fallback]
        is_fallback = True

    if max_items and len(results) > max_items:
        results = results.head(max_items)

    return results, is_fallback

# Backward compatible simple recommenders
def recommend_skin_products(skin_type, concern):
    res, _ = get_skin_recommendations(skin_type, concern)
    return res["Product"].tolist()

def recommend_hair_products(hair_type, concern):
    res, _ = get_hair_recommendations(hair_type, concern)
    return res["Product"].tolist()

def recommend_makeup_products(skin_type):
    res, _ = get_makeup_recommendations(skin_type, "")
    return res["Product"].tolist()