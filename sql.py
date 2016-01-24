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

with sqlite3.connect("jobs.db") as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE AllJobs(job_identifier TEXT, job_title TEXT, employer_name TEXT, unit_name TEXT, location TEXT, number_of_openings INTEGER"
              "discipline TEXT, level TEXT, discipline TEXT, hiring_support TEXT, work_term_support TEXT, comments TEXT, summary TEXT"
              "languages TEXT, in_short_list TEXT )")
