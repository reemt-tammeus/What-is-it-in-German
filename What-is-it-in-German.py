import streamlit as st
from PIL import Image, ImageDraw
import os

st.set_page_config(page_title="Say it in English", layout="wide")

masken_farbe = "#000000" 

st.markdown(
    f"""
    <style>
    /* Hintergrund auf reines Schwarz */
    .stApp {{
        background-color: {masken_farbe} !important;
    }}
    /* Textfarbe weiß */
    h1, h2, h3, p, span, div {{
        color: #FFFFFF !important;
    }}
    /* Großer Smartboard-Button */
    .stButton>button {{
        height: 80px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }}
    
    /* --- DER WICHTIGE NEUE TEIL --- */
    /* Zwingt das Bild, IMMER komplett auf den Bildschirm zu passen */
    [data-testid="stImage"] img {{
        max-height: 85vh !important; /* Maximal 85% der Bildschirmhöhe */
        width: auto !important;      /* Breite passt sich automatisch an */
        object-fit: contain !important; /* Bild wird nicht verzerrt */
        margin: 0 auto !important;   /* Zentriert das Bild in der linken Spalte */
        display: block !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialisiere den Fortschritt des Spiels
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    if st.session_state.schritt >= 4:
        st.session_state.schritt = 1
    else:
        st.session_state.schritt += 1

bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")


# Zwei Spalten. Links: Bild (2 Anteile). Rechts: Steuerung (1 Anteil).
col_bild, col_steuerung = st.columns([2, 1], gap="large")

with col_steuerung:
    st.title("🗣️ Say it in English!")
    st.write("---")
    
    if st.session_state.schritt == 1:
        st.subheader("🤔 Was bedeutet das wirklich?")
    elif st.session_state.schritt == 2:
        st.subheader("📖 Deutsches Sprichwort & Optionen")
    elif st.session_state.schritt == 3:
        st.subheader("❓ What is the correct English phrase?")
        st.info("Sprich deine Antwort jetzt laut aus!")
    elif st.session_state.schritt == 4:
        st.subheader("✅ Die Lösung!")
        st.success("Hattest du recht?")
        
    st.write("---")
    
    if st.session_state.schritt < 4:
        st.button("Weiter ➡️", on_click=naechster_schritt, use_container_width=True)
    else:
        st.button("Nächstes Sprichwort 🔄", on_click=naechster_schritt, use_container_width=True)


with col_bild:
    # use_container_width=True wird jetzt durch unser CSS überschrieben, 
    # sobald das Bild droht, zu hoch für den Bildschirm zu werden!
    if st.session_state.schritt == 1:
        st.image(bild_1_pfad, use_container_width=True)

    elif st.session_state.schritt in [2, 3, 4]:
        bild2 = Image.open(bild_2_pfad).convert("RGB")
        breite, hoehe = bild2.size
        draw = ImageDraw.Draw(bild2)

        if st.session_state.schritt == 2:
            draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)

        elif st.session_state.schritt == 3:
            draw.rectangle([0, hoehe * 0.85, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)

        elif st.session_state.schritt == 4:
            st.image(bild2, use_container_width=True)
