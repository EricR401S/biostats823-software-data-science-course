"""Python file to parse patient's data and lab results."""
import datetime as dt
import sqlite3

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


class Lab:
    """Class to represent lab results."""

    def __init__(
        self,
        Autogen_id: int = 0,
        db_name: str = "",
    ) -> None:
        """Initialize lab object."""
        self.Autogen_id: int = Autogen_id
        self.db_name: str = db_name

    @property
    def patient_id(self) -> str:
        """Return patient ID."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT PatientID FROM LABS WHERE Autogen_id = ?",
            (self.Autogen_id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def admission_id(self) -> int:
        """Return admission ID."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT AdmissionID FROM LABS WHERE Autogen_id = ?",
            (self.Autogen_id,),
        )
        data = cursor.fetchone()
        connection.close()
        return int(data[0])

    @property
    def name(self) -> str:
        """Return lab name."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT Name FROM LABS WHERE Autogen_id = ?""",
            (self.Autogen_id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def value(self) -> float:
        """Return lab value."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT Value FROM LABS WHERE Autogen_id = ?", (self.Autogen_id,)
        )
        data = cursor.fetchone()
        connection.close()
        return float(data[0])

    @property
    def unit(self) -> str:
        """Return lab unit."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT Unit FROM LABS WHERE Autogen_id = ?""",
            (self.Autogen_id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def date(self) -> dt.datetime:
        """Return lab date."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Date FROM LABS WHERE Autogen_id = ?""",
            (self.Autogen_id,),
        )
        data = cursor.fetchone()
        connection.close()
        return date_parser(data[0])


class Patient:
    """Patient class to store patient information."""

    def __init__(
        self,
        patient_id: str = "",
        db_name: str = "",
        lab_results: list[Lab] = [],
    ) -> None:
        """Initialize patient object."""
        self.id = patient_id
        self.db_name = db_name
        self.labs = lab_results

    @property
    def gender(self) -> str:
        """Return the gender of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT Gender FROM PATIENTS WHERE ID = ?", (self.id,))
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def dob(self) -> dt.datetime:
        """Return the date of birth of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT DateOfBirth FROM PATIENTS WHERE ID = ?""",
            (self.id,),
        )
        data = cursor.fetchone()
        connection.close()
        return date_parser(data[0])

    @property
    def race(self) -> str:
        """Return the race of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT Race FROM PATIENTS WHERE ID = ?", (self.id,))
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def marital_status(self) -> str:
        """Return the marital status of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT MaritalStatus FROM PATIENTS WHERE ID = ?""",
            (self.id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def language(self) -> str:
        """Return the language of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT Language FROM PATIENTS WHERE ID = ?""",
            (self.id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def poverty_level(self) -> str:
        """Return the poverty level of the patient."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT PovertyLevel FROM PATIENTS WHERE ID = ?""",
            (self.id,),
        )
        data = cursor.fetchone()
        connection.close()
        return str(data[0])

    @property
    def age(self) -> int:
        """Return patient's age."""
        return dt.datetime.now().year - self.dob.year

    def is_sick(  # type: ignore[return]
        self,
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
        lab_records = self.labs  # O(1)

        is_lab_found = False  # O(1)
        # arbitrary value to please mypy

        lab_value = 0.0  # O(1)
        # arbitrary date to please mypy
        lab_date = dt.datetime(1, 1, 1)  # O(1)

        for lab in lab_records:  # O(K)
            if (lab.name == lab_name) and (is_lab_found is False):  # O(1)
                is_lab_found = True  # O(1)
                lab_value = lab.value  # O(1)
                lab_date = lab.date  # O(1)

            elif (lab.name == lab_name) and (is_lab_found is True):  # O(1)
                new_lab_date = lab.date  # O(1)
                if new_lab_date > lab_date:  # O(1)
                    lab_value = lab.value  # O(1)
                    lab_date = lab.date  # O(1)

        if not is_lab_found:  # O(1)
            raise ValueError(
                "Lab not found. It may not exist, or you may have mistyped it"
            )  # O(1)

        elif operator == ">":  # O(1)
            return lab_value > value  # O(1)

        elif operator == "<":  # O(1)
            return lab_value < value  # O(1)

    @property
    def age_at_first_admission(self) -> int:
        """Return the age of the patient at their first admission.

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
        # today or now is initialized as
        # the earliest possible admission date
        earliest_admission = dt.datetime.now()  # O(1)

        for lab in self.labs:  # O(K)
            admission_date = lab.date  # O(2)
            if admission_date < earliest_admission:  # O(1)
                earliest_admission = admission_date  # O(1)

        first_admission_age = earliest_admission.year - self.dob.year  # O(1)

        return first_admission_age  # O(1)


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
    lab_dict: dict[str, list[Lab]],
    db: sqlite3.Connection,
    name_db: str,
) -> dict[str, Patient]:
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
    cursor = db.cursor()  # O(1)
    cursor.execute("DROP TABLE IF EXISTS PATIENTS")  # O(1)

    # create table
    cursor.execute(
        """
        CREATE TABLE PATIENTS (
            ID VARCHAR(255) PRIMARY KEY,
            Gender VARCHAR(255),
            DateOfBirth DATETIME,
            Race VARCHAR(255),
            MaritalStatus VARCHAR(255),
            Language VARCHAR(255),
            PovertyLevel FLOAT
        )
        """
    )  # O(1)

    db.commit()  # O(1)
    output_dict = dict()  # O(1)

    with open(txt_file, encoding="UTF-8-SIG") as f:  # O(1)
        # Core assumption: first line is header
        # skip and save header
        header = next(f)  # O(1)
        fixed_header = fix_header(header)  # O(M)
        patient_id_index = header.index("PatientID")  # O(M)

        # prepare queue
        sql_queue = []  # O(1)
        # This whole loop has a time complexity of O(NxM)
        for line in f:  # O(N x M)
            records = line.strip().split("\t")  # O(M)

            mapping = dict(zip(fixed_header, records))  # O(M)

            sql_queue.append(
                (
                    mapping["PatientID"],
                    mapping["PatientGender"],
                    date_parser(mapping["PatientDateOfBirth"]),
                    mapping["PatientRace"],
                    mapping["PatientMaritalStatus"],
                    mapping["PatientLanguage"],
                    float(mapping["PatientPopulationPercentageBelowPoverty"]),
                )
            )  # O(1)
            patient_id = mapping["PatientID"]  # O(1)
            patient = Patient(patient_id, name_db, lab_dict[patient_id])  # O(1

            output_dict[records[patient_id_index]] = patient  # O(1)

        cursor.executemany(
            """
            INSERT INTO PATIENTS
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            sql_queue,
        )

        db.commit()  # O(1)

    return output_dict  # O(1)


def lab_file_to_dict(
    txt_file: str,
    db: sqlite3.Connection,
    name_db: str,
) -> dict[str, list[Lab]]:
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
    cursor = db.cursor()  # O(1)
    cursor.execute("DROP TABLE IF EXISTS LABS")  # O(1)

    # create table
    cursor.execute(
        """
        CREATE TABLE LABS (
            PatientID VARCHAR(255),
            AdmissionID INT,
            Name VARCHAR(255),
            Value FLOAT(8),
            Unit VARCHAR(255),
            Date DATETIME,
            Autogen_id INT PRIMARY KEY
        )
        """
    )  # O(1)

    db.commit()  # O(1)

    output_dict = dict()  # O(1)
    generative_id = 1  # O(1)
    with open(txt_file, encoding="UTF-8-SIG") as f:  # O(1)
        # Core assumption: first line is header
        # skip and save header
        header = next(f)  # O(1)
        fixed_header = fix_header(header)  # O(L)
        patient_id_index = fixed_header.index("PatientID")  # O(L)

        # remove patient_id from header
        sql_queue = []  # O(1)
        # This whole loop has a time complexity of O(K x L)
        for line in f:  # O(K x L)
            labs = line.strip().split("\t")  # O(L)
            patient_id = labs[patient_id_index]  # O(1)

            new_labs = dict(zip(fixed_header, labs))  # O(L)

            # the query to insert the data
            sql_queue.append(
                (
                    new_labs["PatientID"],
                    int(new_labs["AdmissionID"]),
                    new_labs["LabName"],
                    float(new_labs["LabValue"]),
                    new_labs["LabUnits"],
                    date_parser(new_labs["LabDateTime"]),
                    generative_id,
                )
            )  # O(1)

            lab_obj = Lab(generative_id, name_db)  # O(1)

            if patient_id not in output_dict:  # O(1)
                output_dict[patient_id] = [lab_obj]  # O(1)

            else:  # O(1)
                output_dict[patient_id].append(lab_obj)  # O(1)

            generative_id += 1  # O(1)

        # insert the data
        cursor.executemany(
            """INSERT INTO LABS
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            sql_queue,
        )  # O(1)

        db.commit()  # O(1)

    return output_dict  # O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, Patient], dict[str, list[Lab]]]:
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
    # connected to database
    connection = sqlite3.connect("EHR.db")  # O(1)

    lab_dict = lab_file_to_dict(lab_filename, connection, "EHR.db")  # O(K x L)
    patient_dict = patient_file_to_dict(
        patient_filename, lab_dict, connection, "EHR.db"
    )  # O(N x M)

    connection.close()  # O(1)
    return patient_dict, lab_dict  # O(1)
