import db
import requests
import re
import csv
import json
from bs4 import BeautifulSoup



class Analytics:
    """Handles tasks related to analytics. Used by Main.py analytics_export()."""
    def __init__(self):
        print('Analytics class called')


    def get_city_count(self):
        return db.get_city_count()

    def get_languages_count(self):
        return db.get_languages_count()

    def get_faculty_count(self):
        return db.get_faculty_count()

    def get_level_count(self):
        return db.get_level_count()

    def get_keywords_count(self):
        return db.get_keywords_count()

    def get_numbers(self):
        return db.get_numbers()

class Download:
    """Handles tasks related to setting of information for the four download formats. Used by donwloads.py. Returns either bool or data (for HTML format)"""

    def __init__(self):
        print('Constructor called')

    def make_format(self, format, offset=-1):
        if format == 'CSV':
             return self.download_csv()
        elif format == 'TXT':
             return  self.download_txt()
        elif format == 'JSON':
            return  self.download_json()
        else:
            return self.get_html_data(offset)



    def get_html_data(self, offset):
        """Returns data about jobs to be placed in the new HTML file"""
        jobs = db.get_html_data(offset)

        #Split a job's discipline and level items and remove trailing spaces so they can be more clearly displayed on the HTML page
        for job in jobs:

            job['discipline'] = [x.strip() for x in job['discipline'].split(',')]
            job['level'] = [x.strip() for x in job['level'].split(',')]

            #we strip the comments of trailing whitespaces to more easily check on client whether to display the comment tag.
            job['comments'] = job['comments'].strip()

        return jobs


    def download_csv(self):
        """Gets data to create csv file and then calls __write_csv(...) to do the actual writing. Returns a flag to indicate if the write operation was successful."""

        jobs = db.get_csv_json_text_data()
        is_successful = self.__write_csv(jobs)

        return is_successful
    def __write_csv(self, jobs):
        """Makes the CSV file and writes to it with job data. Returns True if writing to a csv file was successful, otherwise returns false."""
        try:
            with open('jobs_EZSearch.csv', 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(['job_identifier','job_title','employer_name','unit_name','location',
                                 'number_of_openings', 'level', 'discipline', 'hiring_support',
                                 'work_term_support', 'comments', 'summary'])

                for job in jobs:
                    writer.writerow(job)

            return True

        except:
            return False


    def download_txt(self):
        """Gets data to create txt file and then calls __write_txt(...) to do the actual writing. Returns a flag to indicate if the write operation was successful."""

        jobs = db.get_csv_json_text_data()
        is_successful = self.__write_txt(jobs)

        return is_successful
    def __write_txt(self, jobs):
        """Makes the TXT file and writes to it with job data. Returns True if writing to a csv file was successful, otherwise returns false."""
        try:

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
            return True

        except:
            return False


    def download_json(self):
        """Gets data to create JSON file and then calls __write_json(...) to do the actual writing. Returns a flag to indicate if the write operation was successful."""

        jobs = db.get_csv_json_text_data()
        is_successful = self.__write_json(jobs)

        return is_successful
    def __write_json(self, jobs):
        jobs_json = {}

        for i in range(len(jobs)):
            jobs_json['job'+str(i)] = {'job_identifier': jobs[i][0], 'job_title': jobs[i][1], 'employer_name':jobs[i][2],
                                       'unit_name': jobs[i][3], 'location': jobs[i][4], 'number_of_openings': jobs[i][5],
                                       'level': jobs[i][6], 'discipline': jobs[i][7], 'hiring_support':jobs[i][8],
                                        'work_term_support': jobs[i][9], 'comments':jobs[i][10], 'summary':jobs[i][11]}

        try:
            json_file = open('jobs_EZSearch.json','w')

            json.dump(jobs_json, json_file, indent=4)
            return True

        except:
            return False

class Shortlist:

    def __init__(self):
        print('in  ShortList constructor')

    def login(self, userid, pwd):
        params = {'userid': str(userid), 'pwd': str(pwd) }
        session = requests.Session()
        session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)
        return session

    def remove_from_shortlist(self, job_identifier, session):
        """
        1. Login
        2. Go to Shortlist page
        3. Loop through up to 500 jobs and for each job,
            a) Find if the span containing the id of job exists. If it does, we find the value of the id. Then, we compare the value of the id with the desired id to remove.
                i. If a match occurs, we press the delete button on shortlist
                ii. then we press the save button
            b) If no match occurs, we do nothing, allowing the loop to go to the next value.
        """

        s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL?pslnkid=UW_CO_JOB_SLIST_LINK&FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOB_SLIST_LINK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")
        bsObj = BeautifulSoup(s.text, "html.parser")

        #loop through jobs until find matching one
        for i in range(0,500,1):
            print(str(i))
            #provides a stopping point.
            if bsObj.find("span", {"id" : "UW_CO_STUJOBLST_UW_CO_JOB_ID$" + str(i)}) == None :
                    print('This span does not exist, which means we have already scrolled through all removed jobs')
                    break


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
                database = db.AllJobs()
                database.commit_query("UPDATE AllJobs SET in_short_list = 'N' WHERE job_identifier = '" + job_identifier + "'")
                database.close_connection()
                print('finished making change to database')
                return

            print('match not found,index was at:' + str(i))

    def add_to_shortlist(self, employer_name, job_title, job_identifier, session):
        """We check for the job in the APPROVED section, APPS AVAIL section, and POSTED section. If it exists, add to shortlist,
        make change to the database, and display 'Found' popup"""

        #go to Job Inquiries
        s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")

        #since after we check Approved, Posted, and Cancelled, then every other job must be in Apps Avail. Use complementary counting by first
        #setting all to Apps Avail
        appr = self.__searchForJob('APPR',employer_name, job_title, job_identifier, session)
        appa = self.__searchForJob('APPA',employer_name, job_title, job_identifier, session)
        post = self.__searchForJob('POST',employer_name, job_title ,job_identifier, session)


        if (appr == True) or (appa == True) or (post == True):
            self.__write_found(employer_name, job_identifier, job_title)
            return True

        return False


    def __searchForJob(self,apply, employer_name, job_title, job_identifier, session):
        """Search for the job in the category provided to the parameter 'apply'. We search by matching posting to server
        the employer name, and job title, clicking on the search button, and then examinining the result for the jobs'
        id to be equal to the supplied job_identifier"""

        #search for the job

        paramsForSearch = {
        'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
        'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
        'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
        'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': str(apply),
             'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': str(employer_name),
              'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': str(job_title)
        }
        s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

        #Wee check if this is the correct section.
        # It is the correct section if the span holding the first entry has a matching job id, UW_CO_JOBRES_VW_UW_CO_JOB_ID$0.
        # I think if two jobs have same name, this will fail
        # but that's a small inconvenience and I think the user can manually handle it.

        bsObj = BeautifulSoup(s._content, "html.parser")

        if (bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$0"}).get_text() == job_identifier):

            print('found! The job_identifier is:' + job_identifier)

            #add to short list
            print('about to add to short list')
            paramsForShortList = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_SLIST_HL$0',
                            'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': str(employer_name),
                            'UW_CO_JOBSRCH_UW_CO_JOB_TITLE' : str(job_title)}

            session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForShortList)
            print('just finished adding to short list')
            return True
        else:
            return False

    def __write_found(self, employer_name, job_identifier, job_title):
        """If the job is added to short list, we change its in_short_list flag in database to indicate so.
        Also, write to text file that a successful addition was made."""
        database = db.AllJobs()
        database.commit_query("UPDATE AllJobs SET in_short_list = 'Y' WHERE job_identifier = '" + job_identifier + "'")
        database.close_connection()

        with open("ShortListJobs.txt", "a") as myfile:
            myfile.write("\n\n=================SUCCESSFUL=================\n" + job_title + "\t" + employer_name + "\t" + job_identifier + "\n======================================================================")
        myfile.close()

    def __write_not_found(self, employer_name, job_identifier, job_title):
        """If the job were not added to the short list, indicate so in the text file"""
        with open("ShortListJobs.txt", "a") as myfile:
            myfile.write("=================REQUIRES ATTENTION =================" + job_title + "\t" + employer_name + "\t" + job_identifier + "\n======================================================================")
        myfile.close()


