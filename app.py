import streamlit as st
from utils import fetch_ingredients
from engine import get_ai_reasoning


st.title("🛡️ Encode: AI Health Co-pilot")

# Session state
if "barcode_val" not in st.session_state:
    st.session_state.barcode_val = ""

# User goal
health_goals = st.text_input(
    "What are your health goals?",
    placeholder="e.g., Vegan"
)

# Camera input (AI-native, no decoding)
img = st.camera_input("Show the product")

if img:
    image = Image.open(img)
    st.image(image, caption="Product shown", use_container_width=True)
    st.info("Looking for ingredients that matter to you…")

# Manual barcode input (fallback)
barcode_input = st.text_input(
    "Enter product barcode (optional)",
    key="barcode_val"
)

if st.button("Analyze Product"):
    if barcode_input:
        ingredients = fetch_ingredients(barcode_input)

        if ingredients:
            result = get_ai_reasoning(ingredients, health_goals)
            st.write(f"### Analysis for: {barcode_input}")
            st.success(result)
        else:
            st.error("Product not found.")
    else:
        st.warning("Please enter a barcode or show a product.")
