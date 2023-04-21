"""Python file to parse patient's data and lab results."""
import datetime as dt

"""
The objective of the functions here is to parse patient's data and lab results.
This will help users to extract the data regarding a specific patients.
N will refer to the number of rows in the patient file,
implying the number of patients.
M will refer to the number of columns in the patient file,
implying the number
of features representing patient information.
K will refer to the number of rows in the lab results file,
implying the number of lab tests.
L will refer to the number of columns in the lab results file,
implying the number of features
representing some information about the lab results.
These quantities of N, M, K, and L have an unknown lengths,
so they will be expected to scale with size.
A file may have 500 rows and 5 columns or 5 million rows and 50 columns.
For this reason, no assumptions will be made about the size of the files.
These details will be considered in the time complexity analysis.
"""


def date_parser(date: str) -> dt.datetime:
    """Convert string to datetime object.

    Assumes it always has the format: YYYY-MM-DD hh:mm:ss.[mmm]

    The function takes a string and executes a strip() method on it.
    This method has a time complexity of O(1), because the length
    of the date is assumed to be known and finite. The string
    is not expected to scale in growth at all.

    After this step is completed, the function will use the
    datetime.strptime() method to convert the string to a datetime object.
    This method has a time complexity of O(1), due to the fact that it
    has to iterate through a finite string to
    convert it to a datetime object.

    In total, we have constant time operations,
    so the overall complexity is category of O(1).
    """
    date = date.strip()  # O(1)

    return dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")  # O(1)


def fix_header(header: str) -> list[str]:
    """Split header into list of strings.

    The header has M or K columns, this is one of the main
    quantities that we are considering. If this function
    is run on the patient file, then we are considering
    M columns in the patient header. If the function is
    run on the lab results file, then we are considering
    K columns in the lab results header. Since the function
    depends on the amount of columns in those files,
    the time complexity will scale linearly.

    First, the header is stripped of any whitespace, O(1).
    As for the header's contents, they are being separated
    by using the split() method. A list with the strings is
    returned. This method has a time complexity of O(M) or O(L).
    I speculate that the method iterates through a string
    and saves the string's contents to a placeholder variable.
    Once a tab character is found, the placeholder variable is
    appended to a list. This process is repeated until the end of the
    string is reached. The time complexity is linearly dependent
    on the number of characters in the string, including the tab characters.

    The overall category of time complexity is O(M) or O(L).
    """
    header = header.strip()  # O(1)
    return header.split("\t")  # O(M) or O(L)


def patient_file_to_dict(
    txt_file: str,
) -> dict[str, dict[str, str]]:
    """Open patient txt files to convert them to dictionaries.

    Assume that the first row is the header.

    The objective is build a nested dictionary, where the
    the patient id will be the key for the dictionary.
    The values will be another dictionary where the keys
    are the header's contents and the values are the row's
    contents.

    Opening the file is O(1).
    The output dictionary variable is initialized with an
    empty dictionary. This is O(1).

    The function saves the header.
    This operation has a time complexity of O(1). Fixing this
    header has a time complexity of O(M).

    The function to find the index of the patient id has a time
    complexity of O(M). The method (pop()) to remove the
    patient id from the header has a time complexity of O(1), due
    to knowing the index of the item to remove.

    Up to this point, the time complexity is
    O(1) + O(1) + O(1) + O(M) + O(M) + O(1).

    It summarizes to 2 * O(M) + O(1).

    The function iterates through the file, a text file, and will
    conduct a series of operations per line. By going row by row,
    the time complexity of going through the rows is O(N).

    Inside the loop, the records are split by tab, meaning a complexity of
    O(M). The patient id is popped into a variable, O(1).

    The next and more complex operation is to pair the header's contents
    witht the records' contents. This is done by using the zip() method.
    Then the zipped object is converted to a dictionary.
    The dictionary is then saved as a value corresponding
    to the patient id key in the output dictionary. This step is expected
    to have a time complexity of O(M), due to the fact that the
    zip() method iterates through the header and records, which
    both have a size of M columns.

    Inside the loop, there is a total time complexity of
    O(M) + O(1) + O(M). This can be simplified to 2*O(M) + O(1).
    By factoring in the loop in the calculation, the time complexity
    is O(N)[2*O(M) + O(1)].

    The total time complexity is 2 * O(M) + O(1) + O(N)[2*O(M) + O(1)].
    This simplifies to O(N x M), where N is the number of rows and M
    is the number of columns of the patient file.
    """
    output_dict: dict[str, dict[str, str]] = dict()  # O(1)

    with open(txt_file, encoding="UTF-8-SIG") as f:  # O(1)
        # Core assumption: first line is header
        # skip and save header
        header = next(f)  # O(1)
        fixed_header = fix_header(header)  # O(M)
        patient_id_index = header.index("PatientID")  # O(M)

        # remove patient_id from header
        fixed_header.pop(patient_id_index)  # O(1)

        # This whole loop has a time complexity of O(NxM)
        for line in f:  # O(N x M)
            records = line.strip().split("\t")  # O(M)
            patient_id = records.pop(patient_id_index)  # O(1)

            output_dict[patient_id] = dict(zip(fixed_header, records))  # O(M)

    return output_dict  # O(1)


