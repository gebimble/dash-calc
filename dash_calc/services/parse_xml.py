from io import StringIO
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
import xarray as xr

from dash_calc.domain.model import Metadata, Experiment


TAG_MAP = {
    "file": "content filename",
    "temperature": "content temperature",
    "start_date": "content start_date",
    "data": "content data",
}


def parse(xml_file: Path) -> Experiment:

    xml_content = xml_file.read_text()
    bs = BeautifulSoup(xml_content, "xml")

    return get_data_from_content(bs)


def get_data_from_content(content: BeautifulSoup):

    metadata_dict = {k: content.select(v)[0].text for k, v in TAG_MAP.items()}

    data = pd.read_csv(StringIO(metadata_dict.pop("data")), sep=",")

    data.columns = ["x", "y", "z", "t", "value"]

    data.set_index(["x", "y", "z", "t"])

    datasets = {k: v for k, v in xr.Dataset.from_dataframe(data).items()}

    metadata = Metadata(**metadata_dict)

    return datasets, metadata
