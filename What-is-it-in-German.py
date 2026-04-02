import streamlit as st
from PIL import Image, ImageDraw
import os

# Setzt das Layout auf die volle 16:9 Breite
st.set_page_config(page_title="Say it in English", layout="wide")

masken_farbe = "#000000" 

# --- CSS STYLING ---
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
    
    /* Zentriert das Bild in seiner Spalte */
    [data-testid="stImage"] {{
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }}
    
    /* Zwingt das Bild, IMMER 85% der Bildschirmhöhe einzunehmen */
    [data-testid="stImage"] img {{
        height: 85vh !important;     
        width: auto !important;      
        max-width: 100% !important;  
        object-fit: contain !important; 
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- SPIEL-LOGIK ---
# Initialisiere den Fortschritt des Spiels
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    if st.session_state.schritt >= 4:
        st.session_state.schritt = 1
    else:
        st.session_state.schritt += 1

# Dateipfade anpassen (Ordner 'Pictures')
bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")

# --- LAYOUT-AUFTEILUNG (1:1) ---
col_bild, col_steuerung = st.columns([1, 1], gap="large")

# RECHTE SEITE: Steuerung und Texte
with col_steuerung:
    st.write("")
    st.write("")
    st.title("🗣️ Say it in English!")
    st.write("---")
    
    if st.session_state.schritt == 1:
        st.subheader("🤔 What is the German idiom?")
    elif st.session_state.schritt == 2:
        st.subheader("📖 German idiom & Options") 
    elif st.session_state.schritt == 3:
        st.subheader("❓ What is the correct English phrase?")
    elif st.session_state.schritt == 4:
        st.subheader("✅ The correct answer!")
        st.success("Did you choose the right solution?")
        
    st.write("---")
    
    if st.session_state.schritt < 4:
        st.button("Go on ➡️", on_click=naechster_schritt, use_container_width=True)
    else:
        st.button("Next idiom 🔄", on_click=naechster_schritt, use_container_width=True)

# LINKE SEITE: Bildanzeige und Aufdecken
with col_bild:
    if st.session_state.schritt == 1:
        st.image(bild_1_pfad, use_container_width=True)

    elif st.session_state.schritt in [2, 3, 4]:
        # Lade das zweite Bild und bereite es zum Zeichnen vor
        bild2 = Image.open(bild_2_pfad).convert("RGB")
        breite, hoehe = bild2.size
        draw = ImageDraw.Draw(bild2)

        if st.session_state.schritt == 2:
            # Übermalt alles unterhalb von 25% (Lösung + Optionen versteckt)
            draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)

        elif st.session_state.schritt == 3:
            # Übermalt alles unterhalb von 85% (Nur Lösung unten links versteckt)
            draw.rectangle([0, hoehe * 0.85, breite, hoehe], fill=masken_farbe)
            st.image(bild2, use_container_width=True)

        elif st.session_state.schritt == 4:
            # Zeigt das komplette Bild unmaskiert
            st.image(bild2, use_container_width=True)
