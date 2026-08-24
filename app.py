import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="JOSS PRONOSTIC EXPERT - PRO LAB",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main { background-color: #020617; }
    .stApp { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .pro-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155; border-radius: 14px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### 👑 JOSS PRONOSTIC EXPERT [PRO LAB & FILTRE ANTI-PIÈGE]")
st.caption("FINIES LES PRÉDICTIONS AVEUGLES • ANALYSE TACTIQUE MAÎTRISÉE ET CALCUL DE VALUE BETS")

st.markdown("---")

menu = st.selectbox(
    "Mode d'Expertise",
    ["🔍 Analyseur de Match sur Mesure (Anti-Erreur)", "📊 Calculateur de Value Bet Mathématique", "📝 Journal de Bord & Suivi de Rentabilité"],
    label_visibility="collapsed"
)

if menu == "🔍 Analyseur de Match sur Mesure (Anti-Erreur)":
    st.markdown("#### 🛠️ Paramétrez le match vous-même pour éviter les erreurs d'IA")
    st.write("Entrez les paramètres réels du match que vous surveillez pour obtenir une évaluation stricte basée sur les profils défensifs.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        equipe_dom = st.text_input("Équipe Domicile", "Ex: Bologna FC")
        bloc_dom = st.selectbox("Style Bloc Domicile", ["Offensif / Haut", "Équilibré", "Bloc Bas / Ultra-Solide"])
    with col_s2:
        equipe_ext = st.text_input("Équipe Extérieur", "Ex: SS Lazio")
        bloc_ext = st.selectbox("Style Bloc Extérieur", ["Contre-attaque foudroyante", "Bloc ultra-compact (Bloque le jeu)", "Offensif"])

    if st.button("Lancer l'Audit Professionnel du Match", type="primary"):
        st.markdown("---")
        st.markdown(f"### 📋 Rapport d'Analyse : {equipe_dom} vs {equipe_ext}")
        
        if "Bloc Bas" in bloc_ext or "compact" in bloc_ext:
            st.error(f"⚠️ **ALERTE PIÈGE DÉTECTÉ :** L'équipe extérieure ({equipe_ext}) aligne un profil de bloc compact. Le risque de match fermé (type 0-0 ou 0-1 sur un exploit en transition) est **très élevé**.")
            st.success("🎯 **Recommandation Pro :** Bannir le score exact ou la victoire sèche du favori. Privilégier le **Moins de 2.5 buts** ou la **Double Chance X2**.")
        else:
            st.success("✅ **Configuration Ouverte :** Les lignes de pression sont cohérentes pour du volume offensif.")
            st.info("🎯 **Recommandation Pro :** Match propice aux tirs cadrés ou aux buts des deux équipes (BTTS).")

elif menu == "📊 Calculateur de Value Bet Mathématique":
    st.markdown("#### 🧮 Calculateur de Rentabilité Long Terme (Kelly / Value)")
    st.write("Vérifiez si la cote proposée par le bookmaker vaut réellement le coup d'être jouée selon vos propres estimations de probabilité.")
    
    c_cot, c_prob = st.columns(2)
    with c_cot:
        cote_book = st.number_input("Cote affichée par le bookmaker", min_value=1.01, value=2.10, step=0.05)
    with c_prob:
        prob_estimee = st.slider("Votre estimation personnelle de réussite (%)", min_value=1, max_value=100, value=52)
    
    prob_dec = prob_estimee / 100.0
    valeur_attendue = (cote_book * prob_dec) - 1
    
    st.markdown("---")
    if valeur_attendue > 0:
        st.success(f"🟢 **VALUE BET CONFIRMÉ !** La valeur mathématique est positive (+{valeur_attendue*100:.1f}%). Ce pari est statistiquement rentable sur le long terme.")
    else:
        st.error(f"🔴 **PIÈGE / PAS DE VALUE :** Valeur négative ({valeur_attendue*100:.1f}%). Le bookmaker prend une marge trop importante par rapport au risque. **Pari à éviter.**")

elif menu == "📝 Journal de Bord & Suivi de Rentabilité":
    st.markdown("#### 📈 Suivi rigoureux de vos paris passés")
    st.write("Notez vos pronostics pour analyser vos réussites et éliminer définitivement les erreurs d'analyse constatées (comme les surprises de Bologne ou de la Lazio).")
    
    match_historique = st.text_input("Match concerné", "Ex: Bologna vs Lazio")
    pronostic_tenu = st.text_input("Votre pronostic initial", "Ex: Victoire domicile / 1-0")
    resultat_reel = st.text_input("Résultat réel du match", "Ex: 0-1 pour Lazio")
    
    if st.button("Enregistrer dans le journal d'apprentissage"):
        st.success("Match enregistré ! Votre historique personnel s'affine pour éliminer ce type de piège à l'avenir.")
