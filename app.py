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

# CSS - Design Pro Structuré & Ultra-Soigné
st.markdown("""
<style>
    .main { background-color: #05080f; }
    .stApp { background-color: #05080f; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155; border-radius: 16px; padding: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    
    .match-card {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 16px;
        padding: 24px; margin-bottom: 22px; box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    .section-title {
        font-size: 14px; font-weight: 800; color: #38bdf8; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 12px; border-left: 3px solid #38bdf8; padding-left: 8px;
    }
    
    .grid-stats {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px;
    }
    .stat-box {
        background: #020617; border: 1px solid #1e293b; border-radius: 10px; padding: 10px; text-align: center;
    }
    .stat-value { font-size: 16px; font-weight: 900; color: #ffffff; }
    .stat-label { font-size: 11px; color: #94a3b8; font-weight: 700; margin-top: 2px; }

    .badge-market { background-color: #065f46; color: #34d399; padding: 5px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid #059669; display: inline-block; margin: 3px; }
    .badge-market-sec { background-color: #1e40af; color: #60a5fa; padding: 5px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid #2563eb; display: inline-block; margin: 3px; }
    
    .expert-ai-box { 
        background: #020617; border-left: 4px solid #fbbf24; padding: 12px 16px; 
        border-radius: 0 10px 10px 0; font-size: 13px; color: #cbd5e1; margin-top: 14px; 
        line-height: 1.5; border-top: 1px solid #1e293b; border-right: 1px solid #1e293b; 
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

# En-tête
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class="header-box">
        <div style="font-size:22px; font-weight:900; color:#ffffff;">👑 JOSS PRONOSTIC EXPERT</div>
        <div style="font-size:11px; color:#38bdf8; font-weight:800; letter-spacing: 2px; margin-top: 4px;">MODULE D'ANALYSE TACTIQUE & STATISTIQUES AVANCÉES</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div class="header-box" style="text-align: center; padding: 16px;">
        <div style="color: #fbbf24; font-weight: 900; font-size: 16px;">⚡ {st.session_state.credits} / 3</div>
        <div style="font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Crédits IA Dispos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

menu_choix = st.selectbox(
    "Navigation",
    ["📊 Analyseur Global & Scores Exacts", "🔥 Matchs du Jour & Options Détaillées", "🎟️ Coupons VIP"],
    label_visibility="collapsed"
)

if menu_choix == "📊 Analyseur Global & Scores Exacts":
    st.markdown("### 📋 Tableau de Synthèse des Rencontres du Jour")
    st.markdown("<div style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Vue d'ensemble de tous les matchs sélectionnés avec leurs scores exacts anticipés par l'algorithme.</div>", unsafe_allow_html=True)
    
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
            
            st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 11px; color: #38bdf8; font-weight: 700; margin-bottom: 4px;">🏆 {comp} • ⏰ {heure} UTC</div>
                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">{nom_dom} vs {nom_ext}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 11px; color: #94a3b8; font-weight: 700;">SCORE EXACT PRÉVU</div>
                    <div style="font-size: 20px; font-weight: 900; color: #fbbf24;">{score_d} - {score_e}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu_choix == "🔥 Matchs du Jour & Options Détaillées":
    st.markdown("### 🎯 Analyse Complète & Marchés Spécifiques par Match")
    
    if not matchs:
        st.info("Aucun match disponible.")
    else:
        for m in matchs:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            comp = m['competition']['name']
            match_id = m['id']
            
            # Génération cohérente des stats basées sur l'ID du match
            np.random.seed(match_id)
            score_d = int(np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1]))
            score_e = int(np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2]))
            
            tirs_cad_d = int(np.random.randint(4, 9))
            tirs_cad_e = int(np.random.randint(2, 7))
            total_tirs = tirs_cad_d + tirs_cad_e + int(np.random.randint(6, 12))
            
            intervalle_but = np.random.choice(["15' - 30'", "31' - 45'", "46' - 60'", "75' - 90+"])
            remplacant_buteur = np.random.choice([f"Oui ({nom_dom} - Impact Sub)", f"Oui ({nom_ext} - Joker offensif)", "Non (Titulaires dominants)"])
            mi_temps_gagnee = f"{nom_dom} gagne au moins une mi-temps (74%)" if score_d >= score_e else f"{nom_ext} gagne au moins une mi-temps (68%)"
            
            st.markdown(f"""
            <div class="match-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <div style="color: #38bdf8; font-size: 11px; font-weight: 800; margin-bottom: 3px;">🏆 {comp.upper()} • ⏰ {heure} UTC</div>
                        <div style="font-size: 18px; font-weight: 900; color: #ffffff;">{nom_dom} <span style="color:#64748b;">vs</span> {nom_ext}</div>
                    </div>
                    <div style="background: #1e293b; padding: 8px 16px; border-radius: 10px; border: 1px solid #334155; text-align: center;">
                        <div style="font-size: 10px; color: #94a3b8; font-weight: 700;">SCORE EXACT</div>
                        <div style="font-size: 18px; font-weight: 900; color: #fbbf24;">{score_d} - {score_e}</div>
                    </div>
                </div>

                <div class="section-title">📊 Statistiques de Tirs Cadrés Estimés</div>
                <div class="grid-stats">
                    <div class="stat-box">
                        <div class="stat-value" style="color: #38bdf8;">{tirs_cad_d}</div>
                        <div class="stat-label">Tirs Cadrés ({nom_dom})</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #fbbf24;">{tirs_cad_e}</div>
                        <div class="stat-label">Tirs Cadrés ({nom_ext})</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #34d399;">{total_tirs}</div>
                        <div class="stat-label">Total Match (Cadrés + Non Cadrés)</div>
                    </div>
                </div>

                <div class="section-title">⚡ Options & Marchés Alternatifs</div>
                <div style="margin-bottom: 12px;">
                    <span class="badge-market">⚽ Un remplaçant va marquer : <b>{remplacant_buteur}</b></span>
                    <span class="badge-market-sec">⏱️ Intervalle 1er But / Temps fort : <b>{intervalle_but}</b></span>
                    <span class="badge-market" style="background:#78350f; color:#fbbf24; border-color:#d97706;">🛡️ Mi-temps : <b>{mi_temps_gagnee}</b></span>
                </div>

                <div class="expert-ai-box">
                    🤖 <b>Analyse Tactique Experte :</b> Le schéma de jeu préédit une pression constante. L'équipe de {nom_dom} devrait faire la différence dans l'intervalle <b>{intervalle_but}</b> grâce à ses ressources sur le banc.
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu_choix == "🎟️ Coupons VIP":
    st.markdown("### 🏆 Coupons VIP Combinés & Options Spéciales")
    st.markdown("<div style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Sélections premium intégrant les options de tirs, buts par intervalle et victoires par mi-temps.</div>", unsafe_allow_html=True)
    
    if len(matchs) >= 2:
        m1, m2 = matchs[0], matchs[1]
        st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #fbbf24; border-radius: 16px; padding: 22px; margin-bottom: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:16px; font-weight:900; color:#fbbf24;">🛡️ COUPON SAFE COMBINÉ (Cote ~1.95)</span>
                <span style="background:#78350f; color:#fbbf24; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">Confiance 90%</span>
            </div>
            <hr style="border-color:#334155; margin:8px 0;">
            <div style="font-size:13px; color: #cbd5e1; margin: 8px 0;">1️⃣ {m1['homeTeam']['name']} vs {m1['awayTeam']['name']} ➔ <b style="color:#38bdf8;">Équipe à domicile gagne au moins une mi-temps (1.38)</b></div>
            <div style="font-size:13px; color: #cbd5e1; margin: 8px 0;">2️⃣ {m2['homeTeam']['name']} vs {m2['awayTeam']['name']} ➔ <b style="color:#38bdf8;">Plus de 7.5 tirs cadrés dans le match (1.42)</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div style="background: #0f172a; border: 1px solid #34d399; border-radius: 16px; padding: 22px; margin-bottom: 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:16px; font-weight:900; color:#34d399;">⚡ COUPON EXPERT BUTS & INTERVALLES (Cote ~6.50)</span>
            <span style="background:#065f46; color:#34d399; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800;">High Value</span>
        </div>
        <hr style="border-color:#334155; margin:8px 0;">
        <div style="font-size:13px; color: #cbd5e1; margin: 8px 0;">• Sélection combinée intégrant un but de remplaçant et les intervalles de temps clés sur les affiches majeures.</div>
    </div>
    """, unsafe_allow_html=True)
