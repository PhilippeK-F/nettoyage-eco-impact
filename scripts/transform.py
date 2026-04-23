import pandas as pd
import numpy as np


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et enrichit le dataset brut.
    Produit les colonnes analytiques pour Power BI et Streamlit.
    """
    df = df.copy()

    # --- Nettoyage de base ---
    df.columns = [c.lower().strip() for c in df.columns]
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"])

    # --- Colonnes temporelles ---
    # Utiles pour les axes de tendance dans Power BI
    df["annee"]    = df["date"].dt.year
    df["mois"]     = df["date"].dt.month
    df["trimestre"] = df["date"].dt.quarter
    df["mois_label"] = df["date"].dt.strftime("%Y-%m")

    # --- Indicateurs dérivés ---

    # Charge COV totale : combien de grammes de COV
    # ce lot a-t-il potentiellement émis ?
    df["charge_cov_g"] = (df["cov_g_par_l"] * df["quantite_kg"]).round(2)

    # Drapeau éco-responsable : les familles chimiques
    # qui ont un meilleur profil environnemental
    df["est_eco"] = df["type_chimique"].isin(
        ["biosourcé", "enzymatique", "peroxyde"]
    )

    # Le pH est-il dans la zone neutre (6.5–8.5) ?
    # Important pour le traitement des eaux usées
    df["ph_neutre"] = df["ph"].between(6.5, 8.5)

    # Segment de risque écologique basé sur le score
    df["segment_risque"] = pd.cut(
        df["score_env"],
        bins=[0, 5, 7.5, 10],
        labels=["Risque élevé", "Risque modéré", "Faible risque"]
    ).astype(str)

    # Ratio coût / performance environnementale
    # Un ratio bas = produit éco ET pas cher (idéal)
    df["ratio_cout_score"] = (df["prix_litre_eur"] / df["score_env"]).round(3)

    # Coût total de la commande (approximatif)
    df["cout_total_eur"] = (df["prix_litre_eur"] * df["quantite_kg"]).round(2)

    # --- Réorganisation des colonnes ---
    cols_ordre = [
        "date", "annee", "mois", "trimestre", "mois_label",
        "produit", "categorie", "type_chimique", "fournisseur",
        "quantite_kg", "prix_litre_eur", "cout_total_eur",
        "ph", "ph_neutre",
        "cov_g_par_l", "charge_cov_g",
        "dbo5_mg_par_l", "biodegradabilite_pct",
        "lc50_daphnie_mg_par_l", "dose_utilisation_ml_par_l",
        "score_env", "segment_risque", "ratio_cout_score",
        "est_eco", "ecolabel_eu", "conforme_reach", "nordic_swan",
    ]
    df = df[cols_ordre]

    print(f"[transform] {len(df)} lignes, {len(df.columns)} colonnes")
    return df


if __name__ == "__main__":
    df_raw = pd.read_csv("data/produits_nettoyage.csv", parse_dates=["date"])
    df_clean = transform(df_raw)
    print(df_clean.head())
    print(df_clean.dtypes)