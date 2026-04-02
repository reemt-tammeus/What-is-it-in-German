import streamlit as st
from PIL import Image
import os

# Initialisiere den Fortschritt des Spiels (jetzt 4 Schritte)
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    # Nach Schritt 4 fangen wir wieder bei 1 an
    if st.session_state.schritt >= 4:
        st.session_state.schritt = 1
    else:
        st.session_state.schritt += 1

# Styling
st.title("🗣️ Say it in English!")

# Dateipfade
bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")

# --- SCHRITT 1: Das falsche englische Sprichwort ---
if st.session_state.schritt == 1:
    st.image(bild_1_pfad, use_container_width=True)

# --- SCHRITT 2: Nur die oberen 25% des zweiten Bildes (Deutsches Sprichwort) ---
elif st.session_state.schritt == 2:
    bild2 = Image.open(bild_2_pfad)
    breite, hoehe = bild2.size
    
    # Schneidet nur die oberen 25% aus
    oberer_teil = bild2.crop((0, 0, breite, hoehe * 0.25)) 
    st.image(oberer_teil, use_container_width=True)

# --- SCHRITT 3: Obere 25% + mittlere 60% (Auswahlmöglichkeiten) ---
elif st.session_state.schritt == 3:
    bild2 = Image.open(bild_2_pfad)
    breite, hoehe = bild2.size
    
    # Schneidet die oberen 85% aus (25% oben + 60% Mitte)
    mittlerer_teil = bild2.crop((0, 0, breite, hoehe * 0.85)) 
    st.image(mittlerer_teil, use_container_width=True)
    
    # Die geforderte Aufforderung
    st.subheader("What is the correct English phrase?")

# --- SCHRITT 4: Die kompletten 100% (inkl. der unteren 15% Lösung) ---
elif st.session_state.schritt == 4:
    # Zeigt das ungeschnittene Bild
    st.image(bild_2_pfad, use_container_width=True)


# --- DER ZENTRALE SCHALTER ---
# Wir machen den Button über die ganze Breite (use_container_width=True), 
# damit er leicht zu klicken ist.
st.write("---") # Eine visuelle Trennlinie
if st.session_state.schritt < 4:
    st.button("Weiter ➡️", on_click=naechster_schritt, use_container_width=True)
else:
    st.button("Nächstes Sprichwort 🔄", on_click=naechster_schritt, use_container_width=True)
