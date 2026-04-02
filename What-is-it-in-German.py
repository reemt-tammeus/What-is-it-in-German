import streamlit as st
from PIL import Image, ImageDraw
import os

# WICHTIG: layout="wide" zwingt Streamlit, die volle Bildschirmbreite zu nutzen (16:9 Format)
st.set_page_config(page_title="Say it in English", layout="wide")

# Hintergrund und Abdeckungen auf reines Tiefschwarz
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
    /* NEU: Macht den Button größer und Smartboard-freundlicher */
    .stButton>button {{
        height: 80px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #4CAF50;
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

# Dateipfade
bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")


# --- NEU: DAS SPALTEN-LAYOUT FÜR 16:9 ---
# Wir erstellen zwei Spalten. Die linke Spalte (Bild) ist doppelt so breit wie die rechte (Steuerung).
col_bild, col_steuerung = st.columns([2, 1], gap="large")

# Alles, was im `with col_steuerung:` Block steht, landet auf der rechten Seite des Bildschirms
with col_steuerung:
    st.title("🗣️ Say it in English!")
    st.write("---")
    
    # Der Begleittext ändert sich je nach Schritt dynamisch auf der rechten Seite
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
    
    # Der Button liegt nun permanent rechts und rutscht nicht mehr nach unten
    if st.session_state.schritt < 4:
        st.button("Weiter ➡️", on_click=naechster_schritt, use_container_width=True)
    else:
        st.button("Nächstes Sprichwort 🔄", on_click=naechster_schritt, use_container_width=True)


# Alles, was im `with col_bild:` Block steht, landet groß auf der linken Seite
with col_bild:
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
