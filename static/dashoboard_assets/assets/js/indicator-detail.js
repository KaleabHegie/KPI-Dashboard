function fetchData(tableContainer) {   
    // AJAX request to fetch data
    $.ajax({
        url: `indicator-details/2226/`, // Endpoint URL
        type: "GET",
        beforeSend: function () {
            showLoadingSpinnerDetail('spinnerLoading')
            $('#yearSelect').hide()
            $('#yearMonthSelect').hide();

          },
          complete: function () {
            hideLoadingSpinnerDetail('spinnerLoading')
          },
        success: function (data) {
            document.getElementById('analytics-tab-1').innerHTML = data.kpi_name_eng;

            // Extract the years from the annual plans data
            var years = data.annual_plans.map(function (plan) {
                return plan.year;
            });

            // Find the maximum year
            var maxYear = Math.max(...years);

            // Determine the three most recent years
            var recentYears = [];
            for (var i = 0; i < 3; i++) {
                recentYears.push(maxYear - i);
            }

            // Filter the annual plans data for the recent three years
            var recentAnnualPlans = data.annual_plans.filter(function (plan) {
                return recentYears.includes(plan.year);
            });

            // Check if data is available
            if (recentAnnualPlans && recentAnnualPlans.length > 0) {
                // Populate the table with recent annual plans data
                drawTable(recentAnnualPlans, tableContainer);

                // Draw the chart
                drawChart(recentAnnualPlans);
            } else {
                console.error("No recent annual plans data available for the indicator.");
            }

            // Draw the quarter table with recent quarter progress data
            if (data && data.quarter_progress && data.quarter_progress.length > 0) {
                $('#yearSelect').show()
                
                // Extract the years from the quarter progress data
                var years = data.quarter_progress.map(function (quarter) {
                    return quarter.year;
                });

                // Find the maximum year
                var maxYear = Math.max(...years);

                // Determine the three most recent years
                var recentYears = [];
                for (var i = 0; i < 2; i++) {
                    recentYears.push(maxYear - i);
                }

                // Filter the quarter progress data for the recent three years
                var recentQuarterProgress = data.quarter_progress.filter(function (quarter) {
                    return recentYears.includes(quarter.year);
                });

                // Draw the quarter table with recent quarter progress data
                drawQuarterTable(recentQuarterProgress, document.getElementById('Quarter-detail-table'));

                // Populate the dropdown initially
                populateDropdown(recentQuarterProgress);
            } else {
                $('#yearSelect').hide()
                console.error("No quarterly progress data available for the indicator.");
            }

            // Draw the month table with recent month progress data
            if (data && data.month_progress && data.month_progress.length > 0) {
                $('#yearMonthSelect').show();
                // Extract the years from the month progress data
                var years = data.month_progress.map(function (month) {
                    return month.year;
                });

                // Find the maximum year
                var maxYear = Math.max(...years);

                // Determine the two most recent years
                var recentYears = [];
                for (var i = 0; i < 2; i++) {
                    recentYears.push(maxYear - i);
                }

                // Filter the month progress data for the recent two years
                var recentMonthProgress = data.month_progress.filter(function (month) {
                    return recentYears.includes(month.year);
                });

                // Draw the month table with recent month progress data
                drawMonthTable(recentMonthProgress, document.getElementById('Month-detail-table'));

                // Call the function to populate the select dropdown with initial data
                populateYearMonthSelect(data);
            } else {
                $('#yearMonthSelect').hide();
                console.error("No recent monthly progress data available for the indicator.");
            }

            // Add event listener to dropdown after populating options
            document.getElementById('yearSelect').addEventListener('change', function() {
                updateChart(recentQuarterProgress); // Call the updateChart function with the selected year
            });

            // Event handler for the select element
            document.getElementById('yearMonthSelect').addEventListener('change', function() {
                var selectedYear = parseInt(this.value); // Extract the selected year from the value
                updateMonthlyChart(selectedYear, data); // Call updateMonthlyChart with the selected year and data
            });


        },
        error: function () {
            console.error("Error fetching data");
        }
    });
}
// Function to draw the table
function drawTable(data, tableContainer) {
    document.getElementById("Year-table").innerHTML = "Year Table";

    // Create table element
    var table = document.createElement('table');
    table.classList.add('table', 'table-responsive', 'table-sm');

    // Create table head
    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width: 5%;">No</th><th style="width: 7%;">Year</th><th style="width: 10%;">Annual Target</th><th style="width: 10%;">Annual Performance</th><th style="width: 25%;">Target State</th>';
    thead.appendChild(tr);
    table.appendChild(thead);

    // Create table body
    var tbody = document.createElement('tbody');
    data.forEach(function (item, index) {
        var tr = document.createElement('tr');
        var targetState = item.target_state === 'cum' ? 'Cumulative' : item.target_state;
        tr.innerHTML = '<td>' + (index + 1) + '</td><td>' + item.year + '</td><td>' + item.annual_target + '</td><td>' + item.annual_performance + '</td><td>' + targetState + '</td>';
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    // Append table to tableContainer
    tableContainer.innerHTML = '';
    tableContainer.appendChild(table);
}

let showLoadingSpinnerDetail = (div) => {
    $(`#${div}`).html(
      `
      <div class="text-center">
    <div class="spinner-grow text-success" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
      `
    )
  }
let hideLoadingSpinnerDetail = (div) =>{
    $(`#${div}`).html('')
}

// Function to draw the chart
function drawChart(data) {
    Highcharts.chart('bar', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Annual Performance and Targets Comparsion ',
            align: 'left'
        },
        xAxis: {
            categories: data.map(plan => plan.year),
            crosshair: true,
            title: {
                text: 'Year'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Value'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ''
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: 'Annual Target',
                data: data.map(plan => plan.annual_target)
            },
            {
                name: 'Annual Performance',
                data: data.map(plan => plan.annual_performance)
            }
        ]
    });

   
}

