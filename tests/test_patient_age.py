"""Test patient_age."""
import pytest

from patient_parser_v3 import patient_age

# from patient_parser_v3 import patient_age
import datetime as dt


def test_patient_age() -> None:
    """Test patient_age."""
    # Building the patient dictionary for the test
    patient_dict = {
        "Luis": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1943-02-07 10:04:20.717",
            "PatientRace": "Hispanic",
            "PatientMaritalStatus": "Divorced",
            "PatientLanguage": "Spanish",
            "PatientPopulationPercentageBelowPoverty": "6.67",
        },
        "Josephine": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1959-01-04 05:45:29.580",
            "PatientRace": "Hispanic",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Spanish",
            "PatientPopulationPercentageBelowPoverty": "16.09",
        },
    }

    # testing the patient_age function
    assert patient_age(patient_dict, "Luis") == 80
    assert patient_age(patient_dict, "Josephine") == 64

    # If more patients were added to the
    # test patient dict, this assert loop
    # would test the patient age function for all of them
    for patient in patient_dict:
        birth_year = int(patient_dict[patient]["PatientDateOfBirth"][:4])
        assert (
            patient_age(patient_dict, patient)
            == dt.datetime.now().year - birth_year
        )
