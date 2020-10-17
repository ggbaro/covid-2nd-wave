import pandas as pd
from pathlib import Path
from datetime import timedelta

__out_file__ = Path("../data/dpc-covid19-ita-regioni.json")

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
data["delta_ricoverati_con_sintomi"] = data["ricoverati_con_sintomi"] - dataset_tm1["ricoverati_con_sintomi"]  # noqa: E501
data["delta_terapia_intensiva"] = data["terapia_intensiva"] - dataset_tm1["terapia_intensiva"]  # noqa: E501
data["delta_totale_ospedalizzati"] = data["totale_ospedalizzati"] - dataset_tm1["totale_ospedalizzati"]  # noqa: E501
data["delta_isolamento_domiciliare"] = data["isolamento_domiciliare"] - dataset_tm1["isolamento_domiciliare"]  # noqa: E501
data["delta_totale_positivi"] = data["totale_positivi"] - dataset_tm1["totale_positivi"]  # noqa: E501
data["delta_dimessi_guariti"] = data["dimessi_guariti"] - dataset_tm1["dimessi_guariti"]  # noqa: E501
data["delta_deceduti"] = data["deceduti"] - dataset_tm1["deceduti"]  # noqa: E501
data["delta_casi_da_sospetto_diagnostico"] = data["casi_da_sospetto_diagnostico"] - dataset_tm1["casi_da_sospetto_diagnostico"]  # noqa: E501
data["delta_casi_da_screening"] = data["casi_da_screening"] - dataset_tm1["casi_da_screening"]  # noqa: E501
data["delta_totale_casi"] = data["totale_casi"] - dataset_tm1["totale_casi"]  # noqa: E501
data["delta_tamponi"] = data["tamponi"] - dataset_tm1["tamponi"]  # noqa: E501
data["delta_casi_testati"] = data["casi_testati"] - dataset_tm1["casi_testati"]  # noqa: E501

data = data.reset_index()
data = data.dropna(subset=["totale_casi"])
data["data"] = data["data"].astype(str)
data = data.to_json(orient="records")

__out_file__.write_text(data)
