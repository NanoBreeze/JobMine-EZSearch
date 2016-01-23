from flask import Flask, render_template, request, jsonify
from post import posts
import csv
import json
import filterJobs
import populateLanguage
import getJobs
import requests
from bs4 import BeautifulSoup

#testing purposes only
import sqlite3

app = Flask(__name__)
app.register_blueprint(posts)

#the first page user sees. Requires the user to input their JobMine credentials
@app.route('/')
def welcome():


    with open("ShortListJobs.txt", "w") as myfile:
        myfile.write("This file stores information about the jobs you wanted to short list. \n"
                     "You can use this file as Plan B - manually shortlisting jobs in JobMine - in case there's a bug with EZSearch's Add to and Remove from Shortlist buttons" )
    myfile.close()

    '''
    connection=sqlite3.connect("jobs.db")
    c = connection.cursor()
    cur = (c.execute("SELECT last_day_to_apply FROM AllJobs WHERE job_identifier ='00281629'"))
    c.execute("UPDATE AllJobs SET apply = '" + cur.fetchone()[0] + "', last_day_to_apply = 'TEST' WHERE job_identifier = '00281629'"  )
    connection.commit()
    connection.close()
    '''
    '''
    exist = cur.fetchone()
    if exist[0] == 0:
        print('no')
    else:
        print('yes')
        print(exist[0])
    '''
    '''
    if cur.fetchone()[0]==0:
        print('There is no component named')
    else:
        print('Component %s found in %s row(s))')
        print(cur.fetchone()[0])
    '''

    return render_template("Welcome.html")

#shows the Job Inquiry page, where the user can search for jobs
@app.route('/jobInquiry')
def job_inquiry():
    filter_words = {'sql_query': '',
                    'job_identifier': '',
                    'summary': '',
                    'location' : '',
                    'discipline' : 'Computer, Electrical, Software, Computer Science',
                    'job_title': '',
                    'employer_name' : '',
                    'languages' : '',
                    'junior' : 'junior',
                    'intermediate' : 'intermediate',
                    'senior': 'senior' }

    jobs = []
    return render_template("JobInquiry.html", jobs = jobs, filter_words = filter_words)

