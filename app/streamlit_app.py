# app/streamlit_app.py

import sys
from pathlib import Path

# On ajoute le dossier "src" au PYTHONPATH pour pouvoir faire "import djohodo..."
ROOT = Path(__file__).resolve().parents[1]  # parent de app/ = racine du projet
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from djohodo.db import load_job_category_counts

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Djohodo – Demo",
    layout="wide"
)

st.title("Djohodo – Observatoire des offres d’emploi en Data")

# Cache pour éviter de recharger la BDD à chaque interaction
@st.cache_data
def get_data():
    return load_job_category_counts()

df = get_data()

# --- Filtre de catégorie de métier ---

all_categories = sorted(df["job_category"].unique())
options = ["Toutes les catégories"] + all_categories

selected_category = st.selectbox(
    "Filtrer par catégorie de métier",
    options=options,
    index=0
)

if selected_category == "Toutes les catégories":
    filtered_df = df.copy()
else:
    filtered_df = df[df["job_category"] == selected_category]


# KPIs basés sur le df filtré
total_offers = int(filtered_df["count"].sum())
num_categories = int(filtered_df["job_category"].nunique())

# Si on a au moins 1 catégorie après filtre
if not filtered_df.empty:
    top_category = filtered_df.sort_values("count", ascending=False).iloc[0]["job_category"]
else:
    top_category = "Aucune"


st.markdown("""
<style>
div[data-testid="stMetric"] {
    border: 1px solid #ddd;
    padding: 15px 15px 10px 15px;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total d’offres analysées",
        value=f"{total_offers:,}".replace(",", " ")
    )

with col2:
    st.metric(
        label="Catégories de métiers",
        value=str(num_categories)
    )

with col3:
    st.metric(
        label="Catégorie la plus fréquente",
        value=top_category
    )


# --- Graphique seaborn/matplotlib basé sur la table GOLD ---

# Trier les données du plus grand au plus petit
plot_df  = filtered_df.sort_values("count", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=plot_df,
    x="job_category",
    y="count",
    palette="tab20",
    ax=ax
)

ax.set_xlabel('Catégories')
ax.set_ylabel('Nombre d’offres')
ax.tick_params(axis="x", rotation=45)

sns.set_style("whitegrid")
ax.yaxis.grid(True, linestyle='-', linewidth=0.5, color='lightgrey')
sns.despine(bottom=True)

fig.tight_layout()

# Affichage Streamlit
st.pyplot(fig)

st.write("Aperçu des données :")
st.dataframe(df.head(10))
