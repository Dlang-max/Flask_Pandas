from datetime import datetime
from problem_detected_data_visualization import *

TEST_DATA_DIRECTORY = "test_data"

test_df = build_df_from_csv_files(path_to_csv_directory=TEST_DATA_DIRECTORY, testing=True)
test_problem_detected_df = get_problem_detected_df(test_df)

def test_get_day_num_days_in_past():
    prev_date, current_date = get_day_num_days_in_past(num_days_in_past=1)
    assert prev_date == current_date
    
    # Proper formatting of current_date string.
    prev_date, current_date = get_day_num_days_in_past(current_date="2024-07-07", num_days_in_past=7)
    assert prev_date == datetime.strptime("2024-07-01", "%Y-%m-%d").date()
    assert current_date == datetime.strptime("2024-07-07", "%Y-%m-%d").date()
    
    # Improper formatting of current_date string.
    prev_date, current_date = get_day_num_days_in_past(current_date="2024/07/07", num_days_in_past=7)
    assert current_date == datetime.now().date()
    

def test_get_date_of_file():
    date = datetime.strptime("20240510", '%Y%m%d').date()
    assert get_date_of_file("NRG_N_TODAY_COMP_20240510.csv") == date

def test_build_df_from_csv_files():
    assert test_df["Date"][0] == get_date_of_file("NRG_N_TODAY_COMP_20240510.csv")

def test_get_problem_detected_df():
    assert test_problem_detected_df.shape[0] == 11
    assert test_problem_detected_df.shape[1] == 1

# TESTING build_prev_data_dict():
# File Size
def test_build_prev_data_dict_file_size():
    assert PREV_DATA["Problem_Detected_Study"]["N: Total File Size (MB)"] == 65.26
    
# File Count
def test_build_prev_data_dict_file_count():
    assert PREV_DATA["Problem_Detected_Study"]["N: File Count"] == 68

# TESTING format_problem_detected_column():
# Problem detected in daily study
def test_problem_detected_study():
    row = test_df[test_df["Study ID"] == "Problem_Detected_Study"].reset_index()
    assert row["Problem Detected"][0] == 'E' 

# No problem detected in daily study
def test_no_problem_detected_daily_study():
    row = test_df[test_df["Study ID"] == "No_Errors_Study"].reset_index()
    assert row["Problem Detected"][0] == 'G'

# Weekly study not run 
def test_weekly_study_not_run():
    row = test_df[test_df["Study ID"] == "Weekly_Study_Not_Run"].reset_index()
    assert row["Problem Detected"][0] == "NR"

# Weekly study no problem detected
def test_weekly_study_no_errors():
    row = test_df[test_df["Study ID"] == "Weekly_Study_No_Errors"].reset_index()
    assert row["Problem Detected"][0] == 'G' 

# Weekly study problem detected
def test_weekly_study_problem_detected():
    row = test_df[test_df["Study ID"] == "Weekly_Study_Problem_Detected"].reset_index()
    assert row["Problem Detected"][0] == 'E'

# Daily study file size error
def test_study_file_size_problem_detected_daily():
    row = test_df[test_df["Study ID"] == "Problem_File_Size_Daily"].reset_index()
    assert row["Problem Detected"][0] == 'E'

# Daily study file count error
def test_study_file_count_problem_detected_daily():
    row = test_df[test_df["Study ID"] == "Problem_File_Count_Daily"].reset_index()
    assert row["Problem Detected"][0] == 'E'

# Weekly study file size error
def test_study_file_size_problem_detected_weekly():
    row = test_df[test_df["Study ID"] == "Problem_File_Size_Weekly"].reset_index()
    assert row["Problem Detected"][0] == 'E'

# Weekly study count size error
def test_study_file_count_problem_detected_weekly():
    row = test_df[test_df["Study ID"] == "Problem_File_Count_Weekly"].reset_index()
    assert row["Problem Detected"][0] == 'E'

# Weekly study file size not run
def test_study_file_size_not_run():
    row = test_df[test_df["Study ID"] == "File_Size_Weekly_Not_Run"].reset_index()
    assert row["Problem Detected"][0] == 'NR'

# Weekly study file count not run
def test_study_file_count_not_run():
    row = test_df[test_df["Study ID"] == "File_Count_Weekly_Not_Run"].reset_index()
    assert row["Problem Detected"][0] == 'NR'
    
def test_prev_data_updates_correctly():
    study_id = "Problem_File_Size_Daily"
    
    column = "N: Total File Size (MB)"
    #Test correct file count
    row = test_df[test_df["Study ID"] == study_id]
    assert PREV_DATA[study_id][column] == row[column].iloc[0]
    
    
    column = "N: File Count"
    # Test correct file size
    row = test_df[test_df["Study ID"] == study_id].reset_index()
    assert PREV_DATA[study_id][column] == row[column].iloc[0]
