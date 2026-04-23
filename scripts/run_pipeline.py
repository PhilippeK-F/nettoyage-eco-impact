# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from extract import extract
from transform import transform


def load(df, output_path: str = "data/produits_clean.csv") -> None:
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[load] Fichier sauvegarde → {output_path}")


def main():
    print("=== Pipeline demarrage ===")

    print("\n1. Extraction...")
    df_raw = extract(output_path="data/produits_nettoyage.csv")

    print("\n2. Transformation...")
    df_clean = transform(df_raw)

    print("\n3. Chargement...")
    load(df_clean, output_path="data/produits_clean.csv")

    print("\n=== Pipeline termine ===")
    print(f"    Lignes  : {len(df_clean)}")
    print(f"    Colonnes: {len(df_clean.columns)}")
    print(f"    Fichier : data/produits_clean.csv")


if __name__ == "__main__":
    main()