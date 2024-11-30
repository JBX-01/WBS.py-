import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

# Configuration de la page
st.set_page_config(page_title="WBS Dynamique avec Branches", layout="wide")

st.title("Structure de Découpage du Travail (WBS) avec Branches")

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
st.subheader("Diagramme WBS avec Branches")

# Création du graphe pour représenter les branches du WBS
if not st.session_state["wbs_data"].empty:
    # Initialisation du graphique NetworkX
    G = nx.DiGraph()
    
    # Ajouter des noeuds (tâches) et des arêtes (dépendances)
    for _, row in st.session_state["wbs_data"].iterrows():
        G.add_node(row["Tâche"], label=row["Tâche"])
        if row["Parent"] != "Aucune":
            G.add_edge(row["Parent"], row["Tâche"])

    # Générer une mise en page hiérarchique
    pos = nx.spring_layout(G, seed=42)

    # Créer une figure Plotly
    trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition='top center',
        marker=dict(size=12, color='skyblue', line=dict(width=2)),
    )

    # Créer les liens entre les tâches avec des flèches
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)
    
    # Créer la figure Plotly avec noeuds et arêtes
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        title="WBS avec Branches",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    fig = go.Figure(data=[edge_trace, trace], layout=layout)
    st.plotly_chart(fig)
else:
    st.info("Ajoutez des tâches pour générer le diagramme WBS avec branches.")
