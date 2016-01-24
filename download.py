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

from flask import Blueprint, render_template, jsonify
import logic


downloads = Blueprint('downloads', __name__)

@downloads.route('/exportHtml/<int:offset>')
def export_html(offset):
    """Displays a HTML page containing 1000 jobs. Offset determines which 1000"""

    jobs = helper_download('HTML',offset)
    return render_template("ExportHTML.html", jobs = jobs)



@downloads.route('/exportCsv')
def export_csv():
    """Makes a CSV file containing all information about each job."""

    message = helper_download('CSV')
    return jsonify( followup = message)




@downloads.route('/exportTxt')
def export_txt():
    """Makes a TXT file containing all information about each job."""

    message = helper_download('TXT')
    return jsonify( followup = message)



@downloads.route('/exportJson')
def export_json():
    """Creates a JSON file containing all information about each job."""

    message = helper_download('JSON')
    return jsonify( followup = message)



def helper_download(format, offset=0):
    """Since almost each download uses same code, this method reduces redundancy. If format is HTML, returns the data
    If the format is CSV, TXT, or JSON, returns the display message"""

    download = logic.Download()

    if format == 'HTML':
        return download.make_format(format, offset)

    if download.make_format(format):
        return format + ' file was successfully created!'
    else:
        return 'There was an error creating the ' + format + ' file. If it is already open, try closing and downloading it again'

