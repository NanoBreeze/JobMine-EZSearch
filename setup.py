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

import requests
import sqlite3
from bs4 import BeautifulSoup



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



connection=sqlite3.connect("jobs.db")
c = connection.cursor()

session = requests.Session()
params = {'userid': 'l43cheng', 'pwd':'IAaW132@@@'} #timezoneOffset and submit are unnecessary but also submitted

#===============login
s = session.post('https://jobmine.ccol.uwaterloo.ca/psp/ES/?cmd=login&languageCd=ENG&sessionId= ', params)

#=================go to Job Inquiry, the get method must exist before using a post
s = session.get("https://jobmine.ccol.uwaterloo.ca/psc/ES/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&amp;FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&amp;IsFolder=false&amp;IgnoreParamTempl=FolderPath%2cIsFolder&amp;PortalActualURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentURL=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2fEMPLOYEE%2fWORK%2fc%2fUW_CO_STUDENTS.UW_CO_JOBSRCH.GBL%3fpslnkid%3dUW_CO_JOBSRCH_LINK&amp;PortalContentProvider=WORK&amp;PortalCRefLabel=Job%20Inquiry&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsp%2fES%2f&amp;PortalURI=https%3a%2f%2fjobmine.ccol.uwaterloo.ca%2fpsc%2fES%2f&amp;PortalHostNode=WORK&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes")

getJobs('APPR', True)
getJobs('POST', False)
getJobs('APPA', False)
getJobs('CANC', False)