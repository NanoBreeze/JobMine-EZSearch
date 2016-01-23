import requests
from bs4 import BeautifulSoup
import sqlite3
import populateLanguage

#update jobs, may change each job's Apply and last day to apply values. All jobs either in Approved, Posted, Cancelled, or Application Available
#1. Look in Approved. Maybe dates in approved can change, or posted jobs can go into approved seciont
# Loop through each job on in section and match its ID with my database'. If match change that job in my database
#to have an Apply of "Approved" and jobMine's last date to apply. If the id does not match, insert the job to my database
#2. Look in posted and do same as before. Make sure the Apply section becomes "POSTED"
#3. Look in Cancelled applications. If match is found, change the Apply to CANCEL. If no match, well, add anyways
#4. Everything else must now be in Apps Availalbe
def updateJobs():

    connection=sqlite3.connect("jobs.db")
    c = connection.cursor()


    session = requests.Session()
    params = {'userid': 'l43cheng', 'pwd':'IAaW132!'} #timezoneOffset and submit are unnecessary but also submitted

    #===============login
    s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)

    #=================go to Job Inquiry, the get method must exist before using a post
    s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")
    #since after we check Approved, Posted, and Cancelled, then every other job must be in Apps Avail. I will do complementary counting by first
    #setting all to Apps Avail


    c.execute("UPDATE AllJobs SET apply = 'APPS AVAIL'" )
    connection.commit()
    print('Finished setting all apply to APPS AVAIL')

    examineJobStatus('APPR', True, connection, c, session)
    print('Finished APPROVED page')

    examineJobStatus('POST', False, connection, c, session)
    print('Finished POST page')

    examineJobStatus('CANC', False, connection, c, session)
    print('Finished CANCELLED page')


    connection.close()


#we do each jobstatus' updating here. view_all should only be set to true once. We accept the connection, cursor that has already been made
def examineJobStatus(job_status, view_all, connection, c, session):
    paramsForSearch = {
    'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
    'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '',
    'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
    'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': str(job_status)
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
            returned = c.execute("SELECT COUNT(*)FROM AllJobs WHERE job_identifier = '" + job_identifier + "'")
            exist = returned.fetchone()

            print('about to check if the job exists')
            #if match, then change apply and last_day_to_apply
            if exist[0] == 1:
                inter= c.execute("SELECT last_day_to_apply FROM AllJobs WHERE job_identifier = '" + job_identifier + "'")
                last_day = inter.fetchone()[0]
                c.execute("UPDATE AllJobs SET apply = '" +job_status + "', last_day_to_apply = '" +  last_day + "' WHERE job_identifier = '" + job_identifier + "'" )
                connection.commit()
                print('Updated:' + job_identifier)
            #if the id doesn't match, aka, doesn't exist, add the job with its details to the database.
            else:
                print('the job does not exist, we will insert it')
                #get details about the job
                new_job = extract_details(bsObj,i,job_status, session)

                c.execute("INSERT INTO AllJobs(job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary, apply, last_day_to_apply) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                           (new_job['job_identifier'], new_job['job_title'], new_job['employer_name'], new_job['unit_name'],
                                            new_job['location'], new_job['number_of_openings'], new_job['discipline'], new_job['level'],
                                            new_job['hiring_support'], new_job['work_term_support'], new_job['comments'],
                                            new_job['summary'], new_job['apply'], new_job['last_day_to_apply']))
                print('inserted job')
                connection.commit()
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



#get all job at the start of the program
def getJobs(job_status,view_all):

    #==================get first page of all jobs for the given job_status
    paramsForSearch = {
    'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
    'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '',
    'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
    'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': job_status
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

    print("finished")

    next_page_exists = True

    while next_page_exists == True:

        bsObj = BeautifulSoup(s._content, "html.parser")

        #gather data from each job on the page
        for i in range(0,100,1):

            #=== We first gather the on-page data, such as the job title and the employer
            # we first check if the row exists. If it is a None object, then we have reached the
            # end of all searches (since every search before the last is valid and has value) and can terminate the while loop
            if (bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}) == None) :
                print(i)
                next_page_exists = False
                break
            job_identifier = bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}).get_text()
            job_title = bsObj.find("a", {"id": "UW_CO_JOBTITLE_HL$" + str(i)} ).get_text()
            employer_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_PARENT_NAME$" + str(i)}).get_text()
            unit_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_EMPLYR_NAME1$" + str(i)}).get_text()
            location = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_WORK_LOCATN$" + str(i)}).get_text()
            number_of_openings = int(bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_OPENGS$" + str(i)}).get_text())

            #we only examine approved and posted jobs
            apply=''
            if (job_status == 'APPR'):
                apply='APPROVED'
            else:
                apply = 'POSTED'

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
            '''
            summary = summary.replace('&nbsp;','')

            #change upsidedown question mark with a single quote
            summary = summary.replace('caf\xc3\xa9', '\'')

            #convert the code for a single quote in HTML into a readable single quote
            summary = summary.replace('&#039;', '\'')

            #convert &amp; to &
            summary = summary.replace('&amp;', '&')

            #convert &quot; into "
            summary = summary.replace('&quot;', '"')

            #convert  \xc2\xbf to - (this came from bad encoding)
            summary = summary.replace('\xc2\xbf', '-')

            #maintain line breaks
            summary = summary.replace(r'<br />', '\n')
            '''
            print(summary)
            c.execute("INSERT INTO AllJobs(job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary, apply, last_day_to_apply, in_short_list) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                           (job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary, apply, last_day_to_apply, 'N'))
            connection.commit()


            print("================================================================================================")

        # going to the next section
        paramsForSearch = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165', 'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '', 'ICAction':'UW_CO_JOBRES_VW$fdown$0',
                            'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': job_status}

        #'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'
        s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)






























#here because we commented out its original
session = requests.Session()

'''
connection=sqlite3.connect("jobs.db")

c = connection.cursor()



session = requests.Session()
params = {'userid': 'l43cheng', 'pwd':'IAaW132@'} #timezoneOffset and submit are unnecessary but also submitted

#===============login
s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)

#=================go to Job Inquiry, the get method must exist before using a post
s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")

getJobs('APPR', True)
getJobs('POST', False)

connection.close()

#now that job's core info are in table, let's populate their languages with these preset ones.
populateLanguage.populate(['C', 'C++', 'Arduino', '.NET', 'C#', 'Javascript', 'Java', 'Ruby', 'HTML', 'Python', 'Rails', 'iOS', 'Android', 'MATLAB', 'Unreal', 'Unix', 'Linux', 'SQL', 'ASP'])

'''
'''
#add the 9th job to the short list

paramsForShortList = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_SLIST_HL$9',
                    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'}

m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForShortList)
'''

#go to the Job Short List page. This get might be necessary in order to do a POST

#s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL?pslnkid=UW_CO_JOB_SLIST_LINK&FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOB_SLIST_LINK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")

'''
#delete the first job on the shortlist
paramsForDeleteShortListJob = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_STUJOBLST$delete$0$$0',
                    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k='}

m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL", paramsForDeleteShortListJob)

paramsForSave = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'#ICSave',
                    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k='}

m = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOB_SLIST.GBL ", paramsForSave)
'''