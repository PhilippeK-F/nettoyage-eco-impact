import pandas as pd
from sqlalchemy import create_engine
import os
import time

# Attendre que PostgreSQL soit prêt
time.sleep(5)

# Paramètres de connexion depuis les variables d'environnement
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")
DB_NAME = os.getenv("DB_NAME", "produits_nettoyants")

# Connexion à PostgreSQL
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("✅ Connexion à PostgreSQL réussie")

# Chargement du CSV
df = pd.read_csv("/app/produits_clean.csv")
print(f"✅ CSV chargé — {len(df)} lignes, {len(df.columns)} colonnes")

# Nettoyage basique
df["date"] = pd.to_datetime(df["date"])
df["est_eco"] = df["est_eco"].astype(bool)
df["ecolabel_eu"] = df["ecolabel_eu"].astype(bool)
df["conforme_reach"] = df["conforme_reach"].astype(bool)
df["nordic_swan"] = df["nordic_swan"].astype(bool)
df["ph_neutre"] = df["ph_neutre"].astype(bool)

# Chargement dans PostgreSQL
df.to_sql(
    name="produits_clean",
    con=engine,
    if_exists="replace",
    index=False
)

print(f"✅ Table 'produits_clean' chargée dans PostgreSQL ({len(df)} lignes)")

# Création des tables de dimension (schéma en étoile)

# DIM_Fournisseur
dim_fournisseur = df[["fournisseur"]].drop_duplicates().reset_index(drop=True)
dim_fournisseur.to_sql("dim_fournisseur", con=engine, if_exists="replace", index=False)
print(f"✅ Table 'dim_fournisseur' créée ({len(dim_fournisseur)} lignes)")

# DIM_Produit
dim_produit = df[["produit", "categorie", "type_chimique"]].drop_duplicates().reset_index(drop=True)
dim_produit.to_sql("dim_produit", con=engine, if_exists="replace", index=False)
print(f"✅ Table 'dim_produit' créée ({len(dim_produit)} lignes)")

# DIM_Temps
dim_temps = df[["date", "annee", "mois", "trimestre", "mois_label"]].drop_duplicates().reset_index(drop=True)
dim_temps.to_sql("dim_temps", con=engine, if_exists="replace", index=False)
print(f"✅ Table 'dim_temps' créée ({len(dim_temps)} lignes)")

print("\n🎉 Chargement terminé — toutes les tables sont prêtes dans PostgreSQL !")