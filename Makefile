.PHONY: install el transform run dashboard all clean test

install:
	pip install -r requirements.txt
	cd meltano && meltano install

el:
	cd meltano && meltano run tap-csv target-duckdb

transform:
	cd transform && dbt build --target dev

test:
	cd transform && dbt test --target dev

run:
	dagster dev -m orchestrator.definitions

dashboard:
	streamlit run streamlit/app.py

all: el transform

clean:
	rm -f data/*.duckdb data/*.duckdb.wal
	rm -rf transform/target transform/logs
