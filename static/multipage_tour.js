/*This file is part of JobMine EZSearch.

JobMine EZSearch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

JobMine EZSearch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with JobMine EZSearch.  If not, see <http://www.gnu.org/licenses/>.*/

var tour;

$(function() {
  // Instance the tour
tour = new Tour({
  steps: [
  {
    path: "/",
    element: "#stepOneWhy",
    title: "Stength of the VIth",
    content: "JobMine EZSearch has six distinct advantages over JobMine's search system to help you find relevant jobs quicker"
  },
  {
    path: "/jobInquiry",
    element: "#summary",
    title: " Search by keywords",
    content: "Search by specific words in jobs' summary. eg, Searching for 'game' will return a list of jobs that contains 'game', which means that many of them would be gaming companies." +
     " Please be aware that there can be false positives. We are working on improving the accuracy of the search engine."
  },
  {
    path: "/jobInquiry",
    element: "#location",
    title: "Separate multiple values by commas",
    content: "To find all jobs located in Toronto OR China, separate the two countries with a comma." +
    " This applies to every other textbox except for the SQL Search textbox." +
    " Let's check out what it is..."
  },
   {
    path: "/jobInquiry",
    element: "#sql_query",
    title: "Write your own SQL queries",
    content: "Apply additional search parameters by writing your own SQL queries. The table containing jobs has 15 columns." +
    " You can view these columns by clicking on the ! button. You can also learn how to write SQL queries from the Docs page located on the right of the menu."
  },
{
    path: "/jobInquiry",
    element: "#stepFourLanguages",
    title: "Prioritize your languages",
    placement: 'bottom',
    content: "Displays up to 4 languages, in the order that you prioritized them in."
      },
      {
    path: "/jobInquiry",
    element: "#stepFiveShortList",
    title: "Add to/Remove from shortlist",
    content: "JobMine EZSearch connects to JobMine so you can quickly add or remove jobs from your shortlist."
      },
      {
    path: "/analyticsExport",
    element: "#stepDownloads",
    title: "Download all jobs",
    placement: 'top',
    content: "In addition to a local database, you can also download formated files containing all jobs."
      },
      {
    path: "/feedback",
    element: "#stepContribute",
    title: "Open source",
    placement: 'bottom',
    content: "You can help make JobMine EZSearch a more robust system!"
      },
      {
    path: "/",
    element: "#stepJobs",
    title: "This is the end of our tour",
    content: "We hope JobMine EZSearch can assist you in this term's co-op search"
      }
],

onEnd: function(t) {
   window.localStorage.clear();}
});

  tour.init();

});

function startTour() {
 // init tour
  tour.restart();
}