def cleanLanguages(prioritized_languages):
    """Removes empty string elements and trailing spaces between elements in order for better updating and searching for languages"""

    prioritized_languages = prioritized_languages.split(',')

    #languages have no spaces in their strings and we remove empty strings
    prioritized_languages = [x.strip() for x in prioritized_languages]

    while '' in prioritized_languages:
        prioritized_languages.remove('')

    return prioritized_languages

def updateLanguages(prioritized_languages):
    """Sets the up-to-4 languages to be displayed in the Languages column, according to user's entered list"""

    database = db.AllJobs()

    cur = database.get_query('SELECT job_identifier, summary FROM AllJobs')

    #for each row, or job, we find the first four desired languages that are found. Match by incrementing counters
    for row in cur.fetchall():

        #stores the languages that are associated with the job. Stores up to 4
        included_languages = []

        #keeps track of the number of desired languages found in the job's summary. If equals four, stop adding the language to included_languages and commit to database
        number_of_languages_found = 0

        for language in prioritized_languages:
            if (number_of_languages_found == 4):
                break

            ''' Special match cases:
            " C " or " C," or ",C," or "C/" match to C
            "Javascript" or "JavaScript" match to JavaScript
            "Java[and no s]" match to Java
            '''
            regex=""
            if language == 'C':
                regex = re.compile(' C | C,|,C,|C\/')
            elif language == 'JavaScript' or language == 'Javascript':
                regex = re.compile('JavaScript|Javascript')
            elif language == 'Java':
                regex = re.compile('Java[^(s|S)]|Java\(|Java\)')
            else:
                regex = re.compile(re.escape(language))
            if regex.search(str(row[1])):
                included_languages.append(language)
                number_of_languages_found = number_of_languages_found + 1


        string_of_included_languages = ",".join(included_languages)

        print(string_of_included_languages)

        #now that we finished finding the languages included in the application, we update the language column of the job to contain these languages
        database.commit_query("UPDATE AllJobs SET languages = '" + string_of_included_languages + "' WHERE job_identifier = '" + row[0] + "'")

    database.close_connection()

