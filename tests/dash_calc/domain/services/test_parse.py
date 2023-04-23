import xarray as xr
from dash_calc.domain.model import Experiment, Metadata

from dash_calc.services.parse import parse
from dash_calc.services import parse_xml

def fake_parser(filename: str):
    return Experiment()

def test_parser_creates_experiment_object():

    fake_file = "fake.xml"
    experiment = parse(fake_file, fake_parser)

    assert type(experiment) is xr.Dataset

def test_content_generated_from_beautifulsoup(example_beautifulsoup):
    datasets, metadata = parse_xml.get_data_from_content(example_beautifulsoup)

    assert datasets and type(datasets) is dict
    assert metadata and type(metadata) is Metadata

def test_xml_parser_content_generated_from_fake_xml_file(FakeFile):
    datasets, metadata = parse_xml.parse(FakeFile)

    assert datasets and type(datasets) is dict
    assert metadata and type(metadata) is Metadata

def test_parser_content_generated_from_fake_xml_file(FakeFile):
    datasets, metadata = parse(FakeFile, parse_xml.parse)
    assert datasets and type(datasets) is dict
    assert metadata and type(metadata) is Metadata