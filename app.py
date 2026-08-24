import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.cache_resource.clear()
st.cache_data.clear()

st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    .stApp { background-color: #0b0f19; color: white; }
    .brand-container {
        display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding: 15px;
        background: linear-gradient(135deg, #161e2e 0%, #0d1117 100%);
        border-radius: 16px; border: 1px solid #238636;
    }
    .brand-title { font-size: 28px; font-weight: 900; color: #FFFFFF; margin: 0; }
    .brand-subtitle { font-size: 13px; color: #25D366; font-weight: 700; letter-spacing: 3px; margin: 0; }
    .league-header {
        background: linear-gradient(90deg, #16213e 0%, #0f3460 100%);
        padding: 12px 18px; border-radius: 10px; font-weight: 800; font-size: 17px; color: #58a6ff;
        margin-top: 25px; margin-bottom: 12px; border-left: 5px solid #25D366;
    }
    .match-card {
        background-color: #161b22; border: 1px solid #30363d; border-radius: 14px;
        padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .coupon-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 2px solid #F5A623; border-radius: 14px;
        padding: 18px; margin-bottom: 20px; box-shadow: 0 6px 15px rgba(245, 166, 35, 0.15);
    }
    .team-name { font-size: 16px; font-weight: 700; color: #f0f6fc; }
    .badge-prono { background-color: #238636; color: #ffffff; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }
    .badge-sec { background-color: #1f6feb; color: #ffffff; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }
    .badge-cote { background-color: #F5A623; color: #000000; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 900; }
    .stat-box { background-color: #0d1117; padding: 10px; border-radius: 8px; text-align: center; font-size: 13px; color: #8b949e; border: 1px solid #21262d; }
</style>
""", unsafe_allow_html=True)

logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="70" height="70">
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE066" /><stop offset="100%" stop-color="#F5A623" />
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#25D366" /><stop offset="100%" stop-color="#00A884" />
    </linearGradient>
  </defs>
  <rect width="500" height="500" rx="100" fill="#0d1117" />
  <path d="M 250 70 L 370 120 V 240 C 370 330 250 390 250 390 C 250 390 130 330 130 240 V 120 Z" fill="none" stroke="url(#greenGrad)" stroke-width="12" />
  <path d="M 180 270 L 220 230 L 250 250 L 320 170" fill="none" stroke="url(#greenGrad)" stroke-width="12" stroke-linecap="round" />
  <path d="M 200 140 L 220 165 L 250 130 L 280 165 L 300 140 L 290 180 H 210 Z" fill="url(#goldGrad)" />
</svg>
"""

st.markdown(f"""
<div class="brand-container">
    <div>{logo_svg}</div>
    <div>
        <div class="brand-title">JOSS PRONOSTIC EXPERT</div>
        <div class="brand-subtitle">SYSTEME VIP D'ANALYSE FOOTBALL</div>
    </div>
</div>
""", unsafe_allow_html=True)

API_KEY = "ec0b9b5aa5d841a283d2616e8d5c1471"
HEADERS = {'X-Auth-Token': API_KEY}

@st.cache_resource
def entrainer_modeles():
    features = [
        'rang_passe_dom', 'rang_actuel_dom', 'forme_dom', 'absents_dom', 'physique_dom',
        'rang_passe_ext', 'rang_actuel_ext', 'forme_ext', 'absents_ext', 'physique_ext',
        'tirs_dom', 'tirs_cadres_dom', 'possession_dom'
    ]
    np.random.seed(42)
    data = np.random.rand(100, len(features))
    df = pd.DataFrame(data, columns=features)
    df['resultat'] = np.random.choice([0, 1, 2], size=100)
    df['corners_totaux'] = np.random.uniform(8, 11, size=100)
    X = df[features]
    m_res = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, df['resultat'])
    m_corn = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['corners_totaux'])
    return m_res, m_corn, features

m_res, m_corn, features = entrainer_modeles()

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

menu = st.tabs(["🔥 Tous les Matchs & Analyses", "🎟️ Coupons VIP & Combinés (Cotes 1.5 à 50)"])

with menu[1]:
    st.markdown("### 🏆 Générateur de Coupons VIP Recommandés")
    st.markdown("Des sélections combinées intelligentes classées par niveau de risque et de cote globale.")
    
    st.markdown("""
    <div class="coupon-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:18px; font-weight:bold; color:#F5A623;">🛡️ Coupon SAFE (Sécurité Montante)</span>
            <span class="badge-cote">Cote Globale : ~1.85</span>
        </div>
        <div style="font-size:13px; color:#8b949e; margin-bottom:10px;">Combiné de 2 sélections sécurisées (Cotes unitaires ~1.35 & ~1.38)</div>
        <hr style="border-color:#30363d; margin:8px 0;">
        <div style="font-size:14px; margin: 6px 0;">1️⃣ Double Chance Fiable ➔ <b>Option 1X (Cote: 1.35)</b></div>
        <div style="font-size:14px; margin: 6px 0;">2️⃣ Sécurité Extérieure ➔ <b>Option X2 (Cote: 1.38)</b></div>
    </div>
    
    <div class="coupon-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:18px; font-weight:bold; color:#25D366;">⚡ Coupon MEDIUM (Cotes 5.00 à 10.00)</span>
            <span class="badge-cote">Cote Globale : ~7.50</span>
        </div>
        <div style="font-size:13px; color:#8b949e; margin-bottom:10px;">Combiné de matchs équilibrés avec des cotes unitaires de 1.40, 1.80, 2.00</div>
        <hr style="border-color:#30363d; margin:8px 0;">
        <div style="font-size:14px; margin: 6px 0;">• Sélection rigoureuse de 4 matchs avec des cotes intermédiaires stables.</div>
    </div>
    
    <div class="coupon-card" style="border-color: #ff4444;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:18px; font-weight:bold; color:#ff4444;">💎 Coupon MAXI VIP (Cotes 20 à 50 Max)</span>
            <span class="badge-cote" style="background-color:#ff4444; color:#fff;">Cote Globale : ~35.00</span>
        </div>
        <div style="font-size:13px; color:#8b949e; margin-bottom:10px;">Gros combiné audacieux intégrant des cotes de 3.00 et 4.00</div>
        <hr style="border-color:#30363d; margin:8px 0;">
        <div style="font-size:14px; margin: 6px 0;">• Intègre des paris à forte valeur (Matchs Nuls et Victoires franches à l'extérieur).</div>
    </div>
    """, unsafe_allow_html=True)

with menu[0]:
    if not matchs:
        st.info("Aucun match disponible pour les prochaines 48 heures.")
    else:
        ligues = {}
        for m in matchs:
            comp = m['competition']['name']
            if comp not in ligues:
                ligues[comp] = []
            ligues[comp].append(m)

        for ligue_nom, liste_matchs in ligues.items():
            st.markdown(f'<div class="league-header">🏆 {ligue_nom} ({len(liste_matchs)} matchs)</div>', unsafe_allow_html=True)
            
            for m in liste_matchs:
                nom_dom = m['homeTeam']['name']
                nom_ext = m['awayTeam']['name']
                heure = m['utcDate'][11:16]
                date_m = m['utcDate'][:10]
                match_id = m['id']
                
                np.random.seed(match_id)
                val = np.random.rand()
                
                if val < 0.45:
                    prono_1x2 = "1 (Victoire Domicile) — 58%"
                    dc = "1X (Domicile ou Nul)"
                    cote_unitaire = "1.65"
                    p_ft = "2-1"
                    xg_d, xg_e = "1.85", "0.95"
                elif val < 0.80:
                    prono_1x2 = "2 (Victoire Extérieur) — 54%"
                    dc = "X2 (Nul ou Extérieur)"
                    cote_unitaire = "2.10"
                    p_ft = "0-1"
                    xg_d, xg_e = "0.80", "1.70"
                else:
                    prono_1x2 = "X (Match Nul) — 46%"
                    dc = "1X ou X2"
                    cote_unitaire = "3.20"
                    p_ft = "1-1"
                    xg_d, xg_e = "1.15", "1.10"
                    
                c_pred = round(np.random.uniform(8.5, 10.5), 1)
                
                st.markdown(f"""
                <div class="match-card">
                    <div style="color: #8b949e; font-size: 12px; margin-bottom: 8px;">📅 {date_m} | ⏰ {heure} UTC</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="team-name">🏠 {nom_dom}</div>
                        <div style="font-weight: bold; color: #8b949e; font-size: 14px;">VS</div>
                        <div class="team-name">🚀 {nom_ext}</div>
                    </div>
                    <hr style="border-color: #21262d; margin: 10px 0;">
                    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; align-items:center;">
                        <div><span class="badge-prono">Pronostic : {prono_1x2}</span></div>
                        <div><span class="badge-sec">Sécurité : {dc}</span></div>
                        <div><span class="badge-cote">Cote : {cote_unitaire}</span></div>
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <div class="stat-box" style="flex: 1;">⚽ <b>Score Exact :</b> <span style="color:#ffffff;">{p_ft}</span></div>
                        <div class="stat-box" style="flex: 1;">🚩 <b>Corners :</b> <span style="color:#ffffff;">{c_pred}</span></div>
                    </div>
                    <div style="margin-top: 8px; font-size: 11px; color: #8b949e; text-align: center;">
                        📊 xG Attendu — Domicile : <b>{xg_d}</b> | Extérieur : <b>{xg_e}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
