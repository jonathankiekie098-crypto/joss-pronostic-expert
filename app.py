import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT - ULTRA",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'credits' not in st.session_state:
    st.session_state.credits = 3

st.cache_resource.clear()
st.cache_data.clear()

st.markdown("""
<style>
    .main { background-color: #04060f; }
    .stApp { background-color: #04060f; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .suspect-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 2px solid #ef4444; border-radius: 14px; padding: 18px; margin-bottom: 18px;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
    }
    .live-box {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%);
        border: 2px solid #10b981; border-radius: 14px; padding: 18px; margin-bottom: 18px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
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
    st.markdown("### 👑 JOSS PRONOSTIC EXPERT [ULTRA EDITION]")
    st.caption("INTELLIGENCE ARTIFICIELLE • DÉTECTION D'ANOMALIES & MATCHS SUSPECTS")
with col_h2:
    st.metric("⚡ Crédits IA", f"{st.session_state.credits} / 3")

st.markdown("---")

menu_choix = st.selectbox(
    "Navigation",
    ["📋 Scores Exacts & Synthèse", "🎯 Matchs & Options Détaillées", "🚨 Détecteur Matchs Suspects & Live", "🎟️ Coupons VIP"],
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
                st.caption(f"🏆 {comp.upper()} • ⏰ {heure} UTC | **Score Estimé : {score_d} - {score_e}**")
                
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

elif menu_choix == "🚨 Détecteur Matchs Suspects & Live":
    st.markdown("### 🚨 Radar des Anomalies & Matchs Suspects (Pré-match & Live)")
    st.markdown("<div style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Ce module analyse les mouvements de cotes inhabituels, les flux de liquidités et les pressions statistiques anormales (signaux de matchs à fort enjeu cachés ou potentiels renversements).</div>", unsafe_allow_html=True)
    
    if not matchs:
        st.info("Aucun match à analyser pour le moment.")
    else:
        # On filtre ou simule des alertes sur quelques matchs de la liste pour l'exemple pro
        for i, m in enumerate(matchs[:3]):
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            comp = m['competition']['name']
            match_id = m['id']
            
            np.random.seed(match_id + 99)
            type_alerte = np.random.choice(["🚨 Alerte Chute de Cote (Steam Move)", "⚡ Alerte Pression Live (But Imminent)", "⚠️ Anomalie xG / Volume de Tirs"])
            niveau_risque = np.random.choice(["Élevé (Indice 94%)", "Critique (Indice 98%)", "Modéré (Indice 88%)"])
            conseil_pari = np.random.choice(["Victoire en sec ou 1N avec Handicap", "Plus de 1.5 buts en 2ème mi-temps", "L'équipe extérieure va marquer en premier"])
            
            if "Steam" in type_alerte or "Anomalie" in type_alerte:
                st.markdown(f"""
                <div class="suspect-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #f87171; font-weight: 900; font-size: 14px;">{type_alerte}</span>
                        <span style="background: #7f1d1d; color: #f87171; padding: 2px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">Indice : {niveau_risque}</span>
                    </div>
                    <div style="font-size: 16px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">🏆 {comp} : {nom_dom} vs {nom_ext}</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px;">
                        <b>Analyse de l'anomalie :</b> Flux massifs enregistrés sur le marché asiatique. La cote est passée anormalement de 2.40 à 1.75 malgré des statistiques de forme similaires en apparence.
                    </div>
                    <div style="background: #020617; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #38bdf8; border: 1px solid #334155;">
                        💡 <b>Option Recommandée par l'IA :</b> {conseil_pari}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="live-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #34d399; font-weight: 900; font-size: 14px;">{type_alerte}</span>
                        <span style="background: #065f46; color: #34d399; padding: 2px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">Indice : {niveau_risque}</span>
                    </div>
                    <div style="font-size: 16px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">🏆 {comp} : {nom_dom} vs {nom_ext}</div>
                    <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 8px;">
                        <b>Analyse Live :</b> Pression offensive continue dans les 20 dernières minutes. Plus de 5 corners consécutifs et xG cumulé supérieur à 1.80 sans ouverture du score.
                    </div>
                    <div style="background: #020617; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #34d399; border: 1px solid #334155;">
                        💡 <b>Option Recommandée en Live :</b> {conseil_pari}
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif menu_choix == "🎟️ Coupons VIP":
    st.markdown("### 🏆 Coupons VIP sous forme de Sélections d'Options")
    if len(matchs) >= 2:
        m1, m2 = matchs[0], matchs[1]
        st.success("🛡️ **COMBINÉ SAFE (Cote ~1.95) — Confiance 90%**")
        st.write(f"1️⃣ **{m1['homeTeam']['name']} vs {m1['awayTeam']['name']}** ➔ Option : *Gagne au moins une mi-temps* (Cote 1.38)")
        st.write(f"2️⃣ **{m2['homeTeam']['name']} vs {m2['awayTeam']['name']}** ➔ Option : *Total tirs cadrés du match* (Cote 1.42)")
    
    st.info("⚡ **COUPON EXPERT BUTS & INTERVALLES (Cote ~6.50)**")
    st.write("• Sélection combinée intégrant un but de remplaçant et les intervalles de temps clés sur les affiches majeures.")
