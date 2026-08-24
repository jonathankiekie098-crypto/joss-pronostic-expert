import streamlit as st

st.title("⚽ Tableau de Bord - Matchs & Analyses xG")

# 1. Liste de vos matchs (vous pouvez en ajouter autant que vous voulez)
matchs = [
    {
        "equipe_dom": "CA Osasuna",
        "equipe_ext": "Levante UD",
        "score": "0 - 0",
        "temps_match": "2. mi-temps - 73:49",
        "pos_dom": 48, "pos_ext": 52,
        "tirs_tot_dom": 11, "tirs_tot_ext": 9,
        "tirs_cad_dom": 7, "tirs_cad_ext": 1,
        "grosses_occ_dom": 2, "grosses_occ_ext": 2,
        "corners_dom": 9, "corners_ext": 3,
        "xg_dom": 0.63, "xg_ext": 1.20,
        "prono_cote": "1X (64%)",
        "btts_cote": "Oui (Fort)",
        "tendance": "+2.5 Buts (68%)",
        "analyse_ia": "Malgré une domination d'Osasuna en tirs cadrés et corners, Levante se montre plus efficace."
    },
    # Vous pouvez ajouter un autre match ici facilement :
    {
        "equipe_dom": "Real Madrid",
        "equipe_ext": "FC Barcelone",
        "score": "1 - 1",
        "temps_match": "1. mi-temps - 34:12",
        "pos_dom": 52, "pos_ext": 48,
        "tirs_tot_dom": 8, "tirs_tot_ext": 7,
        "tirs_cad_dom": 4, "tirs_cad_ext": 3,
        "grosses_occ_dom": 1, "grosses_occ_ext": 2,
        "corners_dom": 4, "corners_ext": 5,
        "xg_dom": 1.10, "xg_ext": 0.95,
        "prono_cote": "1X (55%)",
        "btts_cote": "Oui",
        "tendance": "+1.5 Buts (82%)",
        "analyse_ia": "Grosse intensité au milieu de terrain. Les opportunités s'équilibrent de chaque côté."
    }
]

