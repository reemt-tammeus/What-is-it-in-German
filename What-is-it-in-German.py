import streamlit as st
from PIL import Image, ImageDraw
import os

# Optional: Setzt den Titel im Browser-Tab
st.set_page_config(page_title="Say it in English", layout="centered")

# Initialisiere den Fortschritt des Spiels
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    if st.session_state.schritt >= 4:
        st.session_state.schritt = 1
    else:
        st.session_state.schritt += 1

st.title("🗣️ Say it in English!")

# Dateipfade
bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")

# --- NEU: Die Farbe für das Abdecken im Dark Mode ---
# Streamlit nutzt standardmäßig diesen dunklen Blaugrau-Ton
masken_farbe = "#0E1117" 

# --- SCHRITT 1: Das falsche englische Sprichwort ---
if st.session_state.schritt == 1:
    st.image(bild_1_pfad, use_container_width=True)

# --- SCHRITT 2, 3 und 4: Das Aufdecken im Dark Mode ---
elif st.session_state.schritt in [2, 3, 4]:
    bild2 = Image.open(bild_2_pfad).convert("RGB")
    breite, hoehe = bild2.size
    
    draw = ImageDraw.Draw(bild2)

    if st.session_state.schritt == 2:
        # Übermalt mit der dunklen Streamlit-Farbe
        draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
        st.image(bild2, use_container_width=True)

    elif st.session_state.schritt == 3:
        draw.rectangle([0, hoehe * 0.85, breite, hoehe], fill=masken_farbe)
        st.image(bild2, use_container_width=True)
        st.subheader("What is the correct English phrase?")

    elif st.session_state.schritt == 4:
        st.image(bild2, use_container_width=True)

# --- DER ZENTRALE SCHALTER ---
st.write("---") 
if st.session_state.schritt < 4:
    st.button("Weiter ➡️", on_click=naechster_schritt, use_container_width=True)
else:
    st.button("Nächstes Sprichwort 🔄", on_click=naechster_schritt, use_container_width=True)
