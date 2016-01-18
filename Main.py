from flask import Flask, render_template, request
import filterJobs

app = Flask(__name__)

#the first page user sees. Requires the user to input their JobMine credentials
@app.route('/')
def welcome():
    return render_template("Welcome.html")

#shows the Job Inquiry page, where the user can search for jobs
@app.route('/jobInquiry')
def job_inquiry():
    filter_words = {'sql_query': '',
                    'job_identifier': '',
                    'summary': '',
                    'location' : '',
                    'discipline' : '',
                    'job_title': '',
                    'employer_name' : '',
                    'junior' : '',
                    'intermediate' : '',
                    'senior': ''}

    jobs = filterJobs.give_all_jobs()
    return render_template("JobInquiry.html", jobs = jobs, filter_words = filter_words)

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
            {'column_name': 'employer_name', 'value':filter_words['employer_name'].split(',')}
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
                        query += " OR " + filter['column_name'] + " LIKE '%" + val + "%'"
                query += ")"

    print(query)
    jobs = filterJobs.filter_by_SQL(query)

    return render_template("JobInquiry.html", jobs = jobs, filter_words = filter_words)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)