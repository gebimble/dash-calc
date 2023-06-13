from textwrap import dedent
from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def example_xml():
    xml = dedent(
        """<?xml version="1.0" ?>
<content>
    <filename>example.xml</filename>
    <temperature>37.6</temperature>
    <start_date>20081227101921</start_date>
    <data>
    0,0,0,0,1
    0,0,0,1,2
    0,0,0,3,3
    </data>
</content>"""
    )
    return xml


@pytest.fixture
def example_beautifulsoup(example_xml):
    return BeautifulSoup(example_xml, "xml")


@pytest.fixture
def FakeFile(example_xml):
    class File:
        @staticmethod
        def read_text():
            return example_xml

    return File
