import os
import pandas as pd
from datetime import datetime, timedelta

# Constants:
PREV_DATA = {}
TEST_FILE_COUNT = 1000
TEST_FILE_SIZE = 10000
DATA_DIRECTORY = "data_large"
COLUMNS = ["Study ID", "Date", "Occurrence", "Problem Detected", "Last Successful Run Date", 
           "Last Successful Run Time", "Next Run Date", "Next Run Time", "N: File Count", 
           "N: Total File Size (MB)"]
EXCLUDE = {1}
COLUMNS_FROM_CSV_FILE = [element for i, element in enumerate(COLUMNS) if i not in EXCLUDE]
DAYS_IN_MONTH = 30

# Build DataFrame from Data in CSV Files:
def build_df_from_csv_files(path_to_csv_directory=DATA_DIRECTORY, testing=False):
    """
    Constructs a Pandas DataFrame from CSV files in the data directory. The columns of this 
    DataFrame are: "Study ID", "Date", "Occurrence", "Problem Detected", "Last Successful Run Date", 
    "Last Successful Run Time", "Next Run Date", "Next Run Time".
    
    Args:
        path_to_csv_directory (str): path to directory containing CSV files
        testing (bool): True if testing, False otherwise.

    Returns:
        pandas.DataFrame: The Pandas DataFrame built from CSV files in the data directory
    """
    if testing:
        add_test_data_to_prev_data()

    df = pd.DataFrame()
    csv_files = os.listdir(path_to_csv_directory)
    # Order of csv_files could differ based on OS
    csv_files.sort()

    for file in csv_files[-DAYS_IN_MONTH:]:

        # Build current_file_df
        file_path = os.path.join(path_to_csv_directory, file)
        date = get_date_of_file(file_path)
        current_file_df = pd.read_csv(file_path)
        current_file_df = current_file_df.loc[:,COLUMNS_FROM_CSV_FILE]
        
        # Insert date into current file's DataFrame
        current_file_df.insert(loc=1, column="Date", value=date)

        # Format "Problem Detected" Column:
        current_file_df["Problem Detected"] = current_file_df.apply(format_problem_detected_column, axis=1)

        # Keep change previous "N: File Count" and "N: Total File Size (MB)" to current file's:
        current_file_df.apply(build_prev_data_dict, axis=1)

        df = current_file_df.copy() if df.empty else pd.concat([current_file_df, df], ignore_index=True)

    # Reverse rows of df so newest date appears last
    df = df.iloc[::-1]

    return df 

def get_date_of_file(file=''):
    """
    Parses a file's name and returns the date associated with a file. 
    Data files are have the naming convention: NRG_N_TODAY_COMP_YYYYMMDD.csv

    Args:
        file (str): The name of a CSV file

    Returns:
        datetime.date: The date associated with a CSV file
    """
    date_string = file[file.rindex('_') + 1 : file.rindex(".")]
    date_time = datetime.strptime(date_string, '%Y%m%d')
    date = date_time.date()
    return date

def get_problem_detected_df(df):
    """
    Performs a groupby() operation on the Pandas DataFrame built from CSV files
    in the data directory and accesses the values from the "Problem Detected" column.
    It then unstacks the Pandas Series returned by this operation to create a Pandas 
    DataFrame with dates as columns and study ids as indices. The element associated
    with each date and study id represents whether a problem occurred with a study on
    a given date. 

    Args:
        df (pandas.DataFrame): The Pandas DataFrame built from CSV files in the data 
        directory

    Returns:
        pandas.DataFrame: Returns a Pandas DataFrame where each element represents whether 
        a problem occurred with a study on a given date. 
    """
    return df.groupby(["Study ID", "Date"])["Problem Detected"].last().unstack()

def get_problem_detected_df_between_dates(problem_detected_df, current_date=datetime.now().date(), num_days_in_past=1):
    """
    Returns a Pandas DataFrame representing whether a problem occurred with a study on
    a given date. The dates of this DataFrame range from current_date to the date
    num_days_in_past. 

    Args:
        problem_detected_df (pandas.DataFrame): The Pandas DataFrame representing whether
        a problem occurred with a study on a given date.

        current_date (datetime.date or str): The current date. Defaults to today's date 
        in EST time. If inputting a String, it must be formatted as YYYY-MM-DD.

        num_days_in_past (int): The number of days that the returned problem_detected_df
        will range into the past. Defaults to 1, representing taking current_date as the
        only date.
    
    Returns:
        pandas.DataFrame: Returns the problem_detected_df with dates ranging from
        current_date to the date num_days_in_past.
    """
    prev_date, current_date = get_day_num_days_in_past(current_date=current_date, num_days_in_past=num_days_in_past)
    return problem_detected_df.T.loc[prev_date:current_date].T

def get_day_num_days_in_past(current_date=datetime.now().date(), num_days_in_past=1):
    """
    Returns a tuple of prev_date and current_date where current_date represents
    the current date and prev_date represents the date num_days_in_past.

    Args:
        current_date (datetime.date or str): The current date. Defaults to today's date 
        in EST time. If inputting a String, it must be formatted as YYYY-MM-DD.

        num_days_in_past (int): The number of days in the past from current_date. 
        Defaults to 1, representing taking current_date as the only date.
    Returns:
        (prev-date, current_date): Returns a tuple representing current_date and the date
        num_days_in_past.
    """
    if isinstance(current_date, str):
        try:
            current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
        except ValueError:
            current_date = datetime.now().date()
            print("Date String formatted improperly. Using current date instead.")
    prev_date = current_date - timedelta(num_days_in_past - 1)

    return (prev_date, current_date)

