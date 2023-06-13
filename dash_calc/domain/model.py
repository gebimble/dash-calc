from datetime import datetime
from typing import Union
from pathlib import Path

import xarray as xr
from attrs import define, field


ExperimentFile = Union[str, Path]


@define(kw_only=True)
class Metadata:
    _file: Path = field(converter=Path)
    _start_date: datetime = field(
        converter=lambda x: datetime.strptime(x, "%Y%m%d%H%M%S")
    )
    _temperature: float = field(converter=float)


Experiment = xr.Dataset
