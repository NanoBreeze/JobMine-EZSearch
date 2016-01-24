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

