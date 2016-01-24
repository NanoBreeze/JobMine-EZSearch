"""
This file is part of JobMine EZSearch.

JobMine EZSearch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

JobMine EZSearch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with JobMine EZSearch.  If not, see <http://www.gnu.org/licenses/>.
"""

import sqlite3


def get_search_data(query):
    """Returns the jobs that match user's search query, custom SQL query or input."""
    print("In filter_by_SQL")
    connection=sqlite3.connect("jobs.db")
    print(query)
    cur = connection.execute(query)

    jobs = []

    for row in cur.fetchall():
        jobs.append({'job_title': row[1],'level': row[6], 'employer_name': row[2], 'location': row[4], 'number_of_openings':row[5], 'in_short_list':row[15], 'languages' : row[12],
                     'summary': row[11], 'job_identifier':row[0], 'unit_name':row[3], 'discipline': row[7], 'hiring_support': row[8], 'work_term_support':row[9], 'comments': row[10], 'apply': row[13], 'last_day_to_apply':row[14],  })

    connection.close()

    return jobs


def get_csv_json_text_data():
    """Returns all data of every job in database. Used to make csv, json, and text files."""

    connection=sqlite3.connect("jobs.db")
    cur = connection.execute('SELECT * FROM AllJobs')
    jobs = []
    for row in cur.fetchall():
        '''
        jobs.append({'job_identifier': row[0], 'job_title':row[1], 'employer_name':row[2],'unit_name':row[3], 'location':row[4],
                     'number_of_openings':row[5], 'level':row[6], 'discipline':row[7], 'hiring_support':row[8],
                     'work_term_support':row[9], 'comments':row[10], 'summary':row[11]})
        '''

        jobs.append([str(row[0]),str(row[1]),str(row[2]),str(row[3]),
                     str(row[4]),str(row[5]),str(row[6]),str(row[7]),
                     str(row[8]),str(row[9]),str(row[10]),str(row[11])])

    connection.close()
    return jobs


def get_html_data(offset = 0, limit = 1000):
    """Returns some data of every job in database. Used to make one of the HTML files."""

    connection=sqlite3.connect("jobs.db")
    cur = connection.execute('SELECT employer_name, job_title, number_of_openings, location, level, discipline, summary, comments FROM AllJobs LIMIT ' + str(limit) + ' OFFSET ' + str(offset))
    jobs = []

    for row in cur.fetchall():
        jobs.append({'employer_name': row[0],'job_title': row[1], 'number_of_openings': row[2], 'location': row[3], 'level':row[4], 'discipline': row[5], 'summary':row[6], 'comments':row[7] })

    connection.close()
    return jobs


def get_city_count():
    """Returns a list of the top 10 cities that hire the most students and the number of hiring students."""
    connection=sqlite3.connect("jobs.db")
    cur = connection.execute("SELECT * FROM (SELECT COUNT(*) AS Count, location FROM AllJobs GROUP BY Location ORDER BY Count DESC) LIMIT 10")

    jobs = []
    count_of_jobs = 0
    for row in cur.fetchall():
        jobs.append({'count': row[0], 'location1': row[1]})
        count_of_jobs += row[0]

    total_number_of_jobs = connection.execute("SELECT COUNT(*)  FROM AllJobs").fetchone()[0]
    jobs.append({'count': total_number_of_jobs - count_of_jobs, 'location1':'other'})

    connection.close()

    return jobs


#I feel like this is very bad SQL but it works and I'm not sure what the optimized SQL looks like
def get_languages_count():
    """Returns the number of jobs that match a language."""

    connection=sqlite3.connect("jobs.db")
    #not accurate
    java_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE summary LIKE '%Java %' OR summary LIKE '%Java)%'").fetchone()[0]

    c_plus_plus_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE summary LIKE '%C++%'").fetchone()[0]
    c_sharp_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%C#%'").fetchone()[0]
    javascript_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%JavaScript%' OR summary LIKE '%Javascript%'").fetchone()[0]
    iOS_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%iOS%'").fetchone()[0]
    ruby_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%Ruby%'").fetchone()[0]
    sql_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%SQL%'").fetchone()[0]
    net_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%.NET%'").fetchone()[0]

    #not accurate, very inaccurate
    c_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE languages LIKE '%C,%'").fetchone()[0]
    python_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%Python%'").fetchone()[0]
    linux_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE summary LIKE '%Linux%'").fetchone()[0]

    connection.close()

    languages = [{'language': 'Java', 'count': java_count},
                 {'language': 'C++', 'count': c_plus_plus_count},
                 { 'language': 'C#', 'count': c_sharp_count},
                 { 'language': 'JavaScript', 'count': javascript_count},
                 { 'language': 'iOS', 'count': iOS_count},
                 { 'language': 'Ruby', 'count': ruby_count},
                 { 'language': 'SQL', 'count': sql_count},
                 {'language': '.NET', 'count': net_count},
                 {'language': 'C', 'count': c_count},
                 { 'language': 'Python', 'count': python_count},
                 { 'language': 'Linux', 'count': linux_count}
                 ]

    return languages