def submit(filters):
    query='SELECT * FROM AllJobs WHERE '

    #if user typed SQL queries, then filter based on the queries user typed and ignore the values in the other <input>s
    if filters['sql_query']:
        query+= filters['sql_query']

    #If user didn't type SQL queries, examine the values in the other <input>s, beginning with the level because they must exist in an appropriate query

    else:
        query += "(level LIKE '%" + filters['junior'] + "%' OR level LIKE '%" + filters['intermediate'] + "%' OR level LIKE '%" + filters['senior'] + "%')"


        #we make a query with the filters
        non_level_filters = [
            {'column_name': 'job_identifier', 'value': filters['job_identifier'].split(',')},
            {'column_name': 'summary', 'value': filters['summary'].split(',')},
            {'column_name': 'location', 'value': filters['location'].split(',')},
            {'column_name': 'discipline', 'value': filters['discipline'].split(',')},
            {'column_name': 'job_title', 'value': filters['job_title'].split(',')},
            {'column_name': 'employer_name', 'value': filters['employer_name'].split(',')},
            #languages contain the special case of matching C, which shall be matched by C, and ,C
            {'column_name': 'languages', 'value': filters['languages'].split(',')}
        ]

        query = append_other_queries(non_level_filters, query)

    jobs = db.get_search_data(query)

    return jobs


def append_other_queries(other_filters, query):

    for filter in other_filters:

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

    return query




def login(userid, pwd):
        params = {'userid': str(userid), 'pwd': str(pwd) }
        session = requests.Session()
        session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)
        return session

