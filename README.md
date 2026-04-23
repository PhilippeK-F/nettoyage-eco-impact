# nettoyage-eco-impact

Analyse de l'impact écologique des produits de nettoyage industriel.  
Projet Data Engineering + Data Analyst — Python, pandas, Streamlit.

## Contexte

400 achats simulés sur 4 ans (2021–2024), 20 références produits.  
Indicateurs analysés : COV, biodégradabilité, écotoxicité aquatique, pH, score environnemental.

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Docker
```bash
docker compose up --build
```

## Structure
src/pipelines/   → ETL : extract, transform, load
notebooks/       → EDA et KPIs (Jupyter)
dashboard/       → Interface Streamlit
data/            → Dataset CSV (non versionné)
reports/         → Rapport Markdown
tests/           → Tests pytest

## Stack

Python · pandas · Streamlit · Jupyter · Docker · GitHub Actions

## Contenu du dashboard

Le dashboard est organisé en 3 pages :
Page 1 — Vue Générale

4 KPI Cards : Nb Produits, Coût total, Score environnemental moyen, Produits à risque élevé
Donut chart : Répartition écologique des produits
Column chart : Coût total par catégorie

Page 2 — Analyse Environnementale

Bar chart : Top produits par impact environnemental
Scatter plot : Coût vs Impact environnemental (taille = quantité achetée)
Table décisionnelle avec mise en forme conditionnelle (🔴🟠🟢)

Page 3 — Suivi Fournisseurs

Bar chart : Coût total par fournisseur
Line chart : Évolution mensuelle du score environnemental par fournisseur

##  Modèle de données — Schéma en étoile

DIM_Temps ──────────┐
DIM_Produit ─────────┼──► FAIT_Produits (produits_clean)
DIM_Fournisseur ─────┘

## Auteur :

Philippe Kirstetter-Fender
