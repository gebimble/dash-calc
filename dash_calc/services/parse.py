from pathlib import Path

from dash_calc.domain.model import Experiment


def parse(filename: Path, parser) -> Experiment:
    return parser(filename)
