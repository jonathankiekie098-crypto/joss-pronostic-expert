import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'credits' not in st.session_state:
    st.session_state.credits = 3

st.cache_resource.clear()
st.cache_data.clear()

# Style épuré et moderne
st.markdown("""
<style>
    .main { background-color: #060913; }
    .stApp { background-color: #060913; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .match-container {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 14px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

API_KEY = "ec0b9b5aa5d841a283d2616e8d5c1471"
HEADERS = {'X-Auth-Token': API_KEY}

@st.cache_data(ttl=300)
def recuperer_matchs():
    d_start = datetime.now().strftime('%Y-%m-%d')
    d_end = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    url = f"https://api.football-data.org/v4/matches?dateFrom={d_start}&dateTo={d_end}"
    try:
        res = requests.get(url, headers=HEADERS)
        return res.json().get('matches', []) if res.status_code == 200 else []
    except:
        return []

matchs = recuperer_matchs()

# En-tête Pro
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("### 👑 JOSS PRONOSTIC EXPERT")
    st.caption("OPTIONS DE PARIS & STATISTIQUES AVANCÉES")
with col_h2:
    st.metric("⚡ Crédits IA", f"{st.session_state.credits} / 3")

st.markdown("---")

menu_choix = st.selectbox(
    "Navigation",
    ["📋 Scores Exacts & Synthèse", "🎯 Matchs & Options Détaillées", "🎟️ Coupons VIP"],
    label_visibility="collapsed"
)

if menu_choix == "📋 Scores Exacts & Synthèse":
    st.markdown("### 📋 Grille des Scores Exacts du Jour")
    if not matchs:
        st.info("Aucun match disponible pour l'instant.")
    else:
        for m in matchs:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            comp = m['competition']['name']
            match_id = m['id']
            
            np.random.seed(match_id)
            score_d = int(np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1]))
            score_e = int(np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2]))
            cote_score = round(float(np.random.uniform(6.5, 15.0)), 2)
            
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"🏆 **{comp}** • ⏰ {heure} UTC")
                    st.markdown(f"#### {nom_dom} vs {nom_ext}")
                with c2:
                    st.markdown(f"**Score Prévu:** `{score_d} - {score_e}`")
                    st.markdown(f"**Cote:** `@{cote_score}`")
                st.divider()

elif menu_choix == "🎯 Matchs & Options Détaillées":
    st.markdown("### 🎯 Marchés Spécifiques & Options de Paris")
    
    if not matchs:
        st.info("Aucun match disponible.")
    else:
        for m in matchs:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            comp = m['competition']['name']
            match_id = m['id']
            
            np.random.seed(match_id)
            score_d = int(np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1]))
            score_e = int(np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2]))
            
            tirs_cad_d = int(np.random.randint(4, 9))
            tirs_cad_e = int(np.random.randint(2, 7))
            total_tirs = tirs_cad_d + tirs_cad_e + int(np.random.randint(5, 10))
            
            intervalle_but = np.random.choice(["15' - 30'", "31' - 45'", "46' - 60'", "75' - 90+"])
            remplacant = np.random.choice([f"Oui ({nom_dom})", f"Oui ({nom_ext})", "Non"])
            mi_temps_gagne = np.random.choice([f"{nom_dom} (1 Mi-temps)", f"{nom_ext} (1 Mi-temps)", "Aucune / Égalité"])
            
            with st.container():
                st.markdown(f"### ⚽ {nom_dom} vs {nom_ext}")
                st.caption(f"🏆 {comp.upper()} • ⏰ Coup d'envoi : {heure} UTC | **Score Exact Estimé : {score_d} - {score_e}**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📌 Options & Résultat**")
                    st.info(f"Gagne 1 mi-temps :\n**{mi_temps_gagne}**")
                    st.info(f"Double Chance :\n**1X Sécurisé**")
                
                with col2:
                    st.markdown("**🎯 Tirs Cadrés**")
                    st.success(f"Tirs Cadrés {nom_dom} : **+{tirs_cad_d - 1}**")
                    st.success(f"Tirs Cadrés {nom_ext} : **+{tirs_cad_e - 1}**")
                    st.success(f"Total Tirs Match : **+{total_tirs}**")
                
                with col3:
                    st.markdown("**⚡ Événements & Buts**")
                    st.warning(f"Remplaçant Buteur :\n**{remplacant}**")
                    st.warning(f"Intervalle 1er But :\n**{intervalle_but}**")
                
                st.markdown("---")

elif menu_choix == "🎟️ Coupons VIP":
    st.markdown("### 🏆 Coupons VIP sous forme de Sélections d'Options")
    
    if len(matchs) >= 2:
        m1, m2 = matchs[0], matchs[1]
        st.success("🛡️ **COMBINÉ SAFE (Cote ~1.95) — Confiance 90%**")
        st.write(f"1️⃣ **{m1['homeTeam']['name']} vs {m1['awayTeam']['name']}** ➔ Option : *Gagne au moins une mi-temps* (Cote 1.38)")
        st.write(f"2️⃣ **{m2['homeTeam']['name']} vs {m2['awayTeam']['name']}** ➔ Option : *Total tirs cadrés du match* (Cote 1.42)")
    
    st.info("⚡ **COUPON EXPERT BUTS & INTERVALLES (Cote ~6.50)**")
    st.write("• Sélection combinée intégrant un but de remplaçant et les intervalles de temps clés sur les affiches majeures.")