// Function to draw the quarter table with modified quarter names
function drawQuarterTable(quarterData, tableContainer) {
    document.getElementById("Quarter-table").innerHTML="Quarter Table"
    var table = document.createElement('table');
    table.classList.add('table', 'table-responsive', 'table-sm');

    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    tr.innerHTML = '<th>No</th><th>Year</th><th>Quarter</th><th>Quarterly Target</th><th>Quarterly Performance</th>';
    thead.appendChild(tr);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');
    var rowCount = 0;

    var yearsSet = new Set();
    quarterData.forEach(function (quarter) {
        yearsSet.add(quarter.year);
    });

    yearsSet.forEach(function (year) {
        var quartersForYear = quarterData.filter(function (quarter) {
            return quarter.year === year;
        });

        quartersForYear.forEach(function (quarter, index) {
            var trQuarter = document.createElement('tr');
            
            if (index === 0) {
                // First row for this year, create the year cell with rowspan
                trQuarter.innerHTML = '<td rowspan="' + quartersForYear.length + '">' + (++rowCount) + '</td><td rowspan="' + quartersForYear.length + '" style=" vertical-align: middle;">' + year + '</td><td>' + getQuarterName(quarter.quarter) + '</td><td>' + quarter.quarter_target + '</td><td>' + quarter.quarter_performance + '</td>';
                tbody.appendChild(trQuarter);
            } else {
                // Subsequent rows for the same year, append cells without rowspan
                var tdQuarter = document.createElement('td');
                tdQuarter.textContent = getQuarterName(quarter.quarter);
                trQuarter.appendChild(tdQuarter);
                
                var tdTarget = document.createElement('td');
                tdTarget.textContent = quarter.quarter_target;
                trQuarter.appendChild(tdTarget);
                
                var tdPerformance = document.createElement('td');
                tdPerformance.textContent = quarter.quarter_performance;
                trQuarter.appendChild(tdPerformance);
                
                tbody.appendChild(trQuarter);
            }
        });
    });

    table.appendChild(tbody);
    tableContainer.innerHTML = '';
    tableContainer.appendChild(table);
}

// Function to draw the month table
function drawMonthTable(monthData, tableContainer) {
    document.getElementById("Month-table").innerHTML= "Month Table"
    var table = document.createElement('table');
    table.classList.add('table', 'table-responsive', 'table-sm');

    var thead = document.createElement('thead');
    var tr = document.createElement('tr');
    tr.innerHTML = '<th>No</th><th>Year</th><th>Month</th><th>Monthly Target</th><th>Monthly Performance</th>';
    thead.appendChild(tr);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');
    var rowCount = 0;

    var yearsSet = new Set();
    monthData.forEach(function (month) {
        yearsSet.add(month.year);
    });

    yearsSet.forEach(function (year) {
        var monthsForYear = monthData.filter(function (month) {
            return month.year === year;
        });

        monthsForYear.forEach(function (month, index) {
            var trMonth = document.createElement('tr');
            
            if (index === 0) {
                // First row for this year, create the year cell with rowspan
                trMonth.innerHTML = '<td rowspan="' + monthsForYear.length + '">' + (++rowCount) + '</td><td rowspan="' + monthsForYear.length + '" style=" vertical-align: middle;">' + year + '</td><td>' + month.month + '</td><td>' + month.monthly_target + '</td><td>' + month.month_performance + '</td>';
                tbody.appendChild(trMonth);
            } else {
                // Subsequent rows for the same year, append cells without rowspan
                var tdMonth = document.createElement('td');
                tdMonth.textContent = month.month;
                trMonth.appendChild(tdMonth);
                
                var tdTarget = document.createElement('td');
                tdTarget.textContent = month.monthly_target;
                trMonth.appendChild(tdTarget);
                
                var tdPerformance = document.createElement('td');
                tdPerformance.textContent = month.month_performance;
                trMonth.appendChild(tdPerformance);
                
                tbody.appendChild(trMonth);
            }
        });
    });

    table.appendChild(tbody);
    tableContainer.innerHTML = '';
    tableContainer.appendChild(table);
}

