# Anticipated Questions & Concise Responses

Prepared for the executive presentation (CEO, CMO, CTO, VP Eng).

### Business / Strategy

**Q: What's the single most important takeaway?**
Retention is our biggest untapped lever. We're acquiring well (8x GMV growth) but
only 3% of customers reorder. Fixing delivery reliability is the fastest way to
improve both satisfaction and repeat purchase.

**Q: How confident are you in the late-delivery → satisfaction link?**
It's a strong, consistent pattern across ~96K delivered orders: on-time averages
4.29★, late averages 2.57★. It's correlational, but the sample is large and the
gap is wide and stable. We'd validate causality with a controlled SLA pilot.

**Q: What would you do first, and what's the ROI?**
A delivery-SLA program on the worst lanes. The 8.1% of late orders are
concentrated, so targeted fixes are cheaper than a blanket overhaul, and the
satisfaction lift compounds through retention and word-of-mouth.

**Q: Why is São Paulo concentration a risk and an opportunity?**
SP is ~38% of GMV — a single-region dependency. It's also proof the model works;
replicating SP's fulfillment density in RJ/MG could unlock comparable growth.

**Q: The data ends in 2018 — is it still relevant?**
It's a public benchmark dataset, so the absolute numbers are illustrative. The
*methodology and platform* are what we're presenting — they run identically on
live data once connected to production sources.

### Technical

**Q: Why Meltano + dbt + Dagster instead of one tool?**
Separation of concerns: Meltano handles declarative extract/load with swappable
connectors; dbt gives us version-controlled, tested transformations; Dagster
orchestrates with asset lineage and observability. Each is best-in-class and
independently replaceable.

**Q: Why DuckDB locally but Snowflake in production?**
DuckDB gives zero-credential local dev and CI — every PR runs the full DAG free.
Snowflake provides scale and concurrency in production. The dbt models are
identical; only the profile target changes.

**Q: How do you ensure data quality?**
dbt tests on every model — not_null, unique, accepted_values, referential
integrity — plus freshness checks. CI fails the build if any test fails, so bad
data can't reach the dashboard.

**Q: Is this production-ready or a prototype?**
Production-ready structure: env-driven secrets (never committed), CI on DuckDB,
scheduled daily runs via Dagster, modular layers, and a read-only serving app.
Scaling to production means pointing the warehouse target at Snowflake.

**Q: How does it handle schema changes or new sources?**
Add a new tap entry in `meltano.yml` and a staging model in dbt. Dagster picks up
the new dbt assets automatically from the manifest. The layered design isolates
changes.

**Q: What about cost?**
Local/CI is free (DuckDB). Snowflake cost is controllable via warehouse sizing
and the daily-batch schedule (no always-on compute). dbt's incremental models can
further cut warehouse spend as volume grows.

**Q: How would you add real-time / streaming?**
The batch design is intentional for this use case. For real-time, we'd add a
streaming tap or CDC source and a separate Dagster sensor-driven job, keeping the
same dbt marts as the serving contract.