# Get HTML for Today's Problems Detected
# GET RID OF HARD CODED DATE
def get_html_for_problem_detected_df(problem_detected_df, study_id='', num_days_in_past=1):
    """
    Returns the HTML associated with the problem_detected_df Pandas DataFrame

    Args:
        problem_detected_df (pandas.DataFrame): The Pandas DataFrame representing whether
        a problem occurred with a study on a given date.

        study_id (str): The id of a Study. Defaults to ''. Represents including data from all
        studies in the problem_detected_df.

        num_days_in_past (int): The number of days that the returned problem_detected_df
        will range into the past.

    Returns:
        str: The HTML associated with the problem_detected_df

    """
    problem_detected_df = get_problem_detected_df_between_dates(problem_detected_df, current_date="2024-07-07", num_days_in_past=num_days_in_past)

    if study_id != '':
        problem_detected_df = pd.DataFrame(problem_detected_df.loc[study_id]).T

    styled_problem_detected_df = problem_detected_df.style.apply(lambda x : x.map(highlight_errors))
    return styled_problem_detected_df.to_html(escape=False)


def build_prev_data_dict(row):
    """
    Updates "N: File Count" and "N: Total File Size (MB)" in the PREV_DATA dictionary 
    according to an inputted row's values. Each row represents the data associated with
    a study on a given date.

    Args:
        row (pandas.Series): The data associated with a study on a given date. A slice
        of the current_file_df generate while build_df_from_csv_files() runs.
    """
    if row["Occurrence"] == "Weekly" and row["Last Successful Run Date"] != row["Date"].strftime("%Y-%m-%d"):
        return
    PREV_DATA[row["Study ID"]] = {"N: File Count" : row["N: File Count"], "N: Total File Size (MB)": row["N: Total File Size (MB)"]}

def format_problem_detected_column(row):
    """
    Returns the error status of a study on a given date. "NR" represents when a study
    wasn't run on a given date. Either this study runs weekly or wasn't created yet.
    'E' represents when a problem is detected with a study on a given date. A status 
    of 'G' means no errors were detected for a study on a given date. 

    Args:
        row (pandas.Series): The data associated with a study on a given date. A slice
        of the current_file_df generate while build_df_from_csv_files() runs.

    Returns:
        str: The error status of a study on a given date.  
    """
    if row["Occurrence"] == "Weekly" and row["Last Successful Run Date"] != row["Date"].strftime("%Y-%m-%d") and pd.isnull(row["Problem Detected"]):
        return "NR"
    elif (not pd.isnull(row["Problem Detected"]) or row["Study ID"] in PREV_DATA 
            and (is_invalid_files_upload(row) or is_invalid_files_upload(row, column="N: Total File Size (MB)"))):
        return 'E'
    
    return 'G'

def is_invalid_files_upload(row, column="N: File Count"):
    """
    Checks if a given study's file information is correct. "N: File Count" and
    "N: Total File Size (MB)" should not decrease between consecutive days.

    Args:
        row (pandas.Series): The data associated with a study on a given date. A slice
        of the current_file_df generate while build_df_from_csv_files() runs.
        
        column (str, optional): The name of the column that this method will access from
        row. Either "N: File Count" or "N: Total File Size (MB)" Defaults to "N: File Count".

    Returns:
        bool: True if a study's file count or size is greater than or equal to
        its previous file count or size. False otherwise.
    """
    study_id = row["Study ID"]
    file_information = row[column]

    return file_information < PREV_DATA[study_id][column]

def highlight_errors(val):
    """
    Returns a CSS style for background-color of a td HTML element when 
    get_html_for_problem_detected_df() runs. Each td HTML element represents the problem
    detected status of a given study on a given date. If this status is 'E', the td gets 
    colored "red". If it's "NR", its colored "gray". And if its 'G', its colored "green".

    Args:
        val (str): The error status of a given study. 

    Returns:
        str: Returns an f-String f"background-color: {color}" representing the CSS style of 
        a given td HTML element.
    """
    color = "green"
    if val == 'E':
        color = "red"
    elif val == "NR" or val != 'G':
        color = "gray"

    return f"background-color: {color}"

def add_test_data_to_prev_data():
    """
    Method for adding test data to the PREV_DATA dictionary. Only called when tests are run.
    """
    test_file_information_studies = ["Problem_File_Size_Daily", "Problem_File_Count_Daily", 
                                     "Problem_File_Size_Weekly", "Problem_File_Count_Weekly",
                                     "File_Size_Weekly_Not_Run", "File_Count_Weekly_Not_Run"]
    
    for test_study in test_file_information_studies:
        PREV_DATA[test_study] = {"N: File Count" : TEST_FILE_COUNT, 
                                  "N: Total File Size (MB)": TEST_FILE_SIZE}