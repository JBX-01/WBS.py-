import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Structure de Découpage du Travail (WBS)", layout="wide")

st.title("Structure de Découpage du Travail (WBS) Dynamique")

# Initialisation du DataFrame pour stocker les données du WBS
if "wbs_data" not in st.session_state:
    st.session_state["wbs_data"] = pd.DataFrame(columns=["Phase", "Tâche", "Responsable", "Durée", "Dépendance"])

# Fonction pour ajouter une tâche au WBS
def add_task(phase, task_name, responsible, duration, dependency):
    new_task = {
        "Phase": phase,
        "Tâche": task_name,
        "Responsable": responsible,
        "Durée": duration,
        "Dépendance": dependency,
    }
    st.session_state["wbs_data"] = pd.concat([st.session_state["wbs_data"], pd.DataFrame([new_task])], ignore_index=True)

# Zone d'entrée pour ajouter une nouvelle tâche
st.sidebar.header("Ajouter une tâche au WBS")
phase_options = ["Planification", "Exécution", "Contrôle"]
phase = st.sidebar.selectbox("Sélectionnez la phase", phase_options)
task_name = st.sidebar.text_input("Nom de la tâche")
responsible = st.sidebar.text_input("Responsable")
duration = st.sidebar.number_input("Durée (jours)", min_value=1, step=1)
dependency = st.sidebar.text_input("Dépendance (optionnelle)")

if st.sidebar.button("Ajouter la tâche"):
    if task_name and responsible:
        add_task(phase, task_name, responsible, duration, dependency)
        st.sidebar.success(f"La tâche '{task_name}' a été ajoutée.")
    else:
        st.sidebar.error("Le nom de la tâche et le responsable sont requis.")

# Affichage du WBS sous forme de tableau
st.subheader("Structure de Découpage du Travail (WBS) du Projet")
if not st.session_state["wbs_data"].empty:
    st.dataframe(st.session_state["wbs_data"])
else:
    st.info("Ajoutez des tâches pour afficher le WBS.")

# Affichage d'un diagramme de Gantt simple basé sur les données WBS
st.subheader("Diagramme de Gantt des Tâches")
if not st.session_state["wbs_data"].empty:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime, timedelta

    # Simulation des dates de début pour chaque tâche
    st.session_state["wbs_data"]["Début"] = pd.to_datetime("2024-01-01")  # Date de début fictive
    st.session_state["wbs_data"]["Fin"] = st.session_state["wbs_data"]["Début"] + pd.to_timedelta(st.session_state["wbs_data"]["Durée"], unit="D")

    # Créer le diagramme de Gantt
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, row in st.session_state["wbs_data"].iterrows():
        ax.barh(row["Tâche"], (row["Fin"] - row["Début"]).days, left=(row["Début"] - st.session_state["wbs_data"]["Début"].min()).days, color="skyblue", edgecolor="black", height=0.5)

    # Configuration des axes
    ax.set_xlabel("Jours")
    ax.set_ylabel("Tâches")
    ax.set_title("Diagramme de Gantt du WBS")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))

    # Afficher le graphique
    st.pyplot(fig)
else:
    st.info("Ajoutez des tâches pour générer le diagramme de Gantt.")