# 2. Boucle pour afficher chaque match dynamiquement dans l'application
for match in matchs:
    # Calculs automatiques des largeurs de barres pour éviter les divisions par zéro
    total_xg = match["xg_dom"] + match["xg_ext"]
    pct_xg_dom = int((match["xg_dom"] / total_xg) * 100) if total_xg > 0 else 50
    pct_xg_ext = 100 - pct_xg_dom

    total_tirs = match["tirs_tot_dom"] + match["tirs_tot_ext"]
    pct_tirs_dom = int((match["tirs_tot_dom"] / total_tirs) * 100) if total_tirs > 0 else 50
    pct_tirs_ext = 100 - pct_tirs_dom

    total_cadr = match["tirs_cad_dom"] + match["tirs_cad_ext"]
    pct_cadr_dom = int((match["tirs_cad_dom"] / total_cadr) * 100) if total_cadr > 0 else 50
    pct_cadr_ext = 100 - pct_cadr_dom

    total_corn = match["corners_dom"] + match["corners_ext"]
    pct_corn_dom = int((match["corners_dom"] / total_corn) * 100) if total_corn > 0 else 50
    pct_corn_ext = 100 - pct_corn_dom

    # Code HTML de la carte
    html_code = f"""
    <div style="background: #020617; padding: 18px; border-radius: 14px; color: #f8fafc; font-family: sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.3); width: 100%; max-width: 480px; margin-bottom: 20px;">
      
      <!-- En-tête Match & Score -->
      <div style="text-align: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #1e293b;">
        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 4px;">{match["temps_match"]}</div>
        <div style="font-size: 16px; font-weight: bold; color: #f43f5e;">{match["equipe_dom"]} <span style="color: #f8fafc; margin: 0 8px;">{match["score"]}</span> {match["equipe_ext"]}</div>
      </div>

      <!-- Badges de Cotes -->
      <div style="display: flex; gap: 8px; margin-bottom: 16px;">
        <div style="background: #166534; color: #4ade80; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
          Prono : {match["prono_cote"]}
        </div>
        <div style="background: #1e40af; color: #60a5fa; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;">
          BTTS : {match["btts_cote"]}
        </div>
      </div>

      <!-- Statistiques Détaillées -->
      <div style="font-size: 12px; font-weight: bold; color: #38bdf8; margin-bottom: 10px; text-transform: uppercase;">Statistiques Détaillées</div>

      <!-- xG -->
      <div style="margin-bottom: 10px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px; color: #cbd5e1;">
          <span><b>{match["xg_dom"]}</b></span>
          <span style="color: #94a3b8;">Expected Goals (xG)</span>
          <span><b>{match["xg_ext"]}</b></span>
        </div>
        <div style="display: flex; height: 6px; width: 100%; background: #1e293b; border-radius: 3px; overflow: hidden;">
          <div style="width: {pct_xg_dom}%; background: #38bdf8;"></div>
          <div style="width: {pct_xg_ext}%; background: #f43f5e;"></div>
        </div>
      </div>

      <!-- Possession -->
      <div style="margin-bottom: 10px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px; color: #cbd5e1;">
          <span><b>{match["pos_dom"]}%</b></span>
          <span style="color: #94a3b8;">Possession de balle</span>
          <span><b>{match["pos_ext"]}%</b></span>
        </div>
        <div style="display: flex; height: 6px; width: 100%; background: #1e293b; border-radius: 3px; overflow: hidden;">
          <div style="width: {match["pos_dom"]}%; background: #38bdf8;"></div>
          <div style="width: {match["pos_ext"]}%; background: #f43f5e;"></div>
        </div>
      </div>

      <!-- Tirs Totaux -->
      <div style="margin-bottom: 10px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px; color: #cbd5e1;">
          <span><b>{match["tirs_tot_dom"]}</b></span>
          <span style="color: #94a3b8;">Tirs totaux</span>
          <span><b>{match["tirs_tot_ext"]}</b></span>
        </div>
        <div style="display: flex; height: 6px; width: 100%; background: #1e293b; border-radius: 3px; overflow: hidden;">
          <div style="width: {pct_tirs_dom}%; background: #38bdf8;"></div>
          <div style="width: {pct_tirs_ext}%; background: #f43f5e;"></div>
        </div>
      </div>

      <!-- Tirs Cadrés -->
      <div style="margin-bottom: 10px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px; color: #cbd5e1;">
          <span><b>{match["tirs_cad_dom"]}</b></span>
          <span style="color: #94a3b8;">Tirs cadrés</span>
          <span><b>{match["tirs_cad_ext"]}</b></span>
        </div>
        <div style="display: flex; height: 6px; width: 100%; background: #1e293b; border-radius: 3px; overflow: hidden;">
          <div style="width: {pct_cadr_dom}%; background: #38bdf8;"></div>
          <div style="width: {pct_cadr_ext}%; background: #f43f5e;"></div>
        </div>
      </div>

      <!-- Corners -->
      <div style="margin-bottom: 14px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 3px; color: #cbd5e1;">
          <span><b>{match["corners_dom"]}</b></span>
          <span style="color: #94a3b8;">Corners</span>
          <span><b>{match["corners_ext"]}</b></span>
        </div>
        <div style="display: flex; height: 6px; width: 100%; background: #1e293b; border-radius: 3px; overflow: hidden;">
          <div style="width: {pct_corn_dom}%; background: #38bdf8;"></div>
          <div style="width: {pct_corn_ext}%; background: #f43f5e;"></div>
        </div>
      </div>

      <!-- Tendance du Match -->
      <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 12px; padding-top: 8px; border-top: 1px solid #1e293b;">
        <span>Tendance Match</span>
        <b style="color: #f8fafc;">{match["tendance"]}</b>
      </div>

      <!-- Boîte d'Analyse IA -->
      <div class="expert-ai-box" style="background: #0f172a; border-left: 3px solid #38bdf8; padding: 10px 12px; border-radius: 0 8px 8px 0; font-size: 12px; color: #cbd5e1; line-height: 1.4;">
        🤖 <b>Analyse d'Expert IA :</b> {match["analyse_ia"]}
      </div>

    </div>
    """
    
    # Affichage de chaque carte dans l'application
    st.markdown(html_code, unsafe_allow_html=True)
