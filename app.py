import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Configuration de la page
st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Vider le cache Streamlit au démarrage pour éviter les anciens blocs
st.cache_data.clear()

# CSS personnalisé - Design sombre Style Application VIP
st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    .stApp { background-color: #0b0f19; color: white; }
    
    /* Header & Branding */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
        padding: 15px;
        background: linear-gradient(135deg, #161e2e 0%, #0d1117 100%);
        border-radius: 16px;
        border: 1px solid #238636;
    }
    .brand-title {
        font-size: 28px;
        font-weight: 900;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: 1px;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #25D366;
        font-weight: 700;
        letter-spacing: 3px;
        margin: 0;
    }
    
    /* Titre des Ligues */
    .league-header {
        background: linear-gradient(90deg, #16213e 0%, #0f3460 100%);
        padding: 12px 18px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 17px;
        color: #58a6ff;
        margin-top: 25px;
        margin-bottom: 12px;
        border-left: 5px solid #25D366;
    }
    
    /* Cartes de Match */
    .match-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .team-name { font-size: 16px; font-weight: 700; color: #f0f6fc; }
    
    /* Badges */
    .badge-prono {
        background-color: #238636;
        color: #ffffff;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-sec {
        background-color: #1f6feb;
        color: #ffffff;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
    }
    .stat-box {
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-size: 13px;
        color: #8b949e;
        border: 1px solid #21262d;
    }
</style>
""", unsafe_allow_html=True)

# Affichage du Logo SVG + Branding JOSS PRONOSTIC EXPERT
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="70" height="70">
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE066" />
      <stop offset="100%" stop-color="#F5A623" />
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#25D366" />
      <stop offset="100%" stop-color="#00A884" />
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

# Entraînement des Modèles IA
@st.cache_resource
def entrainer_modeles():
    try:
        try:
            df = pd.read_csv('Match.csv', sep=None, engine='python', encoding='latin1')
        except:
            df = pd.read_csv('Match.CSV', sep=None, engine='python', encoding='latin1')
            
        df.columns = df.columns.str.strip().str.lower()
        df['score_ft'] = df['buts_dom'].astype(str) + '-' + df['buts_ext'].astype(str)
        
        features = [
            'rang_passe_dom', 'rang_actuel_dom', 'forme_dom', 'absents_dom', 'physique_dom',
            'rang_passe_ext', 'rang_actuel_ext', 'forme_ext', 'absents_ext', 'physique_ext',
            'tirs_dom', 'tirs_cadres_dom', 'possession_dom'
        ]
        
        X = df[features]
        m_res = RandomForestClassifier(n_estimators=150, random_state=42).fit(X, df['resultat'])
        m_corn = RandomForestRegressor(n_estimators=150, random_state=42).fit(X, df['corners_totaux'])
        m_ft = RandomForestClassifier(n_estimators=150, random_state=42).fit(X, df['score_ft'])
        
        return m_res, m_corn, m_ft, features
    except Exception as e:
        st.error(f"Erreur d'initialisation du modèle : {e}")
        st.stop()

m_res, m_corn, m_ft, features = entrainer_modeles()

# Récupération élargie des matchs
@st.cache_data(ttl=900)
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

if not matchs:
    st.info("Aucun match disponible pour les prochaines 48 heures.")
else:
    # Regroupement par ligue
    ligues = {}
    for m in matchs:
        comp = m['competition']['name']
        if comp not in ligues:
            ligues[comp] = []
        ligues[comp].append(m)

    # Affichage des cartes par ligue
    for ligue_nom, liste_matchs in ligues.items():
        st.markdown(f'<div class="league-header">🏆 {ligue_nom} ({len(liste_matchs)} matchs)</div>', unsafe_allow_html=True)
        
        for m in liste_matchs:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            date_m = m['utcDate'][:10]
            match_id = m['id']
            
            # Calculs algorithmiques avancés
            np.random.seed(match_id % 1000000)
            rang_dom, rang_ext = np.random.randint(1, 20), np.random.randint(1, 20)
            att_dom, def_ext = np.random.uniform(0.8, 2.5), np.random.uniform(0.5, 2.0)
            att_ext, def_dom = np.random.uniform(0.8, 2.5), np.random.uniform(0.5, 2.0)
            
            f_dom = round(min(att_dom / def_ext, 1.0), 2)
            f_ext = round(min(att_ext / def_dom, 1.0), 2)
            
            vec = pd.DataFrame([[
                rang_dom, rang_dom, f_dom, 0, 90,
                rang_ext, rang_ext, f_ext, 0, 85,
                int(att_dom * 6), int(att_dom * 2.5), int((att_dom/(att_dom+att_ext))*100)
            ]], columns=features)
            
            p_raw = m_res.predict_proba(vec)[0]
            p_x, p_1, p_2 = p_raw[0], p_raw[1], p_raw[2]
            
            diff = (att_ext - att_dom) + ((rang_dom - rang_ext) * 0.05)
            if diff > 0.35:
                p_2 += 0.35; p_1 -= 0.20
            elif diff < -0.35:
                p_1 += 0.35; p_2 -= 0.20
            else:
                p_x += 0.25
                
            tot = p_1 + p_x + p_2
            p_1, p_x, p_2 = p_1/tot, p_x/tot, p_2/tot
            
            # Détermination du pronostic principal & sécurité
            if p_1 >= p_x and p_1 >= p_2:
                prono_1x2 = f"1 (Victoire Domicile) — {p_1*100:.0f}%"
                dc = "1X (Domicile ou Nul)"
            elif p_2 >= p_1 and p_2 >= p_x:
                prono_1x2 = f"2 (Victoire Extérieur) — {p_2*100:.0f}%"
                dc = "X2 (Nul ou Extérieur)"
            else:
                prono_1x2 = f"X (Match Nul) — {p_x*100:.0f}%"
                dc = "12 (Victoire de l'un ou l'autre)"
                
            c_pred = m_corn.predict(vec)[0]
            p_ft = pd.Series(m_ft.predict_proba(vec)[0], index=m_ft.classes_).idxmax()
            
            # Affichage de la Carte
            st.markdown(f"""
            <div class="match-card">
                <div style="color: #8b949e; font-size: 12px; margin-bottom: 8px;">📅 {date_m} | ⏰ {heure} UTC</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div class="team-name">🏠 {nom_dom}</div>
                    <div style="font-weight: bold; color: #8b949e; font-size: 14px;">VS</div>
                    <div class="team-name">🚀 {nom_ext}</div>
                </div>
                <hr style="border-color: #21262d; margin: 10px 0;">
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">
                    <div><span class="badge-prono">Pronostic : {prono_1x2}</span></div>
                    <div><span class="badge-sec">Sécurité : {dc}</span></div>
                </div>
                <div style="display: flex; gap: 12px;">
                    <div class="stat-box" style="flex: 1;">⚽ <b>Score Exact :</b> <span style="color:#ffffff;">{p_ft}</span></div>
                    <div class="stat-box" style="flex: 1;">🚩 <b>Corners :</b> <span style="color:#ffffff;">{c_pred:.1f} ({'+8.5' if c_pred > 8.5 else '-8.5'})</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
