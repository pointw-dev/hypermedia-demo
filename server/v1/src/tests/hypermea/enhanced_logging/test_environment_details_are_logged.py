import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.enhanced_logging import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Environment details are logged')
def test_environment_details_are_logged():
    pass
