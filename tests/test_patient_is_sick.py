"""Test patient_is_sick."""
import pytest

import datetime as dt
from patient_parser_v3 import Patient, Labs


def test_patient_is_sick() -> None:
    """Test patient_is_sick."""
    # Building the tables for the fake files
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

    # Testing the patient_is_sick function
    assert Luis.is_sick("METABOLIC: ALBUMIN", ">", 3.0)
    assert not (Luis.is_sick("METABOLIC: ALBUMIN", "<", 3.5))

    try:
        assert Luis.is_sick("Urinalysis", ">", 3.0)
    except ValueError:
        print("ValueError: Urinalysis is not a valid lab name")
        print("This error was caught successfully")
        pass
