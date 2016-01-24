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

from flask import Flask, render_template, request, jsonify
from post import posts
from download import downloads

import logic

app = Flask(__name__)
app.register_blueprint(posts)
app.register_blueprint(downloads)

@app.route('/')
def welcome():
    """The front EZSearch Page. First page users see when they access EZSearch for the first time."""

    with open("ShortListJobs.txt", "w") as myfile:
        myfile.write("This file stores information about the jobs you wanted to short list. \n"
                     "You can use this file as Plan B - manually shortlisting jobs in JobMine - in case there's a bug with EZSearch's Add to and Remove from Shortlist buttons" )
    myfile.close()

    return render_template("Welcome.html")

#shows the Job Inquiry page, where the user can search for jobs
@app.route('/jobInquiry')
def job_inquiry():
    """Displays the Job Inquiry page"""
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


@app.route('/analyticsExport')
def analytics_export():
    """Displays the Analytics and Downloads page"""

    analytics = logic.Analytics()

    return render_template("AnalyticsExport.html",
                           analytics_city_count = analytics.get_city_count(),
                           analytics_languages_count = analytics.get_languages_count(),
                           analytics_faculties_count = analytics.get_faculty_count(),
                           analytics_levels_count = analytics.get_level_count(),
                           analytics_total_numbers_count = analytics.get_numbers(),
                           analytics_job_containing_keywords_count = analytics.get_keywords_count()
                           )

@app.route('/about')
def docs():
    """Displays the documentation page"""
    return render_template("About.html")

@app.route('/feedback')
def feedback():
    """Displays the feedback page"""
    return render_template("Feedback.html")



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)