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

# CSS - Style Option de Paris / Bookmaker Pro
st.markdown("""
<style>
    .main { background-color: #060913; }
    .stApp { background-color: #060913; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155; border-radius: 14px; padding: 18px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }
    
    .match-box {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 14px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .market-category {
        font-size: 13px; font-weight: 800; color: #38bdf8; text-transform: uppercase;
        letter-spacing: 0.8px; margin: 14px 0 8px 0; display: flex; align-items: center; gap: 6px;
    }

    /* Grille de type Boutons / Options de Pari */
    .odds-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; margin-bottom: 10px;
    }
    
    .odd-btn {
        background: #020617; border: 1px solid #334155; border-radius: 8px;
        padding: 10px 12px; text-align: left; transition: all 0.2s;
        display: flex; justify-content: space-between; align-items: center;
    }
    .odd-btn:hover { border-color: #38bdf8; background: #090d1f; }
    
    .market-name { font-size: 12px; color: #94a3b8; font-weight: 600; }
    .market-value { font-size: 13px; color: #ffffff; font-weight: 800; }
    .market-odd { background: #1e293b; color: #fbbf24; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: 900; }
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
        <div style="font-size:20px; font-weight:900; color:#ffffff;">👑 JOSS PRONOSTIC EXPERT</div>
        <div style="font-size:11px; color:#38bdf8; font-weight:800; letter-spacing: 1.5px; margin-top: 2px;">INTERFACES MARCHÉS & OPTIONS DE PARIS PRO</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div class="header-box" style="text-align: center; padding: 14px;">
        <div style="color: #fbbf24; font-weight: 900; font-size: 15px;">⚡ {st.session_state.credits} / 3</div>
        <div style="font-size: 9px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Crédits IA</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

menu_choix = st.selectbox(
    "Navigation",
    ["📋 Scores Exacts & Synthèse", "🎯 Matchs & Options Détaillées", "🎟️ Coupons VIP"],
    label_visibility="collapsed"
)

if menu_choix == "📋 Scores Exacts & Synthèse":
    st.markdown("### 📋 Grille des Scores Exacts du Jour")
    st.markdown("<div style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Sélection complète des matchs avec leurs scores exacts modélisés sous forme d'options prêtes à l'emploi.</div>", unsafe_allow_html=True)
    
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
            
            st.markdown(f"""
            <div class="match-box" style="display: flex; justify-content: space-between; align-items: center; padding: 16px;">
                <div>
                    <div style="font-size: 11px; color: #38bdf8; font-weight: 700; margin-bottom: 3px;">🏆 {comp} • ⏰ {heure} UTC</div>
                    <div style="font-size: 15px; font-weight: 800; color: #ffffff;">{nom_dom} vs {nom_ext}</div>
                </div>
                <div style="background: #020617; border: 1px solid #334155; padding: 8px 16px; border-radius: 10px; text-align: right;">
                    <div style="font-size: 10px; color: #94a3b8; font-weight: 700;">OPTION SCORE EXACT</div>
                    <div style="display: flex; gap: 10px; align-items: center; margin-top: 2px;">
                        <span style="font-size: 18px; font-weight: 900; color: #fbbf24;">{score_d} - {score_e}</span>
                        <span class="market-odd">@{cote_score}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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
            
            st.markdown(f"""
            <div class="match-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">
                    <div>
                        <div style="color: #38bdf8; font-size: 11px; font-weight: 800; margin-bottom: 2px;">🏆 {comp.upper()} • ⏰ {heure} UTC</div>
                        <div style="font-size: 17px; font-weight: 900; color: #ffffff;">{nom_dom} <span style="color:#64748b;">vs</span> {nom_ext}</div>
                    </div>
                    <div style="background: #020617; padding: 6px 14px; border-radius: 8px; border: 1px solid #334155; text-align: center;">
                        <div style="font-size: 9px; color: #94a3b8; font-weight: 700;">SCORE EXACT</div>
                        <div style="font-size: 15px; font-weight: 900; color: #fbbf24;">{score_d} - {score_e}</div>
                    </div>
                </div>

                <div class="market-category">⚽ Options Principales & Résultat</div>
                <div class="odds-grid">
                    <div class="odd-btn">
                        <span class="market-name">1X2 / Double Chance</span>
                        <span class="market-value">1X (Sécurisé)</span>
                    </div>
                    <div class="odd-btn">
                        <span class="market-name">Gagne au moins 1 mi-temps</span>
                        <span class="market-value">{mi_temps_gagne}</span>
                    </div>
                </div>

                <div class="market-category">🎯 Statistiques de Tirs Cadrés</div>
                <div class="odds-grid">
                    <div class="odd-btn">
                        <span class="market-name">Tirs Cadrés ({nom_dom})</span>
                        <span class="market-odd">+{tirs_cad_d - 1}</span>
                    </div>
                    <div class="odd-btn">
                        <span class="market-name">Tirs Cadrés ({nom_ext})</span>
                        <span class="market-odd">+{tirs_cad_e - 1}</span>
                    </div>
                    <div class="odd-btn">
                        <span class="market-name">Total Tirs (Cadrés + Non)</span>
                        <span class="market-odd">+{total_tirs}</span>
                    </div>
                </div>

                <div class="market-category">⚡ Événements & Intervalles de Buts</div>
                <div class="odds-grid">
                    <div class="odd-btn">
                        <span class="market-name">Un remplaçant va marquer</span>
                        <span class="market-value">{remplacant}</span>
                    </div>
                    <div class="odd-btn">
                        <span class="market-name">Intervalle 1er But / Temps Fort</span>
                        <span class="market-value" style="color:#38bdf8;">{intervalle_but}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu_choix == "🎟️ Coupons VIP":
    st.markdown("### 🏆 Coupons VIP sous forme de Sélections d'Options")
    st.markdown("<div style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Combinés professionnels structurés par options de paris claires.</div>", unsafe_allow_html=True)
    
    if len(matchs) >= 2:
        m1, m2 = matchs[0], matchs[1]
        st.markdown(f"""
        <div class="match-box" style="border-color: #fbbf24;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:15px; font-weight:900; color:#fbbf24;">🛡️ COMBINÉ SAFE (Cote ~1.95)</span>
                <span style="background:#78350f; color:#fbbf24; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 800;">Confiance 90%</span>
            </div>
            <div class="odds-grid">
                <div class="odd-btn" style="border-color: #fbbf24;">
                    <div>
                        <div class="market-name">{m1['homeTeam']['name']} vs {m1['awayTeam']['name']}</div>
                        <div class="market-value">Gagne au moins une mi-temps</div>
                    </div>
                    <span class="market-odd">1.38</span>
                </div>
                <div class="odd-btn" style="border-color: #fbbf24;">
                    <div>
                        <div class="market-name">{m2['homeTeam']['name']} vs {m2['awayTeam']['name']}</div>
                        <div class="market-value">Total tirs cadrés du match</div>
                    </div>
                    <span class="market-odd">1.42</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
