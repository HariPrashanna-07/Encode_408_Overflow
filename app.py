import streamlit as st  
from utils import fetch_ingredients
from engine import get_ai_reasoning
from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode

st.title("🛡️ Encode: AI Health Co-pilot")

# Initialize session state for barcode if not exists
if "barcode_val" not in st.session_state:
    st.session_state.barcode_val = ""

# User inputs
health_goals = st.text_input("What are your health goals?", placeholder="e.g., Vegan")

# Scanner Toggle
show_scanner = st.checkbox("Show Barcode Scanner")
if show_scanner:
    img_buffer = st.camera_input("Scan a barcode")
    if img_buffer:
        try:
            # Convert to image for processing
            image = Image.open(img_buffer)
            img_array = np.array(image)
            
            # Decode
            decoded_objects = decode(img_array)
            if decoded_objects:
                for obj in decoded_objects:
                    detected_code = obj.data.decode("utf-8")
                    st.success(f"Detected: {detected_code}")
                    # Update session state
                    st.session_state.barcode_val = detected_code
            else:
                st.warning("No barcode detected in this image. Try getting closer or better lighting.")
        except Exception as e:
            st.error(f"Scanner error: {e}")

# Barcode Input (linked to session state)
barcode_input = st.text_input("Scan or show the product", key="barcode_val")

if st.button("Analyze Product"):
    if barcode_input:
        # 1. Fetch data from Open Food Facts
        ingredients = fetch_ingredients(barcode_input)

        if ingredients:
            # 2. Run AI stra
            result = get_ai_reasoning(ingredients, health_goals)
            st.write(f"### Analysis for: {barcode_input}")
            st.success(result)
        else:
            st.error("Product not found in database.")
    else:
        st.warning("Please enter a barcode first.")
