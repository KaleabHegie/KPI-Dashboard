const bgColorList = [
  "#0f172a", // Slate 900
  "#b91c1c", // Red 700
  "#065f46", // Emerald 800
  "#1e3a8a", // Blue 800
  "#ca8a04", // Yellow 600
  "#0e7490", // Cyan 700
  "#7e22ce", // Purple 800
  "#374151", // Gray 700
  "#9f1239", // Rose 700
  "#713f12", // Amber 800
  "#312e81", // Indigo 900
  "#5b21b6", // Violet 800
  "#15803d", // Green 700
  "#7c2d12", // Orange 800
  "#be123c", // Pink 700
  "#166534", // Green 800
  "#4338ca", // Indigo 700
  "#6366f1", // Indigo 500
  "#1f2937", // Gray 800
  "#92400e", // Orange 700
  "#dc2626", // Red 600
  "#047857", // Emerald 700
  "#4a5568", // Gray 600
  "#075985", // Sky 700
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

const fetchData = async (url) => {
  let response = await axios.get(url);
  try {
    return response.data;
  } catch (err) {
    console.log(err);
  }
};

const chartProgress = (id, percent, color) => {
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
  const isMobile = window.innerWidth < 768; // Define a breakpoint for mobile
  const chartHeight = isMobile ? "50%" : "50%"; // Larger height for mobile
  const paneSize = isMobile ? "90%" : "140%"; // Adjust pane size for mobile
  const labelFontSize = isMobile ? "10px" : "14px"; // Smaller font for mobile
  const dataLabelFontSize = isMobile ? "12px" : "16px"; // Adjust data label font

  Highcharts.chart(`chartdiv${id}`, {
    chart: {
      type: "gauge",
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      height: chartHeight, // Responsive height
      backgroundColor: "transparent",
    },
    credits: {
      enabled: false,
    },
    title: {
      text: "",
    },
    pane: {
      startAngle: -90,
      endAngle: 89.9,
      background: null,
      center: ["50%", "75%"],
      size: paneSize, // Responsive pane size
    },
    yAxis: {
      min: 0,
      max: 100,
      tickPixelInterval: 30,
      tickPosition: "inside",
      tickColor: "#fff",
      tickLength: 20,
      tickWidth: 2,
      minorTickInterval: null,
      labels: {
        distance: 20,
        style: {
          fontSize: labelFontSize, // Responsive label font size
          color: "#fff",
        },
      },
      lineWidth: 0,
      plotBands: [
        {
          from: 0,
          to: 25,
          color: "#DF5353", // red
          thickness: 20,
        },
        {
          from: 25,
          to: 50,
          color: "#ffa500", // orange
          thickness: 20,
        },
        {
          from: 50,
          to: 75,
          color: "#DDDF0D", // yellow
          thickness: 20,
        },
        {
          from: 75,
          to: 100,
          color: "#55BF3B", // green
          thickness: 20,
        },
      ],
    },
    exporting: { enabled: false },
    series: [
      {
        name: "Average score",
        data: [Math.floor(percent)], // Only one data point
        tooltip: {
          valueSuffix: "",
        },
        dataLabels: {
          format: "{y} ",
          borderWidth: 0,
          color:
            (Highcharts.defaultOptions.title &&
              Highcharts.defaultOptions.title.style &&
              Highcharts.defaultOptions.title.style.color) ||
            "#333333",
          style: {
            fontSize: dataLabelFontSize, // Responsive data label font size
          },
        },
        dial: {
          radius: "80%",
          backgroundColor: "white",
          baseWidth: 12,
          baseLength: "0%",
          rearLength: "0%",
        },
        pivot: {
          backgroundColor: "white",
          radius: 6,
        },
      },
    ],
  });
};

const ministryCard = async () => {
  let type = $("#dataType").val();
  let typeValue = $("#dataTypeLists").val();
  typeValue = 2016;
  let url = `/affiliated_ministries_list/${
    type == "year"
      ? "?year=" + typeValue
      : "?year=" +
        typeValue.split("-")[0] +
        "&quarter=" +
        typeValue.split("-")[1]
  }`;
  let data = await fetchData(url);
  $("#ministryCardLists").html(``);
  const card = data.map((ministry, index) => {
    return `
            <div class="col-6 col-lg-3">
                <div class="card card-shadow" style="height: 170px;" name="ministry-card" data-ministry="${ministry.id}" data-ministry-name="${ministry.responsible_ministry_eng}" data-ministry-image="${ministry.image}" >
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
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
            `;
  });

  $("#ministryCardLists").append(card);

  data.forEach((ministryData) => {
    let percent = Math.floor(Math.random() * 100);
    chartProgress(
      ministryData.id,
      ministryData.ministry_score_card.avg_score,
      ministryData.ministry_score_card.scorecard_color
    );
  });
};

const goalListCard = async (ministry_id, id, color, policy_area_name) => {
  let type = $("#dataType").val();
  let typeValue = $("#dataTypeLists").val();

  //check is year or quarter
  let url = `/api/ministry/policy_area_with_goal/${id}?ministry_id=${ministry_id}${
    type == "year"
      ? "&year=" + typeValue
      : "&year=" +
        typeValue.split("-")[0] +
        "&quarter=" +
        typeValue.split("-")[1]
  }`;
  let goals = await fetchData(url);

  let card = goals.policy_area_goal.map((goal) => {
    let avgScoreWidth =
      goal.ministry_strategic_goal_score_card.avg_score.toFixed(2);
    return `
   <div class="col-md-6">
   <div class="card card-shadow" style="height: 170px; border-style: solid; border-width: 1px; border-color: var(--bs-${color})" name="goal-card" data-goal="${
      goal.id
    }" data-goal-name="${
      goal.goal_name_eng
    }" data-color="${color}" data-score-color="${
      goal.ministry_strategic_goal_score_card.scorecard_color
    }" data-score="${avgScoreWidth}"  data-ministryId="${ministry_id}">
       <div class="card-body">
           <div class="h-100">
              <h6 class="mb-2 f-w-400  data-bs-toggle="tooltip" data-bs-placement="top" title="${
                goal.goal_name_eng
              }" text-muted">${
      goal.goal_name_eng.length > 45
        ? goal.goal_name_eng.slice(0, 45) + "..."
        : goal.goal_name_eng
    }</h6>
           </div>
       </div>
       <div class="card-footer">
                <div class="w-100 progress" style="height: 20px">
                       <div class="progress-bar" role="progressbar" style="width: ${avgScoreWidth}%; background-color:${
      goal.ministry_strategic_goal_score_card.scorecard_color
    };" aria-valuenow="${
      goal.ministry_strategic_goal_score_card.avg_score
    }" aria-valuemin="0" aria-valuemax="100">${avgScoreWidth}%</div>
                   </div>
       </div>
   </div>
</div>
   `;
  });

  let totalWight = 0;
  goals?.policy_area_goal?.forEach(
    (goal) => (totalWight += parseFloat(goal.goal_weight))
  );
  let shareGoalNameLists = goals?.policy_area_goal?.map(
    (goal) => goal.goal_name_eng
  );
  let shareGoalValueLists = goals?.policy_area_goal?.map(
    (goal) => goal.goal_weight || 0
  );
  let sentValue = shareGoalValueLists?.map((val) => (val * 100) / totalWight);

  return card.join("");
};

const filterDataOption = async () => {
  let data = await fetchData(`/year_quarter_list/`);

  const yearOption = () => {
    return data?.years?.map((year, index) => {
      return `<option ${
        index + 1 == data.years.length ? "selected" : ""
      } value="${year.year_amh}">${year.year_amh}</option>`;
    });
  };

  const quarterOption = () => {
    return data?.years?.map((year, indexYear) => {
      return data?.quarters?.map((quarter, indexQuarter) => {
        return `<option ${
          indexYear + 1 == data.years.length &&
          indexQuarter + 1 == data.quarters.length
            ? "selected"
            : ""
        }  value="${year.year_amh}-${quarter.quarter_eng}">${year.year_amh} (${
          quarter.quarter_eng
        })</option>`;
      });
    });
  };

  //call for first default option
  $("#dataTypeLists").html(yearOption());
  $("#selectedDataValue").html($("#dataTypeLists").val());

  //handle data type changed
  $("#dataType").on("change", () => {
    let dataType = $("#dataType").val();
    $("#dataTypeLists").html(
      dataType === "quarter" ? quarterOption() : yearOption()
    );
    $("#selectedDataValue").html($("#dataTypeLists").val());
  });
};

const selectedMinistryCard = async (
  ministry_name,
  ministry_id,
  color,
  ministry_image
) => {
  let type = $("#dataType").val();
  let typeValue = $("#dataTypeLists").val();

  //check is year or quarter

  let url = `/api/ministry/dashboard_ministries/${ministry_id}${
    type == "year"
      ? "?year=" + typeValue
      : "?year=" +
        typeValue.split("-")[0] +
        "&quarter=" +
        typeValue.split("-")[1]
  }`;
  let ministry_dashboard = await fetchData(url);

  ministryData = await fetchData(
    `/api/ministry/ministry_with_policy_area/${ministry_id}${
      type == "year"
        ? "?year=" + typeValue
        : "?year=" +
          typeValue.split("-")[0] +
          "&quarter=" +
          typeValue.split("-")[1]
    }`
  );

  $("#ministryKra").html(``);
  $("#policyAreaMainCard").html(``);
  $("#goalWithKraList").html(``);
  $("#ministryDashboard").html(``);
  $("#goalShare").html("");
  $("#goalShare").html('<h3 class="text-center">Goal Shares</h3>');
  $("#ministryDashboard").append(
    `
   
          <div class="mt-5">
             <h3 style="color: var(--bs-${color})">${ministry_name} <img src="${ministry_image}" alt="" class="img-fluid float-end mb-5" style="height:80px;width:95px" /> </h3>
             <hr class="mt-2">
          </div>
  
      
      <div id="dash" class="row justify-content-center mb-4">
      </div>
     

      `
  );
  ministry_dashboard.dashboard.forEach((dashboard, index) => {
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
    );
  });
  if (ministryData.length == 1) {
    ministryData.forEach(async (policy) => {
      let policyAreaCard = `
        <div class="col-lg-6" style="margin-bottom: 50px">
        <div style="background-color: ${
          bgColorList[Math.floor(Math.random() * bgColorList.length)]
        }" class="card h-100 dropbox-card" data-ministryId="${ministry_id}">
           <div class="card-body">
                <div class="d-flex align-items-center justify-content-between">
                    <h5 class="text-white">${policy.policyAreaEng}</h5>
                    <div><i class="fas ${
                      policy.icon
                        ? "fa-" + policy.icon.split(",")[1]
                        : "fa-tractor"
                    } text-white" style="font-size:80px"></i></div>
                </div>
                <div class="row justify-content-center ">
                    <div class="col chartdiv  pt-5 w-100 h-100" id="chartdiv${
                      policy.id
                    }"></div>
                </div>
            </div>
        </div>
    </div>
    `;

      $("#policyAreaMainCard").append(policyAreaCard);
      $("#goalShare").append(
        `<div class="col-md-5 text-center ">
                               <div class="row justify-content-center">
                                   <div id="piechart_${policy.id}"></div>
                               </div>
                </div>
        `
      );
      chartGauge2(
        policy.id,
        Math.floor(policy.ministry_policy_area_score_card.avg_score * 100) / 100
      );

      letGoalTest = await goalListCard(
        ministry_id,
        policy.id,
        color,
        policy.policyAreaEng
      );
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
  } else if (ministryData.length > 1) {
    ministryData.forEach(async (policy) => {
      $("#goalShare").append(
        `<div class="col-md-4 text-center ">
                               <div class="row justify-content-center">
                                   <div id="piechart_${policy.id}"></div>
                               </div>
                </div>
        `
      );

      letGoalTest = await goalListCard(
        ministry_id,
        policy.id,
        color,
        policy.policyAreaEng
      );

      let goalListCardHtml = `
      <div class="" style="margin-bottom: 50px">
         <h3>Goals</h3>
              <div class="row h-100 mt-3">
               ${letGoalTest}
              </div>
      </div>`;

      let policyAreaCard = `
                <div class="col-lg-6" style="margin-bottom: 50px;">
                    <div style="background-color: ${
                      bgColorList[
                        Math.floor(Math.random() * bgColorList.length)
                      ]
                    }" class="card dropbox-card" data-ministryId="${ministry_id}">
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
                                <div class="col chartdiv" id="chartdiv${
                                  policy.id
                                }"></div>
                            </div>
                        </div>
                    </div>

                    ${goalListCardHtml}
                    
                </div>
            `;

      $("#policyAreaMainCard").append(policyAreaCard);

      chartGauge2(policy.id, policy.ministry_policy_area_score_card.avg_score); // Display progress chart for the policy
    });
  } else {
    $("#policyAreaMainCard").append(`
          <div class="mt-5">
             <h4 class="text-center text-danger mb-5">No data found for this ministry</h4>
          </div>
          `);
  }
};



const selectedGoalCard = async (goal_id ,ministry_id , color, score, scoreColor) => {
    let type = $("#dataType").val()
    let typeValue = $("#dataTypeLists").val()
    
  
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
const main = async () => {
  await filterDataOption();
  ministryCard();
  $("#year").html($("#dataTypeLists").val());
};

$(document).on("click", "[name='ministry-card']", async function () {
  const ministry_id = $(this).data("ministry");
  const ministry_name = $(this).data("ministryName");
  const ministry_image = $(this).data("ministryImage");
  let type = $("#dataType").val();
  let typeValue = $("#dataTypeLists").val();

  //check is year or quarter
  let url = `/api/ministry/ministry_with_policy_area/${ministry_id}?${
    type == "year"
      ? "?year=" + typeValue
      : "?year=" +
        typeValue.split("-")[0] +
        "&quarter=" +
        typeValue.split("-")[1]
  }`;

  let data = await fetchData(url);

  selectedMinistryCard(ministry_name, ministry_id, ministry_image);
  $("html, body").animate(
    {
      scrollTop: $("#policyAreaMainCard").offset().top,
    },
    500
  );
});



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

main();
