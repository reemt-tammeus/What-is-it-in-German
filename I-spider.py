import streamlit as st
from PIL import Image, ImageDraw
import os
import json
import random

# Setzt das Layout auf die volle 16:9 Breite und den Tab-Titel
st.set_page_config(page_title="I spider", layout="wide")

masken_farbe = "#000000" 

# --- CSS STYLING ---
# Zuerst ein paar globale Styles, dann spezifische CSS-Positionierung
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
        margin-top: 0 !important;
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

    /* Hover-Status der Buttons */
    .stButton>button:hover {{
        background-color: #4CAF50 !important; 
        border: 3px solid #4CAF50 !important;
    }}
    .stButton>button:hover p {{
        color: #000000 !important; 
    }}
    
    /* Bildzentrierung und feste Höhe */
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
    
    /* DROP-DOWN STYLING (Set-Auswahl) */
    .stSelectbox div[data-baseweb="select"] {{
        font-size: 24px !important;
        border: 2px solid #FFFFFF !important;
    }}
    .stSelectbox label {{
        font-size: 20px !important;
        color: #FFFFFF !important;
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

# --- INITIALISIERUNG DES SESSION STATE ---
# Damit die App nach einem Absturz weiß, wo sie war
if 'idiom_index' not in st.session_state:
    st.session_state.idiom_index = 0
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1
if 'aktuelle_set_shuffled' not in st.session_state:
    st.session_state.aktuelle_set_shuffled = []
if 'ausgewaehltes_set_text' not in st.session_state:
    st.session_state.ausgewaehltes_set_text = ""

# Überprüfen, ob Daten geladen wurden
if not all_idioms_daten:
    st.error("Fehler: Konnte 'idioms.json' nicht finden. Bitte erstelle die Datei im selben Ordner.")
else:
    # --- HEADER-AUFTEILUNG (Titel links, Logo rechts) ---
    col_titel, col_logo = st.columns([85, 15], gap="medium")
    with col_titel:
        st.title("I spider")
    with col_logo:
        # Logo zentriert und passend groß anzeigen
        try:
            st.image("I spider.png", use_container_width=True)
        except FileNotFoundError:
            st.error("Logo 'I spider.png' nicht gefunden.")

    # --- SET-AUSWAHL (Oben) ---
    st.write("### Menü")
    set_optionen = [f"Set {i} (Idioms {(i-1)*6+1}-{i*6})" for i in range(1, 10)]
    set_optionen.append("Set 10 (Idioms 55-59)") # Set 10 hat nur 5
    
    auswahl = st.selectbox(
        "Wähle das Set für diesen Leerlauf:",
        options=set_optionen,
        key="set_selection"
    )

    # --- LOGIK: WELCHE BILDER GEHÖREN ZUM SET? (Mit Mini-Shuffle) ---
    # Wir extrahieren die Zahl aus "Set X"
    set_nummer = int(auswahl.split(" ")[1])
    
    # Prüfen, ob sich die Set-Auswahl geändert hat. 
    # Wenn ja, mischen wir den Pool für dieses Set neu!
    if st.session_state.ausgewaehltes_set_text != auswahl:
        # Feste Indizes für die Sets festlegen
        if set_nummer < 10:
            start_index = (set_nummer - 1) * 6
            end_index = start_index + 6
        else: # Set 10
            start_index = 54
            end_index = 59
            
        # Wir schneiden uns exakt diese Bilder aus der großen JSON-Liste heraus
        # und mischen NUR DIESE 6 BILDER im aktuellen Durchlauf
        pool = all_idioms_daten[start_index:end_index]
        random.shuffle(pool)
        
        # Neuen Pool und neue Set-Text im Session State speichern
        st.session_state.aktuelle_set_shuffled = pool
        st.session_state.ausgewaehltes_set_text = auswahl
        st.session_state.idiom_index = 0
        st.session_state.schritt = 1 # Auch Schritt resetten beim Set-Wechsel

    # Aktuellen Pool aus dem Session State holen
    aktuelle_set_bilder = st.session_state.aktuelle_set_shuffled

    # --- SPIEL-FUNKTIONEN ---
    def naechster_schritt():
        if st.session_state.schritt >= 4:
            # Reset auf Schritt 1 für das nächste Bild
            st.session_state.schritt = 1
            # Gehe zum nächsten Bild-Paar, oder fange wieder bei 0 an, wenn das Set durch ist
            if st.session_state.idiom_index < len(aktuelle_set_bilder) - 1:
                st.session_state.idiom_index += 1
            else:
                st.session_state.idiom_index = 0
        else:
            st.session_state.schritt += 1

    # Aktuelle Bildpfade dynamisch aus dem gemischten Set laden
    if st.session_state.idiom_index < len(aktuelle_set_bilder):
        aktuelles_idiom = aktuelle_set_bilder[st.session_state.idiom_index]
        bild_1_pfad = os.path.join("Pictures", aktuelles_idiom["image_a"])
        bild_2_pfad = os.path.join("Pictures", aktuelles_idiom["image_b"])

        # --- LAYOUT-AUFTEILUNG (1:1) ---
        st.write("---") # Trennlinie
        col_bild, col_steuerung = st.columns([1, 1], gap="large")

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
                        # Oben links wird nur der obere Teil gezeigt (Deutsches Sprichwort)
                        draw.rectangle([0, hoehe * 0.25, breite, hoehe], fill=masken_farbe)
                        st.image(bild2, use_container_width=True)

                    elif st.session_state.schritt == 3:
                        # Unterer Abschnitt auf 10% (0.90) verdeckt nur die Lösung
                        draw.rectangle([0, hoehe * 0.90, breite, hoehe], fill=masken_farbe)
                        st.image(bild2, use_container_width=True)

                    elif st.session_state.schritt == 4:
                        st.image(bild2, use_container_width=True)
            except FileNotFoundError:
                st.error(f"Fehler: Konnte das Bild nicht finden. Bitte stelle sicher, dass {bild_1_pfad} und {bild_2_pfad} existieren.")

        # RECHTE SEITE: Steuerung und Texte
        with col_steuerung:
            st.write("")
            st.write("")
            st.title("")
            st.write("---")
            
            if st.session_state.schritt == 1:
                st.subheader("What is the German idiom?")
            elif st.session_state.schritt == 2:
                st.subheader("Recognize the idiom in German!")
            elif st.session_state.schritt == 3:
                st.subheader("What is the correct English phrase?")
            elif st.session_state.schritt == 4:
                st.subheader("Here is the correct answer!")
                
            st.write("---")
            
            # Button wird in eine zentrierte, schmalere Spalte gelegt
            # Die Zahlen [1, 2, 1] bedeuten: 25% Platz links, 50% für den Button, 25% Platz rechts
            col_spacer1, col_btn, col_spacer2 = st.columns([1, 2, 1])
            with col_btn:
                if st.session_state.schritt < 4:
                    st.button("Go on", on_click=naechster_schritt, use_container_width=True)
                else:
                    st.button("Next idiom", on_click=naechster_schritt, use_container_width=True)
            
            # Zeigt an, bei welchem Bild ihr gerade im Set seid
            st.markdown(f"<p style='text-align: right; color: gray;'>Idiom {st.session_state.idiom_index + 1} / {len(aktuelle_set_bilder)} ({auswahl})</p>", unsafe_allow_html=True)

    else:
        # Dieser Fall sollte nicht eintreten, hilft aber beim Debuggen
        st.error(f"Fehler beim Laden des Idioms (Index {st.session_state.idiom_index})")
