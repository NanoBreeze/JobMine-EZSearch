
var tour;

$(function() {
alert('ehy');
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
    placement: 'top',
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
    placement: 'left',
    content: "In addition to a local database, you can also download formated files containing all jobs."
      },
      {
    path: "/feedback",
    element: "#stepContribute",
    title: "Open source",
    placement: 'left',
    content: "You can help make JobMine EZSearch a more robust system!"
      },
      {
    path: "/",
    element: "#stepLogin",
    title: "This is the end of our tour",
    content: "Type in your user ID and password (will be store in local database) so we can get the jobs for you and use the shortlist feature."
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