def lab_file_to_dict(
    txt_file: str,
) -> dict[str, list[dict[str, str]]]:
    """Open patient lab txt files to convert them to dictionaries.

    Assume that the first row is the header.

    The objective is build a nested dictionary, where the
    the patient id will be the key for the dictionary.
    The values will be a list of dictionaries where the keys
    are the header's contents and the values are the row's
    contents. This is due to the likelihood of having
    there are multiple lab results per patient.

    The text file is opened, so it has a time complexity of O(1).
    The output dictionary variable is initialized with an
    empty dictionary. This is O(1).

    The function first saves the header.
    This operation has a time complexity of O(1). Fixing this
    header has a time complexity of O(L).

    The function to find the index of the patient id has a time
    complexity of O(L). The code (pop()) to remove the
    patient id from the header has a time complexity of O(1), due
    to knowing the index of the item to remove.

    Up to this point, the total time complexity is
    O(1) + O(1) + O(1) + O(L) + O(L) + O(1).

    This summarizes to 2 * O(L) + O(1).

    The function iterates through the file, a text file, and will
    conduct a series of operations per line. By going row by row,
    the time complexity of going through the rows is O(K).

    Inside the loop, the records are split by tab or column, meaning
    a complexity of O(L). The patient id is popped into a variable, O(1).

    Then two checks occur.
    Checking if the patient is not in the dictionary is O(1).
    If that is the case, then an entry with is created in the dictionary
    with the patient id as the key, and the value is a list containing
    a singular dictionary representing a lab test record. This lab test's
    keys are the header's contents and the values are the row's contents.
    This step is expected to have a time complexity of O(L), due to the fact
    that the zip() method iterates through the header and records, which
    both have a size of L columns. I needed a placeholder variable to
    work with pycodesyle, so I used the variable "new_labs", which is
    an O(1) operation.

    The second check occurs when the patient is in the dictionary.
    This check is O(1). In this scenario, a lab record, also a dictionary with
    the header's contents as keys and the row's contents as values, is appended
    to the list of dictionaries corresponding to that patient key. This is
    accomplished via use of the zip(), dict() and append() methods.
    This step is also expected to have a time complexity of O(L). The appending
    is O(1).

    The time complexity of the contents inside the loop is
    O(L) + O(1) + O(1) + O(L) + O(1) + O(L) + O(L) + O(1).
    This simplifies to 3 * O(L) + O(1).
    Because the loop is iterating through the rows, the time complexity
    is O(K)[3 * O(L) + O(1)].

    This sums to 2 * O(L) + O(1) + O(1) (for opening the file)
    + O(K)[3 * O(L) + O(1)] + O(1) (the return statement).
    This simplifies to O(K x L), the highest order term.
    """
    output_dict: dict[str, list[dict[str, str]]] = dict()  # O(1)

    with open(txt_file, encoding="UTF-8-SIG") as f:  # O(1)
        # Core assumption: first line is header
        # skip and save header
        header = next(f)  # O(1)
        fixed_header = fix_header(header)  # O(L)
        patient_id_index = fixed_header.index("PatientID")  # O(L)

        # remove patient_id from header
        fixed_header.pop(patient_id_index)  # O(1)

        # This whole loop has a time complexity of O(K x L)
        for line in f:  # O(K x L)
            labs = line.strip().split("\t")  # O(L)
            patient_id = labs.pop(patient_id_index)  # O(1)

            if patient_id not in output_dict:  # O(1)
                new_labs = [dict(zip(fixed_header, labs))]  # O(L)
                output_dict[patient_id] = new_labs  # O(1)

            else:
                newer_labs = dict(zip(fixed_header, labs))  # O(L)
                output_dict[patient_id].append(newer_labs)  # O(1)

    return output_dict  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Take patient and lab files and converts them into dictionaries.

    They are assumed to be tab-delimited text files,
    and they are returned as dictionaries
    with the patient ids as their keys.

    As described in the docstrings for the other helper functions,
    the time complexity for the patient_file_to_dict is O(N x M), and
    the time complexity for the lab_file_to_dict is O(K x L). The
    total time complexity is O(N x M) + O(K x L). The return statement
    has a time complexity of O(1).

    Regardless, the highest complexity is :
    O(N x M) + O(K x L)
    """
    patient_dict = patient_file_to_dict(patient_filename)  # O(N x M)
    lab_dict = lab_file_to_dict(lab_filename)  # O(K x L)

    return patient_dict, lab_dict  # O(1)


def patient_age(records: dict[str, dict[str, str]], patient_id: str) -> int:
    """Return patient age from records.

    Take dictionary of patient records and the patient id
    as inputs to return the patient's age in year.

    The helper functions below have already been described.
    The time complexity for finding the date of birth is
    O(1), due to the date corresponding to a dictionary key.
    It is assumed that the name of that key is known.
    The time complexity for parsing the date is O(1).
    The time complexity for computing the age is O(1).
    The return statement has a time complexity of O(1).

    The overall time complexity is :

    O(1) + + O(1) + O(1) + O(1) =  O(1)

    This simplifies to an O(1) series of operations.
    """
    bday = records[patient_id]["PatientDateOfBirth"]  # O(1)
    birth_date: dt.datetime = date_parser(bday)  # O(1)

    age: int = dt.datetime.now().year - birth_date.year  # O(1)

    return age  # O(1)


def patient_is_sick(  # type: ignore[return]
    records: dict[str, list[dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return boolean based on threshold for test.

    This is a function that determines if the patient is sick,
    depending on the threshold values chosen for the patient,
    for a specific lab test.
    The lab records are a dictionary with a patient key mapped
    to a list of dictionaries that represent lab tests.
    The operators to compare against the thresholds are '>' and '<'.

    The first step is to save the patient's lab records to a variable.
    This is O(1). Three variables are initialized. The first is a flag
    variable that is set to False, and it is meant to indicate if a
    specific lab test exists for a patient. If False, that test does
    not exist, and the function will return an error message (later on
    in the function). The second variable is meant to hold a lab value,
    and the last one will hold a lab date. For simplicity, the latter
    two will be initialized to None and will be updated if the lab test
    is found. This is O(1) + O(1) + O(1).

    We have a complexity of O(1) + O(1) + O(1) + O(1) = O(1) up
    to this point.

    The next step is to iterate through the patient's lab records in order
    to find the lab test that matches the lab_name. This is O(K).
    Although K referred to the number of rows (tests) in the lab file,
    it is also used to represent the number of lab tests for
    a patient in this unique case. Part of the nuance of K is that we don't
    know how many lab tests there are  in total, in addition to lab tests
    per patient. We can have 10, 20, 30, 40 or maybe hundreds of labs
    for a given patient.

    Within this loop, two checks occur. The first ascertains that the lab
    name has been found and that the flag is set to False. This is O(1).
    This is equivalent to finding that lab file for the first time.
    The flag is updated to True, the lab value is found and converted
    to a float and used to update the lab_value variable. The lab date
    is parsed and is used to update the lab_date variable.
    This is O(1) + O(1) + O(1). This sums to O(1).

    The second check assumes a new lab test has been found again, given
    that the flag is currently set to True. This check is O(1).
    The accessing and parsing of the new date is O(1).
    The comparison of the new date to the old date is O(1).
    If the new date is more recent, the lab value and date are updated
    in an identical fashion. The updating of the lab value is O(1).
    The updating of the lab date is O(1). This sums to
    O(1) + O(1) + O(1) + O(1) + O(1) = O(1).

    These checks all occur within the loop, so the time complexity
    is O(K) + O(K) = 2 * O(K).

    The function then proceeds to validate if no test was found.
    this check is O(1). The function then returns an error message
    if the test was not found. This is O(1).

    The next checks are to verify which operators are being used.
    One full check is performed for each of the two, < and >, and
    a boolean is returned for each by comparing the lab value found
    to the threshold value by using the designated operator.
    The checking is O(1), and the comparison is O(1),
    and the return is O(1).

    Now, to calculate the final tally.
    The initialization of the variables is O(1).
    The loop is 2*O(K).
    The checks for the potential lab not found is O(1).
    The checks for the operators, as well as their comparisons and
    return statements are 2 * O(1) = O(1).

    This simplifies to an overall time complexity of O(K).
    """
    lab_records = records[patient_id]  # O(1)

    is_lab_found = False  # O(1)
    # arbitrary value to please mypy

    lab_value = 0.0  # O(1)
    # arbitrary date to please mypy
    lab_date = dt.datetime(1, 1, 1)  # O(1)

    for lab in lab_records:  # O(K)
        if (lab["LabName"] == lab_name) and (is_lab_found is False):  # O(1)
            is_lab_found = True  # O(1)
            lab_value = float(lab["LabValue"])  # O(1)
            lab_date = date_parser(lab["LabDateTime"])  # O(1)

        elif (lab["LabName"] == lab_name) and (is_lab_found is True):  # O(1)
            new_lab_date = date_parser(lab["LabDateTime"])  # O(1)
            if new_lab_date > lab_date:  # O(1)
                lab_value = float(lab["LabValue"])  # O(1)
                lab_date = new_lab_date  # O(1)

    if not is_lab_found:  # O(1)
        raise ValueError(
            "Lab not found. It may not exist, or you may have mistyped it"
        )  # O(1)

    elif operator == ">":  # O(1)
        return lab_value > value  # O(1)

    elif operator == "<":  # O(1)
        return lab_value < value  # O(1)


