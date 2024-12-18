import pytest

from bilangrender import render

__author__ = "Xiaoguang Zhu"
__copyright__ = "Xiaoguang Zhu"
__license__ = "MIT"


def test_render():
    """API Tests"""
    assert render("<a>hello</a>") == "<a>Bonjour</a>"

