# Olist Brazilian E-Commerce — End-to-End Data Platform

An end-to-end **ELT pipeline and analytics workflow** for the Olist Brazilian
e-commerce dataset, built by **Team 3** (Clement, Chih Chang, HengQing, BenJ, Danny).

Raw CSVs → **Meltano** (extract/load) → cloud warehouse → **dbt + Dagster**
(transform/orchestrate) → **Jupyter** analysis → **Streamlit** executive dashboard.

---

## Architecture

```
                ┌─────────────┐      ┌──────────────────┐      ┌──────────────────┐
  Kaggle CSVs ─▶│   Meltano   │─────▶│  Warehouse        │─────▶│  dbt (transform) │
  (raw, gitignored)│ tap-csv → │      │  DuckDB (dev/CI)  │      │  staging → marts │
                │ target-*    │      │  Snowflake (prod) │      └────────┬─────────┘
                └─────────────┘      └──────────────────┘               │
                        ▲                                                ▼
                        │                                       ┌──────────────────┐
                ┌───────┴────────┐                              │  Analytics layer │
                │     Dagster     │  schedules + asset lineage   │ Jupyter notebook │
                │  (orchestration)│◀─────────────────────────────│ Streamlit app    │
                └─────────────────┘                              └──────────────────┘
```

| Layer        | Tool                | Why                                                        |
|--------------|---------------------|------------------------------------------------------------|
| Extract/Load | **Meltano** (Singer)| Declarative EL, swappable taps/targets, env-driven config  |
| Warehouse    | **DuckDB** / **Snowflake** | Zero-setup local dev; cloud scale in prod          |
| Transform    | **dbt**             | Versioned SQL models, tests, docs, lineage                 |
| Orchestrate  | **Dagster**         | Asset-based DAG, schedules, observability, retries         |
| Analyze      | **Jupyter**         | Exploratory + reproducible analysis                        |
| Serve        | **Streamlit**       | Executive-facing interactive dashboard                     |

---

## Data Reference

Raw data is **excluded from this repo** (see `.gitignore`) because it is large
(~120 MB). Download the 9 CSVs from Kaggle:

> **Olist Brazilian E-Commerce Public Dataset**
> https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Place all CSVs in `data/raw/`. Expected files:

```
olist_orders_dataset.csv              olist_order_items_dataset.csv
olist_order_payments_dataset.csv      olist_order_reviews_dataset.csv
olist_customers_dataset.csv           olist_sellers_dataset.csv
olist_products_dataset.csv            olist_geolocation_dataset.csv
product_category_name_translation.csv
```
Marketing funnel (separate Kaggle dataset, optional):
`olist_marketing_qualified_leads_dataset.csv`, `olist_closed_deals_dataset.csv`

**Scale:** ~100K orders, 113K order items, $13.6M GMV, Sept 2016 – Oct 2018.

---

## Quickstart (local, zero credentials — runs on DuckDB)

```bash
# 1. Clone + environment
git clone <repo-url> && cd olist-pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Put the Kaggle CSVs in data/raw/  (see Data Reference above)

# 3. Extract + Load (Meltano → DuckDB)
cd meltano && meltano install && meltano run tap-csv target-duckdb && cd ..

# 4. Transform (dbt via Dagster, or directly)
cd transform && dbt build --target dev && cd ..

# 5. Orchestrate everything (Dagster UI on :3000)
dagster dev -m orchestrator.definitions

# 6. Launch the executive dashboard
streamlit run streamlit/app.py
```

`make all` runs steps 3–4 end to end. See `Makefile`.

## Production (Snowflake)

Set credentials as environment variables (never commit them):

```bash
export MELTANO_TARGET=target-snowflake
export SNOWFLAKE_ACCOUNT=... SNOWFLAKE_USER=... SNOWFLAKE_PASSWORD=...
export SNOWFLAKE_DATABASE=OLIST SNOWFLAKE_WAREHOUSE=COMPUTE_WH SNOWFLAKE_ROLE=TRANSFORMER
meltano run tap-csv target-snowflake
dbt build --target prod
```

---

## Repository Layout

```
olist-pipeline/
├── meltano/                 # Meltano project (EL)
│   ├── meltano.yml          # taps, targets, env config
│   └── extract/files.yml    # CSV → stream mapping
├── transform/               # dbt project (T)
│   ├── dbt_project.yml
│   ├── profiles.yml         # dev=duckdb, prod=snowflake
│   └── models/
│       ├── staging/         # 1:1 cleaned source models + tests
│       └── marts/           # business-grade fact/dim tables
├── orchestrator/            # Dagster
│   └── definitions.py       # Meltano + dbt assets, schedule
├── notebooks/
│   └── 01_olist_analysis.ipynb
├── streamlit/
│   └── app.py
├── analysis/                # exported figures + findings
├── docs/                    # architecture, Q&A, findings
├── requirements.txt
├── Makefile
└── .gitignore
```

## Data Quality

Enforced as **dbt tests** (`not_null`, `unique`, `accepted_values`,
referential integrity) plus freshness checks. CI runs `dbt build` on DuckDB so
every PR validates the full DAG without cloud credentials.

## Key Findings (summary)

See `docs/FINDINGS.md` and the executive deck. Headlines:
- **$13.6M GMV**, ~100K orders, **AOV ≈ R$161**, avg review **4.09 / 5**.
- **Late delivery is the #1 satisfaction killer**: on-time orders score **4.29**,
  late orders **2.57** — a 1.7-point drop. 8.1% of orders arrive late.
- **Revenue is geographically concentrated**: São Paulo state ≈ **38% of GMV**.
- **Retention is the biggest untapped lever**: only **3.1%** of customers reorder.