def age_at_first_admission(
    patient_records: dict[str, dict[str, str]],
    lab_records: dict[str, list[dict[str, str]]],
    patient_id: str,
) -> int:
    """Return the age of a patient at their first admission.

    The function uses the patient records and lab records to
    determine the age of a patient at their first admission.
    Firstly, the patient's date of birth is accessed, O(2)
    and parsed, O(1).

    The patient's lab records are then saved, O(1).

    An arbitrary admission date is then initialized, O(1).

    A loop initiates to iterate through the patient's lab records.
    This is O(K) (rows in the lab file). Within this loop, the
    admission date is accessed and parsed, O(2).
    Then a check occurs to see if the admission date is older
    than the earliest admission date. This is O(1).
    If the admission date is older, the earliest admission date
    is updated, O(1). If the admission date is not older,
    the loop continues after it hits the else statement O(1).

    After exiting the loop, the age of the patient at their
    first admission is calculated, O(1). This is then
    returned, O(1).

    We have a total time complexity of
    O(2) + O(1) + O(1) + O(K x 5) = O(K x 5) + O(4).
    This simplifies to O(K), as expected.
    """
    dob = patient_records[patient_id]["PatientDateOfBirth"]  # O(2)
    dob_formatted = date_parser(dob)  # O(1)

    patient_lab_records = lab_records[patient_id]  # O(1)

    # today or now is initialized as
    # the earliest possible admission date
    earliest_admission = dt.datetime.now()  # O(1)

    for lab in patient_lab_records:  # O(K)
        admission_date = date_parser(lab["LabDateTime"])  # O(2)
        if admission_date < earliest_admission:  # O(1)
            earliest_admission = admission_date  # O(1)

    first_admission_age = earliest_admission.year - dob_formatted.year  # O(1)

    return first_admission_age  # O(1)
