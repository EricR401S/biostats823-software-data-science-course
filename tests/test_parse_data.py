"""Test parse_data function."""
import pytest

from fake_files import fake_files
from patient_parser_v3 import parse_data


def test_parse_data() -> None:
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
            "2",
            "METABOLIC: ALBUMIN",
            "5.8",
            "gm/dL",
            "2005-07-26 09:51:51.223",
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

    assert patient_dict == {
        "1": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1947-12-28 02:45:40.547",
            "PatientRace": "White",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "English",
            "PatientPopulationPercentageBelowPoverty": "0.1",
        },
        "2": {
            "PatientGender": "Female",
            "PatientDateOfBirth": "1999-11-30 03:40:20.247",
            "PatientRace": "Black",
            "PatientMaritalStatus": "Single",
            "PatientLanguage": "Spanish",
            "PatientPopulationPercentageBelowPoverty": "16.09",
        },
    }

    # Running the assertions for the lab dictionary
    # Only two patients
    assert lab_dict == {
        "1": [
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "3.1",
                "LabUnits": "gm/dL",
                "LabDateTime": "1992-07-01 08:10:42.320",
            },
            {
                "AdmissionID": "2",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "5.8",
                "LabUnits": "gm/dL",
                "LabDateTime": "2005-07-26 09:51:51.223",
            },
            {
                "AdmissionID": "3",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "3.9",
                "LabUnits": "gm/dL",
                "LabDateTime": "2011-12-19 02:49:23.900",
            },
        ],
        "2": [
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: URINE PROTEIN",
                "LabValue": "3.9",
                "LabUnits": "gm/dL",
                "LabDateTime": "2011-12-19 02:49:23.900",
            }
        ],
    }
