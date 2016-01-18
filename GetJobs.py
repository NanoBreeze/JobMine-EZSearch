import requests
from bs4 import BeautifulSoup

import re

import sqlite3

connection=sqlite3.connect("jobs.db")

c = connection.cursor()



session = requests.Session()
params = {'userid': 'l43cheng', 'pwd':'IAaW132@'} #timezoneOffset and submit are unnecessary but also submitted

#===============login
s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)

#=================go to Job Inquiry, the get method must exist before using a post
s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")

#==================get first page of all jobs
paramsForSearch = {
    'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165',
    'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '',
    'ICAction':'UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN',
    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=',
    'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'
 }

s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

#viewing 100 entries
paramsForSearch = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165','ICAction':'UW_CO_JOBRES_VW$hviewall$0',
                    'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', 'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'}

s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)


print("finished")
applications = []

next_page_exists = True

while next_page_exists == True:

    bsObj = BeautifulSoup(s._content, "html.parser")

    #gather data from each job on the page
    for i in range(0,100,1):

        #=== We first gather the on-page data, such as the job title and the employer
        # we first check if the row exists. If it is a None object, then we have reached the
        # end of all searches (since every search before the last is valid and has value) and can terminate the while loop
        if (bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}) == None) :
            next_page_exists = False
            break;
        job_identifier = bsObj.find("span", {"id" : "UW_CO_JOBRES_VW_UW_CO_JOB_ID$" + str(i)}).get_text()
        job_title = bsObj.find("a", {"id": "UW_CO_JOBTITLE_HL$" + str(i)} ).get_text()
        employer_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_PARENT_NAME$" + str(i)}).get_text()
        unit_name = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_EMPLYR_NAME1$" + str(i)}).get_text()
        location = bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_WORK_LOCATN$" + str(i)}).get_text()
        number_of_openings = int(bsObj.find("span", {"id": "UW_CO_JOBRES_VW_UW_CO_OPENGS$" + str(i)}).get_text())

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
        c.execute("INSERT INTO AllJobs(job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                                       (job_identifier, job_title, employer_name, unit_name, location, number_of_openings, discipline, level, hiring_support, work_term_support, comments, summary,))
        connection.commit()


        print("================================================================================================")

    # going to the next section
    paramsForSearch = { 'UW_CO_JOBSRCH_UW_CO_WT_SESSION':'1165', 'UW_CO_JOBSRCH_UW_CO_ADV_DISCP1' : '', 'ICAction':'UW_CO_JOBRES_VW$fdown$0',
                        'ICSID':'HCQMdvPKP9qJwk2PhhqrkjaIevBaXGrrkxYfuBnMw9k=', }

#'UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS': 'POST'
    s = session.post("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL", paramsForSearch)

connection.close()

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