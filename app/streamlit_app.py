# app/streamlit_app.py

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from djohodo.db import load_job_categories_df

# Configuration de la page
st.set_page_config(
    page_title="Djohodo – Demo",
    layout="wide"
)

st.title("Djohodo – Observatoire des offres d’emploi en Data")

# Cache pour éviter de recharger la BDD à chaque interaction
@st.cache_data
def get_data():
    return load_job_categories_df()

df = get_data()

st.write(f"Nombre de lignes : {df.shape[0]}")
st.write("Aperçu des données :")
st.dataframe(df.head())

# --- Graphique seaborn/matplotlib ---

# 1. Ordre trié du plus fréquent au moins fréquent
order = df["job_category"].value_counts().index

# 2. Créer la figure et l'axe matplotlib
fig, ax = plt.subplots(figsize=(12, 6))

# 3. Palette
palette = sns.color_palette("tab20", n_colors=len(order))

sns.countplot(
    data=df,
    x="job_category",
    order=order,
    palette=palette,
    ax=ax
)

# Personnalisation
ax.set_xlabel('Categories')
ax.set_ylabel('Frequency')
ax.tick_params(axis="x", rotation=45)

sns.set_style("whitegrid")
ax.yaxis.grid(True, linestyle='-', linewidth=0.5, color='lightgrey')
sns.despine(bottom=True)

fig.tight_layout()

# 4. Affichage dans Streamlit
st.pyplot(fig)
