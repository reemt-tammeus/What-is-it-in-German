import streamlit as st
from PIL import Image, ImageDraw
import os

# WICHTIG: layout="wide" nutzt die volle 16:9 Breite der digitalen Tafel
st.set_page_config(page_title="Say it in English", layout="wide")

masken_farbe = "#000000" 

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {masken_farbe} !important;
    }}
    h1, h2, h3, p, span, div {{
        color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    if st.session_state.schritt >= 4:
        st.session_state.schritt = 1
    else:
        st.session_state.schritt += 1

bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")

# --- LAYOUT-AUFTEILUNG ---
# col_bild bekommt Faktor 1.5 (größer), col_text bekommt Faktor 1.0 (kleiner)
col_bild, col_text = st.columns([1.5, 1], gap="large")

# --- RECHTE SPALTE (Steuerung & Text) ---
with col_text:
    st.title("🗣️ Say it in English!")
    st.write("---")
    
    # Wir erstellen einen Platzhalter für den Text. 
    # So können wir den Text aus der linken Spalte heraus ändern, 
    # je nachdem, welches Bild gerade geladen wird.
    text_platzhalter = st.empty()
    
    st.write("---")
    
    # Der Button ist jetzt immer bequem auf der rechten Seite greifbar
    if st.session_state.schritt < 4:
        st.button("Weiter ➡️", on_click=naechster_schritt, use_container_width=True)
    else:
        st.button("Nächstes Sprichwort 🔄", on_click=naechster_schritt, use_container_width=True)

# --- LINKE SPALTE (Bilder) ---
with col_bild:
    if st.session_state.schritt == 1:
        st.image(bild_1_pfad, use_container_width=True)
        # Text in die rechte Spalte schicken
        text_platzhalter.subheader("🤔 Was bedeutet das wirklich?")

    elif st.session_state.schritt in [2, 3, 4]:
        bild2 = Image.open(bild_2_pfad).convert("RGB")
        breite, hoehe = bild2.size
        
        draw = ImageDraw.Draw(bild2)

        if st.session_state.schritt == 2:
            draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)
            text_platzhalter.subheader("🇩🇪 Deutsches Sprichwort")

        elif st.session_state.schritt == 3:
            draw.rectangle([0, hoehe * 0.85, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)
            text_platzhalter.subheader("🇬🇧 What is the correct English phrase?")

        elif st.session_state.schritt == 4:
            st.image(bild2, use_container_width=True)
            text_platzhalter.success("🎉 Die Lösung steht unten links!")
