import streamlit as st
from PIL import Image, ImageDraw
import os
import json

# Setzt das Layout auf die volle 16:9 Breite
st.set_page_config(page_title="Say it in German", layout="wide")

masken_farbe = "#000000" 

# --- CSS STYLING ---
st.markdown(
    f"""
    <style>
    /* Hintergrund auf reines Schwarz */
    .stApp {{
        background-color: {masken_farbe} !important;
    }}
    /* Standard-Textfarbe weiß */
    h1, h2, p, span, div {{
        color: #FFFFFF !important;
    }}
    
    /* Schrift für die Subheader (Texte) etwas anpassen */
    h3 {{
        color: #FFFFFF !important;
        font-size: 48px !important;
        line-height: 1.3 !important;
    }}

    /* Smartboard-Button - Höhe verkleinert auf 80px */
    .stButton>button {{
        min-height: 80px !important;
        border-radius: 10px;
        border: 3px solid #4CAF50 !important;
        background-color: transparent !important;
        transition: all 0.3s ease-in-out !important;
    }}
    
    /* Schriftgröße im Button verkleinert auf 32px */
    .stButton>button p {{
        font-size: 32px !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
        margin: 0 !important;
    }}

    /* Invertierung der Buttons korrigieren (Hover-Status) */
    .stButton>button:hover {{
        background-color: #4CAF50 !important; 
        border: 3px solid #4CAF50 !important;
    }}
    .stButton>button:hover p {{
        color: #000000 !important; 
    }}
    .stButton>button:active {{
        background-color: #3e8e41 !important;
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

# --- DATEN LADEN ---
# Diese Funktion lädt die JSON-Datei nur einmal und speichert sie im Cache
@st.cache_data
def lade_idiom_daten():
    try:
        with open("idioms.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

idioms_daten = lade_idiom_daten()

# --- SPIEL-LOGIK ---
# Initialisiere den Fortschritt und den Bild-Index
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1
if 'idiom_index' not in st.session_state:
    st.session_state.idiom_index = 0

def naechster_schritt():
    if st.session_state.schritt >= 4:
        # Reset auf Schritt 1 für das nächste Bild
        st.session_state.schritt = 1
        # Gehe zum nächsten Bild-Paar, oder fange wieder bei 0 an, wenn wir am Ende sind
        if st.session_state.idiom_index < len(idioms_daten) - 1:
            st.session_state.idiom_index += 1
        else:
            st.session_state.idiom_index = 0
    else:
        st.session_state.schritt += 1

# Überprüfen, ob Daten geladen wurden
if not idioms_daten:
    st.error("Fehler: Konnte 'idioms.json' nicht finden. Bitte erstelle die Datei im selben Ordner.")
else:
    # Aktuelle Bildpfade dynamisch aus der JSON-Datei laden
    aktuelles_idiom = idioms_daten[st.session_state.idiom_index]
    bild_1_pfad = os.path.join("Pictures", aktuelles_idiom["image_a"])
    bild_2_pfad = os.path.join("Pictures", aktuelles_idiom["image_b"])

    # --- LAYOUT-AUFTEILUNG (1:1) ---
    col_bild, col_steuerung = st.columns([1, 1], gap="large")

    # RECHTE SEITE: Steuerung und Texte
    with col_steuerung:
        st.write("")
        st.write("")
        st.title("")
        st.write("---")
        
        if st.session_state.schritt == 1:
            st.subheader("What is the German idiom?")
        elif st.session_state.schritt == 2:
            st.subheader("")
        elif st.session_state.schritt == 3:
            st.subheader("What is the correct English phrase?")
        elif st.session_state.schritt == 4:
            st.subheader("Here is the correct answer!")
            
        st.write("---")
        
        if st.session_state.schritt < 4:
            st.button("Go on", on_click=naechster_schritt, use_container_width=True)
        else:
            st.button("Next idiom", on_click=naechster_schritt, use_container_width=True)
        
        # Zeigt an, bei welchem Bild ihr gerade seid
        st.markdown(f"<p style='text-align: right; color: gray;'>Idiom {st.session_state.idiom_index + 1} / {len(idioms_daten)}</p>", unsafe_allow_html=True)

    # LINKE SEITE: Bildanzeige und Aufdecken
    with col_bild:
        try:
            if st.session_state.schritt == 1:
                st.image(bild_1_pfad, use_container_width=True)

            elif st.session_state.schritt in [2, 3, 4]:
                # Lade das zweite Bild und bereite es zum Zeichnen vor
                bild2 = Image.open(bild_2_pfad).convert("RGB")
                breite, hoehe = bild2.size
                draw = ImageDraw.Draw(bild2)

                if st.session_state.schritt == 2:
                    draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
                    st.image(bild2, use_container_width=True)

                elif st.session_state.schritt == 3:
                    # HIER GEÄNDERT: Startet das Zeichnen erst bei 93% (verdeckt nur 7% für 2-zeilige Antworten)
                    draw.rectangle([0, hoehe * 0.93, breite, hoehe], fill=masken_farbe)
                    st.image(bild2, use_container_width=True)

                elif st.session_state.schritt == 4:
                    st.image(bild2, use_container_width=True)
        except FileNotFoundError:
            st.error(f"Fehler: Konnte das Bild nicht finden. Bitte stelle sicher, dass {bild_1_pfad} und {bild_2_pfad} existieren.")
