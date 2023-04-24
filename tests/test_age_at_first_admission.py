"""Test patient_age_at_first_admission."""
import pytest

from patient_parser_v3 import Patient, Labs
import datetime as dt


def test_age_at_first_admission() -> None:
    """Test age_at_first_admission."""
    # Building the tables for the fake files
    Nando = Patient(
        "1",
        "Male",
        dt.datetime(1963, 2, 7, 10, 4, 20, 717),
        "White",
        "Single",
        "Spanish",
        "0.5",
        patient_labs=[
            Labs(
                "1",
                "1",
                "METABOLIC: ALBUMIN",
                3.1,
                "gm/dL",
                dt.datetime(1992, 7, 1, 8, 10, 42, 320000),
            ),
            Labs(
                "1",
                "3",
                "METABOLIC: ALBUMIN",
                3.9,
                "gm/dL",
                dt.datetime(2011, 12, 19, 2, 49, 23, 900000),
            ),
        ],
    )

    # running the tests
    assert Nando.age_at_first_admission == 29
