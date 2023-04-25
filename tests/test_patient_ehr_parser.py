"""Test parse_data function."""
import pytest

from fake_files import fake_files
from patient_parser_v4 import parse_data, Patient, Lab
import datetime as dt


def test_parser() -> None:
    """Test parse_data."""
    # Building the tables for the fake files
    table_patient = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        [
            "1",
            "Male",
            "1947-12-28 02:45:40.547",
            "White",
            "Married",
            "English",
            "0.1",
        ],
        [
            "2",
            "Female",
            "1999-11-30 03:40:20.247",
            "Black",
            "Single",
            "Spanish",
            "16.09",
        ],
    ]

    table_lab = [
        [
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        [
            "1",
            "1",
            "METABOLIC: ALBUMIN",
            "3.1",
            "gm/dL",
            "1992-07-01 08:10:42.320",
        ],
        [
            "1",
            "3",
            "METABOLIC: ALBUMIN",
            "3.9",
            "gm/dL",
            "2011-12-19 02:49:23.900",
        ],
        [
            "2",
            "1",
            "METABOLIC: URINE PROTEIN",
            "3.9",
            "gm/dL",
            "2011-12-19 02:49:23.900",
        ],
    ]
    # crearting the patient and lab dictionaries
    with fake_files(table_patient, table_lab) as files:
        patient_dict, lab_dict = parse_data(files[0], files[1])

    # Running the assertions for the patient dictionary

    # asserting patient attributes minus labs
    assert patient_dict["1"].id == "1"
    assert patient_dict["1"].gender == "Male"
    # pleasing pycode style
    validation_date_patient_1 = dt.datetime(1947, 12, 28, 2, 45, 40, 547000)
    assert patient_dict["1"].dob == validation_date_patient_1
    assert patient_dict["1"].race == "White"
    assert patient_dict["1"].marital_status == "Married"
    assert patient_dict["1"].language == "English"
    assert patient_dict["1"].poverty_level == "0.1"

    assert patient_dict["2"].id == "2"
    assert patient_dict["2"].gender == "Female"
    # pleasing pycode style
    validation_date_patient_2 = dt.datetime(1999, 11, 30, 3, 40, 20, 247000)
    assert patient_dict["2"].dob == validation_date_patient_2
    assert patient_dict["2"].race == "Black"
    assert patient_dict["2"].marital_status == "Single"
    assert patient_dict["2"].language == "Spanish"
    assert patient_dict["2"].poverty_level == "16.09"

    # asserting patient labs

    assert patient_dict["1"].labs[0].patient_id == "1"
    assert patient_dict["1"].labs[0].admission_id == 1
    assert patient_dict["1"].labs[0].name == "METABOLIC: ALBUMIN"
    assert patient_dict["1"].labs[0].value == 3.1
    assert patient_dict["1"].labs[0].unit == "gm/dL"
    validation_lab_date_patient_1 = dt.datetime(1992, 7, 1, 8, 10, 42, 320000)
    patient_dict_patient_1_lab_0_date = patient_dict["1"].labs[0].date
    assert patient_dict_patient_1_lab_0_date == validation_lab_date_patient_1

    assert patient_dict["1"].labs[1].patient_id == "1"
    assert patient_dict["1"].labs[1].admission_id == 3
    assert patient_dict["1"].labs[1].name == "METABOLIC: ALBUMIN"
    assert patient_dict["1"].labs[1].value == 3.9
    assert patient_dict["1"].labs[1].unit == "gm/dL"
    assert patient_dict["1"].labs[1].date == dt.datetime(
        2011, 12, 19, 2, 49, 23, 900000
    )

    assert patient_dict["2"].labs[0].patient_id == "2"
    assert patient_dict["2"].labs[0].admission_id == 1
    assert patient_dict["2"].labs[0].name == "METABOLIC: URINE PROTEIN"
    assert patient_dict["2"].labs[0].value == 3.9
    assert patient_dict["2"].labs[0].unit == "gm/dL"
    assert patient_dict["2"].labs[0].date == dt.datetime(
        2011, 12, 19, 2, 49, 23, 900000
    )

    # assert for age
    assert patient_dict["1"].age == 76
    assert patient_dict["2"].age == 24

    # assert for is_sick
    assert patient_dict["1"].is_sick("METABOLIC: ALBUMIN", ">", 3.6)
    assert not (
        patient_dict["2"].is_sick("METABOLIC: URINE PROTEIN", ">", 5.0)
    )
    try:
        assert patient_dict["2"].is_sick(
            """
            METABOLIC: URINE PROTEIN
            """,
            "<",
            2.8,
        )
    except ValueError:
        print("ValueError: Urinalysis is not a valid lab name")
        print("This error was caught successfully")
        pass

    # assert for age_at_first_admission
    assert patient_dict["1"].age_at_first_admission == 45
    assert patient_dict["2"].age_at_first_admission == 12
