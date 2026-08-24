import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT",
    page_icon="👑",
    layout="wide"
)

st.title("👑 JOSS PRONOSTIC EXPERT [VERSION PRO]")
st.write("Le système quantitatif a été réinitialisé avec succès.")

# Test simple de connexion API
API_KEY = "ec0b9b5aa5d841a283d2616e8d5c1471"
HEADERS = {'X-Auth-Token': API_KEY}
url = f"https://api.football-data.org/v4/matches"

try:
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        matchs = res.json().get('matches', [])
        st.success(f"Connexion réussie ! {len(matchs)} matchs récupérés pour analyse.")
        
        for m in matchs[:5]:
            dom = m['homeTeam']['name']
            ext = m['awayTeam']['name']
            st.info(f"⚽ {dom} vs {ext}")
    else:
        st.error("Erreur de connexion à l'API.")
except Exception as e:
    st.error(fErreur : {e}")
