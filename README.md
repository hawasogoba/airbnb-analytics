# 🏠 Airbnb Analytics Platform

Plateforme analytique permettant d'analyser les logements, les hôtes et les avis clients Airbnb, avec un focus particulier sur l'impact des nuits de pleine lune sur les avis. Les indicateurs sont restitués via un dashboard interactif Streamlit.

## 📑 Sommaire
- [Contexte](#contexte)
- [Stack technique](#stack-technique)
- [Architecture](#architecture)
- [Installation et exécution](#installation-et-exécution)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Tests de qualité des données](#tests-de-qualité-des-données)
- [Indicateurs clés](#indicateurs-clés)
- [Répartition des tâches](#répartition-des-tâches)

## Contexte

Airbnb souhaite mettre en place une plateforme analytique permettant :
- d'analyser les logements ;
- d'analyser les hôtes ;
- d'analyser les avis clients ;
- d'étudier l'impact des nuits de pleine lune sur les avis ;
- de mettre à disposition des indicateurs via une application Streamlit.

## Stack technique

| Outil | Rôle |
|---|---|
| **DuckDB** | Moteur analytique (base de données embarquée) |
| **dbt** | Transformations SQL (architecture Bronze → Silver → Gold) |
| **Streamlit** | Dashboard de restitution interactif |
| **Git / GitHub** | Versioning et collaboration |

## Architecture

```
                GitHub
                   │
                   ▼
            dbt Project
                   │
     ┌─────────────┼─────────────┐
     ▼              ▼              ▼
  Bronze          Silver           Gold
     │              │               │
     └──────────────┴───────────────┘
                   │
                DuckDB
                   │
                   ▼
              Streamlit
                   │
                   ▼
            Business Users
```

- **Bronze** : ingestion brute des données sources (hosts, listings, reviews, dates de pleine lune)
- **Silver** : nettoyage, typage, jointures (ex. avis ↔ nuits de pleine lune)
- **Gold** : indicateurs métier prêts à consommer (KPIs logements, hôtes, impact pleine lune)

## Installation et exécution

### Prérequis
- Python 3.10+
- Git

### Étapes

```bash
# 1. Cloner le repo
git clone https://github.com/hawasogoba/airbnb-analytics.git
cd airbnb-analytics

# 2. Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source venv/bin/activate       # macOS / Linux

# 3. Installer les dépendances
pip install duckdb dbt-duckdb streamlit pandas requests

# 4. Télécharger les données sources
mkdir data\raw
Invoke-WebRequest -Uri "https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/hosts.csv" -OutFile "data\raw\hosts.csv"
Invoke-WebRequest -Uri "https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv" -OutFile "data\raw\reviews.csv"
Invoke-WebRequest -Uri "https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/listings.csv" -OutFile "data\raw\listings.json"
Invoke-WebRequest -Uri "https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/seed_full_moon_dates.csv" -OutFile "data\raw\seed_full_moon_dates.csv"

# 5. Lancer l'ingestion Bronze (crée airbnb.duckdb)
cd dbt_project
python ingest_bronze.py

# 6. Lancer les transformations dbt (Silver + Gold) et les tests
cd airbnb_dbt
dbt run
dbt test

# 7. Lancer le dashboard
cd ..\..\streamlit_app
streamlit run app.py
```

> ℹ️ Les fichiers de données brutes (`data/raw/`) et la base `airbnb.duckdb` ne sont **pas versionnés** sur Git (voir `.gitignore`) : ils sont régénérés localement via les étapes 4 à 6 ci-dessus.

## Fonctionnalités

- **Ingestion Bronze** : chargement brut des 4 sources de données dans DuckDB
- **Transformations Silver** : nettoyage, typage (ex. conversion du prix en nombre), jointure entre les avis et les dates de pleine lune
- **Indicateurs Gold** :
  - KPIs logements (nombre et prix moyen par type de logement)
  - KPIs hôtes (nombre de logements par hôte)
  - Impact des nuits de pleine lune sur le sentiment des avis
- **Dashboard Streamlit** :
  - Visualisations interactives (graphiques en barres, tableaux)
  - Filtre dynamique par type de logement
- **Tests de qualité de données** : `not_null` et `unique` sur les tables sources (hosts, listings)

## Structure du projet

```
airbnb-analytics/
├── data/
│   └── raw/                      # Données sources (non versionnées)
├── dbt_project/
│   ├── ingest_bronze.py          # Script d'ingestion Bronze
│   └── airbnb_dbt/
│       ├── models/
│       │   ├── sources.yml       # Déclaration des sources + tests
│       │   ├── silver/           # Modèles Silver (nettoyage, jointures)
│       │   └── gold/             # Modèles Gold (indicateurs métier)
│       └── dbt_project.yml
├── streamlit_app/
│   └── app.py                    # Dashboard Streamlit
├── .gitignore
└── README.md
```

## Tests de qualité des données

Exécutés via dbt (`dbt test`) sur les tables sources :
- `not_null` sur les identifiants (`hosts.id`, `listings.id`)
- `unique` sur les identifiants (`hosts.id`, `listings.id`)

## Indicateurs clés

| Indicateur | Description |
|---|---|
| Répartition des logements | Nombre et prix moyen par type de logement |
| Top hôtes | Hôtes classés par nombre de logements |
| Impact pleine lune | Comparaison du sentiment des avis selon que la nuit était une nuit de pleine lune ou non |

## Projet réalisé en solo 
Hawa SOGOBA 
---
