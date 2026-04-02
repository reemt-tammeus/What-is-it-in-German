import streamlit as st
from PIL import Image
import os

# Initialisiere den Fortschritt des Spiels
if 'schritt' not in st.session_state:
    st.session_state.schritt = 1

def naechster_schritt():
    st.session_state.schritt += 1

def reset_spiel():
    st.session_state.schritt = 1

# Ein bisschen Styling für die App
st.title("🗣️ Say it in English!")
st.write("Finde die richtige englische Übersetzung für typische Denglisch-Fehler.")

# Die Dateipfade wurden an den Ordner "Pictures" angepasst
bild_1_pfad = os.path.join("Pictures", "1a.jpg")
bild_2_pfad = os.path.join("Pictures", "1b.jpg")

# --- SCHRITT 1: Das falsche englische Sprichwort ---
if st.session_state.schritt == 1:
    # use_container_width passt das Bild perfekt an die Breite der App an
    st.image(bild_1_pfad, use_container_width=True, caption="Was bedeutet das wirklich?")
    st.button("Tipps anzeigen", on_click=naechster_schritt)

# --- SCHRITT 2: Deutsches Sprichwort + Auswahlmöglichkeiten ---
elif st.session_state.schritt == 2:
    bild2 = Image.open(bild_2_pfad)
    
    # Bild zuschneiden: Wir behalten die oberen 85%, um die Lösung unten links zu verstecken, 
    # aber die Option "c" noch voll lesbar zu lassen.
    breite, hoehe = bild2.size
    oberer_teil = bild2.crop((0, 0, breite, hoehe * 0.85)) 
    
    st.image(oberer_teil, use_container_width=True, caption="Deutsches Sprichwort & Optionen")
    
    st.info("Welche Option ist richtig? a, b oder c? Sprich es jetzt laut aus!")
    st.button("Lösung aufdecken", on_click=naechster_schritt)

# --- SCHRITT 3: Die Auflösung ---
elif st.session_state.schritt == 3:
    # Jetzt zeigen wir das komplette, ungeschnittene Bild
    st.image(bild_2_pfad, use_container_width=True, caption="Die Lösung steht unten links!")
    
    st.success("Hattest du recht? Third time lucky!")
    st.button("Nochmal von vorn", on_click=reset_spiel)