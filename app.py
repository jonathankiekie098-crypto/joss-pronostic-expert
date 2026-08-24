import streamlit as st

# Votre code HTML complet intégré dans Streamlit
html_code = """
<div style="background: #020617; padding: 16px; border-radius: 12px; color: #f8fafc; font-family: sans-serif; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); width: 100%; max-width: 450px;">
  
  <!-- Badges de Cotes -->
  <div style="display: flex; gap: 8px; margin-bottom: 14px;">
    <div style="background: #166534; color: #4ade80; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
      Prono : 1X (64%)
    </div>
    <div style="background: #1e40af; color: #60a5fa; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
      BTTS : Oui (Fort)
    </div>
  </div>

  <!-- En-tête des Équipes et xG -->
  <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 8px;">
    <span>CA Osasuna <span style="color: #38bdf8; font-weight: normal;">(xG: 2.18)</span></span>
    <span>Levante UD <span style="color: #fbbf24; font-weight: normal;">(xG: 1.63)</span></span>
  </div>

  <!-- Barre de progression proportionnelle xG -->
  <div style="display: flex; height: 10px; width: 100%; background: #1e293b; border-radius: 5px; overflow: hidden; margin-bottom: 12px;">
    <div style="width: 57%; background: #38bdf8; transition: width 0.3s ease;"></div>
    <div style="width: 43%; background: #fbbf24; transition: width 0.3s ease;"></div>
  </div>

  <!-- Statistiques Complémentaires (Tirs Cadrés) -->
  <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; margin-bottom: 12px; background: #0f172a; padding: 8px 12px; border-radius: 6px;">
    <span>Tirs Cadrés : <b style="color: #f8fafc;">7</b></span>
    <span>Tirs Cadrés : <b style="color: #f8fafc;">4</b></span>
  </div>

  <!-- Tendance du Match -->
  <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 12px; padding-top: 6px; border-top: 1px solid #1e293b;">
    <span>Tendance Match</span>
    <b style="color: #f8fafc;">+2.5 Buts (68%)</b>
  </div>

  <!-- Boîte d'Analyse IA -->
  <div class="expert-ai-box" style="background: #0f172a; border-left: 3px solid #38bdf8; padding: 10px 12px; border-radius: 0 8px 8px 0; font-size: 12px; color: #cbd5e1; line-height: 1.4;">
    🤖 <b>Analyse d'Expert IA :</b> Le modèle anticipe une emprise territoriale d'Osasuna qui devrait se traduire par de nombreuses occasions franches, favorisant un match ouvert avec des opportunités des deux côtés.
  </div>

</div>
"""

# Affichage dans l'application Streamlit
st.markdown(html_code, unsafe_allow_html=True)
