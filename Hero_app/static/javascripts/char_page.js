document.addEventListener('DOMContentLoaded', function () {
    const AllDataButton = document.getElementById('all_data_button');
    const AllData = document.getElementById('all_data');

    const MonthDataButton = document.getElementById('month_summary_button');
    const MonthSummary = document.getElementById('month_summary');

    const WeekDataButton = document.getElementById('week_summary_button');
    const WeekSummary = document.getElementById('week_summary');


    AllDataButton.addEventListener('click', function () {
        if (AllData.style.display === 'block') {
            AllData.style.display = 'none';
        } else {
            AllData.style.display = 'block'
        }
    })


    MonthDataButton.addEventListener('click', function () {
        if (MonthSummary.style.display === 'block') {
            MonthSummary.style.display = 'none';
        } else {
            MonthSummary.style.display = 'block'
        }
    })


    WeekDataButton.addEventListener('click', function () {
        if (WeekSummary.style.display === 'block') {
            WeekSummary.style.display = 'none';
        } else {
            WeekSummary.style.display = 'block'
        }
    })

});