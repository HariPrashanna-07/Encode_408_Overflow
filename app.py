import streamlit as st
hi
from utils import fetch_ingredients
from engine import get_ai_reasoning

st.title("🛡️ Encode: AI Health Co-pilot")

# Session state
if "barcode_val" not in st.session_state:
    st.session_state.barcode_val = ""

# Health goal
health_goals = st.text_input(
    "What are your health goals?",
    placeholder="e.g., Vegan"
)

# Product input
barcode_input = st.text_input(
    "Enter product barcode",
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
        st.warning("Please enter a barcode.")
