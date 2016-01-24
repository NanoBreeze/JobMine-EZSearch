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

from flask import Blueprint, Flask, render_template, request, jsonify

import logic


posts = Blueprint('posts', __name__)

@posts.route('/submit', methods=['POST'])
def submit():
    """Submits user's query to the database and returns with appropriate results"""

    #do not add request.form['junior'] or other levels here. Will cause 500 errors
    filters = {'sql_query': request.form['sql_query'],
                    'job_identifier': str(request.form['job_identifier']),
                    'summary': request.form['summary'],
                    'location' : request.form['location'],
                    'discipline' : request.form['discipline'],
                    'job_title': request.form['job_title'],
                    'employer_name' : request.form['employer_name'],
                    'languages' : request.form['languages'],
                    }
    print('going into intialize_level_filters(filters)')

    try:
        if request.form['junior']:
            filters['junior'] = 'junior'
    except:
        filters['junior'] = 'impossible'
    print('set junior, which is now' + filters['junior'])

    try:
        if request.form['intermediate']:
            filters['intermediate'] = 'intermediate'
    except:
        filters['intermediate'] = 'impossible'
    print('set intermediate, which is now' + filters['intermediate'])

    try:
        if request.form['senior']:
            filters['senior'] = 'senior'
    except:
        filters['senior'] = 'impossible'
    print('set senior, which is now' + filters['senior'])


    jobs = logic.submit(filters)

    return render_template("JobInquiry.html", jobs = jobs, filter_words = filters)



@posts.route('/update_languages', methods=['POST'])
def update_languages():
    """Updates user's prioritization of languages and shows the updated languages in the languages column"""

    prioritized_languages = request.json['prioritized_languages']

    prioritized_languages = logic.cleanLanguages(prioritized_languages)
    logic.updateLanguages(prioritized_languages)

    return jsonify(a = 'nothing')


@posts.route('/removeFromShortList', methods=['POST'])
def remove_from_short_list():
    """Removes selected job from the short list"""

    job_identifier = request.json['job_identifier']

    shortlist = logic.Shortlist()
    session = shortlist.login('l43cheng', 'IAaW132@@@')
    shortlist.remove_from_shortlist(job_identifier, session)

    return jsonify (a = 'nothing')

@posts.route('/addToShortList', methods=['POST'])
def add_to_short_list():

    job_title = request.json['job_title']
    employer_name = request.json['employer_name']
    job_identifier = request.json['job_identifier']

    shortlist = logic.Shortlist()
    session = shortlist.login('l43cheng', 'IAaW132@@@')
    is_successful = shortlist.add_to_shortlist(employer_name, job_title, job_identifier, session)

    if is_successful:
        return jsonify(a = "Found!")
    else:
        return jsonify(a = "Not found")



@posts.route('/update_jobs')
def update_jobs():
    logic.updateJobs()
    return jsonify(a = 'nothing')



