import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

# Configuration de la page
st.set_page_config(page_title="WBS Dynamique avec Branches", layout="wide")

st.title("Structure de Découpage du Travail (WBS) avec Branches et Rectangles")

# Initialisation du DataFrame pour stocker les données du WBS
if "wbs_data" not in st.session_state:
    st.session_state["wbs_data"] = pd.DataFrame(columns=["Phase", "Tâche", "Responsable", "Durée", "Dépendance", "Parent"])

# Fonction pour ajouter une tâche au WBS
def add_task(phase, task_name, responsible, duration, dependency, parent):
    new_task = {
        "Phase": phase,
        "Tâche": task_name,
        "Responsable": responsible,
        "Durée": duration,
        "Dépendance": dependency,
        "Parent": parent,
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
parent_task = st.sidebar.selectbox("Tâche parente", ["Aucune"] + list(st.session_state["wbs_data"]["Tâche"].values))

if st.sidebar.button("Ajouter la tâche"):
    if task_name and responsible:
        add_task(phase, task_name, responsible, duration, dependency, parent_task)
        st.sidebar.success(f"La tâche '{task_name}' a été ajoutée.")
    else:
        st.sidebar.error("Le nom de la tâche et le responsable sont requis.")

# Affichage du WBS sous forme de tableau
st.subheader("Structure de Découpage du Travail (WBS) du Projet")
if not st.session_state["wbs_data"].empty:
    st.dataframe(st.session_state["wbs_data"])
else:
    st.info("Ajoutez des tâches pour afficher le WBS.")

# Création du graphique WBS avec des branches
st.subheader("Diagramme WBS avec Rectangles et Branches")

# Création du graphe pour représenter les branches du WBS
if not st.session_state["wbs_data"].empty:
    # Initialisation du graphique Plotly
    fig = go.Figure()

    # Coordonnées pour positionner les rectangles
    x_offset = 0  # Décalage horizontal pour chaque phase
    y_offset = 0  # Décalage vertical pour chaque tâche

    # Créer des rectangles pour les phases (Planification, Exécution, Contrôle)
    phases = ["Planification", "Exécution", "Contrôle"]
    for i, phase in enumerate(phases):
        # Ajouter un rectangle pour chaque phase
        fig.add_trace(go.Scatter(
            x=[x_offset, x_offset + 4, x_offset + 4, x_offset],
            y=[y_offset + 1, y_offset + 1, y_offset, y_offset],
            fill='toself',
            fillcolor='lightblue',
            line=dict(color='black'),
            text=phase,
            mode="text+lines",
            textposition="middle center",
            name=phase
        ))
        y_offset -= 2  # Diminuer la position verticale pour la prochaine phase
        x_offset += 5  # Déplacer horizontalement pour la phase suivante

    # Ajouter les tâches sous les phases
    for _, row in st.session_state["wbs_data"].iterrows():
        parent_phase = row["Phase"]
        task_name = row["Tâche"]
        # Ajuster la position en fonction de la phase
        if parent_phase == "Planification":
            y_pos = 0
        elif parent_phase == "Exécution":
            y_pos = -2
        else:
            y_pos = -4
        
        # Créer un rectangle pour chaque tâche
        fig.add_trace(go.Scatter(
            x=[x_offset, x_offset + 3, x_offset + 3, x_offset],
            y=[y_pos + 0.5, y_pos + 0.5, y_pos - 0.5, y_pos - 0.5],
            fill='toself',
            fillcolor='lightgreen',
            line=dict(color='black'),
            text=task_name,
            mode="text+lines",
            textposition="middle center",
            name=task_name
        ))

        # Relier la tâche à la phase par une ligne
        fig.add_trace(go.Scatter(
            x=[x_offset + 1.5, x_offset + 1.5],
            y=[y_pos, y_pos + 1],  # Relier la tâche à la phase
            mode="lines",
            line=dict(color='black', width=2),
            showlegend=False
        ))

        y_pos -= 1  # Placer la prochaine tâche sous celle-ci

    # Configuration de la mise en page
    fig.update_layout(
        showlegend=False,
        title="WBS avec Rectangles et Branches",
        xaxis=dict(showgrid=False, zeroline=False, range=[0, 12]),
        yaxis=dict(showgrid=False, zeroline=False, range=[-6, 1]),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig)
else:
    st.info("Ajoutez des tâches pour générer le diagramme WBS avec rectangles et branches.")
