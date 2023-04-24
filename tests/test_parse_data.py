"""Test parse_data function."""
import pytest

from fake_files import fake_files
from patient_parser_v3 import parse_data, Patient, Labs
import datetime as dt


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

    correct_answer_patient_dict = {
        "1": Patient(
            "1",
            "Male",
            dt.datetime(1947, 12, 28, 2, 45, 40, 547000),
            "White",
            "Married",
            "English",
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
        ),
        "2": Patient(
            "2",
            "Female",
            dt.datetime(1999, 11, 30, 3, 40, 20, 247000),
            "Black",
            "Single",
            "Spanish",
            "16.09",
            patient_labs=[
                Labs(
                    "2",
                    "1",
                    "METABOLIC: URINE PROTEIN",
                    3.9,
                    "gm/dL",
                    dt.datetime(2011, 12, 19, 2, 49, 23, 900000),
                )
            ],
        ),
    }

    assert patient_dict.keys() == correct_answer_patient_dict.keys()
    for key in patient_dict.keys():
        patient = patient_dict[key]
        copy_patient = correct_answer_patient_dict[key]

        assert patient.patient_id == copy_patient.patient_id
        assert patient.gender == copy_patient.gender
        assert patient.dob == copy_patient.dob
        assert patient.race == copy_patient.race
        assert patient.marital_status == copy_patient.marital_status
        assert patient.language == copy_patient.language
        assert patient.poverty_level == copy_patient.poverty_level

        for lab in patient.labs:
            lab_index = patient.labs.index(lab)
            assert lab.patient_id == copy_patient.labs[lab_index].patient_id
            assert (
                lab.admission_id == copy_patient.labs[lab_index].admission_id
            )
            assert lab.name == copy_patient.labs[lab_index].name
            assert lab.value == copy_patient.labs[lab_index].value
            assert lab.unit == copy_patient.labs[lab_index].unit
            assert lab.date == copy_patient.labs[lab_index].date