'''
#receives all search filters user posts from Job Inquiry
#If the user typed SQL queries (sql_query is not an empty string), then we examine the SQL queries only and ignore the values in the other <input>s
#we only examine the value of <input>s that contain content and ignore all empty <input>s
@app.route('/submit', methods=['POST'])
def submit():


    filter_words = {'sql_query': request.form['sql_query'],
                    'job_identifier': str(request.form['job_identifier']),
                    'summary': request.form['summary'],
                    'location' : request.form['location'],
                    'discipline' : request.form['discipline'],
                    'job_title': request.form['job_title'],
                    'employer_name' : request.form['employer_name'],
                    'languages' : request.form['languages']
                    }

    print(filter_words)

    #Will contain the SQL query to be given to filterJobs.filter_by_SQL(sql_query), something else
    query='SELECT * FROM AllJobs WHERE '

    #if user typed SQL queries, then filter based on the queries user typed and ignore the values in the other <input>s
    if request.form['sql_query']:
        query+=request.form['sql_query']

    #the user didn't type SQL queries so we examine the values in the other <input>s.
    #If the input is not empty, we concatenate its value to an appropriate WHERE statement
    #If more than two filters are on, then we write only one WHERE statement. Thus, once one WHERE statement already exists, we contatenate  the other filters with AND
    else:

        try:
            if request.form['junior']:
                filter_words['junior'] = 'junior'
        except:
            filter_words['junior'] = 'impossible'

        try:
            if request.form['intermediate']:
                filter_words['intermediate'] = 'intermediate'
        except:
            filter_words['intermediate'] = 'impossible'

        try:
            if request.form['senior']:
                filter_words['senior'] = 'senior'
        except:
                filter_words['senior'] = 'impossible'


        query += "(level LIKE '%" + filter_words['junior'] + "%' OR level LIKE '%" + filter_words['intermediate'] + "%' OR level LIKE '%" + filter_words['senior'] + "%')"

        #contains the other filters
        filters = [
            {'column_name': 'job_identifier', 'value': filter_words['job_identifier'].split(',')},
            {'column_name': 'summary', 'value': filter_words['summary'].split(',')},
            {'column_name': 'location', 'value': filter_words['location'].split(',')},
            {'column_name': 'discipline', 'value':filter_words['discipline'].split(',')},
            {'column_name': 'job_title', 'value':filter_words['job_title'].split(',')},
            {'column_name': 'employer_name', 'value':filter_words['employer_name'].split(',')},
            #languages contain the special case of matching C, which shall be matched by C, and ,C
            {'column_name': 'languages', 'value':filter_words['languages'].split(',')}
        ]

        #if the value for that filter doesn't exist, then user doesn't want to filter that value so do nothing with that filter.
        #we append with AND because where has already been appended
        for filter in filters:

            # remove all trailing whitespaces in each item in a filter for accurate searches with list comprehension
            filter['value'] = [x.strip() for x in filter['value']]

            #we assume the user types in elements to filter by xxxx,yyyy OR xxxx , yyyy. Even if user plays funny business, eg, , , xxxx, y, we handle them by ignoring empty elements
            #if the filter contains things to filter, aka, the first element is not empty (if it is, then skip that filter and go to next one)
            #then the general filter begins with an AND statement that uses many ORs to combine each specific query.
            if filter['value'][0]:
                query += " AND ("
                for val in filter['value']:
                    #handling empty elements, eg, ,   , by ignoring them
                    if not val:
                        continue
                    if val == filter['value'][0]:
                        query += filter['column_name'] + " LIKE '%" + val + "%'"
                    else:
                        #special matching if we're filtering languages and the language is C
                        if (filter['column_name'] == 'languages') and val == 'C':
                            query += " OR languages LIKE '%C,%' OR languages LIKE '%,C%'"
                        else:
                            query += " OR " + filter['column_name'] + " LIKE '%" + val + "%'"
                query += ")"

    print(query)
    jobs = filterJobs.filter_by_SQL(query)

    return render_template("JobInquiry.html", jobs = jobs, filter_words = filter_words)
'''


#displays the Analytics and Exports page
@app.route('/analyticsExport')
def analytics_export():

    filter_words = {'sql_query': '',
                    'job_identifier': '',
                    'summary': '',
                    'location' : '',
                    'discipline' : '',
                    'job_title': '',
                    'employer_name' : '',
                    'languages' : '',
                    'junior' : '',
                    'intermediate' : '',
                    'senior': ''}

    jobs = []

    #return render_template("JobInquiry.html", jobs = jobs, filter_words = filter_words)

    #gets analytics on the number of jobs in cities
    analytics_city_count = filterJobs.analytics_city_count()
    print("analytics_city_count" + str(analytics_city_count))

    #gets analytics on the number of pre-set programming languages
    analytics_languages_count = filterJobs.analytics_language_count()
    print("analytics_languages_count" + str(analytics_languages_count))

    #gest analytics on the number of jobs per faculty
    analytics_faculties_count = filterJobs.analytics_faculty_count()
    print("analytics_faculties_count" + str(analytics_faculties_count))

    #gets analytics on the number of jobs per level
    analytics_levels_count = filterJobs.analytics_level_count()
    print("analytics_levels_count" + str(analytics_levels_count))

    #gets analytics on the total number of jobs, unique employers, and unique locations
    analytics_total_numbers_count = filterJobs.analytics_total_numbers()
    print("analytics_total_numbers_count" + str(analytics_total_numbers_count))

    #gets analytics on number of jobs that contain keywords
    analytics_job_containing_keywords_count = filterJobs.analytics_jobs_containing_keywords_count()
    print("analytics_job_containing_keywords_count" + str(analytics_job_containing_keywords_count))



    return render_template("AnalyticsExport.html",
                           analytics_city_count = analytics_city_count,
                           analytics_languages_count = analytics_languages_count,
                           analytics_faculties_count = analytics_faculties_count,
                           analytics_levels_count = analytics_levels_count,
                           analytics_total_numbers_count = analytics_total_numbers_count,
                           analytics_job_containing_keywords_count = analytics_job_containing_keywords_count
                           )

