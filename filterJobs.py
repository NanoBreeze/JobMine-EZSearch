import sqlite3

def give_all_jobs():
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute('SELECT * FROM AllJobs')
    job = []

    for row in cur.fetchall():
        job.append({'job_title': row[1],'level': row[6], 'employer_name': row[2], 'location': row[4], 'number_of_openings':row[5], 'shortlist': 'TO DO: ADD SHORT LIST', 'language' : 'TO DO: ADD LANGUAGE',  })
    '''
    jobs = [dict(job_identifier = row[0], job_title=row[1], employer_name=row[2], unit_name = row[3], location = row[4], number_of_openings = row[5],
                 level = row[6], discipline = row[7], hiring_support = row[8], work_term_support = row[9], comments = row[10], summary = row[11]) for row in cur.fetchone()]
    '''
    return job