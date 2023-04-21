"""Test patient_age_at_first_admission."""
import pytest

from patient_parser_v3 import age_at_first_admission


def test_age_at_first_admission() -> None:
    """Test age_at_first_admission."""
    # Building the tables for the fake files
    patient_dict = {
        "Nando": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1963-02-07 10:04:20.717",
            "PatientRace": "Hispanic",
            "PatientMaritalStatus": "Divorced",
            "PatientLanguage": "Spanish",
            "PatientPopulationPercentageBelowPoverty": "6.67",
        },
        "Ileis": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1998-01-04 05:45:29.580",
            "PatientRace": "Hispanic",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Spanish",
            "PatientPopulationPercentageBelowPoverty": "16.09",
        },
    }

    lab_dict = {
        "Nando": [
            {
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            },
            {
                "AdmissionID": "2",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "3.5",
                "LabUnits": "mg/dL",
                "LabDateTime": "1992-06-30 09:35:52.383",
            },
            {
                "AdmissionID": "1",
                "LabName": "CBC: MCH",
                "LabValue": "35.8",
                "LabUnits": "pg",
                "LabDateTime": "1992-06-30 03:50:11.777",
            },
            {
                "AdmissionID": "3",
                "LabName": "METABOLIC: ALBUMIN",
                "LabValue": "4.2",
                "LabUnits": "mg/dL",
                "LabDateTime": "1993-01-30 12:09:46.107",
            },
        ],
        "Ileis": [
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: ANION GAP",
                "LabValue": "15.4",
                "LabUnits": "mmol/L",
                "LabDateTime": "2002-10-09 10:01:48.483",
            },
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: ALK PHOS",
                "LabValue": "127.9",
                "LabUnits": "U/L",
                "LabDateTime": "2002-10-10 06:05:43.107",
            },
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: CALCIUM",
                "LabValue": "11.7",
                "LabUnits": "mg/dL",
                "LabDateTime": "2002-10-10 04:12:53.323",
            },
            {
                "AdmissionID": "1",
                "LabName": "CBC: EOSINOPHILS",
                "LabValue": "0.6",
                "LabUnits": "k/cumm",
                "LabDateTime": "2002-10-09 18:07:16.363",
            },
            {
                "AdmissionID": "4",
                "LabName": "METABOLIC: CALCIUM",
                "LabValue": "12.6",
                "LabUnits": "gm/dl",
                "LabDateTime": "2020-10-09 16:49:02.957",
            },
        ],
    }

    # running the tests
    assert age_at_first_admission(patient_dict, lab_dict, "Nando") == 29
    assert age_at_first_admission(patient_dict, lab_dict, "Ileis") == 4
