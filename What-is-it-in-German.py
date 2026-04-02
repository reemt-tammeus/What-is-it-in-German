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
    
    /* --- DIE LÖSUNG FÜR DIE PROPORTIONEN --- */
    /* Macht den Bild-Container zu einer Flexbox und zentriert alles */
    [data-testid="stImage"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 80vh !important; /* Nimmt 80% der Bildschirmhöhe ein */
    }}
    
    /* Zwingt das Bild, den Container perfekt auszufüllen, ohne zu verzerren */
    [data-testid="stImage"] img {{
        max-height: 100% !important;
        max-width: 100% !important;
        width: auto !important; 
        object-fit: contain !important;
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

# --- SPALTEN AUF 1:1 ANGEPASST ---
col_bild, col_steuerung = st.columns([1, 1], gap="large")

with col_steuerung:
    # Ein paar leere Zeilen, damit die Steuerung vertikal weiter unten startet
    st.write("")
    st.write("")
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
    # use_container_width=True wurde entfernt, da unser neues CSS jetzt 
    # die perfekte, mittige Skalierung übernimmt!
    if st.session_state.schritt == 1:
        st.image(bild_1_pfad)

    elif st.session_state.schritt in [2, 3, 4]:
        bild2 = Image.open(bild_2_pfad).convert("RGB")
        breite, hoehe = bild2.size
        draw = ImageDraw.Draw(bild2)

        if st.session_state.schritt == 2:
            draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
            st.image(bild2)

        elif st.session_state.schritt == 3:
            draw.rectangle([0, hoehe * 0.85, breite, hoehe], fill=masken_farbe)
            st.image(bild2)

        elif st.session_state.schritt == 4:
            st.image(bild2)