// Function to get the quarter name based on its position
function getQuarterName(quarter) {
    switch (quarter) {
        case "1st Quarter":
            return "3 Month";
        case "2nd Quarter":
            return "6 Month";
        case "3rd Quarter":
            return "9 Month";
        case "4th Quarter":
            return "Annual";
        default:
            return quarter;
    }
}
// Call fetchData function to fetch and draw the table
fetchData(document.getElementById('Year-detail-table'));

function populateDropdown(data) {
    var select = document.getElementById('yearSelect');
    var years = [];
    data.forEach(function(progress) {
        if (!years.includes(progress.year)) {
            years.push(progress.year);
            var option = document.createElement('option');
            option.value = progress.year;
            option.textContent = progress.year;
            select.appendChild(option);
        }
    });


    // Trigger the change event with the first year selected
    if (select.options.length > 0) {
        var firstYear = select.options[0].value;
        select.value = firstYear;
        updateChart(data); // Call updateChart function with the first year selected
    }
}

function updateChart(data) {
    console.log("called");
    var selectedYear = document.getElementById('yearSelect').value;
    var selectedQuarterData = data.filter(function(progress) {
        return progress.year == selectedYear;
    });
    if (selectedQuarterData.length > 0) {
        var categories = selectedQuarterData.map(function(progress) {
            return progress.quarter;
        });
        var targetData = selectedQuarterData.map(function(progress) {
            return progress.quarter_target;
        });
        var performanceData = selectedQuarterData.map(function(progress) {
            return progress.quarter_performance;
        });
        var chart = Highcharts.chart('QuarterBar', {
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Quarter Performance and Targets Comparsion ',
                align: 'left'
            },
            xAxis: {
                categories: categories,
                title: {
                    text: null
                },
                gridLineWidth: 1,
                lineWidth: 0
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Percent',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                },
                gridLineWidth: 0
            },
            tooltip: {
                valueSuffix: ' %',
                formatter: function() {
                    var tooltip = '<b>' + this.x + '</b><br/>'; // Quarter
                    tooltip += 'Year: <b>' + selectedYear + '</b><br/>'; // Year
                    tooltip += this.series.name + ': <b>' + this.y + '%</b>'; // Data point
                    return tooltip;
                }
            },
            plotOptions: {
                bar: {
                    borderRadius: '50%',
                    dataLabels: {
                        enabled: true
                    },
                    groupPadding: 0.1
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -40,
                y: 80,
                floating: true,
                borderWidth: 1,
                backgroundColor: Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
                shadow: true
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Quarterly Target',
                data: targetData
            }, {
                name: 'Quarterly Performance',
                data: performanceData
            }]
        });
    }
}

// Function to create the Highcharts line chart for monthly data
function createMonthlyChart(data) {
    Highcharts.chart('area', {
        chart: {
            type: 'line' // Change chart type to line for monthly data
        },
        title: {
            text: 'Month Performance and Targets Comparsion ',
        },
        xAxis: {
            categories: data.map(month => month.month), // Update x-axis categories to represent months
            title: {
                text: 'Month'
            }
        },
        yAxis: {
            title: {
                text: 'Values'
            }
        },
        tooltip: {
            pointFormat: '{series.name} had a value of <b>{point.y:,.0f}</b> in {point.x}'
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: true,
                    symbol: 'circle',
                    radius: 3
                },
                color: 'green' // Set the color for the line
            }
        },
        series: [{
            name: 'Monthly Target',
            data: data.map(month => month.monthly_target),
            color: 'blue' // Set the color for the area of this series
        }, {
            name: 'Monthly Performance',
            data: data.map(month => month.month_performance),
            color: 'red' // Set the color for the area of this series
        }]
    });
}

// Function to populate the select dropdown with unique years
function populateYearMonthSelect(data) {
    var select = document.getElementById('yearMonthSelect');
    var years = [];
    data.month_progress.forEach(month => {
        if (!years.includes(month.year)) {
            years.push(month.year);
            var option = document.createElement('option');
            option.value = month.year;
            option.textContent = month.year;
            select.appendChild(option);
        }
    });
    // Trigger the change event with the first year selected
    if (select.options.length > 0) {
        var firstYear = select.options[0].value;
        select.value = firstYear;
        updateMonthlyChart(firstYear, data); // Call updateMonthlyChart function with the first year selected
    }
}

// Function to update the Highcharts area chart with selected year's month data
function updateMonthlyChart(selectedYear, data) {

    var selectedYearData = data.month_progress.filter(month => Number(month.year) === Number(selectedYear));
    if (selectedYearData.length > 0) {
        createMonthlyChart(selectedYearData);
    } else {
        console.error("No data available for the selected year.");
    }
}










