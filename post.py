from flask import Blueprint, Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import sqlite3

import populateLanguage
import getJobs
import filterJobs


posts = Blueprint('posts', __name__)

@posts.route('/submit', methods=['POST'])
def submit():
    """Submits user's query to the database and returns with appropriate results"""
    print('hey')
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



@posts.route('/update_languages', methods=['POST'])
def update_languages():
    """Updates user's prioritization of languages and shows the updated languages in the languages column"""
    user_languages_list = request.json['user_languages_list'].split(',')

    #languages have no spaces in their strings and we remove empty strings
    user_languages_list = [x.strip() for x in user_languages_list]

    while '' in user_languages_list:
        user_languages_list.remove('')


    populateLanguage.populate(user_languages_list)
    return jsonify(a = 'nothing')


@posts.route('/removeFromShortList', methods=['POST'])
def remove_from_short_list():
    """Removes selected job from the short list"""

    job_identifier = request.json['job_identifier']
    session = requests.Session()
    params = {'userid': 'l43cheng', 'pwd':'IAaW132@@@'} #timezoneOffset and submit are unnecessary but also submitted

    #===============login
    s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)


    #================go to the Job Short List page. This get might be necessary in order to do a POST

    s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL?pslnkid=UW_CO_JOB_SLIST_LINK&FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOB_SLIST_LINK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")

    bsObj = BeautifulSoup(s.text, "html.parser")
    print('on job short list page, about to loop through jobs to find correct one, by matching job_identifier')

    k = bsObj.find("span", {"id" : "UW_CO_STUJOBLST_UW_CO_JOB_ID$0"}).get_text()
    print(k)

    #loop through jobs until find matching one
    for i in range(0,100,1):
        print(str(i))
        #provides a stopping point.
        if bsObj.find("span", {"id" : "UW_CO_STUJOBLST_UW_CO_JOB_ID$" + str(i)}) == None :
                print('This span does not exist, which means we have already scrolled through all removed jobs')
                break
        print('not in if statement')
        #print('we are in the else statement. The value of the find is: '+ bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}))
        short_list_job_identifier = bsObj.find("span", {"id" : "UW_CO_STUJOBLST_UW_CO_JOB_ID$" + str(i)}).get_text()
        print(short_list_job_identifier)
        #if the found ID in JobMine's shortlist matches the one we're looking, remove that job
        if (short_list_job_identifier == job_identifier):
            print('found a match!')
            #delete the job on the shortlist that matches the same id as the selected job
            paramsForDeleteShortListJob = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_STUJOBLST$delete$' + str(i) + '$$0',
                                            'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k='}

            m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL", paramsForDeleteShortListJob)

            print('finished deleting and about to save')

            paramsForSave = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'#ICSave',
                              'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k='}

            m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL ", paramsForSave)

            print('finished saving delete')

        print('match not found,index was at:' + str(i))

    return jsonify (a = 'nothing')

@posts.route('/addToShortList', methods=['POST'])
def add_to_short_list():
    job_title = request.json['job_title']
    #job_title = 'Manufacturing Design'

    employer_name = request.json['employer_name']
    #employer_name = 'Apple Inc'

    #maybe not needed after all, even with duplicates, use intelligence
    job_identifier = request.json['job_identifier']

    #search for the job with employer name and job title

    session = requests.Session()
    params = {'userid': 'l43cheng', 'pwd':'IAaW132@@@'} #timezoneOffset and submit are unnecessary but also submitted

    #===============login
    s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)

    #=================go to Job Inquiry, the get method must exist before using a post
    s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")
    #since after we check Approved, Posted, and Cancelled, then every other job must be in Apps Avail. I will do complementary counting by first
    #setting all to Apps Avail

    appr = searchForJob('APPR',employer_name,job_title,job_identifier, session)
    appa = searchForJob('APPA',employer_name,job_title,job_identifier, session)
    post = searchForJob('POST',employer_name,job_title,job_identifier, session)

    with open("AddingToShortList.txt", "a") as myfile:
        myfile.write(employer_name + "\r\t")
    myfile.close()


    if (appr == True) or (appa == True) or (post == True):
        connection=sqlite3.connect("jobs.db")
        c = connection.cursor()
        c.execute("UPDATE AllJobs SET in_short_list = 'Y' WHERE job_identifier = '" + job_identifier + "'" )
        connection.commit()
        connection.close()

        with open("ShortListJobs.txt", "a") as myfile:
            myfile.write("\n\n=================SUCCESSFUL=================\n" + job_title + "\t" + employer_name + "\t" + job_identifier + "\n======================================================================")
        myfile.close()
        return jsonify(a = 'Found')
    else:
        with open("ShortListJobs.txt", "a") as myfile:
            myfile.write("=================REQUIRES ATTENTION =================" + job_title + "\t" + employer_name + "\t" + job_identifier + "\n======================================================================")
        myfile.close()
        return jsonify(a = 'Not Found')

def searchForJob(apply, employer_name, job_title, job_identifier, session):

    #search for the job
    print('about to search')
    paramsForSearch = {
    'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
    'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
    'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': str(apply),
         'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': str(employer_name),
          'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': str(job_title)
    }
    s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

    print('just pressed the search button')

    #here, we check if this is the correct section and we can post to it.
    # It is the correct section if the span holding the first entry has a matching job id, UW_CO_JOBRES_VW_UW_CO_JOB_ID$0.
    # I think if two jobs have same name, this will fail
    # but that's a small inconvenience and I think the user can manually handle it.

    #print(s.text)

    bsObj = BeautifulSoup(s._content, "html.parser")
    print(bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$0"}).get_text())

    if (bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$0"}).get_text() == job_identifier):

        print('found! The job_identifier is:' + job_identifier)
        #add to short list
        print('about to add to short list')
        paramsForShortList = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_SLIST_HL$0',
                        'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': str(employer_name),
                        'UW_CO_JOBSRCH_UW_CO_JOB_TITLE' : str(job_title)}

        #'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': str(apply)

        m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForShortList)
        print('just finished adding')
        return True
    else:
        return False



@posts.route('/update_jobs', methods=['POST'])
def update_jobs():
    getJobs.updateJobs()
    return jsonify(a = 'nothing')