def get_faculty_count():
    """#returns a list of the number of jobs posted to each faculty."""
    connection=sqlite3.connect("jobs.db")

    ahs_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE discipline LIKE '%AHS%'").fetchone()[0]
    arts_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE discipline LIKE '%ARTS%'").fetchone()[0]
    eng_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE discipline LIKE '%ENG%'").fetchone()[0]
    env_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE discipline LIKE '%ENV%'").fetchone()[0]
    math_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE discipline LIKE '%MATH%'").fetchone()[0]
    sci_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE discipline LIKE '%SCI%'").fetchone()[0]

    connection.close()

    faculties = [{'faculty': 'AHS', 'count': ahs_count},
                 {'faculty': 'ARTS', 'count': arts_count},
                 { 'faculty': 'ENG', 'count': eng_count},
                 { 'faculty': 'ENV', 'count': env_count},
                 { 'faculty': 'MATH', 'count': math_count},
                 { 'faculty': 'SCI', 'count': sci_count}
                 ]

    return faculties


def get_level_count():
    """Returns the number of jobs in Junior, Intermediate, and Senior."""

    connection=sqlite3.connect("jobs.db")

    junior_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE level LIKE '%Junior%'").fetchone()[0]
    intermediate_count = connection.execute("SELECT COUNT(*)  FROM AllJobs WHERE level LIKE '%Intermediate%'").fetchone()[0]
    senior_count = connection.execute("SELECT COUNT(*) FROM AllJobs WHERE level LIKE '%Senior%'").fetchone()[0]

    connection.close()

    levels = [{'faculty': 'Junior', 'count': junior_count},
                 {'faculty': 'Intermediate', 'count': intermediate_count},
                 { 'faculty': 'Senior', 'count': senior_count}
             ]

    return levels

def get_keywords_count():
    connection=sqlite3.connect("jobs.db")

    software = connection.execute("SELECT COUNT(*)  FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Software%')").fetchone()[0]
    hardware = connection.execute("SELECT COUNT(*)  FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Hardware%')").fetchone()[0]
    embedded = connection.execute("SELECT COUNT(*) FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Embedded%')").fetchone()[0]
    engineer = connection.execute("SELECT COUNT(*) FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Engineer%')").fetchone()[0]
    analyst = connection.execute("SELECT COUNT(*) FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Analyst%')").fetchone()[0]
    developer = connection.execute("SELECT COUNT(*)  FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Developer%')").fetchone()[0]
    coop = connection.execute("SELECT COUNT(*)  FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Co-op%')").fetchone()[0]
    intern = connection.execute("SELECT COUNT(*)  FROM (SELECT employer_name FROM AllJobs WHERE job_title LIKE '%Intern%')").fetchone()[0]

    connection.close()

    jobs_keywords = [
        {'job_title':'Software', 'count':software},
        {'job_title':'Hardware', 'count':hardware},
        {'job_title':'Embedded', 'count':embedded},
        {'job_title':'Engineer', 'count':engineer},
        {'job_title':'Analyst', 'count':analyst},
        {'job_title':'Developer', 'count':developer},
        {'job_title':'Co-op', 'count':coop},
        {'job_title':'Intern', 'count':intern}
    ]

    return jobs_keywords

def get_numbers():
    """Returns the total number of jobs, locations, and employers availalble."""
    connection=sqlite3.connect("jobs.db")

    total_jobs = connection.execute("SELECT COUNT(*)  FROM AllJobs").fetchone()[0]
    total_unique_location = connection.execute("SELECT COUNT(*)  FROM (SELECT location FROM AllJobs GROUP BY location)").fetchone()[0]
    total_unique_employer = connection.execute("SELECT COUNT(*) FROM (SELECT employer_name FROM AllJobs GROUP BY employer_name)").fetchone()[0]

    connection.close()

    total_numbers = [{'total_jobs' : total_jobs},
                     {'total_unique_location':total_unique_location},
                     {'total_unique_employer':total_unique_employer}
                     ]

    return total_numbers





#================================================USE THE CURSOR
class AllJobs:
    """Writes or reads from the database."""

    __connection = None
    __cur = None


    def __init__(self):
        """Sets a cursor to the database."""
        self.__connection = sqlite3.connect("jobs.db")
        self.__cur = self.__connection.cursor()

    def commit_query(self, query, values=None):
        """Updates the database if values=None, inserts to the database otherwise."""
        if values is None:
            self.__cur.execute(query)
        else:
            self.__cur.execute(query, values)
        self.__connection.commit()


    def get_query(self, query):
        """Reading from the database. Returns the rows of the query"""
        return self.__cur.execute(query)

    def close_connection(self):
        """Closes the connection."""
        self.__connection.close()








