import streamlit as st
from PIL import Image, ImageDraw
import os

# Setzt den Titel und zentriert das Layout
st.set_page_config(page_title="Say it in English", layout="centered")

# --- NEU: Hintergrund und Abdeckungen auf reines Tiefschwarz synchronisieren ---
masken_farbe = "#000000" 

st.markdown(
    f"""
    <style>
    /* Zwingt den gesamten App-Hintergrund auf reines Schwarz */
    .stApp {{
        background-color: {masken_farbe} !important;
    }}
    /* Stellt sicher, dass der Text gut lesbar bleibt */
    h1, h2, h3, p, span, div {{
        color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# -------------------------------------------------------------------------------

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

# --- SCHRITT 1: Das falsche englische Sprichwort ---
if st.session_state.schritt == 1:
    st.image(bild_1_pfad, use_container_width=True)

# --- SCHRITT 2, 3 und 4: Das Aufdecken ---
elif st.session_state.schritt in [2, 3, 4]:
    bild2 = Image.open(bild_2_pfad).convert("RGB")
    breite, hoehe = bild2.size
    
    draw = ImageDraw.Draw(bild2)

    if st.session_state.schritt == 2:
        # Übermalt mit tiefschwarz
        draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
        st.image(bild2, use_container_width=True)

    elif st.session_state.schritt == 3:
        # Übermalt mit tiefschwarz
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
