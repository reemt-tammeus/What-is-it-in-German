import streamlit as st
from PIL import Image, ImageDraw
import os
import json
import random

# Setzt das Layout auf die volle 16:9 Breite und den Tab-Titel
st.set_page_config(page_title="I spider", layout="wide")

masken_farbe = "#000000" 

# --- CSS STYLING ---
st.markdown(
    f"""
    <style>
    /* Hintergrund auf reines Schwarz */
    .stApp {{
        background-color: {masken_farbe} !important;
    }}
    
    /* Standard-Textfarbe weiß (außerhalb des Dropdowns) */
    .main h1, .main h2, .main p, .main span, .main label {{
        color: #FFFFFF !important;
    }}
    
    /* Nimmt das obere Padding weg, ERLAUBT ABER SCROLLEN falls der Bildschirm extrem klein ist (kein Abschneiden mehr!) */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 98% !important;
    }}

    /* Textformatierung */
    h3 {{
        color: #FFFFFF !important;
        font-size: 42px !important;
        line-height: 1.3 !important;
        text-align: center !important;
        margin-top: 20px !important;
        margin-bottom: 30px !important;
    }}

    /* Smartboard-Button */
    .stButton>button {{
        min-height: 80px !important;
        border-radius: 10px;
        border: 3px solid #4CAF50 !important;
        background-color: transparent !important;
        transition: all 0.3s ease-in-out !important;
    }}
    
    .stButton>button p {{
        font-size: 32px !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
        margin: 0 !important;
    }}

    .stButton>button:hover {{
        background-color: #4CAF50 !important; 
        border: 3px solid #4CAF50 !important;
    }}
    .stButton>button:hover p {{
        color: #000000 !important; 
    }}
    
    /* BILDGRÖSSE BLEIBT AUF 85% */
    [data-testid="stImage"] {{
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }}
    
    [data-testid="stImage"] img {{
        height: 85vh !important;     
        width: auto !important;      
        max-width: 100% !important;  
        object-fit: contain !important; 
    }}
    
    /* --- DROP-DOWN STYLING REPARIERT --- */
    /* Geschlossener Zustand */
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: #111111 !important;
        border: 2px solid #FFFFFF !important;
    }}
    .stSelectbox div[data-baseweb="select"] span {{
        color: #FFFFFF !important;
        font-size: 24px !important;
    }}
    
    /* Geöffneter Zustand (Dropdown-Liste) -> Erzwungen auf schwarze Schrift für Lesbarkeit */
    div[data-baseweb="popover"] li {{
        color: #000000 !important; 
        font-size: 20px !important;
    }}
    div[data-baseweb="popover"] li:hover {{
        background-color: #4CAF50 !important;
        color: #000000 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- DATEN LADEN ---
@st.cache_data
def lade_idiom_daten():
    try:
        with open("idioms.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

all_idioms_daten = lade_idiom_daten()

# --- SET-WECHSEL LOGIK ---
def wechsle_set():
    auswahl = st.session_state.set_auswahl_box
    set_nummer = int(auswahl.split(" ")[1])
    
    if set_nummer < 10:
        start_index = (set_nummer - 1) * 6
        end_index = start_index + 6
    else: 
        start_index = 54
        end_index = 59
        
    pool = all_idioms_daten[start_index:end_index]
    random.shuffle(pool)
    
    st.session_state.aktuelle_set_shuffled = pool
    st.session_state.idiom_index = 0
    st.session_state.schritt = 1

# --- INITIALISIERUNG DES SESSION STATE ---
if 'idiom_index' not in st.session_state:
    st.session_state.idiom_index = 0
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1
if 'aktuelle_set_shuffled' not in st.session_state:
    if all_idioms_daten:
        pool = all_idioms_daten[0:6]
        random.shuffle(pool)
        st.session_state.aktuelle_set_shuffled = pool

if not all_idioms_daten:
    st.error("Fehler: Konnte 'idioms.json' nicht finden. Bitte erstelle die Datei im selben Ordner.")
else:
    set_optionen = [f"Set {i} (Idioms {(i-1)*6+1}-{i*6})" for i in range(1, 10)]
    set_optionen.append("Set 10 (Idioms 55-59)")

    def naechster_schritt():
        aktuelle_bilder = st.session_state.aktuelle_set_shuffled
        if st.session_state.schritt >= 4:
            st.session_state.schritt = 1
            if st.session_state.idiom_index < len(aktuelle_bilder) - 1:
                st.session_state.idiom_index += 1
            else:
                st.session_state.idiom_index = 0
        else:
            st.session_state.schritt += 1

    # --- HAUPT-LAYOUT (2 SPALTEN) ---
    col_bild, col_steuerung = st.columns([1, 1], gap="large")

    # LINKE SEITE: Großes Bild
    with col_bild:
        aktuelle_set_bilder = st.session_state.aktuelle_set_shuffled
        if st.session_state.idiom_index < len(aktuelle_set_bilder):
            aktuelles_idiom = aktuelle_set_bilder[st.session_state.idiom_index]
            bild_1_pfad = os.path.join("Pictures", aktuelles_idiom["image_a"])
            bild_2_pfad = os.path.join("Pictures", aktuelles_idiom["image_b"])
            
            try:
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
                        # HIER GEÄNDERT: Maske auf 12% hochgezogen (0.88 statt 0.90), damit auch bei Bild 1 der rote Kreis weg ist
                        draw.rectangle([0, hoehe * 0.88, breite, hoehe], fill=masken_farbe)
                        st.image(bild2, use_container_width=True)

                    elif st.session_state.schritt == 4:
                        st.image(bild2, use_container_width=True)
            except FileNotFoundError:
                st.error(f"Bild nicht gefunden: {bild_1_pfad} oder {bild_2_pfad}")

    # RECHTE SEITE: Steuerung 
    with col_steuerung:
        # 1. LOGO OBEN RECHTS
        col_leer, col_logo_bild = st.columns([6, 4])
        with col_logo_bild:
            try:
                st.image("I spider.png", use_container_width=True)
            except FileNotFoundError:
                st.warning("Logo nicht gefunden")
        
        # 2. SET-AUSWAHL
        st.selectbox(
            "Wähle dein Set:",
            options=set_optionen,
            key="set_auswahl_box",
            on_change=wechsle_set,
            label_visibility="collapsed"
        )
        
        # 3. TEXTE (Mit sanftem Abstand nach oben und unten)
        text_anzeige = ""
        if st.session_state.schritt == 1:
            text_anzeige = "What is the German idiom?"
        elif st.session_state.schritt == 2:
            text_anzeige = "Recognize the idiom in German!"
        elif st.session_state.schritt == 3:
            text_anzeige = "What is the correct English phrase?"
        elif st.session_state.schritt == 4:
            text_anzeige = "Here is the correct answer!"
            
        st.markdown(f"<h3>{text_anzeige}</h3>", unsafe_allow_html=True)
        
        # 4. BUTTON (Zentriert)
        col_spacer1, col_btn, col_spacer2 = st.columns([1, 2, 1])
        with col_btn:
            if st.session_state.schritt < 4:
                st.button("Go on", on_click=naechster_schritt, use_container_width=True)
            else:
                st.button("Next idiom", on_click=naechster_schritt, use_container_width=True)
        
        # 5. COUNTER 
        st.markdown(f"<p style='text-align: right; color: gray; margin-top: 15px;'>Idiom {st.session_state.idiom_index + 1} / {len(st.session_state.aktuelle_set_shuffled)}</p>", unsafe_allow_html=True)
