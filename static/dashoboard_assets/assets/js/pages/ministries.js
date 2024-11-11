$(document).ready(() => {

  const preLoading = (divId, size, width)=>{
    let spinner = `
    <div class="col-md-3 col-xl-${width} ">
        <div class="card social-widget-card">
            <div class="card-body d-flex justify-content-between align-items-center p-2">
                <div class="bg-body  d-flex flex-column justify-content-center align-items-center text-primary m-3 rounded" style="height:100px; width: 100%;">
                    <div class="spinner-grow" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `.repeat(size)

    $("#"+divId).html(`<div class="row">${spinner}</div>`)
  }

  const bgColorList = [
    "#0f172a",  // Slate 900
    "#b91c1c",  // Red 700
    "#065f46",  // Emerald 800
    "#1e3a8a",  // Blue 800
    "#ca8a04",  // Yellow 600
    "#0e7490",  // Cyan 700
    "#7e22ce",  // Purple 800
    "#374151",  // Gray 700
    "#9f1239",  // Rose 700
    "#713f12",  // Amber 800
    "#312e81",  // Indigo 900
    "#5b21b6",  // Violet 800
    "#15803d",  // Green 700
    "#7c2d12",  // Orange 800
    "#be123c",  // Pink 700
    "#166534",  // Green 800
    "#4338ca",  // Indigo 700
    "#6366f1",  // Indigo 500
    "#1f2937",  // Gray 800
    "#92400e",  // Orange 700
    "#dc2626",  // Red 600
    "#047857",  // Emerald 700
    "#4a5568",  // Gray 600
    "#075985"   // Sky 700
  ];
  

  const colorList = [
    "green",
    "red",
    "blue",
    "yellow",
    "indigo",
    "purple",
    "pink",
    "orange",
    "green",
    "teal",
    "cyan",
  ];
 
  const randomColor = () => {
    return colorList[Math.floor(Math.random() * colorList.length)];
  };

  const fetchData = async (url) => {
    let response = await axios.get(url);
    try {
      return response.data;
    } catch (err) {
      console.log(err);
    }
  };


  const goalSharePieChart = ( policy_area_name , label , value , id) =>{
   
  
    new ApexCharts(document.querySelector(`#piechart_${id}`), {
      chart: { height: 300, type: "pie" },
      labels: label,
      series: value,
      title: {
        text: policy_area_name,
        align: 'left',
        margin: 10,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
          fontSize:  '14px',
          fontWeight:  'bold',
          color:  '#263238'
        },
      },
      fill: { opacity: [1, 0.6, 0.4, 0.6, 0.8, 1] },
      legend: {show : false },
      dataLabels: { enabled: !0, dropShadow: { enabled: !1 } },
      responsive: [
          {
              breakpoint: 575,
              options: { chart: { height: 250 }, dataLabels: { enabled: !1 } },
          },
      ],
  }).render()


  }


  const chartProgress = (id, percent , color) => {
    var options = {
      series: [percent],
      chart: {
        height: 110,
        type: "radialBar",
      },
      plotOptions: {
        radialBar: {
          startAngle: -90,
          endAngle: 270,
          hollow: {
            margin: 5,
            size: "70%",
            background: "#fff",
            image: undefined,
            imageOffsetX: 0,
            imageOffsetY: 0,
            position: "front",
            dropShadow: {
              enabled: true,
              top: 5,
              left: 0,
              blur: 4,
              opacity: 0.3,
            },
          },
          track: {
            background: "#fff",
            strokeWidth: "67%",
            margin: 0, // margin is in pixels
            dropShadow: {
              enabled: true,
              top: -3,
              left: 0,
              blur: 4,
              opacity: 0.35,
            },
          },

          dataLabels: {
            show: true,
            name: {
              offsetY: -10,
              show: true,
              color: "#888",
              fontSize: "8px",
            },
            value: {
              formatter: function (val) {
                return parseInt(val);
              },
              color: "#111",
              fontSize: "15px",
              offsetY: -10,
              show: true,
            },
          },
        },
      },
      fill: {
        type: "gradient",
        gradient: {
          shade: "dark",
          type: "horizontal",
          shadeIntensity: 0.9,
          colorStops: [
            {
              offset: 0,
              color: color,
            },
            {
              offset: 50,
              color: color,
            },
          ],
          inverseColors: true,
          opacityFrom: 10,
          opacityTo: 10,
          stops: [0, 100],
        },
      },
      stroke: {
        lineCap: "round",
      },
      labels: [""],
    };

    var chart = new ApexCharts(
      document.querySelector(`#chart-progress-${id}`),
      options
    );
    chart.render();
  };

  const chartGauge2 = (id, percent) => {
    const isMobile = window.innerWidth < 768;  // Define a breakpoint for mobile
    const chartHeight = isMobile ? '50%' : '50%'; // Larger height for mobile
    const paneSize = isMobile ? '90%' : '140%'; // Adjust pane size for mobile
    const labelFontSize = isMobile ? '10px' : '14px'; // Smaller font for mobile
    const dataLabelFontSize = isMobile ? '12px' : '16px'; // Adjust data label font
   
    Highcharts.chart(`chartdiv${id}`, {
      chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false,
        height: chartHeight, // Responsive height
        backgroundColor: 'transparent',
      },
      credits: {
        enabled: false
      },
      title: {
        text: ''
      },
      pane: {
        startAngle: -90,
        endAngle: 89.9,
        background: null,
        center: ['50%', '75%'],
        size: paneSize // Responsive pane size
      },
      yAxis: {
        min: 0,
        max: 100,
        tickPixelInterval: 30,
        tickPosition: 'inside',
        tickColor: '#fff',
        tickLength: 20,
        tickWidth: 2,
        minorTickInterval: null,
        labels: {
          distance: 20,
          style: {
            fontSize: labelFontSize, // Responsive label font size
            color: '#fff'
          }
        },
        lineWidth: 0,
        plotBands: [{
          from: 0,
          to: 25,
          color: '#DF5353', // red
          thickness: 20,
        }, {
          from: 25,
          to: 50,
          color: '#ffa500', // orange
          thickness: 20,
        }, {
          from: 50,
          to: 75,
          color: '#DDDF0D', // yellow
          thickness: 20
        }, {
          from: 75,
          to: 100,
          color: '#55BF3B', // green
          thickness: 20
        }]
      },
      exporting: { enabled: false },
      series: [{
        name: 'Average score',
        data: [Math.floor(percent)], // Only one data point
        tooltip: {
          valueSuffix: ''
        },
        dataLabels: {
          format: '{y} ',
          borderWidth: 0,
          color: (
            Highcharts.defaultOptions.title &&
            Highcharts.defaultOptions.title.style &&
            Highcharts.defaultOptions.title.style.color
          ) || '#333333',
          style: {
            fontSize: dataLabelFontSize // Responsive data label font size
          }
        },
        dial: {
          radius: '80%',
          backgroundColor: 'white',
          baseWidth: 12,
          baseLength: '0%',
          rearLength: '0%'
        },
        pivot: {
          backgroundColor: 'white',
          radius: 6
        }
      }]
    });
  }
  
  const chartGauge = (id, percent) => {
    var options = {
      series: [percent],
      chart: {
        height: 300,
        type: "radialBar",
        sparkline: {
          enabled: true,
        },
      },
      plotOptions: {
        radialBar: {
          hollow: {
            margin: 0,
            size: "20%",
            background: "transparent",
            imageOffsetX: 0,
            imageOffsetY: 0,
            position: "front",
          },
          track: { background: "#bfbfbf", strokeWidth: "50%" },
          dataLabels: {
            show: !0,
            name: { show: !1 },
            value: {
              formatter: function (e) {
                return parseInt(e);
              },
              offsetY: 7,
              color: "#bfbfbf",
              fontSize: "17px",
              fontWeight: "500",
              show: !0,
            },
          },
        },
      },
      colors: ["#ffffff"],
      fill: { type: "solid" },
      stroke: { lineCap: "round" },
    };

    var gauge_chart = new ApexCharts(
      document.querySelector(`#gauge_chart_${id}`),
      options
    );
    gauge_chart.render();
  };

  const ministryCard = async () => {
    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()
    
    let url = `/api/ministry/ministries${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
  
    preLoading('ministryCardLists' , 8 , 3)
    let data = await fetchData(url);
    $("#ministryCardLists").html(`
     
      `);
    const card = data.map((ministry, index) => {
      let color = randomColor();

      return `
            <div class="col-6 col-lg-3">
                <div class="card card-shadow" style="height: 170px;" name="ministry-card" data-ministry="${ministry.id}" data-ministry-name="${ministry.responsible_ministry_eng}" data-ministry-image="${ministry.image}" data-color="${color}">
                    <div class="card-body">
                        <div class="row mt-3">
                            <div class="col-5">
                                <div>
                                    <img src="${ministry.image}" class="img-fluid" style="width: 70px;" alt="">
                                </div>
                                <div>
                                    <h4 class="mt-2">${ministry.code}</h4>
                                </div>
                            </div>
                            <div class="col-7">
                                <div  id="chart-progress-${ministry.id}"></div>
                                <div>
                                
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
            `;
      // return `
      //        <div class="col-xl-2 col-md-6 mt-0 card-shadow">
      //                 <div class="card mini-stats bg-light text-dark shadow-sm" name="ministry-card" data-ministry="${ministry.id}" data-ministry-name="${ministry.responsible_ministry_eng}" data-color="${color}" style="border-style: solid; border-width: 1px; border-color: var(--bs-${color})">
      //                   <div class="p-3 mini-stats-content">
      //                       <div>
      //                           <div class="text-end justify-content-center">
                                    
      //                               <img src="${ministry.image}" class="img-fluid mx-auto d-block" style="width: 100px; height: 100px;" alt="">
      //                           </div>
                                     
      //                       </div>
      //                   </div>
      //                   <div class="mx-2">
      //                       <div class="p-4 rounded-top shadow-lg" style="background-color: var(--bs-${color})">
      //                           <div class="my-n4" style="width: 130px">
      //                               <div class="my-n4 ml-2" id="gauge_chart_${ministry.id}"></div>
      //                           </div>
                              

      //                       </div>
      //                   </div>
      //               </div>
      //           </div>
      //       `;
    
    });

    $("#ministryCardLists").append(card);

    data.forEach((ministryData) => {
      let percent = Math.floor(Math.random() * 100);
      // chartGauge(ministryData.id, percent , randomColor());
     chartProgress(ministryData.id, ministryData.ministry_score_card.avg_score , ministryData.ministry_score_card.scorecard_color);
    });
  };

  const goalListCard = async (ministry_id ,id, color , policy_area_name) => {
       let type = $("#dataType").val()
        let typeValue = $("#dataTypeLists").val()

        //check is year or quarter
        let url = `/api/ministry/policy_area_with_goal/${id}?ministry_id=${ministry_id}${type == 'year' ? '&year='+typeValue : '&year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
    let goals = await fetchData(url);
      

    let card = goals.policy_area_goal.map((goal) => {
      let avgScoreWidth = goal.ministry_strategic_goal_score_card.avg_score.toFixed(2);
      return `
      <div class="col-md-6">
      <div class="card card-shadow" style="height: 170px; border-style: solid; border-width: 1px; border-color: var(--bs-${color})" name="goal-card" data-goal="${goal.id}" data-goal-name="${goal.goal_name_eng}" data-color="${color}" data-score-color="${goal.ministry_strategic_goal_score_card.scorecard_color}" data-score="${avgScoreWidth}"  data-ministryId="${ministry_id}">
          <div class="card-body">
              <div class="h-100">
                 <h6 class="mb-2 f-w-400  data-bs-toggle="tooltip" data-bs-placement="top" title="${goal.goal_name_eng}" text-muted">${goal.goal_name_eng.length > 45 ? goal.goal_name_eng.slice(0,45)+'...' : goal.goal_name_eng}</h6>
              </div>
          </div>
          <div class="card-footer">
                   <div class="w-100 progress" style="height: 20px">
                          <div class="progress-bar" role="progressbar" style="width: ${avgScoreWidth}%; background-color:${goal.ministry_strategic_goal_score_card.scorecard_color};" aria-valuenow="${goal.ministry_strategic_goal_score_card.avg_score}" aria-valuemin="0" aria-valuemax="100">${avgScoreWidth}%</div>
                      </div>
          </div>
      </div>
  </div>
      `;
  });

  
  let totalWight = 0
  goals?.policy_area_goal?.forEach((goal)=> totalWight += parseFloat(goal.goal_weight)) 
  let shareGoalNameLists = goals?.policy_area_goal?.map((goal)=> goal.goal_name_eng)
  let shareGoalValueLists = goals?.policy_area_goal?.map((goal)=>goal.goal_weight || 0)
  let sentValue = shareGoalValueLists?.map((val)=> val * 100 / totalWight)


  goalSharePieChart(policy_area_name , shareGoalNameLists , sentValue , id   )

  return card.join('')

  };

  const selectedMinistryCard = async (ministry_name, ministry_id , color , ministry_image) => {
    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()

    //check is year or quarter
    
    let url = `/api/ministry/dashboard_ministries/${ministry_id}${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
    let ministry_dashboard = await fetchData(url)
    preLoading('ministryDashboard' , 8 , 2)


    ministryData = await fetchData( `/api/ministry/ministry_with_policy_area/${ministry_id}${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`)

    
    $("#ministryKra").html(``);
    $("#policyAreaMainCard").html(``);
    $("#goalWithKraList").html(``);
    $("#ministryDashboard").html(``);
    $('#goalShare').html('')
    $('#goalShare').html('<h3 class="text-center">Goal Shares</h3>')
    $("#ministryDashboard").append(
      `
   
          <div class="mt-5">
             <h3 style="color: var(--bs-${color})">${ministry_name} <img src="${ministry_image}" alt="" class="img-fluid float-end mb-5" style="height:80px;width:95px" /> </h3>
             <hr class="mt-2">
          </div>
  
      
      <div id="dash" class="row justify-content-center mb-4">
      </div>
     

      `
    )
    ministry_dashboard.dashboard.forEach((dashboard , index) => {
    $("#dash").append(
      `
      <div class="col-6 col-md-3 mt-2">
        <div class="m-0 card bg-${colorList[index]}-500"">
            <div class="card-body p-3">
                <div class="d-flex align-items-center justify-content-between">
                    <div>
                        <p class="mb-0 text-white text-opacity-75">${dashboard.title}</p>
                    </div>
                    <div class="avtar">
                        <h4 class="mb-0 text-white">${dashboard.value}</h4>
                    </div>
            </div>
          </div>
        </div>
      </div>

      `
    )
  })
    if (ministryData.length == 1) {
      ministryData.forEach(async(policy) => {
        let policyAreaCard = `
        <div class="col-lg-6" style="margin-bottom: 50px">
        <div style="background-color: ${bgColorList[Math.floor(Math.random() * bgColorList.length)]}" class="card h-100 dropbox-card" data-ministryId="${ministry_id}">
           <div class="card-body">
                <div class="d-flex align-items-center justify-content-between">
                    <h5 class="text-white">${
                      policy.policyAreaEng
                    }</h5>
                    <div><i class="fas ${
                      policy.icon
                        ? "fa-" + policy.icon.split(",")[1]
                        : "fa-tractor"
                    } text-white" style="font-size:80px"></i></div>
                </div>
                <div class="row justify-content-center ">
                    <div class="col chartdiv  pt-5 w-100 h-100" id="chartdiv${policy.id}"></div>
                </div>
            </div>
        </div>
    </div>
    `;

      $("#policyAreaMainCard").append(policyAreaCard)   
      $('#goalShare').append(
        `<div class="col-md-5 text-center ">
                               <div class="row justify-content-center">
                                   <div id="piechart_${policy.id}"></div>
                               </div>
                </div>
        `
      )
      chartGauge2(policy.id , Math.floor(policy.ministry_policy_area_score_card.avg_score*100)/ 100 ); 
      
      letGoalTest =  await goalListCard(ministry_id, policy.id , color , policy.policyAreaEng)
        // Display goals for the policy
        $("#policyAreaMainCard").append(`
                  <div class="col-lg-6" style="margin-bottom: 50px">
                      <h3>Goals</h3>
                      <div class="row h-100 mt-3">
                     
                      ${letGoalTest}
                      </div>
                  </div>
              `);
      

              
      });
    } 


    else if (ministryData.length > 1) {
      
  


    ministryData.forEach(async(policy) => {
      $('#goalShare').append(
        `<div class="col-md-4 text-center ">
                               <div class="row justify-content-center">
                                   <div id="piechart_${policy.id}"></div>
                               </div>
                </div>
        `
      )

      letGoalTest =  await goalListCard(ministry_id, policy.id , color , policy.policyAreaEng)
      
      let goalListCardHtml = `
      <div class="" style="margin-bottom: 50px">
         <h3>Goals</h3>
              <div class="row h-100 mt-3">
               ${letGoalTest}
              </div>
      </div>`

      let policyAreaCard = `
                <div class="col-lg-6" style="margin-bottom: 50px;">
                    <div style="background-color: ${bgColorList[Math.floor(Math.random() * bgColorList.length)]}" class="card dropbox-card" data-ministryId="${ministry_id}">
                        <div class="card-body" style="height:350px;">
                            <div class="d-flex align-items-center justify-content-between">
                                <h5 class="text-white">${
                                  policy.policyAreaEng
                                }</h5>
                                <div><i class="fas ${
                                  policy.icon
                                    ? "fa-" + policy.icon.split(",")[1]
                                    : "fa-tractor"
                                } text-white" style="font-size:80px"></i></div>
                            </div>
                            <div class="d-flex align-items-center h-75">
                                <div class="col chartdiv" id="chartdiv${policy.id}"></div>
                            </div>
                        </div>
                    </div>

                    ${goalListCardHtml}
                    
                </div>
            `;


          $("#policyAreaMainCard").append(policyAreaCard)
       
        
          
          chartGauge2(policy.id , policy.ministry_policy_area_score_card.avg_score); // Display progress chart for the policy

    

           
            
    });
    }
    else {
      $("#policyAreaMainCard").append(`
          <div class="mt-5">
             <h4 class="text-center text-danger mb-5">No data found for this ministry</h4>
          </div>
          `);
    }

    kpiStatues(ministry_id)
  };

  const indicatorList = (indicators) =>{
    return indicators.map((indicator) =>{

      let previousIndicator = indicator?.annual_indicators?.find((item) => item?.year == (indicator?.annual[0]?.year-1) )
      let diff = Math.floor(indicator?.annual[0]?.annual_performance - previousIndicator?.annual_performance)
      let direction = diff > 1 ? 'fa-arrow-up' : diff >= 0 &&  diff == 0 ? 'fa-arrow-right': 'fa-arrow-down'
      let directionColor = diff > 1 ? 'text-success' : diff >= 0 &&  diff == 0 ? 'text-dark': 'text-danger'
            
      let hasTarget = indicator?.annual[0]?.annual_target ? 'primary' : 'primary'
      let score = indicator?.annual[0]?.score || 'None'



      let performanceType = score >= 70 ? 'good' :( score >= 50 ? 'average' : (score < 50 ? 'poor' : 'nodata'))



      return `
          <div name="indicator-lists" class="col-lg-4 d-none border">
              <div name="${performanceType}">
                  <div class="d-flex align-items-center">
                      <div class="flex-shrink-0">
                        <span class="p-2 d-block rounded-circle"  style="height: 30px; width: 30px; font-size: 70px; background-color: ${indicator?.annual[0]?.annual_target || indicator?.annual[0]?.quarter_target  ? indicator?.annual[0]?.scorecard || 'red' : 'gray'}"></span>
                      </div>
                      <div class="ml-3"> &nbsp <i class="fas ${ indicator?.annual[0]?.annual_target ? direction : 'fa-arrow-up'}  ${indicator?.annual[0]?.annual_target ? directionColor : 'text-muted' }  " style=" font-size: 30px;"></i></div>
                      <div class="flex-grow-1 mx-2">
                          <button name="indicator-btn" data-indicator-name="${indicator.kpi_name_eng}"  data-indicator-id="${indicator.id}" class="btn btn btn-link-secondary mb-0 d-grid text-start" type="button" data-bs-toggle="modal" data-bs-target="#indicatorModal" aria-controls="offcanvasExample">
                              <span class="w-100" data-bs-toggle="tooltip" data-bs-placement="top" title="${indicator.kpi_name_eng}">${indicator.kpi_name_eng.length > 25 ? indicator.kpi_name_eng.slice(0,25) + '...' : indicator.kpi_name_eng}</span>
                          </button>
                      </div>
                      <div class="badge bg-light-secondary f-12">${score}</div>
                  </div>
              </div>
          </div>
        `
    })
}



  const kpiStatuesGraph = async (per) => {
  var options = {
    series: per,
    labels: [`High Performance ${[per[0]]}`, `Average Performance ${[per[1]]}`, `Low Performance ${[per[2]]}`],
    chart: {
    type: 'donut',
    height: 300
  },
  colors: ['#20c997', '#fd7e14', '#dc3545'],
  responsive: [{
    breakpoint: 300,
    options: {
      chart: {
        width: 50
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  var chart = new ApexCharts(document.querySelector("#kpiStatuesGraph"), options);
  chart.render();
  }


  $(document).on("click", "[name='ministry-card']", async function () {
  const ministry_id = $(this).data("ministry");
  const ministry_name = $(this).data("ministryName");
  const ministry_image = $(this).data("ministryImage");
  const color = $(this).data("color");
  let type = $("#dataType").val()
  let typeValue = $("#dataTypeLists").val()

  //check is year or quarter
  let url = `/api/ministry/ministry_with_policy_area/${ministry_id}?${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
 
  let data = await fetchData(url)
  
  selectedMinistryCard(ministry_name, ministry_id , color , ministry_image);
  $("html, body").animate(
    {
      scrollTop: $("#policyAreaMainCard").offset().top,
    },
    500
  );
  });

  const kpiStatues = async (ministry_id) => {
  let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()

    //check is year or quarter
    let url = `/api/ministry/ministry_with_policy_area/${ministry_id}${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
   
    let data = await fetchData(url)
   
  $('#kpiStatus').html(``)
  let card = `
  <div class="row col-lg-6 justify-content-center">
      <div id="kpiStatuesGraph">
      </div>
  </div>
  `;

  let card2 = `
  <div class=" col-lg-6 border">

    <div class="row bg-teal-400 rounded justify-content-center ">

      <div class="col-md-4 p-3">
          <div class="card" style="height: 200px;">
              <div class="card-body p-3">
                <div class="bg-primary p-3 pt-4 rounded-4 mt-3 align-items-bottom">
                      <h3 class="text-center text-white">${data[0].count_has_performance}</h3>
                  </div>
                  <h6 class="mb-1 text-center mt-2">Indicators with performance</h6>
              </div>
          </div>
      </div>

       <div class="col-md-4 p-3">
          <div class="card" style="height: 200px;">
              <div class="card-body p-3">
                  <div class="bg-warning p-3 pt-4 rounded-4 mt-3 align-items-bottom">
                      <h3 class="text-center text-white">${data[0].count_has_no_performance}</h3>
                  </div>
                  <h6 class="mb-1 text-center mt-2">Indicators with target but no performance</h6>
              </div>
          </div>
      </div>
       <div class="col-md-4 p-3">
          <div class="card" style="height: 200px;">
              <div class="card-body p-3">
                  <div class="bg-danger p-3 pt-4 rounded-4 mt-3 align-items-bottom">
                      <h3 class="text-center text-white">${data[0].count_has_no_target}</h3>
                  </div>
                  <h6 class="mb-1 text-center mt-2">Indicators with out target</h6>
              </div>
          </div>
      </div>
    </div>

  </div>
  `;

  $('#kpiStatus').append(card);
  $('#kpiStatus').append(card2);
  let per = [data[0].high_performance , data[0].average_performance , data[0].low_performance]
  if (data[0].high_performance == 0 && data[0].average_performance == 0 && data[0].low_performance == 0) {
    $('#kpiStatuesGraph').html`
    <div class="mt-5 p-5">
       <h4 class="text-danger text-center"> No indicator with performance found </h4>
    </div>
    `
  }
  else{
  kpiStatuesGraph(per)
  }
  }

  const selectedGoalCard = async (goal_id ,ministry_id , color, score, scoreColor) => {
    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()
    
    preLoading('goalWithKraList', 3 , 4)

    //check is year or quarter
    let url = `/api/ministry/goal_with_kra/${goal_id}?ministry_id=${ministry_id}${type == 'year' ? '&year='+typeValue : '&year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
    let goal = await fetchData(url)
    $("#goalWithKraList").html(``);
    $("#goalWithKraList").append(
      `<div>
         <h3 style="color: var(--bs-${color})"><span class="badge" style="background-color: ${scoreColor};">  ${score} </span> &nbsp${goal.goal_name_eng}</h3>
         <hr>
       </div>
      `
    );
   
    if (goal.kra_goal.length > 0) {
      let kra_lists = goal.kra_goal.map((kra) => {
        return `
        <h6 name="kra-lists" class="pt-3 col-6"><span class="badge" style="background-color: ${kra?.ministry_key_result_area_score_card?.scorecard_color};">  ${Math.floor(kra?.ministry_key_result_area_score_card?.avg_score) || 0}</span> &nbsp ${kra.activity_name_eng}</h6>
         ${indicatorList(kra.indicators).join("")}
          `;
      });
      let goalHtml = `
           <div class="row">
              ${kra_lists.join("")}
          </div> `;

          $("#goalWithKraList").append(`

            <div class="form-check mb-2">
               <input class="form-check-input" type="checkbox" value="" id="showIndicator"> 
               <label class="form-check-label" for="showIndicator">Show with Indicator</label>
            </div>
      
     
            <h1 name="indicator-lists" class="d-none">Indicators</h1>
            <p name="indicator-lists" class="d-none fw-bold" >Click on an indicator for values, time series, and metadata.</p>
     
            <div name="indicator-lists" class="d-none row gap-2">
     
                 
                 <div class="col-md-2 d-flex align-items-center">
                     <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #28A745;"></div>
                     <div class="ms-2">Very Good Perf <br>  (95% - 100%)</div>
                 </div>
         
     
                 <div class="col-md-2 d-flex align-items-center">
                     <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #8BC34A; "></div>
                     <div class="ms-2">&nbsp Good Perf <br> &nbsp; (85% - 94%) </div>
                 </div>
     
                 <div class="col-md-2 d-flex align-items-center">
                      <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #FFC107; "></div>
                      <div class="ms-2">&nbsp Average Perf <br> &nbsp; (65% - 84%)</div>
                 </div>
     
                 <div class="col-md-2 d-flex align-items-center">
                      <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #FF9800; "></div>
                      <div class="ms-2">&nbsp Low Perf <br> &nbsp; (50% - 64%)</div>
                 </div>
     
                 <div class="col-md-2 d-flex align-items-center">
                     <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #DC3545; "></div>
                     <div class="ms-2">&nbsp Very Poor Perf <br> &nbsp; (0% - 49%) </div>
                 </div>
     
             </div>
     
     
             <p name="indicator-lists" class="mt-4 d-none fw-bold" >Comparing with last year</p>
             <div name="indicator-lists" class="d-none d-flex align-items-center ">
                 <div class="flex-shrink-0">
                    <i class="fas fa-arrow-up text-success " style=" font-size: 22px;"></i>
                 </div>
                 <div class="pe-5"> &nbsp Increasing</div>
         
                 <div class="flex-shrink-0">
                   <i class="fas fa-arrow-right " style=" font-size: 22px;"></i>
                 </div>
                 <div class="pe-5"> &nbsp Constant</div>
         
                 <div class="flex-shrink-0">
                     <i class="fas fa-arrow-down text-danger " style=" font-size: 22px;"></i>
                 </div>
                 
                 <div class="pe-5"> &nbsp Decreasing</div>
             </div>
     
     
            ${goalHtml}
            `)
         }
    else {
      $("#goalWithKraList").append(`
      <h4 class="text-center text-danger mb-5">No data found for this goal</h4>
      `);
    }
  };

  const chartProgressVsPerformance = (years, target , performance) => {
    $("#indicator-key-performance-chart").html("")
    var options = {
      series: [{
        name: 'Performance',
        data: performance
      },
      ],
      chart: {
      height: 350,
      type: 'line',
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'straight'
    },
    grid: {
      row: {
        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
        opacity: 0.5
      },
    },
    xaxis: {
      categories: years,
    }
    };


  //   var options = {
  //     series: [{
  //     name: 'Target',
  //     data: target
  //   }, {
  //     name: 'Performance',
  //     data: performance
  //   }],
  //     chart: {
  //     type: 'bar',
  //     height: 350,
  //     parentHeightOffset: 0,
  //     toolbar: {
  //       show: false
  //     }
  //   },
  //   grid: {
  //     show: true
  // },
  //   plotOptions: {
  //     bar: {
  //       horizontal: false,
  //       columnWidth: '85%',
  //       endingShape: 'rounded'
  //     },
  //   },
  //   dataLabels: {
  //     enabled: false
  //   },
  //   stroke: {
  //     show: true,
  //     width: 2,
  //     colors: ['transparent']
  //   },
  //   xaxis: {
  //     categories: years,
  //   },
  //   yaxis: {
  //   },
  //   fill: { colors: ["#2ca87f", "#A0D683"]},
  //   colors: ["#2ca87f", "#A0D683;"],
  //   stroke: { show: !0, width: 3, colors: ["transparent"] },
  //     title: {
  //       text: "Target Vs Performance",
  //       align: 'left',
  //       margin: 15,
  //       offsetX: 0,
  //       offsetY: 0,
  //       floating: false,
  //       style: {
  //         fontSize:  '14px',
  //         fontWeight:  'bold',
  //         color:  '#263238'
  //       },
  //   },
  //   tooltip: {
  //     y: {
  //       formatter: function (val) {
  //         return  val 
  //       }
  //     }
  //   }
  //   };

    var chart = new ApexCharts(document.querySelector("#indicator-key-performance-chart"), options);
    chart.render();
  }
  const modalIndicatorAnnualPlan = (data, year) => {

    let type = $("#dataType").val() // identify whether it is year or quarter
    let typeValue = $("#dataTypeLists").val()

    let table = data.map((item) => {
      let changePercentage = item?.previous_year_performance_data ? Math.round(item?.previous_year_performance_data[0] * 100)/100 : null
      let changeInAbsolute = item?.previous_year_performance_data ? Math.round(item?.previous_year_performance_data[1] * 100)/100 : null
      
      


      let direction = changePercentage > 1 ? 'fa-arrow-up' : changePercentage >= 0 &&  changePercentage == 0 ? 'fa-arrow-right': 'fa-arrow-down'
      let directionColor = changePercentage > 1 ? 'text-success' : changePercentage >= 0 &&  changePercentage == 0 ? 'text-dark': 'text-danger'
  
      return `
        <tr  class="${item.year == year ? 'table-success' : '' }">
          <td>${type == 'year' ? item?.year : item?.quarter}</td>
          <td>${item?.annual_target || item?.quarter_target || 'None'}</td>
          <td>${item.annual_performance || item.quarter_performance || 'None' }</td>
          <td class="fw-bold" style="color: ${item.scorecard || 'red'}" >${item.score || 'None'}</td>
          <td class="${item.annual_performance || item.quarter_performance   ? directionColor : 'text-danger'} fw-bold"> <i class="fas ${item.annual_performance || item.quarter_performance ? direction : 'fa-arrow-down'} fa-sm "></i>${changePercentage}</td>
          <td class="${item.annual_performance ||  item.quarter_performance  ? directionColor : 'text-danger'} fw-bold">${changeInAbsolute}%</td>
        </tr>
      `
    })
    $("#table-title").html(type == 'year' ? 'Annual Plan' : 'Quarter Plan ' + typeValue.split('-')[0])
    $("#table-year-type").html(type == 'year' ? 'Year' : 'Quarter' )
    $("#modalAnnualPlanTable").html(table)
}


const indicatorModal = (title, data) =>{
  let type = $("#dataType").val()
  let typeValue = $("#dataTypeLists").val()

  $('#indicatorModalLabel').html(title)
  $('#kpi-unit').html(data.kpi_measurement_units || 'None')
  $('#kpi-char').html(data.kpi_characteristics)
  $('#kpi-weight').html(data.kpi_weight || 'None')
  $('#kpi-kra').html(data.keyResultArea > 5 ? data.keyResultArea.slice(0, 5) : data.keyResultArea)
  $('#kpi-ministry').html(data?.responsible_ministries?.code || 'None')
  let yearValueUtilCurrent = data.annual_indicators.filter((year) => year.year <= typeValue)

  data.annual_indicators.sort((a, b) => {

    function splitNumberAndText(input) {
      const match = input.match(/^(\d+)(\D+)$/);
      if (match) {
        const [numberPart, textPart] = match.slice(1, 3);
        return [ numberPart, textPart ];
      } else {
        return { error: "Input format is incorrect" };
      }
    }

    
    if (a.quarter && b.quarter) {
      const numberPartA= splitNumberAndText(a.quarter);
      const numberPartB= splitNumberAndText(b.quarter);

      if (Number(numberPartA[0]) < Number(numberPartB[0])) {
       
        return -1
      }
      return 1

    } else {
      if (a.year < b.year) {
        return -1
      }
      return 1
    }
    return -1
  })

  

  let years = yearValueUtilCurrent.map((year) => year.year)
  let quarter =  data.annual_indicators.map((item) => item.quarter)

  let performance = yearValueUtilCurrent.map((performance) => performance.annual_performance || 0)
  let performanceQuarter =  data.annual_indicators.map((item) => item.quarter_performance || 0)
  
  let target = yearValueUtilCurrent.map((target) => target.annual_target || 0)
  let targetQuarter =  data.annual_indicators.map((item) => item.quarter_target || 0)

  chartProgressVsPerformance(type == 'year' ? years : quarter, type == 'year' ? target : targetQuarter, type == 'year' ? performance :performanceQuarter ) //modal chart
  modalIndicatorAnnualPlan(data.annual_indicators, typeValue)

 


}


// Dashboard top cards
  const dashboardCard = async() =>{
  preLoading('dashboardInfo', 5 , 2)
  let data = await fetchData('/api/ministry/dashboard/')

  const icon = ['briefcase', 'bullseye', 'suitcase', 'chart-line' , 'building']
  

  let card = data.dashboard.map((card, index) =>{
    let color = randomColor()
    return`
          <div class="col-xl-2 m-0  " >
               <div class="card social-widget-card p-0 m-0  border bg-${color}-500" style="width: 100%;" >
                   <div class="card-body">
                       <h2 class="text-white m-0">${card.value}</h2>
                       <span class="fw-bold">${card.title}</span>
                       <i style="font-size: 80px;" class="fas fa-${icon[index]}"></i>
                   </div>
               </div>
          </div>
    `
  })

  $("#dashboardInfo").html(card)
  }


  $(document).on("click", "[name='goal-card']", async function () {
    const goal_id = $(this).data("goal");
    const ministry_id = $(this).data("ministryid");
    const color = $(this).data("color");
    let score = $(this).data("score")
    let scoreColor = $(this).data("scoreColor")

    selectedGoalCard(goal_id , ministry_id ,color, score, scoreColor);
    $("html, body").animate(
      {
        scrollTop: $("#goalWithKraList").offset().top,
      },
      500
    );
  });


  $(document).on('click', "[name='performance-card']", async function(){
    let type = $(this).data('type')

    $("[name='indicator-lists']").addClass('d-none')
    $("[name='kra-lists']").removeClass('mt-3 col-6').addClass('d-none');  
    $(`[name=${type}]`).parent().parent().prev().removeClass('d-none')
    $(`[name=${type}]`).parent().parent().prev().prev().removeClass('d-none')
    $(`[name=${type}]`).parent().parent().prev().prev().prev().removeClass('d-none')
    $(`[name=${type}]`).parent().removeClass('d-none')
    $("html, body").animate(
      {
        scrollTop: $("#performanceAnalysis").offset().top,
      },
      300
    );

  })



  $(document).on('click', "[name='indicator-btn']", async function() {
    const indicatorId = $(this).data('indicatorId')
    const indicatorName = $(this).data('indicatorName')
    const goal = $(this).data('goal')

    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()
    let data = await fetchData(`/api/ministry/indicator/${indicatorId}/${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`)



    $('#kpi-goal').html(goal || 'None')
    indicatorModal(indicatorName, data)


  })

  const filterDataOption = async() =>{
    let data = await fetchData(`/api/ministry/time_series_year/`)

    const yearOption = () =>{
      return  data?.years?.map((year, index) => {
        return `<option ${index+1 == data.years.length ? 'selected' : ''} value="${year.year_amh}">${year.year_amh}</option>`
      })
    }


    
    const quarterOption = () =>{
      return  data?.years?.map((year, indexYear) => {
        return data?.quarters?.map((quarter, indexQuarter) => {
          return `<option ${indexYear+1 == data.years.length && indexQuarter+1 == data.quarters.length ? 'selected' : ''}  value="${year.year_amh}-${quarter.quarter_eng}">${year.year_amh} (${quarter.quarter_eng})</option>`
        })
      })


    }

    //call for first default option
    $("#dataTypeLists").html(yearOption())
    $("#selectedDataValue").html($("#dataTypeLists").val())
  
    //handle data type changed
    $('#dataType').on('change', ()=>{
      let dataType = $('#dataType').val()
      $("#dataTypeLists").html(dataType === 'quarter' ? quarterOption() : yearOption())
      $("#selectedDataValue").html($("#dataTypeLists").val())
      
    })
    
   
  }





  const main = async () => {
    await filterDataOption() 
      dashboardCard()
      ministryCard();
      ministryIndicatorShare();
      $("#year").html($("#dataTypeLists").val())
  }

  main()


  $(document).on('change' , '#dataTypeLists', () =>{
    $("#selectedDataValue").html($("#dataTypeLists").val())
  
      $("#ministryCardLists").html('')
      $("#ministryDashboard").html('')
      $("#policyAreaMainCard").html('')
      $("#kpiStatus").html('')
      $("#goalWithKraList").html('')
      $("#year").html($("#dataTypeLists").val())
    
     
      ministryCard();
  })


  $(document).on('change' , '#dataType', () =>{
    $("#selectedDataValue").html($("#dataType").val())
  
      $("#ministryCardLists").html('')
      $("#ministryDashboard").html('')
      $("#policyAreaMainCard").html('')
      $("#kpiStatus").html('')
      $("#goalWithKraList").html('')
      $("#year").html($("#dataTypeLists").val())
    
     
      ministryCard();
      
  })

  
  $(document).on('change', '#showIndicator', async function () {
    let value = $('#showIndicator').prop('checked')
    value ? $("[name='indicator-lists']").removeClass('d-none') :  $("[name='indicator-lists']").addClass('d-none')
    $("[name='kra-lists']").toggleClass('mt-3 col-6', !value);

  })

  const ministryIndicatorShare = async () => { 
    let url = `/api/ministry/ministries/`;
    
    // Preload data and show loading animation
    preLoading('policyAreaCardLists', 1, 1);

    // Fetch ministry data
    let data = await fetchData(url);

    var options = {
        series: [
            {
                data: []
            }
        ],
        legend: {
            show: false
        },
        chart: {
            height: 350,
            type: 'treemap',
            events: {
                // Event triggered when a ministry is clicked on the treemap
                dataPointSelection: async function(event, chartContext, config) {
                    // Get selected ministry code
                    let ministryCode = config.w.config.series[0].data[config.dataPointIndex].x;

                    // Find ministry details based on the ministry code
                    const ministryData = data.find(item => item.code === ministryCode);
                    const ministry_id = ministryData.id;
                    const ministry_image = ministryData.image;
                    const ministry_name = ministryCode;

                    // Call ministryIndicatorShareClicked when a share is clicked
                    ministryIndicatorShareClicked(ministry_id , ministry_name , ministry_image);
                    

                    
                    // Scroll to the policy area main card
                    $("html, body").animate(
                        {
                            scrollTop: $("#policyAreaMainCard").offset().top,
                        },
                        500 
                    );
                }
            }
        },
        title: {
            text: 'Ministries Indicator Share',
            align: 'center'
        },
        colors: [
           '#2ca87f', '#4680ff', '#6610f2', '#673ab7', '#e83e8c', '#dc2626', '#fd7e14', '#e58a00', '#2ca87f', '#008080', '#3ec9d6' , "#FF1A66", "#E6331A", "#33FFCC",
            "#66994D", "#B366CC", "#4D8000", "#B33300", "#CC80CC",
            "#66664D", "#991AFF", "#E666FF", "#4DB3FF", "#1AB399",
            "#E666B3", "#33991A", "#CC9999", "#B3B31A", "#00E680",
            "#4D8066", "#809980", "#E6FF80", "#1AFF33", "#999933",
            "#FF3380", "#CCCC00", "#66E64D", "#4D80CC", "#9900B3",
            "#E64D66", "#4DB380", "#FF4D4D", "#99E6E6", "#6666FF"
        ],
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: false
            }
        },
        tooltip: {
            y: {
                formatter: function(value) {
                    return value + ' Indicators';
                }
            }
        }
    };

    // Add ministry data to the chart options
    data.forEach((item, index) => {
        options.series[0].data.push({ x: item.code, y: item.count_indicator });
    });

    // Render the chart
    var chart = new ApexCharts(document.querySelector("#ministryIndicatorShare"), options);
    chart.render();
};

// Function to handle ministry card click and fetch detailed KRA data




const performanceAnalysisCard = (data) =>{

  $("#performanceAnalysis").html('')
  data.forEach((item,index) =>{
    let card = `
    <div class="col-md-3">
      <div name="performance-card" data-name="kpi-status" data-type="${item?.type}" data-ministry-id="1" class="card card-shadow social-widget-card text-dark">
        <div class="card-body m-0">
            <div class="row justify-content-center">
                <div class="col-5">
                    <div id="total-performance-graph-${index}" class="p-0 m-0"></div>
                </div>
                <div class="col-7 d-flex align-items-center">
                     <div class="w-100"><h6 class="mb-1 fw-bold">${item.title}</h6></div>
                     <div class="w-100">  <h1 class="w-100 p-2 fw-bold">${item.value}</h1></div>
                </div>
            </div>
        </div>
      </div>
    </div>`

    $("#performanceAnalysis").append(card)
    performanceAnalysisPieChart(`total-performance-graph-${index}`, item?.percentage || 0, item.color)

  })
}
  const ministryIndicatorShareClicked = async (ministry_id , ministry_name , ministry_image) => {


    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()

    let url = `/api/ministry/ministry_kra_serializer/${ministry_id}/${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`;




    let urlDash = `/api/ministry/ministry_with_policy_area/${ministry_id}${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
   
    let data = await fetchData(urlDash)
    let totalData = data[0]?.average_performance + data[0]?.high_performance + data[0]?.low_performance + data[0]?.count_has_no_performance
    let percentage = [data[0]?.average_performance / totalData * 100 , data[0]?.high_performance / totalData * 100 , data[0]?.low_performance / totalData * 100 , data[0]?.count_has_no_performance / totalData * 100]


    const performanceData = [{
      title : 'Good Per',
      value : data[0]?.high_performance || 0,
      percentage : percentage[1] || 0,
      color : '#2ca87f',
      type : 'good' //don't change it, it's for filter
    },
    {
      title : 'Average Per',
      value : data[0]?.average_performance || 0,
      percentage : percentage[0] || 0,
      color : '#ffc107',
      type : 'average' //don't change it, it's for filter
    },
    {
      title : 'Poor Per',
      value : data[0]?.low_performance || 0,
      percentage : percentage[2] || 0,
      color : '#dc2626',
      type : 'poor' //don't change it, it's for filter
    },
    {
      title : 'No data',
      value : data[0]?.count_has_no_performance || 0,
      percentage :  percentage[3] || 0,
      color : '#6c757d',
      type : 'nodata' //don't change it, it's for filter
    },
    
  ]

    // Fetch ministry KRA details based on ministry ID and year
    $('#ministryKra').html('')
    $('#ministryDashboard').html('')
    $('#policyAreaMainCard').html('')
    $('#goalShare').html('')
    $('#goalWithKraList').html('')
    $('#kpiStatus').html('')
    preLoading('ministryKra',1,12)
    let ministryDetails = await fetchData(url);
    $('#ministryKra').html('')
   
    

    $("#ministryKra").append(
      `

           <div class="mt-5">
             <h3>${ministry_name} <img src="${ministry_image}" alt="" class="img-fluid float-end mb-5" style="height:80px;width:95px" /> </h3>
             <hr class="mt-2">
          </div>
          <h3 class="text-center text-info"> KRA with indicators </h3>

  

      `
    )
    
    performanceAnalysisCard(performanceData)


    if (ministryDetails.length > 0) {
      let kra_lists = ministryDetails.map((kra) => {
        return `
        <h6 name="kra-lists" class="pt-3 col-6"><span class="badge" style="background-color: ${kra?.ministry_key_result_area_score_card?.scorecard_color};">  ${Math.floor(kra?.ministry_key_result_area_score_card?.avg_score) || 0}</span> &nbsp ${kra.activity_name_eng}</h6>
         ${indicatorList(kra.indicators).join("")}
          `;
      });
      let kraHTML = `
           <div class="row">
              ${kra_lists.join("")}
          </div> `;

      $("#ministryKra").append(`
       <div class="form-check mb-2">
          <input class="form-check-input" type="checkbox" value="" id="showIndicator"> 
          <label class="form-check-label" for="showIndicator">Show with Indicator</label>
       </div>
 

       <h1 name="indicator-lists" class="d-none">Indicators</h1>
       <p name="indicator-lists" class="d-none fw-bold" >Click on an indicator for values, time series, and metadata.</p>

       <div name="indicator-lists" class="d-none row gap-2">

            
            <div class="col-md-2 d-flex align-items-center">
                <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #28A745;"></div>
                <div class="ms-2">Very Good Perf <br>  (95% - 100%)</div>
            </div>
    

            <div class="col-md-2 d-flex align-items-center">
                <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #8BC34A; "></div>
                <div class="ms-2">&nbsp Good Perf <br> &nbsp; (85% - 94%) </div>
            </div>

            <div class="col-md-2 d-flex align-items-center">
                 <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #FFC107; "></div>
                 <div class="ms-2">&nbsp Average Perf <br> &nbsp; (65% - 84%)</div>
            </div>

            <div class="col-md-2 d-flex align-items-center">
                 <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #FF9800; "></div>
                 <div class="ms-2">&nbsp Low Perf <br> &nbsp; (50% - 64%)</div>
            </div>

            <div class="col-md-2 d-flex align-items-center">
                <div class="border rounded-circle d-flex" style="height: 30px; width: 30px; background-color: #DC3545; "></div>
                <div class="ms-2">&nbsp Very Poor Perf <br> &nbsp; (0% - 49%) </div>
            </div>

        </div>


        <p name="indicator-lists" class="mt-4 d-none fw-bold" >Comparing with last year</p>
        <div name="indicator-lists" class="d-none d-flex align-items-center ">
            <div class="flex-shrink-0">
               <i class="fas fa-arrow-up text-success " style=" font-size: 22px;"></i>
            </div>
            <div class="pe-5"> &nbsp Increasing</div>
    
            <div class="flex-shrink-0">
              <i class="fas fa-arrow-right " style=" font-size: 22px;"></i>
            </div>
            <div class="pe-5"> &nbsp Constant</div>
    
            <div class="flex-shrink-0">
                <i class="fas fa-arrow-down text-danger " style=" font-size: 22px;"></i>
            </div>
            
            <div class="pe-5"> &nbsp Decreasing</div>
        </div>


       ${kraHTML}
       `)
    } else {
      $("#ministryKra").append(`
      <h4 class="text-center text-danger mb-5">No data found for this goal</h4>
      `);
    }};



    
    
    const performanceAnalysisPieChart = (id,value,color) =>{
      $("#"+id).html('')
      
      var options = {
        series: [value],
        chart: { height: 190, type: "radialBar",  parentHeightOffset: 0,  sparkline: {enabled: true}},
        colors: [color],
        plotOptions: {
          radialBar: {
            hollow: {
              margin: 0,
              size: "60%",
              background: "transparent",
              imageOffsetX: 0,
              imageOffsetY: 0,
              position: "front",
        },
        track: { background: "#f2f2f2", strokeWidth: "150%" },
        dataLabels: {
          show: !0,
          name: { show: !1 },
          value: {
            formatter: function (e) {
              return parseInt(e) + "%";
            },
            offsetY: 7,
            color: color,
            fontSize: "20px",
            fontWeight: "700",
            show: !0,
          },
        },
      },
    },
    stroke: { lineCap: "round" },
    fill: { type: "solid" },
      };

      var chart = new ApexCharts(document.querySelector(`#${id}`), options);
      chart.render();
    }
   


 
});















