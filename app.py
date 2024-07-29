import os
import time
from datetime import datetime
from problem_detected_data_visualization import *
from flask import Flask, render_template, redirect

print(datetime.now().date(), flush=True)
st = time.time()
df = build_df_from_csv_files()
et = time.time()
print("Runtime Build DF: ", et - st, flush=True)


problem_detected_df = get_problem_detected_df(df)
todays_problem_detected_df = get_html_for_problem_detected_df(problem_detected_df)
past_month_problem_detected_df = get_html_for_problem_detected_df(problem_detected_df, num_days_in_past=30)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def display_past_month():
    """
    Displays past_month_problem_detected_df for all studies

    Returns:
        str: Returns a rendered template of home.html that displays 
        past_month_problem_detected_df as an HTML table
    """
    return render_template("home.html", table=past_month_problem_detected_df, duration="in Past Month")

@app.route("/today", methods=["GET"])
def display_today():
    """
    Displays todays_problem_detected_df for all studies. Page will be blank
    if there is no data for today.

    Returns:
        str: Returns a rendered template of home.html that displays 
        todays_problem_detected_df as an HTML table
    """
    
    if todays_problem_detected_df == "":
        return render_template("home.html", table=todays_problem_detected_df, duration="Today: NO DATA UPLOADED")
    return render_template("home.html", table=todays_problem_detected_df, duration="Today")

@app.route("/displaySingle/<col>", methods=["GET"])
def display_single(col):
    """
    Displays a given study's "Occurrence", "Last Successful Run Date",
    "Last Successful Run Time", "Next Run Date", "Next Run Time", and its 
    problem_detected_df over the past week and month.

    Args:
       col (str): a studies Study ID 

    Returns:
        str: Returns a rendered template of single.html that displays 
        a study's meta information and problem_detected_df over the past week 
        and month. 
    """
    if col == '\xa0':
        return redirect("/", code=302)
        
    # Use either a date string "YYYY-MM-DD" or datetime.now().date() to build study_run_info_df
    if os.getenv("RUNNING_WITH_DATE_STRING", 'False') == 'True':
        DATE_STRING = os.getenv("DATE_STRING")
        study_run_info_df = df[(df["Study ID"] == col) & (df["Date"] == datetime.strptime(DATE_STRING, "%Y-%m-%d").date())]
    
    else:    
        study_run_info_df = df[(df["Study ID"] == col) & (df["Date"] == datetime.now().date())]
    
    
    if study_run_info_df.empty:
        past_week_problem_detected_HTML = get_html_for_problem_detected_df(problem_detected_df, study_id=col, num_days_in_past=7)
        past_month_problem_detected_HTML = get_html_for_problem_detected_df(problem_detected_df, study_id=col, num_days_in_past=30)
        return render_template("single.html", study_id=col, past_week_table=past_week_problem_detected_HTML, past_month_table=past_month_problem_detected_HTML)
    
    occurrence = study_run_info_df.iloc[-1]["Occurrence"]
    last_successful_run_date = study_run_info_df.iloc[-1]["Last Successful Run Date"]
    last_successful_run_time = study_run_info_df.iloc[-1]["Last Successful Run Time"]
    next_run_date = study_run_info_df.iloc[-1]["Next Run Date"]
    next_run_time = study_run_info_df.iloc[-1]["Next Run Time"]

    past_week_problem_detected_HTML = get_html_for_problem_detected_df(problem_detected_df, study_id=col, num_days_in_past=7)
    past_month_problem_detected_HTML = get_html_for_problem_detected_df(problem_detected_df, study_id=col, num_days_in_past=30)

    return render_template("single.html", study_id=col, metadata_dict={"occurrence" : occurrence, "last_successful_run_date" : last_successful_run_date,
                           "last_successful_run_time" : last_successful_run_time, "next_run_date" : next_run_date, "next_run_time" : next_run_time},
                           past_week_table=past_week_problem_detected_HTML, past_month_table=past_month_problem_detected_HTML)


@app.cli.command()
def build_todays_df():
    """
    Run by a cron job every day at 10:00 AM EST. Reloads the Flask app and builds
    a new problem_detected_df with data entries from the current date.
    """
    print("Building Today's Problem Detected DataFrame")