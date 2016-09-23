# JobMine-EZSearch

JobMine EZSearch is a productivity application was conceived from the belief that there are more efficient ways to search through JobMine jobs than clicking on each one.

Imagine that you wanted to apply to all jobs that required C++ skills. How would you search for these jobs using JobMine's current search system? One way is to click on every job to read if its summary contains "C++" but that would be very time consuming. If only there were some way of automating this process. And there is! Welcome to EZSearch. Simply type in C++ in the search bar and all jobs that require C++ will appear.

## Core Features:
- **Refined Search Mechanism:** In addition to almost all of JobMine’s search filters, JobMine EZSearch can also search by keywords, prioritized languages, or you can write your own SQL queries.
- **Integrates with Short List:** Add or remove jobs from your shortlist with a single click. A text file is also created showing all jobs you have added to shortlist.
- **Download Formats:** Download all jobs in four file formats: Word, HTML, CSV, and TXT
- **Open to Extension:** Stores jobs from JobMine to a local database so that you can use the data to build your own applications.
- **Fast and Functional:** Once JobMine EZSearch has finished setting up the local database with all jobs, you can instantaneously* search through 3000+ jobs and view jobs without waiting for page loads
- **GUI:** A rich responsive display powered by Bootstrap.
- **GNU GPL3 License:** Play with the source code however you wish.

## Installation
Yes I know, it looks like there are a quadrillion steps but don’t worry, they’re easier than they seem and generally takes less than 15 minutes (including waiting for file to install). 

1. Since JobMine EZSearch is a Python project, let’s download Python 3.5.2 from https://www.python.org/downloads/. On the first wizard path check the “Add Python 3.5 to PATH” checkbox and install Python.
2. After Python 3.5.2 has been installed, download the PyCharm Community IDE from https://www.jetbrains.com/pycharm/download/#section=windows.
3. Open PyCharm and click on “Check out from Version Control” and select “Git”. In the new popup, enter https://github.com/NanoBreeze/JobMine-EZSearch.git into Git Repository URL.
4. This part is a bit tricky. Open your browser to http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml and download the file lxml-3.6.4-cp35-cp35m-win32.whl. This file is needed to create Word documents of jobs. 
5. Open your Command Prompt as Administrator (if you’re on an administrator account, it automatically opens in Administrator mode) and navigate to the directory that contains lxml-3.6.4-cp35-cp35m-win32.whl is installed. Type cd.. to go up a folder and cd <folder name> to go to a child folder.
6. Type into Command Prompt *pip install lxml-3.6.4-cp35-cp35m-win32.whl*
7. Run preSetup.py from Pycharm’s Project window (on the left side of the screen) and remember to enter your username and password in the run console. These are stored in a local database and aren’t being snooped by mastermind. Your entered credentials stay only on your drive
8. After a job is downloaded, its summary will appear in the Run panel. It normally takes 5-15 mins to download all the jobs. After the jobs are downloaded double click on Main.py (or use python Main.py from the Command Prompt). Then run Main.py (click on Run->Run…->Main). If Main.py threw an “Error running Main:” exception, you can set the Interpreter by Run->Edit Configurations… and select Python 3.5.2.
9. Click the blue link that appears in the Run window (eg, http://127.0.0.1:5000). This opens JobMine EZSearch. Any time you want to open JobMine EZSearch, run Main.py. You can navigate to “Job Inquiry & Shortlist” to search and shortlist jobs. 

Hope this helps! If you run into any troubles, please don't hesitate to contact me at l43cheng@uwaterloo.ca.

