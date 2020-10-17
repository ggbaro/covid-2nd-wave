import pandas as pd
from pathlib import Path
from datetime import timedelta

__out_file__ = Path("./data/dpc-covid19-ita-regioni.json")

data = pd.read_csv(
    "https://github.com/pcm-dpc/COVID-19/raw/master/"
    "dati-regioni/dpc-covid19-ita-regioni.csv",
    parse_dates=["data"]
)
data["data"] = data["data"].dt.floor("D")

data["to_bench_date"] = data["data"] + timedelta(days=1)
dataset_tm1 = data.set_index(
    ["denominazione_regione", "to_bench_date"]
)
dataset_tm1.index.names = ["denominazione_regione", "data"]

data = data.set_index(["denominazione_regione", "data"])
data = data.drop(columns=["to_bench_date"])

dataset_tm1 = dataset_tm1.loc[:, [
        "ricoverati_con_sintomi",
        "terapia_intensiva",
        "totale_ospedalizzati",
        "isolamento_domiciliare",
        "totale_positivi",
        "dimessi_guariti",
        "deceduti",
        "casi_da_sospetto_diagnostico",
        "casi_da_screening",
        "totale_casi",
        "tamponi",
        "casi_testati"
    ]]

data = data.reindex(dataset_tm1.index)
for col in dataset_tm1.columns:
    data[f"delta_{col}"] = data[col] - dataset_tm1[col]

data = data.reset_index()
data = data.dropna(subset=["totale_casi"])
data["data"] = data["data"].astype(str)
data = data.to_json(orient="records")

__out_file__.write_text(data)
