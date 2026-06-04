# Architecture

## Flow
Kaggle CSVs (gitignored) → **Meltano** (tap-csv → target) → **Warehouse**
(DuckDB dev / Snowflake prod) → **dbt** (staging → marts) → **Dagster**
(orchestration + schedule) → **Jupyter** (analysis) + **Streamlit** (serving).

## Layers
- **raw**: 1:1 loaded source tables (Meltano).
- **staging**: typed, cleaned, renamed; one view per source; dbt tests applied.
- **marts**: business entities — `fct_orders`, `dim_customers`,
  `fct_category_performance`, `fct_monthly_revenue`.

## Environments
| Env  | Warehouse | Trigger        |
|------|-----------|----------------|
| dev  | DuckDB    | local / CI     |
| prod | Snowflake | Dagster 06:00 daily |

## Secrets
All credentials come from environment variables. Nothing sensitive is committed
(`.gitignore` blocks `.env`, keys, credentials).