#update jobs, may change each job's Apply and last day to apply values. All jobs either in Approved, Posted, Cancelled, or Application Available
#1. Look in Approved. Maybe dates in approved can change, or posted jobs can go into approved seciont
# Loop through each job on in section and match its ID with my database'. If match change that job in my database
#to have an Apply of "Approved" and jobMine's last date to apply. If the id does not match, insert the job to my database
#2. Look in posted and do same as before. Make sure the Apply section becomes "POSTED"
#3. Look in Cancelled applications. If match is found, change the Apply to CANCEL. If no match, well, add anyways
#4. Everything else must now be in Apps Availalbe
def updateJobs():

    database = db.AllJobs()

    #===============loginv to JobMine
    session = login('l43cheng', 'IAaW132@@@')

    #=================go to Job Inquiry, the get method must exist before using a post
    session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")


    #since after we check Approved, Posted, and Cancelled, then every other job must be in Apps Avail. I will do complementary counting by first
    #setting all to Apps Avail
    database.commit_query("UPDATE AllJobs SET apply = 'APPS AVAIL'")

    print('Finished setting all apply to APPS AVAIL')

    examineJobStatus('APPR', True, database, session)
    print('Finished APPROVED page')

    examineJobStatus('POST', False, database, session)
    print('Finished POST page')

    examineJobStatus('CANC', False, database, session)
    print('Finished CANCELLED page')

    database.close_connection

#we do each jobstatus' updating here. view_all should only be set to true once. We accept the connection, cursor that has already been made
def examineJobStatus(job_status, view_all, database, session):
    #empty the jot title and employer name in case previous operation had been a search
    paramsForSearch = {
    'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
    'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '',
    'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
    'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': str(job_status),
    'UW_CO_JOBSRCH_UW_CO_JOB_TITLE': '',
    'UW_CO_JOBSRCH_UW_CO_EMPLYR_NAME': ''
    }
    s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

    #viewing 100 entries, surrounded in try/except because this *should throw an error if there are less than 25 entries
    try:
        #if view_all has already been pressed, there will always be 100 jobs max to show and we don't want to press it again. Thus, second time this function is called, the caller ensures that view_all is False
        if (view_all):
            paramsForSearch = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_JOBRES_VW$hviewall$0',
                                'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': job_status}
            s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)
        print(' posted to View 100')
    except:
        print("in the except block")

    print("about to traverse pages")

    next_page_exists = True

    while next_page_exists == True:

        bsObj = BeautifulSoup(s._content, "html.parser")
        for i in range(0,100,1):

            #=== We first gather the on-page data, such as the job title and the employer
            # we first check if the row exists. If it is a None object, then we have reached the
            # end of all searches (since every search before the last is valid and has value) and can terminate the while loop
            if (bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}) == None) :
                print('we end this section because the id cannot be found, at position:' + str(i))
                next_page_exists = False
                break
            job_identifier = bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}).get_text()

            print(str(job_identifier))

            #try to match the job_identifier from this job to the one in database

            exist = database.get_query("SELECT COUNT(*)FROM AllJobs WHERE job_identifier = '" + job_identifier + "'").fetchone()

            print('about to check if the job exists')
            #if match, then change apply and last_day_to_apply
            if exist[0] == 1:
                inter = database.get_query("SELECT last_day_to_apply FROM AllJobs WHERE job_identifier = '" + job_identifier + "'")
                #inter= c.execute("SELECT last_day_to_apply FROM AllJobs WHERE job_identifier = '" + job_identifier + "'")
                last_day = inter.fetchone()[0]
                database.commit_query("UPDATE AllJobs SET apply = '" +job_status + "', last_day_to_apply = '" +  last_day + "' WHERE job_identifier = '" + job_identifier + "'" )
                print('Updated:' + job_identifier)

            #if the id doesn't match, aka, doesn't exist, add the job with its details to the database.
            else:
                print('the job does not exist, we will insert it')
                #get details about the job
                new_job = extract_details(bsObj,i,job_status, session)

                database.commit_query("INSERT INTO AllJobs(job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary, apply, last_day_to_apply) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                           (new_job['job_identifier'], new_job['job_title'], new_job['employer_name'], new_job['unit_name'],
                                            new_job['location'], new_job['number_of_openings'], new_job['discipline'], new_job['level'],
                                            new_job['hiring_support'], new_job['work_term_support'], new_job['comments'],
                                            new_job['summary'], new_job['apply'], new_job['last_day_to_apply']))

                '''
                c.execute("INSERT INTO AllJobs(job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary, apply, last_day_to_apply) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                           (new_job['job_identifier'], new_job['job_title'], new_job['employer_name'], new_job['unit_name'],
                                            new_job['location'], new_job['number_of_openings'], new_job['discipline'], new_job['level'],
                                            new_job['hiring_support'], new_job['work_term_support'], new_job['comments'],
                                            new_job['summary'], new_job['apply'], new_job['last_day_to_apply']))
                connection.commit()
                '''
        # going to the next section
        paramsForSearch = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165', 'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '', 'ICAction':'UW_CO_JOBRES_VW$fdown$0',
                            'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': job_status}

        #'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'
        s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

