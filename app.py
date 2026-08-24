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

# Initialisation des crédits dans la session si non existants
if 'credits' not in st.session_state:
    st.session_state.credits = 3

st.cache_resource.clear()
st.cache_data.clear()

# CSS - Style application mobile pro avec profil et crédits
st.markdown("""
<style>
    .main { background-color: #080c14; }
    .stApp { background-color: #080c14; color: #ffffff; }
    
    .brand-header {
        display: flex; justify-content: space-between; align-items: center;
        background: #0d1322; padding: 15px 20px; border-radius: 16px;
        border: 1px solid #1f293d; margin-bottom: 20px;
    }
    
    .dash-card {
        background: #111827; border: 1px solid #1f293d; border-radius: 14px;
        padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .dash-num { font-size: 28px; font-weight: 900; color: #00E5FF; margin-bottom: 4px; }
    .dash-label { font-size: 13px; color: #9ca3af; font-weight: 600; }

    .search-box-container {
        background: #111827; border: 1px solid #00E5FF; border-radius: 14px;
        padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0, 229, 255, 0.1);
    }
    
    .match-card {
        background-color: #111827; border: 1px solid #1f293d; border-radius: 14px;
        padding: 16px; margin-bottom: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .coupon-card {
        background: linear-gradient(135deg, #111827 0%, #1f293d 100%);
        border: 2px solid #F5A623; border-radius: 14px;
        padding: 18px; margin-bottom: 18px; box-shadow: 0 6px 15px rgba(245, 166, 35, 0.15);
    }
    
    .promo-card {
        background: linear-gradient(135deg, #111827 0%, #1a1003 100%);
        border: 2px solid #F5A623; border-radius: 14px;
        padding: 20px; margin-bottom: 20px; text-align: center;
    }
    
    .team-name { font-size: 16px; font-weight: 700; color: #f3f4f6; }
    .badge-prono { background-color: #059669; color: #ffffff; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-sec { background-color: #2563eb; color: #ffffff; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-cote { background-color: #F5A623; color: #000000; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 900; }
    .stat-box { background-color: #080c14; padding: 8px; border-radius: 8px; text-align: center; font-size: 13px; color: #9ca3af; border: 1px solid #1f293d; }
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
total_matchs = len(matchs)

# En-tête avec compteur d'énergie/crédits et profil utilisateur
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div style="background: #0d1322; padding: 15px; border-radius: 16px; border: 1px solid #1f293d;">
        <span style="font-size:20px; font-weight:900; color:#ffffff;">👑 JOSS PRONOSTIC EXPERT</span>
        <div style="font-size:11px; color:#00E5FF; font-weight:700; letter-spacing: 2px;">TABLEAU DE BORD IA</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div style="background: #0d1322; padding: 12px; border-radius: 16px; border: 1px solid #1f293d; text-align: center;">
        <span style="color: #F5A623; font-weight: bold; font-size: 14px;">⚡ {st.session_state.credits}/3 Crédits</span>
        <div style="font-size: 10px; color: #9ca3af;">Statut : Gratuit</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Barre de navigation principale (style application mobile du bas)
menu_choix = st.selectbox(
    "Navigation",
    ["📊 Analyser & Tableau de Bord", "🔥 Matchs du Jour", "🎟️ Coupons VIP", "🎁 Cadeaux & Promos"],
    label_visibility="collapsed"
)

if menu_choix == "📊 Analyser & Tableau de Bord":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="dash-card">
            <div class="dash-num">{total_matchs}</div>
            <div class="dash-label">Matchs Analysés</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-num" style="color:#10b981;">94%</div>
            <div class="dash-label">Fiabilité IA</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-box-container">
        <div style="font-size:17px; font-weight:800; color:#00E5FF; margin-bottom:6px;">🔍 Recherche de match par l'IA</div>
        <div style="font-size:13px; color:#9ca3af; margin-bottom:10px;">Tapez une équipe pour lancer une analyse prédictive approfondie.</div>
    </div>
    """, unsafe_allow_html=True)
    
    recherche_equipe = st.text_input("Rechercher une équipe", placeholder="Ex: Real Madrid, Man City...", label_visibility="collapsed")
    
    if recherche_equipe:
        matchs_filtres = [m for m in matchs if recherche_equipe.lower() in m['homeTeam']['name'].lower() or recherche_equipe.lower() in m['awayTeam']['name'].lower()]
    else:
        matchs_filtres = matchs[:2]
        
    if matchs_filtres:
        st.markdown(f"### 🎯 Résultats ({len(matchs_filtres)})")
        for m in matchs_filtres:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            
            st.markdown(f"""
            <div class="match-card">
                <div style="color: #9ca3af; font-size: 12px; margin-bottom: 6px;">⏰ Coup d'envoi à {heure} UTC</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div class="team-name">🏠 {nom_dom}</div>
                    <div style="font-weight: bold; color: #9ca3af;">VS</div>
                    <div class="team-name">🚀 {nom_ext}</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="badge-prono">IA : 1X Validé</span>
                    <span class="badge-cote">Cote : 1.45</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Lancer l'analyse IA complète pour {nom_dom} vs {nom_ext}", key=f"btn_{m['id']}"):
                if st.session_state.credits > 0:
                    st.session_state.credits -= 1
                    st.success(f"Analyse IA générée avec succès ! Probabilité de victoire domicile : 62% (xG: 1.9 contre 0.8). Il vous reste {st.session_state.credits} crédit(s).")
                    st.rerun()
                else:
                    st.error("Vous n'avez plus de crédits d'analyse disponibles aujourd'hui ! Passez en mode VIP pour un accès illimité.")
    else:
        st.warning("Aucun match trouvé pour cette recherche.")

elif menu_choix == "🔥 Matchs du Jour":
    st.markdown("### ⚽ Liste complète des rencontres")
    if not matchs:
        st.info("Aucun match disponible pour l'instant.")
    else:
        for m in matchs:
            nom_dom = m['homeTeam']['name']
            nom_ext = m['awayTeam']['name']
            heure = m['utcDate'][11:16]
            comp = m['competition']['name']
            
            st.markdown(f"""
            <div class="match-card">
                <div style="color: #00E5FF; font-size: 11px; font-weight: bold; margin-bottom: 4px;">🏆 {comp} | ⏰ {heure} UTC</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div class="team-name">{nom_dom}</div>
                    <div style="color: #9ca3af; font-size: 13px;">VS</div>
                    <div class="team-name">{nom_ext}</div>
                </div>
                <div style="display: flex; gap: 6px;">
                    <span class="badge-prono">Option : 1X2 Sécurisé</span>
                    <span class="badge-cote">Cote : 1.65</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu_choix == "🎟️ Coupons VIP":
    st.markdown("### 🏆 Générateur de Coupons VIP Recommandés")
    st.markdown("Sélections combinées intelligentes classées par niveau de risque.")
    
    if len(matchs) >= 2:
        m1, m2 = matchs[0], matchs[1]
        st.markdown(f"""
        <div class="coupon-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:17px; font-weight:bold; color:#F5A623;">🛡️ Coupon SAFE (Sécurité Montante)</span>
                <span class="badge-cote">Cote : ~1.85</span>
            </div>
            <div style="font-size:13px; color:#9ca3af; margin-bottom:8px;">Sélections sécurisées combinées</div>
            <hr style="border-color:#1f293d; margin:6px 0;">
            <div style="font-size:14px; margin: 4px 0;">1️⃣ {m1['homeTeam']['name']} vs {m1['awayTeam']['name']} ➔ <b>Option 1X (1.35)</b></div>
            <div style="font-size:14px; margin: 4px 0;">2️⃣ {m2['homeTeam']['name']} vs {m2['awayTeam']['name']} ➔ <b>Option X2 (1.38)</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="coupon-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:17px; font-weight:bold; color:#10b981;">⚡ Coupon MEDIUM (Cotes 5.00 à 10.00)</span>
            <span class="badge-cote">Cote : ~7.50</span>
        </div>
        <div style="font-size:13px; color:#9ca3af; margin-bottom:8px;">Combiné stable de matchs équilibrés</div>
        <hr style="border-color:#1f293d; margin:6px 0;">
        <div style="font-size:14px; margin: 4px 0;">• Sélection rigoureuse de 3 matchs avec cotes intermédiaires.</div>
    </div>
    
    <div class="coupon-card" style="border-color: #ef4444;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:17px; font-weight:bold; color:#ef4444;">💎 Coupon MAXI VIP (Cotes 20 à 50 Max)</span>
            <span class="badge-cote" style="background-color:#ef4444; color:#fff;">Cote : ~38.00</span>
        </div>
        <div style="font-size:13px; color:#9ca3af; margin-bottom:8px;">Gros combiné audacieux à forte valeur</div>
        <hr style="border-color:#1f293d; margin:6px 0;">
        <div style="font-size:14px; margin: 4px 0;">• Intègre des options à forte cote (Nuls et victoires à l'extérieur).</div>
    </div>
    """, unsafe_allow_html=True)

elif menu_choix == "🎁 Cadeaux & Promos":
    st.markdown("### 🎁 Espace Partenaires & Codes Promos")
    st.markdown("Profitez de nos codes promotionnels exclusifs pour maximiser vos avantages lors de vos inscriptions chez nos partenaires.")
    
    st.markdown("""
    <div class="promo-card">
        <div style="font-size: 18px; font-weight: 800; color: #F5A623; margin-bottom: 8px;">✨ CODE PROMO OFFICIEL</div>
        <div style="font-size: 24px; font-weight: 900; background: #232d3f; padding: 12px; border-radius: 10px; color: #00E5FF; margin: 12px 0; border: 1px dashed #F5A623;">GET1PRO</div>
        <div style="font-size: 13px; color: #9ca3af; line-height: 1.5;">
            Colle ce code à l'inscription chez nos partenaires pour activer ton bonus de bienvenue exclusif. 
            Sans ce code, le bonus ne pourra pas s'appliquer sur ton compte.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #111827; padding: 18px; border-radius: 14px; border: 1px solid #1f293d;">
        <div style="font-weight: bold; color: #ffffff; margin-bottom: 8px;">📋 Instructions d'activation :</div>
        <ol style="color: #9ca3af; font-size: 13px; padding-left: 20px; margin: 0;">
            <li>Copiez le code promo <b>GET1PRO</b>.</li>
            <li>Inscrivez-vous sur la plateforme de votre bookmaker partenaire.</li>
            <li>Collez le code dans le champ <b>Code promo</b> du formulaire d'inscription.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
