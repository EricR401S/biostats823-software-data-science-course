"""Test patient_age."""
import pytest

from patient_parser_v3 import Patient, Labs
import datetime as dt


def test_patient_age() -> None:
    """Test patient_age."""
    # Building the patient dictionary for the test
    Luis = Patient(
        "1",
        "Male",
        dt.datetime(1947, 12, 28, 2, 45, 40, 547000),
        "White",
        "Married",
        "Spanish",
        "0.1",
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

    # testing the patient_age function
    assert Luis.age == 76
