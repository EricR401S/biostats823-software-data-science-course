"""Test patient_is_sick."""
import pytest

from patient_parser_v3 import patient_is_sick


def test_patient_is_sick() -> None:
    """Test patient_is_sick."""
    # Building the tables for the fake files
    lab_dict = {
        "1": [
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
        "2": [
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: ANION GAP",
                "LabValue": "15.4",
                "LabUnits": "mmol/L",
                "LabDateTime": "1987-10-09 10:01:48.483",
            },
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: ALK PHOS",
                "LabValue": "127.9",
                "LabUnits": "U/L",
                "LabDateTime": "1987-10-10 06:05:43.107",
            },
            {
                "AdmissionID": "1",
                "LabName": "METABOLIC: CALCIUM",
                "LabValue": "11.7",
                "LabUnits": "mg/dL",
                "LabDateTime": "1987-10-10 04:12:53.323",
            },
            {
                "AdmissionID": "1",
                "LabName": "CBC: EOSINOPHILS",
                "LabValue": "0.6",
                "LabUnits": "k/cumm",
                "LabDateTime": "1987-10-09 18:07:16.363",
            },
            {
                "AdmissionID": "4",
                "LabName": "METABOLIC: CALCIUM",
                "LabValue": "12.6",
                "LabUnits": "gm/dl",
                "LabDateTime": "1987-10-09 16:49:02.957",
            },
        ],
    }

    # Testing the patient_is_sick function
    assert patient_is_sick(lab_dict, "1", "METABOLIC: ALBUMIN", ">", 3.0)
    assert not (patient_is_sick(lab_dict, "1", "METABOLIC: ALBUMIN", "<", 4.0))
    assert not (patient_is_sick(lab_dict, "1", "METABOLIC: ALBUMIN", ">", 5.0))

    assert patient_is_sick(lab_dict, "1", "METABOLIC: ALBUMIN", ">", 4.0)
    assert patient_is_sick(lab_dict, "2", "METABOLIC: CALCIUM", ">", 11.0)
    assert not (
        patient_is_sick(lab_dict, "2", "METABOLIC: CALCIUM", "<", 10.0)
    )

    try:
        assert patient_is_sick(lab_dict, "1", "Urinalysis", ">", 3.0)
    except ValueError:
        print("ValueError: Urinalysis is not a valid lab name")
        print("This error was caught successfully")
        pass
