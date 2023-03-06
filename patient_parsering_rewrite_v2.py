"""Python file to parse patient's data and lab results."""

import datetime as dt


def date_parser(date: str) -> dt.datetime:
    """Convert string to datetime object.

    Assumes it always has the format: YYYY-MM-DD hh:mm:ss.[mmm]
    """
    date = date.strip()

    return dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


def fix_header(header: str) -> list[str]:
    """Split header into list of strings."""
    return header.split("\t")


def col_index_finder(header: list[str], column_name: list[str]) -> int:
    """Return the index of the patient id in the header.

    Assumes not all future files have identical column names.
    """
    for column in header:
        lowercased_col = column.lower()

        for i in column_name:
            if i in lowercased_col:
                return header.index(column)

            else:
                pass
    raise ValueError("The column name was not found in header")


def patient_file_to_dict(
    txt_file: str,
) -> dict[str, list[str]]:
    """Open patient txt files to convert them to dictionaries.

    Assume that the first row is the header.
    """
    output_dict: dict[str, list[str]] = dict()

    with open(txt_file) as f:
        # Core assumption: first line is header
        header = next(f)  # skip and save header
        fixed_header = fix_header(header)
        patient_id_index = col_index_finder(
            fixed_header, ["patient_id", "patientid"]
        )
        fixed_header.pop(patient_id_index)  # remove patient_id from header
        output_dict["header"] = fixed_header  # save header

        for line in f:
            records = line.split("\t")
            patient_id = records.pop(patient_id_index)

            # Implements a list as the value for patient records
            if patient_id in output_dict:  # In case of update
                output_dict[patient_id] = records
            else:
                output_dict[patient_id] = records

    return output_dict


def lab_file_to_dict(
    txt_file: str,
) -> dict[str, dict[str, list[list[str]]]]:
    """Open lab tests txt files to convert them to dictionaries.

    Assume that the first row is the header.
    """
    output_dict: dict[str, dict[str, list[list[str]]]] = dict()

    with open(txt_file) as f:
        # Core assumption: first line is header
        header = next(f)  # skip and save header
        fixed_header = fix_header(header)
        patient_id_index = col_index_finder(
            fixed_header, ["patient_id", "patientid"]
        )
        fixed_header.pop(patient_id_index)  # remove patient_id from header
        # to please mypy, I have to add the header to the dict
        output_dict["header"] = dict(
            {"header": [fixed_header]}
        )  # save header"
        lab_name_index = col_index_finder(
            fixed_header, ["lab_name", "labname"]
        )
        for line in f:
            records = line.split("\t")
            patient_id = records.pop(patient_id_index)

            # Implements a list of lists as the value for lab records
            lab_name = records[lab_name_index]
            if patient_id not in output_dict:
                output_dict[patient_id] = dict({lab_name: [records]})

            elif (
                patient_id in output_dict
                and lab_name not in output_dict[patient_id]
            ):
                r = [records]  # to please pycodestyle
                output_dict[patient_id][lab_name] = r

            else:
                # the scenario in which the patient_id and lab_name \
                # are both in the dict
                # making use of pointers
                # to please pycodestyle
                lab_dn = output_dict[patient_id]
                test = lab_dn[lab_name]
                test.append(records)

    return output_dict


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, list[str]], dict[str, dict[str, list[list[str]]]]]:
    """Take patient and lab files and converts them into dictionaries.

    They are assumed to be tab-delimited text files,
    and they are returned as dictionaries
    with the patient ids as their keys.
    """
    patient_dict = patient_file_to_dict(patient_filename)
    lab_dict = lab_file_to_dict(lab_filename)

    return patient_dict, lab_dict


def patient_age(records: dict[str, list[str]], patient_id: str) -> int:
    """Return patient age from records.

    Take dictionary of patient records and the patient id
    as inputs to return the patient's age in year
    """
    bday_index = col_index_finder(
        records["header"],
        ["date_of_birth", "dob", "birth_date", "birthdate", "dateofbirth"],
    )
    birth_date: dt.datetime = date_parser(records[patient_id][bday_index])

    age: int = dt.datetime.now().year - birth_date.year

    return age


def patient_is_sick(
    records: dict[str, dict[str, list[str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return boolean based on threshold for test.

    This is a function that determines if the patient is sick,
    depending on the threshold values chosen for the patient,
    for a specific lab test.
    The lab data is a dictionary, and the operators
    to compare against the thresholds are '>' and '<'.
    """
    if lab_name not in records[patient_id]:
        raise ValueError("The lab name was not found in the patient records")
    header_copy: list[str] = ((records["header"])["header"].copy())[
        0
    ]  # type: ignore[assignment]
    lab_records = records[patient_id][lab_name]
    lab_value_index = col_index_finder(header_copy, ["lab_value", "labvalue"])
    lab_date_index = col_index_finder(header_copy, ["lab_date", "labdate"])

    def find_recent_test(
        patient_lab_records: list[list[str]],
        lab_date_index: int,
    ) -> list[str]:
        """Return the most recent test for a patient."""
        recent_test: list[str] = patient_lab_records[0]
        recent_test_date: dt.datetime = date_parser(
            recent_test[lab_date_index]
        )
        if len(patient_lab_records) == 1:
            return recent_test

        else:
            for test in patient_lab_records:
                test_date: dt.datetime = date_parser(test[lab_date_index])

                if test_date > recent_test_date:
                    recent_test = test
                    recent_test_date = test_date

            return recent_test

    a = lab_records  # to please pycodestyle
    b = lab_date_index  # to please pycodestyle
    most_recent_test = find_recent_test(a, b)  # type: ignore[arg-type]

    if operator == ">":
        return float(most_recent_test[lab_value_index]) > value

    elif operator == "<":
        return float(most_recent_test[lab_value_index]) < value

    else:
        raise ValueError("The operator is not valid, use '>' or '<'")
