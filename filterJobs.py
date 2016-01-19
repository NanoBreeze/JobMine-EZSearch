import sqlite3


#return the relevant tabular info related to every job
def give_all_jobs():
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute('SELECT * FROM AllJobs')
    jobs = []

    for row in cur.fetchall():
        jobs.append({'job_title': row[1],'level': row[6], 'employer_name': row[2], 'location': row[4], 'number_of_openings':row[5], 'shortlist': 'TO DO: ADD SHORT LIST', 'languages' : row[12]  })

    connection.close()
    return jobs

#return the data related to jobs that are filtered by custom SQL
def filter_by_SQL(query):
    print("In filter_by_SQL")
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute(query)

    jobs = []

    for row in cur.fetchall():
        jobs.append({'job_title': row[1],'level': row[6], 'employer_name': row[2], 'location': row[4], 'number_of_openings':row[5], 'shortlist': 'TO DO: ADD SHORT LIST', 'languages' : row[12],
                     'summary': row[11], 'job_identifier':row[0], 'unit_name':row[3], 'discipline': row[7], 'hiring_support': row[8], 'work_term_support':row[9], 'comments': row[10], 'apply': row[13], 'last_day_to_apply':row[14]   })

    connection.close()

    return jobs

#returns a list of the number of jobs that contain one of 10 pre-set languages
def analytics_language_count():
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute("SELECT * FROM (SELECT COUNT(*) AS Count, location FROM AllJobs GROUP BY Location ORDER BY Count DESC) LIMIT 10")

#returns a list of the top 10 cities that hire the most students
def analytics_city_count():
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute("SELECT * FROM (SELECT COUNT(*) AS Count, location FROM AllJobs GROUP BY Location ORDER BY Count DESC) LIMIT 10")

    jobs = []

    for row in cur.fetchall():
        jobs.append({'Count': row[0], 'location': row[1]})

    print(jobs)
    return jobs



'''
    jobs = [dict(job_identifier = row[0], job_title=row[1], employer_name=row[2], unit_name = row[3], location = row[4], number_of_openings = row[5],
                 level = row[6], discipline = row[7], hiring_support = row[8], work_term_support = row[9], comments = row[10], summary = row[11]) for row in cur.fetchone()]
'''