import streamlit as st

# 1. Définition des variables du match (récupérées de votre modèle ou base de données)
equipe_dom = "CA Osasuna"
equipe_ext = "Levante UD"
xg_dom = 2.18
xg_ext = 1.63
pct_dom = 57  # Largeur de la barre en %
pct_ext = 43
tirs_dom = 7
tirs_ext = 4
prono_cote = "1X (64%)"
btts_cote = "Oui (Fort)"
tendance = "+2.5 Buts (68%)"
analyse_ia = "Le modèle anticipe une emprise territoriale d'Osasuna qui devrait se traduire par de nombreuses occasions franches, favorisant un match ouvert avec des opportunités des deux côtés."

# 2. Intégration dans le template HTML avec une f-string
html_code = f"""
<div style="background: #020617; padding: 16px; border-radius: 12px; color: #f8fafc; font-family: sans-serif; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); width: 100%; max-width: 450px;">
  
  <!-- Badges de Cotes -->
  <div style="display: flex; gap: 8px; margin-bottom: 14px;">
    <div style="background: #166534; color: #4ade80; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
      Prono : {prono_cote}
    </div>
    <div style="background: #1e40af; color: #60a5fa; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
      BTTS : {btts_cote}
    </div>
  </div>

  <!-- En-tête des Équipes et xG -->
  <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
    <span>{equipe_dom} <span style="color: #38bdf8; font-weight: normal;">(xG: {xg_dom})</span></span>
    <span>{equipe_ext} <span style="color: #fbbf24; font-weight: normal;">(xG: {xg_ext})</span></span>
  </div>

  <!-- Barre de progression proportionnelle xG -->
  <div style="display: flex; height: 10px; width: 100%; background: #1e293b; border-radius: 5px; overflow: hidden; margin-bottom: 12px;">
    <div style="width: {pct_dom}%; background: #38bdf8; transition: width 0.3s ease;"></div>
    <div style="width: {pct_ext}%; background: #fbbf24; transition: width 0.3s ease;"></div>
  </div>

  <!-- Statistiques Complémentaires (Tirs Cadrés) -->
  <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; margin-bottom: 12px; background: #0f172a; padding: 8px 12px; border-radius: 6px;">
    <span>Tirs Cadrés : <b style="color: #f8fafc;">{tirs_dom}</b></span>
    <span>Tirs Cadrés : <b style="color: #f8fafc;">{tirs_ext}</b></span>
  </div>

  <!-- Tendance du Match -->
  <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 12px; padding-top: 6px; border-top: 1px solid #1e293b;">
    <span>Tendance Match</span>
    <b style="color: #f8fafc;">{tendance}</b>
  </div>

  <!-- Boîte d'Analyse IA -->
  <div class="expert-ai-box" style="background: #0f172a; border-left: 3px solid #38bdf8; padding: 10px 12px; border-radius: 0 8px 8px 0; font-size: 12px; color: #cbd5e1; line-height: 1.4;">
    🤖 <b>Analyse d'Expert IA :</b> {analyse_ia}
  </div>

</div>
"""

# 3. Rendu dans l'application
st.markdown(html_code, unsafe_allow_html=True)
