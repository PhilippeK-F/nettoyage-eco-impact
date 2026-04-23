import pandas as pd
import numpy as np
import os

def extract(output_path: str = "data/produits_nettoyage.csv") -> pd.DataFrame:
    """
    Simule l'extraction d'un dataset de produits de nettoyage industriel.
    En production : remplacer par une connexion BDD ou API fournisseur.
    """
    np.random.seed(42)

    produits = [
        ("Dégraissant alcalin HD",          "dégraissant",      "alcalin"),
        ("Dégraissant solvant chloré",       "dégraissant",      "solvant"),
        ("Dégraissant biosourcé CitraClean", "dégraissant",      "biosourcé"),
        ("Désinfectant quaternaire QAC-50",  "désinfectant",     "ammonium quaternaire"),
        ("Désinfectant peroxyde EcoPur",     "désinfectant",     "peroxyde"),
        ("Nettoyant acide détartrant",       "détartrant",       "acide"),
        ("Nettoyant acide biosourcé",        "détartrant",       "biosourcé"),
        ("Décapant sol industriel",          "décapant",         "solvant"),
        ("Décapant sol enzymatique",         "décapant",         "enzymatique"),
        ("Mousse nettoyante toutes surfaces","nettoyant multi",  "tensioactif"),
        ("Mousse écologique certifiée",      "nettoyant multi",  "biosourcé"),
        ("Nettoyant haute pression concentré","nettoyant HP",    "alcalin"),
        ("Nettoyant HP vert dilution forte", "nettoyant HP",     "biosourcé"),
        ("Désodorisant industriel masquant", "désodorisant",     "synthétique"),
        ("Désodorisant enzymatique",         "désodorisant",     "enzymatique"),
        ("Cire sol industrielle",            "entretien sol",    "solvant"),
        ("Emulsion sol biosourcée",          "entretien sol",    "biosourcé"),
        ("Antirouille process",              "traitement surface","acide"),
        ("Nettoyant inox alimentaire",       "nettoyant inox",   "acide"),
        ("Nettoyant inox écologique",        "nettoyant inox",   "biosourcé"),
    ]

    fournisseurs = ["ChemPro", "EcoClean", "IndustraNett", "VerteChimie", "ProHygiène"]

    rows = []
    for _ in range(400):
        idx = np.random.randint(0, len(produits))
        nom, categorie, type_chimique = produits[idx]

        # Drapeaux utiles pour calculer les indicateurs
        biosource  = type_chimique in ("biosourcé", "enzymatique", "peroxyde")
        solvant    = type_chimique == "solvant"
        acide      = type_chimique == "acide"
        qac        = type_chimique == "ammonium quaternaire"

        # COV (Composés Organiques Volatils) en g/L
        # Les solvants émettent beaucoup, les biosourcés presque rien
        cov_base = 0.5 if biosource else (120 if solvant else (15 if qac else 8))
        cov = max(0, np.random.normal(cov_base, cov_base * 0.25))

        # DBO5 : demande biologique en oxygène — mesure la biodégradabilité
        dbo_base = 800 if biosource else (120 if acide else (200 if qac else 350))
        dbo5 = max(10, np.random.normal(dbo_base, dbo_base * 0.2))

        # pH : acides très bas, alcalins très hauts, biosourcés neutres
        if acide:
            ph = round(np.random.uniform(1.5, 4.0), 1)
        elif type_chimique == "alcalin":
            ph = round(np.random.uniform(10.5, 13.5), 1)
        elif biosource:
            ph = round(np.random.uniform(6.5, 8.5), 1)
        else:
            ph = round(np.random.uniform(5.0, 10.0), 1)

        # Dose d'utilisation en mL par litre d'eau
        dose = round(np.random.uniform(2, 80), 1)

        # Biodégradabilité en % — les biosourcés se dégradent bien mieux
        biodeg = np.random.uniform(75, 99) if biosource else np.random.uniform(20, 65)
        biodeg = round(biodeg, 1)

        # LC50 Daphnie (mg/L) : écotoxicité aquatique
        # Plus la valeur est haute, moins le produit est toxique pour les organismes aquatiques
        lc50_base = 400 if biosource else (8 if solvant else (25 if qac else 80))
        lc50 = max(1, np.random.normal(lc50_base, lc50_base * 0.3))
        lc50 = round(lc50, 1)

        # Score environnemental composite sur 10
        # Combine biodégradabilité, écotoxicité, COV et neutralité du pH
        score = (
            (biodeg / 100) * 3
            + min(lc50 / 500, 1) * 3
            + (1 - min(cov / 150, 1)) * 2
            + (1 - min(abs(ph - 7) / 6.5, 1)) * 2
        )
        score = round(min(max(score, 1), 10), 2)

        # Prix au litre — les biosourcés coûtent ~40% plus cher
        prix = round(np.random.uniform(2.5, 45) * (1.4 if biosource else 1), 2)

        # Certifications
        ecolabel   = biosource and np.random.random() > 0.3
        reach_ok   = not solvant or np.random.random() > 0.6
        nordic_swan = biosource and np.random.random() > 0.5

        annee = np.random.randint(2021, 2025)
        mois  = np.random.randint(1, 13)

        rows.append({
            "date":                      f"{annee}-{mois:02d}-01",
            "produit":                   nom,
            "categorie":                 categorie,
            "type_chimique":             type_chimique,
            "fournisseur":               np.random.choice(fournisseurs),
            "quantite_kg":               round(np.random.uniform(5, 500), 1),
            "prix_litre_eur":            prix,
            "ph":                        ph,
            "cov_g_par_l":               round(cov, 2),
            "dbo5_mg_par_l":             round(dbo5, 1),
            "biodegradabilite_pct":      biodeg,
            "lc50_daphnie_mg_par_l":     round(lc50, 1),
            "dose_utilisation_ml_par_l": dose,
            "score_env":                 score,
            "ecolabel_eu":               ecolabel,
            "conforme_reach":            reach_ok,
            "nordic_swan":               nordic_swan,
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"[extract] {len(df)} lignes extraites → {output_path}")
    return df


if __name__ == "__main__":
    extract()
