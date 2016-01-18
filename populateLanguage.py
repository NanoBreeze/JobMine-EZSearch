import sqlite3
import re

#def populate(languages):
connection=sqlite3.connect("jobs.db")
# c = connection.cursor()
cur = connection.execute('SELECT job_identifier, summary FROM AllJobs')

languages = [' C ', 'C++', 'Java', 'C#', 'SQL', 'JavaScript', 'Linux']

#for each row, or job, we find the first four languages that are found. Match by incrementing counters
for row in cur.fetchall():

    #stores the languages that are found in the job
    included_languages = []

    #keeps track of the number of desired languages that are in the job's summary. If equals four, stop adding the language to included_languages
    number_of_languages_found = 0

    for language in languages:
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
            regex = re.compile('Java[^(s|S)]')
        else:
            regex = re.compile(re.escape(language))
        if regex.search(str(row[1])):
            included_languages.append(language)
            number_of_languages_found = number_of_languages_found + 1


    string_of_included_languages = ",".join(included_languages)
    print(string_of_included_languages)
    #now that we finished finding the languages included in the application, we update the language column to have those included languages
    cur.execute("UPDATE AllJobs SET languages = '" + string_of_included_languages + "' WHERE job_identifier = '" + row[0] + "'")
    connection.commit()

connection.close()