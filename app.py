 import streamlit as st
import math

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT",
    page_icon="⚽",
    layout="wide"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    text-align: center;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background: #1a1f2b;
    text-align: center;
    margin: 10px 0;
}

.score {
    font-size: 42px;
    font-weight: bold;
}

.big-number {
    font-size: 30px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TITRE
# ============================================================

st.title("👑 JOSS PRONOSTIC EXPERT")
st.subheader("⚽ QUANT MODEL — VERSION 3")

st.info(
    "Cette version utilise les caractéristiques des deux équipes "
    "pour calculer une estimation statistique."
)

# ============================================================
# INFORMATIONS DU MATCH
# ============================================================

st.header("⚽ 1. Informations du match")

col1, col2 = st.columns(2)

with col1:
    equipe_home = st.text_input(
        "Équipe à domicile",
        value="Équipe A"
    )

with col2:
    equipe_away = st.text_input(
        "Équipe à l'extérieur",
        value="Équipe B"
    )

st.divider()

# ============================================================
# DONNÉES ÉQUIPE DOMICILE
# ============================================================

st.header("📊 2. Statistiques de l'équipe à domicile")

col1, col2, col3 = st.columns(3)

with col1:
    attaque_home = st.slider(
        "Force offensive",
        0.1,
        5.0,
        2.0,
        0.1
    )

with col2:
    defense_home = st.slider(
        "Force défensive",
        0.1,
        5.0,
        2.0,
        0.1
    )

with col3:
    forme_home = st.slider(
        "Forme récente",
        0.0,
        5.0,
        2.5,
        0.1
    )

# ============================================================
# DONNÉES ÉQUIPE EXTÉRIEURE
# ============================================================

st.header("📊 3. Statistiques de l'équipe à l'extérieur")

col1, col2, col3 = st.columns(3)

with col1:
    attaque_away = st.slider(
        "Force offensive ",
        0.1,
        5.0,
        2.0,
        0.1
    )

with col2:
    defense_away = st.slider(
        "Force défensive ",
        0.1,
        5.0,
        2.0,
        0.1
    )

with col3:
    forme_away = st.slider(
        "Forme récente ",
        0.0,
        5.0,
        2.5,
        0.1
    )

# ============================================================
# BOUTON DE PRÉDICTION
# ============================================================

st.divider()

analyser = st.button(
    "🚀 ANALYSER LE MATCH",
    use_container_width=True
)

# ============================================================
# FONCTION POISSON
# ============================================================

def poisson_probability(lam, k):

    if lam <= 0:
        return 0

    return (
        math.exp(-lam)
        * (lam ** k)
        / math.factorial(k)
    )


# ============================================================
# MOTEUR DE PRÉDICTION
# ============================================================

if analyser:

    # --------------------------------------------------------
    # CALCUL DES FORCES
    # --------------------------------------------------------

    home_attack_factor = (
        attaque_home * 0.55
        + forme_home * 0.25
        + 2.0 * 0.20
    )

    away_attack_factor = (
        attaque_away * 0.55
        + forme_away * 0.25
        + 2.0 * 0.20
    )

    home_defense_factor = (
        defense_home * 0.60
        + forme_home * 0.20
        + 2.0 * 0.20
    )

    away_defense_factor = (
        defense_away * 0.60
        + forme_away * 0.20
        + 2.0 * 0.20
    )

    # --------------------------------------------------------
    # BUTS ATTENDUS
    # --------------------------------------------------------

    expected_home = (
        0.45
        + home_attack_factor * 0.32
        + (3.0 - away_defense_factor) * 0.18
    )

    expected_away = (
        0.35
        + away_attack_factor * 0.30
        + (3.0 - home_defense_factor) * 0.18
    )

    # Limites de sécurité
    expected_home = max(0.15, min(expected_home, 4.5))
    expected_away = max(0.15, min(expected_away, 4.5))

    # --------------------------------------------------------
    # MATRICE DES SCORES
    # --------------------------------------------------------

    scores = []

    for home_goals in range(0, 7):

        for away_goals in range(0, 7):

            p_home = poisson_probability(
                expected_home,
                home_goals
            )

            p_away = poisson_probability(
                expected_away,
                away_goals
            )

            probability = p_home * p_away

            scores.append(
                (
                    home_goals,
                    away_goals,
                    probability
                )
            )

    scores.sort(
        key=lambda x: x[2],
        reverse=True
    )

    # --------------------------------------------------------
    # SCORE PRINCIPAL
    # --------------------------------------------------------

    best_score = scores[0]

    predicted_home = best_score[0]
    predicted_away = best_score[1]

    score_probability = best_score[2] * 100

    # --------------------------------------------------------
    # 1X2
    # --------------------------------------------------------

    home_win = sum(
        p for h, a, p in scores
        if h > a
    )

    draw = sum(
        p for h, a, p in scores
        if h == a
    )

    away_win = sum(
        p for h, a, p in scores
        if h < a
    )

    # --------------------------------------------------------
    # OVER 2.5
    # --------------------------------------------------------

    over_25 = sum(
        p for h, a, p in scores
        if h + a >= 3
    )

    under_25 = sum(
        p for h, a, p in scores
        if h + a <= 2
    )

    # --------------------------------------------------------
    # BTTS
    # --------------------------------------------------------

    btts_yes = sum(
        p for h, a, p in scores
        if h >= 1 and a >= 1
    )

    btts_no = 1 - btts_yes

    # --------------------------------------------------------
    # TOTAL BUTS ATTENDUS
    # --------------------------------------------------------

    expected_total = (
        expected_home + expected_away
    )

    # --------------------------------------------------------
    # CONFIANCE
    # --------------------------------------------------------

    confidence = min(
        95,
        max(
            35,
            50 + abs(home_win - away_win) * 25
        )
    )

    # ========================================================
    # AFFICHAGE
    # ========================================================

    st.divider()

    st.header("🎯 RÉSULTAT DE L'ANALYSE")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Buts attendus",
            f"{expected_home:.2f} - {expected_away:.2f}"
        )

    with col2:
        st.metric(
            "Total attendu",
            f"{expected_total:.2f}"
        )

    with col3:
        st.metric(
            "Confiance modèle",
            f"{confidence:.1f}%"
        )

    # ========================================================
    # SCORE EXACT
    # ========================================================

    st.markdown(
        f"""
        <div class="result-box">
            <div>⚽ SCORE EXACT LE PLUS PROBABLE</div>
            <div class="score">
                {equipe_home} {predicted_home}
                -
                {predicted_away} {equipe_away}
            </div>
            <div>
                Probabilité mathématique :
                {score_probability:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # 1X2
    # ========================================================

    st.header("🏆 Marché 1X2")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"🏠 {equipe_home}",
            f"{home_win * 100:.1f}%"
        )

    with col2:
        st.metric(
            "🤝 Match nul",
            f"{draw * 100:.1f}%"
        )

    with col3:
        st.metric(
            f"✈️ {equipe_away}",
            f"{away_win * 100:.1f}%"
        )

    # ========================================================
    # OVER / UNDER
    # ========================================================

    st.header("⚽ Total de buts")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🔥 Over 2.5",
            f"{over_25 * 100:.1f}%"
        )

    with col2:
        st.metric(
            "🧊 Under 2.5",
            f"{under_25 * 100:.1f}%"
        )

    # ========================================================
    # BTTS
    # ========================================================

    st.header("🥅 Les deux équipes marquent")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "✅ BTTS OUI",
            f"{btts_yes * 100:.1f}%"
        )

    with col2:
        st.metric(
            "❌ BTTS NON",
            f"{btts_no * 100:.1f}%"
        )

    # ========================================================
    # TOP 5 SCORES
    # ========================================================

    st.header("🔢 Top 5 des scores probables")

    for i, (h, a, p) in enumerate(scores[:5], 1):

        st.write(
            f"**{i}. {equipe_home} {h} - {a} {equipe_away}** "
            f"→ {p * 100:.2f}%"
        )

    # ========================================================
    # CONSEIL
    # ========================================================

    st.divider()

    if home_win > max(draw, away_win):

        principal = f"Victoire {equipe_home}"

    elif away_win > max(home_win, draw):

        principal = f"Victoire {equipe_away}"

    else:

        principal = "Match nul"

    st.success(
        f"🎯 Orientation principale du modèle : **{principal}**"
    )

    st.warning(
        "⚠️ Ces probabilités sont des estimations mathématiques. "
        "Elles ne garantissent pas le résultat réel d'un match."
    )
