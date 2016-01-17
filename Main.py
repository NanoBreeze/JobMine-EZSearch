from flask import Flask, render_template, request
import filterJobs

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("Welcome.html")

@app.route('/jobInquiry')
def job_inquiry():
    print("GOOD")
    jobs = filterJobs.give_all_jobs()
    print(jobs)
    print("About to render template")
    return render_template("JobInquiry.html", jobs = jobs)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form['customSearch'])


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)