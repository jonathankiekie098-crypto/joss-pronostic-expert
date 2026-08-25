 import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import math

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT - QUANT MODEL V2",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.main {
    background-color: #020617;
}

.stApp {
    background-color: #020617;
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

.expert-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.section-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
}

.badge-pro {
    background: #0284c7;
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
}

.badge-warning {
    background: #e11d48;
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
}

.badge-success {
    background: #16a34a;
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
}

.big-score {
    font-size: 30px;
    font-weight: 900;
    color: #f59e0b;
}

.small-muted {
    color: #94a3b8;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# API
# ============================================================

# IMPORTANT :
# Mets ta nouvelle clé dans .streamlit/secrets.toml :
#
# FOOTBALL_API_KEY = "TA_NOUVELLE_CLE"
#
# Si secrets.toml n'existe pas, crée-le.

try:
    API_KEY = st.secrets["FOOTBALL_API_KEY"]
except Exception:
    API_KEY = ""

HEADERS = {
    "X-Auth-Token": API_KEY
}

BASE_URL = "https://api.football-data.org/v4"

# ============================================================
# OUTILS API
# ============================================================

@st.cache_data(ttl=300)
def api_get(endpoint, params=None):
    if not API_KEY:
        return None

    try:
        response = requests.get(
            BASE_URL + endpoint,
            headers=HEADERS,
            params=params,
            timeout=15
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


# ============================================================
# MATCHS À VENIR
# ============================================================

@st.cache_data(ttl=300)
def charger_matchs():

    date_start = datetime.now().strftime("%Y-%m-%d")
    date_end = (
        datetime.now() + timedelta(days=3)
    ).strftime("%Y-%m-%d")

    data = api_get(
        "/matches",
        {
            "dateFrom": date_start,
            "dateTo": date_end
        }
    )

    if data:
        return data.get("matches", [])

    return []


# ============================================================
# HISTORIQUE D'UNE ÉQUIPE
# ============================================================

@st.cache_data(ttl=600)
def charger_historique_team(team_id):

    data = api_get(
        f"/teams/{team_id}/matches",
        {
            "status": "FINISHED",
            "limit": 20
        }
    )

    if data:
        return data.get("matches", [])

    return []


# ============================================================
# STATISTIQUES D'UNE ÉQUIPE
# ============================================================

def calculer_stats_equipe(team_id):

    matchs = charger_historique_team(team_id)

    if not matchs:
        return None

    matchs = [
        m for m in matchs
        if m.get("score", {}).get("fullTime", {}).get("home") is not None
        and m.get("score", {}).get("fullTime", {}).get("away") is not None
    ]

    if not matchs:
        return None

    matchs = sorted(
        matchs,
        key=lambda x: x.get("utcDate", ""),
        reverse=True
    )

    matchs = matchs[:10]

    buts_marques = []
    buts_encaisses = []

    domicile_buts = []
    domicile_encaisses = []

    exterieur_buts = []
    exterieur_encaisses = []

    victoires = 0
    nuls = 0
    defaites = 0

    for m in matchs:

        home_id = m["homeTeam"]["id"]
        away_id = m["awayTeam"]["id"]

        home_goals = m["score"]["fullTime"]["home"]
        away_goals = m["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:

            buts_marques.append(home_goals)
            buts_encaisses.append(away_goals)

            domicile_buts.append(home_goals)
            domicile_encaisses.append(away_goals)

            if home_goals > away_goals:
                victoires += 1
            elif home_goals == away_goals:
                nuls += 1
            else:
                defaites += 1

        elif team_id == away_id:

            buts_marques.append(away_goals)
            buts_encaisses.append(home_goals)

            exterieur_buts.append(away_goals)
            exterieur_encaisses.append(home_goals)

            if away_goals > home_goals:
                victoires += 1
            elif away_goals == home_goals:
                nuls += 1
            else:
                defaites += 1

    if not buts_marques:
        return None

    return {
        "matchs": len(buts_marques),
        "buts_marques": np.mean(buts_marques),
        "buts_encaisses": np.mean(buts_encaisses),

        "dom_buts": (
            np.mean(domicile_buts)
            if domicile_buts else np.mean(buts_marques)
        ),

        "dom_encaisses": (
            np.mean(domicile_encaisses)
            if domicile_encaisses else np.mean(buts_encaisses)
        ),

        "ext_buts": (
            np.mean(exterieur_buts)
            if exterieur_buts else np.mean(buts_marques)
        ),

        "ext_encaisses": (
            np.mean(exterieur_encaisses)
            if exterieur_encaisses else np.mean(buts_encaisses)
        ),

        "victoires": victoires,
        "nuls": nuls,
        "defaites": defaites
    }


# ============================================================
# POISSON
# ============================================================

def poisson_prob(lmbda, buts):

    if lmbda <= 0:
        return 0

    return (
        math.exp(-lmbda)
        * (lmbda ** buts)
        / math.factorial(buts)
    )


# ============================================================
# MATRICE DES SCORES
# ============================================================

def calculer_matrice(xg_home, xg_away, max_goals=6):

    matrix = {}

    for home_goals in range(max_goals + 1):

        for away_goals in range(max_goals + 1):

            p_home = poisson_prob(
                xg_home,
                home_goals
            )

            p_away = poisson_prob(
                xg_away,
                away_goals
            )

            matrix[
                (home_goals, away_goals)
            ] = p_home * p_away

    total = sum(matrix.values())

    if total > 0:

        for key in matrix:

            matrix[key] /= total

    return matrix


# ============================================================
# ANALYSE DES PROBABILITÉS
# ============================================================

def analyser_probabilites(matrix):

    home_win = 0
    draw = 0
    away_win = 0

    over15 = 0
    over25 = 0
    over35 = 0

    under15 = 0
    under25 = 0
    under35 = 0

    btts = 0

    for (hg, ag), p in matrix.items():

        if hg > ag:
            home_win += p

        elif hg == ag:
            draw += p

        else:
            away_win += p

        total_goals = hg + ag

        if total_goals >= 2:
            over15 += p

        if total_goals >= 3:
            over25 += p

        if total_goals >= 4:
            over35 += p

        if total_goals <= 1:
            under15 += p

        if total_goals <= 2:
            under25 += p

        if total_goals <= 3:
            under35 += p

        if hg > 0 and ag > 0:
            btts += p

    return {
        "home": home_win,
        "draw": draw,
        "away": away_win,

        "over15": over15,
        "over25": over25,
        "over35": over35,

        "under15": under15,
        "under25": under25,
        "under35": under35,

        "btts": btts,
        "no_btts": 1 - btts
    }


# ============================================================
# MEILLEURS SCORES
# ============================================================

def meilleurs_scores(matrix, nombre=5):

    scores = sorted(
        matrix.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:nombre]


# ============================================================
# CALCUL DES XG
# ============================================================

def calculer_xg(stats_home, stats_away):

    # Moyennes générales
    attaque_home = stats_home["buts_marques"]
    defense_home = stats_home["buts_encaisses"]

    attaque_away = stats_away["buts_marques"]
    defense_away = stats_away["buts_encaisses"]

    # Spécificité domicile / extérieur
    home_attack = stats_home["dom_buts"]
    home_defense = stats_home["dom_encaisses"]

    away_attack = stats_away["ext_buts"]
    away_defense = stats_away["ext_encaisses"]

    # Mélange des informations
    xg_home = (
        0.45 * home_attack
        + 0.25 * attaque_home
        + 0.30 * away_defense
    )

    xg_away = (
        0.45 * away_attack
        + 0.25 * attaque_away
        + 0.30 * home_defense
    )

    # Limites raisonnables
    xg_home = max(0.15, min(xg_home, 4.5))
    xg_away = max(0.15, min(xg_away, 4.5))

    return round(xg_home, 2), round(xg_away, 2)


# ============================================================
# SCORE DE CONFIANCE
# ============================================================

def calculer_confiance(probas, stats_home, stats_away):

    meilleure = max(
        probas["home"],
        probas["draw"],
        probas["away"]
    )

    stabilite = min(
        stats_home["matchs"],
        stats_away["matchs"]
    )

    score = meilleure * 100

    # Petit bonus si beaucoup de données
    if stabilite >= 8:
        score += 5

    elif stabilite >= 5:
        score += 2

    # Limitation
    score = max(0, min(score, 95))

    return round(score)


# ============================================================
# VERDICT
# ============================================================

def determiner_verdict(probas):

    options = {
        "Victoire domicile": probas["home"],
        "Match nul": probas["draw"],
        "Victoire extérieur": probas["away"],
        "Plus de 1.5 buts": probas["over15"],
        "Moins de 2.5 buts": probas["under25"],
        "Les deux équipes marquent": probas["btts"],
        "Les deux équipes ne marquent pas": probas["no_btts"]
    }

    meilleur_nom = max(
        options,
        key=options.get
    )

    meilleure_prob = options[meilleur_nom]

    if meilleure_prob >= 0.72:

        return (
            "🟢 SÉLECTION FORTE",
            meilleur_nom,
            meilleure_prob
        )

    elif meilleure_prob >= 0.62:

        return (
            "🟡 SÉLECTION INTÉRESSANTE",
            meilleur_nom,
            meilleure_prob
        )

    else:

        return (
            "🔴 NO BET",
            "Aucune sélection suffisamment forte",
            meilleure_prob
        )


# ============================================================
# CHARGEMENT
# ============================================================

matchs = charger_matchs()


# ============================================================
# HEADER
# ============================================================

c1, c2 = st.columns([3, 1])

with c1:

    st.markdown(
        "### 👑 JOSS PRONOSTIC EXPERT "
        "[QUANTITATIVE & TACTICAL LAB]"
    )

    st.caption(
        "MOTEUR STATISTIQUE • FORME • DOMICILE/EXTÉRIEUR "
        "• POISSON • PROBABILITÉS • DÉTECTION NO BET"
    )

with c2:

    st.metric(
        "🎯 Matchs chargés",
        len(matchs)
    )

st.markdown("---")


# ============================================================
# MENU
# ============================================================

menu = st.selectbox(
    "Module d'Analyse Avancée",
    [
        "📊 Modélisation Mathématique des Matchs du Jour",
        "🛡️ Audit Tactique & Détecteur de Blocs Fermés",
        "🧮 Calculateur de Value Bet & Kelly Pro"
    ],
    label_visibility="collapsed"
)


# ============================================================
# MODULE PRINCIPAL
# ============================================================

if menu == "📊 Modélisation Mathématique des Matchs du Jour":

    st.markdown(
        "### 📊 Analyse Probabiliste Avancée"
    )

    st.markdown(
        """
        <div class="small-muted">
        Le moteur utilise maintenant l'historique récent des équipes,
        leurs performances domicile/extérieur, les buts marqués/encaissés
        et une modélisation de Poisson.
        </div>
        """,
        unsafe_allow_html=True
    )

    if not API_KEY:

        st.error(
            "⚠️ Clé API absente. "
            "Ajoute FOOTBALL_API_KEY dans st.secrets."
        )

    elif not matchs:

        st.warning(
            "Aucun match disponible pour la période actuelle."
        )

    else:

        for m in matchs:

            try:

                dom = m["homeTeam"]["name"]
                ext = m["awayTeam"]["name"]

                dom_id = m["homeTeam"]["id"]
                ext_id = m["awayTeam"]["id"]

                comp = m["competition"]["name"]

                heure = m["utcDate"][11:16]

                # ==========================================
                # HISTORIQUE
                # ==========================================

                stats_home = calculer_stats_equipe(dom_id)
                stats_away = calculer_stats_equipe(ext_id)

                if not stats_home or not stats_away:

                    st.warning(
                        f"⚠️ Données insuffisantes : "
                        f"{dom} vs {ext}"
                    )

                    continue

                # ==========================================
                # XG
                # ==========================================

                xg_home, xg_away = calculer_xg(
                    stats_home,
                    stats_away
                )

                # ==========================================
                # POISSON
                # ==========================================

                matrix = calculer_matrice(
                    xg_home,
                    xg_away
                )

                probas = analyser_probabilites(
                    matrix
                )

                scores = meilleurs_scores(
                    matrix,
                    5
                )

                # ==========================================
                # CONFIANCE
                # ==========================================

                confiance = calculer_confiance(
                    probas,
                    stats_home,
                    stats_away
                )

                # ==========================================
                # VERDICT
                # ==========================================

                verdict, selection, prob_selection = (
                    determiner_verdict(probas)
                )

                # ==========================================
                # AFFICHAGE
                # ==========================================

                with st.container():

                    st.markdown(
                        f"""
                        <div class="expert-card">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            margin-bottom:10px;
                        ">

                            <span class="badge-pro">
                                {comp.upper()}
                            </span>

                            <span class="small-muted">
                                ⏰ {heure} UTC
                            </span>

                        </div>

                        <div style="
                            font-size:21px;
                            font-weight:900;
                            margin-bottom:15px;
                        ">
                            ⚽ {dom}
                            <span style="color:#38bdf8;">
                            vs
                            </span>
                            {ext}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ======================================
                    # XG
                    # ======================================

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.metric(
                            "xG domicile",
                            f"{xg_home:.2f}"
                        )

                    with c2:

                        st.metric(
                            "xG extérieur",
                            f"{xg_away:.2f}"
                        )

                    with c3:

                        st.metric(
                            "Confiance",
                            f"{confiance}%"
                        )

                    # ======================================
                    # PROBABILITÉS 1X2
                    # ======================================

                    st.markdown(
                        "#### 🎯 Probabilités 1X2"
                    )

                    p1, p2, p3 = st.columns(3)

                    with p1:

                        st.metric(
                            f"🏠 {dom}",
                            f"{probas['home']*100:.1f}%"
                        )

                    with p2:

                        st.metric(
                            "🤝 Nul",
                            f"{probas['draw']*100:.1f}%"
                        )

                    with p3:

                        st.metric(
                            f"✈️ {ext}",
                            f"{probas['away']*100:.1f}%"
                        )

                    # ======================================
                    # MARCHÉS
                    # ======================================

                    st.markdown(
                        "#### 📈 Marchés"
                    )

                    a, b, c, d = st.columns(4)

                    with a:

                        st.metric(
                            "Over 1.5",
                            f"{probas['over15']*100:.1f}%"
                        )

                    with b:

                        st.metric(
                            "Over 2.5",
                            f"{probas['over25']*100:.1f}%"
                        )

                    with c:

                        st.metric(
                            "Under 2.5",
                            f"{probas['under25']*100:.1f}%"
                        )

                    with d:

                        st.metric(
                            "BTTS",
                            f"{probas['btts']*100:.1f}%"
                        )

                    # ======================================
                    # FORME
                    # ======================================

                    st.markdown(
                        "#### 📊 Forme statistique"
                    )

                    f1, f2 = st.columns(2)

                    with f1:

                        st.write(
                            f"**{dom}**"
                        )

                        st.write(
                            f"Matchs analysés : "
                            f"{stats_home['matchs']}"
                        )

                        st.write(
                            f"Buts marqués/match : "
                            f"{stats_home['buts_marques']:.2f}"
                        )

                        st.write(
                            f"Buts encaissés/match : "
                            f"{stats_home['buts_encaisses']:.2f}"
                        )

                    with f2:

                        st.write(
                            f"**{ext}**"
                        )

                        st.write(
                            f"Matchs analysés : "
                            f"{stats_away['matchs']}"
                        )

                        st.write(
                            f"Buts marqués/match : "
                            f"{stats_away['buts_marques']:.2f}"
                        )

                        st.write(
                            f"Buts encaissés/match : "
                            f"{stats_away['buts_encaisses']:.2f}"
                        )

                    # ======================================
                    # SCORES
                    # ======================================

                    st.markdown(
                        "#### 🔮 Top 5 scores modélisés"
                    )

                    score_text = ""

                    for i, ((hg, ag), prob) in enumerate(
                        scores,
                        start=1
                    ):

                        score_text += (
                            f"**{i}. {hg}-{ag}** — "
                            f"{prob*100:.2f}%  \n"
                        )

                    st.markdown(score_text)

                    # ======================================
                    # VERDICT
                    # ======================================

                    if "SÉLECTION FORTE" in verdict:

                        st.success(
                            f"{verdict}  \n"
                            f"🎯 **{selection}** — "
                            f"{prob_selection*100:.1f}%"
                        )

                    elif "INTÉRESSANTE" in verdict:

                        st.warning(
                            f"{verdict}  \n"
                            f"🎯 **{selection}** — "
                            f"{prob_selection*100:.1f}%"
                        )

                    else:

                        st.error(
                            f"{verdict}  \n"
                            "Le modèle considère que les "
                            "probabilités sont trop faibles "
                            "pour proposer une sélection."
                        )

                    st.markdown("---")


# ============================================================
# AUDIT TACTIQUE
# ============================================================

elif menu == "🛡️ Audit Tactique & Détecteur de Blocs Fermés":

    st.markdown(
        "### 🛡️ Audit Tactique"
    )

    col1, col2 = st.columns(2)

    with col1:

        equipe_dom = st.text_input(
            "Équipe reçue",
            "Bologna FC"
        )

        style_dom = st.selectbox(
            "Animation domicile",
            [
                "Possession / Attaque placée",
                "Bloc haut / Pressing intense",
                "Équilibré"
            ]
        )

    with col2:

        equipe_ext = st.text_input(
            "Équipe visiteuse",
            "SS Lazio"
        )

        style_ext = st.selectbox(
            "Animation extérieure",
            [
                "Bloc bas compact",
                "Contre rapide",
                "Bloc médian prudent"
            ]
        )

    if st.button(
        "Lancer l'Audit Tactique Expert",
        type="primary"
    ):

        st.markdown("---")

        st.markdown(
            f"### 📋 {equipe_dom} vs {equipe_ext}"
        )

        if "Bloc bas" in style_ext:

            st.markdown(
                '<div class="badge-warning">'
                '⚠️ POTENTIEL MATCH FERMÉ'
                '</div>',
                unsafe_allow_html=True
            )

            st.warning(
                "Le scénario tactique indique une "
                "possibilité de réduction des espaces."
            )

            st.info(
                "Marchés à étudier : Under 3.5, "
                "Under 2.5 ou BTTS No."
            )

        else:

            st.markdown(
                '<div class="badge-success">'
                'CONFIGURATION PLUS OUVERTE'
                '</div>',
                unsafe_allow_html=True
            )

            st.info(
                "Les espaces et transitions peuvent "
                "favoriser les occasions."
            )


# ============================================================
# VALUE BET / KELLY
# ============================================================

elif menu == "🧮 Calculateur de Value Bet & Kelly Pro":

    st.markdown(
        "### 🧮 Calculateur de Value Bet & Kelly"
    )

    col_a, col_b = st.columns(2)

    with col_a:

        cote = st.number_input(
            "Cote bookmaker",
            min_value=1.01,
            value=2.20,
            step=0.05
        )

    with col_b:

        prob_perso = st.slider(
            "Probabilité estimée (%)",
            1,
            100,
            55
        )

    prob_dec = prob_perso / 100

    ev = (
        cote * prob_dec
    ) - 1

    # Kelly
    b = cote - 1

    if b > 0:

        kelly = (
            (b * prob_dec)
            - (1 - prob_dec)
        ) / b

    else:

        kelly = 0

    st.markdown("---")

    if ev > 0:

        st.success(
            f"🟢 VALUE BET\n\n"
            f"Espérance : **+{ev*100:.2f}%**"
        )

        st.info(
            f"Kelly théorique : "
            f"**{max(kelly,0)*100:.2f}%**"
        )

    else:

        st.error(
            f"🔴 PAS DE VALUE\n\n"
            f"Espérance : **{ev*100:.2f}%**"
        )

        st.info(
            "Le modèle estime que la cote "
            "ne compense pas suffisamment le risque."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "👑 JOSS PRONOSTIC EXPERT — "
    "Modèle statistique expérimental. "
    "Les probabilités ne garantissent jamais le résultat d'un match."
)
