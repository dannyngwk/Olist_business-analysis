"""Dagster orchestration for the Olist pipeline.

Assets:
  meltano_el  -> runs Meltano (tap-csv -> target-duckdb/snowflake)
  dbt models  -> loaded from the dbt project via dagster-dbt

A daily schedule materializes the full DAG. Run locally with:
    dagster dev -m orchestrator.definitions
"""
import os
import subprocess
from pathlib import Path

from dagster import (
    AssetExecutionContext,
    Definitions,
    ScheduleDefinition,
    asset,
    define_asset_job,
)
from dagster_dbt import DbtCliResource, dbt_assets

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MELTANO_DIR = PROJECT_ROOT / "meltano"
DBT_DIR = PROJECT_ROOT / "transform"
MELTANO_TARGET = os.getenv("MELTANO_TARGET", "target-duckdb")

# dbt assets are generated from the manifest produced by `dbt parse`.
dbt_resource = DbtCliResource(project_dir=os.fspath(DBT_DIR), profiles_dir=os.fspath(DBT_DIR))
manifest_path = DBT_DIR / "target" / "manifest.json"


@asset(compute_kind="meltano")
def meltano_el(context: AssetExecutionContext) -> None:
    """Extract raw CSVs and load them into the warehouse via Meltano."""
    context.log.info(f"Running Meltano: tap-csv {MELTANO_TARGET}")
    result = subprocess.run(
        ["meltano", "run", "tap-csv", MELTANO_TARGET],
        cwd=MELTANO_DIR,
        capture_output=True,
        text=True,
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise RuntimeError("Meltano EL run failed")


if manifest_path.exists():

    @dbt_assets(manifest=manifest_path)
    def olist_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
        # dbt models depend on meltano_el having loaded raw schema first.
        yield from dbt.cli(["build"], context=context).stream()

    all_assets = [meltano_el, olist_dbt_assets]
else:
    # Manifest not yet built: run `dbt parse` in transform/ to enable dbt assets.
    all_assets = [meltano_el]

pipeline_job = define_asset_job("olist_pipeline", selection="*")

daily_schedule = ScheduleDefinition(
    job=pipeline_job,
    cron_schedule="0 6 * * *",  # 06:00 daily
)

defs = Definitions(
    assets=all_assets,
    jobs=[pipeline_job],
    schedules=[daily_schedule],
    resources={"dbt": dbt_resource},
)
