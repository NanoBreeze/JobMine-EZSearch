import sqlite3

with sqlite3.connect("jobs.db") as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE AllJobs(job_identifier TEXT, job_title TEXT, employer_name TEXT, unit_name TEXT, location TEXT, number_of_openings INTEGER"
              "discipline TEXT, level TEXT, discipline TEXT, hiring_support TEXT, work_term_support TEXT, comments TEXT, summary TEXT"
              "languages TEXT, in_short_list TEXT )")