#this function finds all the details associated with a job, eg, job_identifier, employer_name, etc. It uses BeautifulSoup
def extract_details(bsObj,i,job_status, session):

    new_job = []

    job_identifier = bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}).get_text()
    job_title = bsObj.find("a", {"id": "UW_CO_JOBTITLE_HL$" + str(i)} ).get_text()
    employer_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_PARENT_NAME$" + str(i)}).get_text()
    unit_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_EMPLYR_NAME1$" + str(i)}).get_text()
    location = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_WORK_LOCATN$" + str(i)}).get_text()

    #since the opening column are spaces when the job_status is canceled, we automatically set the number_of_openings to 0
    if (job_status == 'CANC'):
        number_of_openings = 0
    else:
        number_of_openings = int(bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_OPENGS$" + str(i)}).get_text())

    #we only examine approved and posted jobs
    apply=''
    if (job_status == 'APPR'):
        apply='APPROVED'
    elif (job_status == 'POST'):
        apply = 'POSTED'
    elif (job_status == 'CANC'):
        apply = 'CANCELLED'
    else:
        apply = 'APPS AVAIL';

    #apply = bsObj.find("span", {"class": "PSHYPERLINKDISABLED"}).get_text()
    last_day_to_apply = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_CHAR_DATE$" + str(i)}).get_text()


    #gather more advanced data about the job
    html = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES_12/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?Page=UW_CO_STU_JOBDTLS&Action=U&UW_CO_JOB_ID=" + job_identifier)

    bsObj_content = BeautifulSoup(html._content, "html.parser")

    discipline = bsObj_content.find("span", {"id" : "UW_CO_JOBDTL_DW_UW_CO_DESCR"}).get_text()
    level = bsObj_content.find("span", {"id": "UW_CO_JOBDTL_DW_UW_CO_DESCR_100"}).get_text()
    hiring_support = bsObj_content.find("span", {"id" : "UW_CO_OD_DV2_UW_CO_NAME"}).get_text()
    work_term_support = bsObj_content.find("span", {"id": "UW_CO_OD_DV2_UW_CO_NAME2"}).get_text()
    comments = bsObj_content.find("span", {"id": "UW_CO_JOBDTL_VW_UW_CO_JOB_SUMMARY"}).get_text()

    #using bsObj_content to find the summary doesn't return a fruitful result. We'll need to manually find the summary.
    summary_start_index = str(html._content).index(r"id=\'UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR\'")
    summary_end_index = str(html._content).index('<!-- UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR -->')
    summary = str(html._content)[summary_start_index + 39: summary_end_index-7]

    summary = summary.replace(r'\r', '')
    summary = summary.replace(r'\t', '')

    print(summary)
    print('=================================================================')
    new_job = {'job_identifier':job_identifier, 'job_title': job_title, 'employer_name': employer_name, 'unit_name': unit_name,
               'location': location, 'number_of_openings': number_of_openings, 'discipline': discipline, 'level': level,
               'hiring_support': hiring_support, 'work_term_support': work_term_support, 'comments': comments, 'summary': summary,
               'apply': apply, 'last_day_to_apply': last_day_to_apply}
    return new_job