@app.route('/docs')
def docs():
    return render_template("Docs.html")

@app.route('/feedback')
def feedback():
    return render_template("Feedback.html")

#displays all jobs
@app.route('/exportHtml/<int:offset>')
def export_html(offset):

    jobs = filterJobs.get_jobs_for_HTML_export(offset)

    for job in jobs:

        job['discipline'] = [x.strip() for x in job['discipline'].split(',')]
        job['level'] = [x.strip() for x in job['level'].split(',')]

        #we strip the comments of trailing whitespaces to more easily check on client whether to display the comment tag.
        job['comments'] = job['comments'].strip()

    return render_template("ExportHTML.html", jobs = jobs)

#makes a csv file with all job details
@app.route('/exportCsv')
def export_csv():

    jobs = filterJobs.give_all_jobs()


    with open('jobs_EZSearch.csv', 'w') as csv_file:
        #the } is the rarest delimiter I can find.
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(['job_identifier','job_title','employer_name','unit_name','location',
                         'number_of_openings', 'level', 'discipline', 'hiring_support',
                         'work_term_support', 'comments', 'summary'])

        for job in jobs:
            writer.writerow(job)
    return jsonify(a = 'nothing')

#makes a txt file with all job details
@app.route('/exportTxt')
def export_txt():

    jobs = filterJobs.give_all_jobs()

    writer = open('jobs_EZSearch.txt','w')

    for job in jobs:
        writer.write('\n')
        writer.write('job_identifier:')
        writer.write(job[0])
        writer.write('\n')

        writer.write('job_title:')
        writer.write(job[1])
        writer.write('\n')

        writer.write('employer_name:')
        writer.write(job[2])
        writer.write('\n')

        writer.write('unit_name:')
        writer.write(job[3])
        writer.write('\n')

        writer.write('location:')
        writer.write(job[4])
        writer.write('\n')

        writer.write('number_of_openings:')
        writer.write(job[5])
        writer.write('\n')

        writer.write('level:')
        writer.write(job[6])
        writer.write('\n')

        writer.write('discipline:')
        writer.write(job[7])
        writer.write('\n')

        writer.write('hiring_support:')
        writer.write(job[8])
        writer.write('\n')

        writer.write('work_term_support:')
        writer.write(job[9])
        writer.write('\n')

        writer.write('comments:')
        writer.write(job[10])
        writer.write('\n')

        writer.write('summary:')
        writer.write(job[11])
        writer.write('\n')
        writer.write('==================================================')

    writer.close()

    return jsonify(a = 'nothing')

#makes a json file with details associated to every job
@app.route('/exportJson')
def export_json():

    jobs = filterJobs.give_all_jobs()

    jobs_json = {}

    for i in range(len(jobs)):
        jobs_json['job'+str(i)] = {'job_identifier': jobs[i][0], 'job_title': jobs[i][1], 'employer_name':jobs[i][2],
                                   'unit_name': jobs[i][3], 'location': jobs[i][4], 'number_of_openings': jobs[i][5],
                                   'level': jobs[i][6], 'discipline': jobs[i][7], 'hiring_support':jobs[i][8],
                                    'work_term_support': jobs[i][9], 'comments':jobs[i][10], 'summary':jobs[i][11]}


    json_file = open('jobs_EZSearch.json','w')

    json.dump(jobs_json, json_file, indent=4)

    return jsonify(a = 'nonthing')



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)