$(document).ready(()=>{  
    const colorList = ['green', 'blue', 'indigo', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'cyan']
    const colorCOode = ['#2ca87f', '#4680ff', '#6610f2', '#673ab7', '#e83e8c', '#dc2626', '#fd7e14', '#e58a00', '#2ca87f', '#008080', '#3ec9d6']
    
    const randomColor = ()=> colorList[Math.floor(Math.random()*colorList.length)]

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
    
    const fetchData =async(url)=>{
        let response = await axios.get(url)
        try{
           return response.data
        }catch(err){
            console.log(err)
        }
    }

    const goalSharePieChart = (label , value, color) =>{
      $("#piechart").html('')
      let colorCode = colorList.findIndex((item)=> item == color)
      color = colorCOode[colorCode]

      new ApexCharts(document.querySelector("#piechart"), {
        chart: { height: 400, type: "pie" },
        labels: label,
        series: value,
        title: {
          text: 'Goal Weight',
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
        legend: { position: 'bottom' },
        dataLabels: { enabled: !0, dropShadow: { enabled: !1 } },
        responsive: [
            {
                breakpoint: 575,
                options: { chart: { height: 250 }, dataLabels: { enabled: !1 } },
            },
        ],
    }).render()


    }

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

    const performanceAnalysisCard = (data) =>{

      $("#performanceAnalysis").html('')
      
      data.forEach((item,index) =>{
        let card = `
        <div class="col-md-3 card">
            <div class="card-body p-2 m-0">
                <div class="row justify-content-center">
                    <div class="col-5">
                        <div id="total-performance-graph-${index}" class="p-0 m-0"></div>
                    </div>
                    <div class="col-7 d-flex align-items-center">
                         <div class="w-100"><p class="mb-1 fw-bold">${item.title}</p></div>
                         <div class="w-100">  <h1 class="w-100 p-2 fw-bold">${item.value}</h1></div>
                    </div>
                </div>
            </div>
        </div>`
        $("#performanceAnalysis").append(card)
        performanceAnalysisPieChart(`total-performance-graph-${index}`, item?.percentage || 0, item.color)
    
      })
       
     
     

    }
    const chartProgress = (percent) =>{
      $(`#chart-progress-policy-area`).html('')
        let options = {
            series: [percent],
            chart: {
            height: 200,
            type: 'radialBar',
          },
          plotOptions: {
            radialBar: {
              startAngle: -135,
              endAngle: 225,
               hollow: {
                margin: 0,
                size: '70%',
                background: '#fff',
                image: undefined,
                imageOffsetX: 0,
                imageOffsetY: 0,
                position: 'front',
                dropShadow: {
                  enabled: true,
                  top: 3,
                  left: 0,
                  blur: 4,
                  opacity: 0.24
                }
              },
              track: {
                background: '#fff',
                strokeWidth: '67%',
                margin: 0, // margin is in pixels
                dropShadow: {
                  enabled: true,
                  top: -3,
                  left: 0,
                  blur: 4,
                  opacity: 0.35
                }
              },
          
              dataLabels: {
                show: true,
                name: {
                  offsetY: -10,
                  show: true,
                  color: '#888',
                  fontSize: '17px'
                },
                value: {
                  formatter: function(val) {
                    return parseInt(val);
                  },
                  color: '#111',
                  fontSize: '36px',
                  show: true,
                }
              }
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'dark',
              type: 'horizontal',
              shadeIntensity: 0.5,
              colorStops: [
          {
            offset: 0,
            color: '#80b918'
          },
          {
            offset: 50,
            color: '#dddf00'
          }
        ],
              inverseColors: true,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100]
            }
          },
          stroke: {
            lineCap: 'round'
          },
          labels: ['Percent'],
          };
  
          let chart = new ApexCharts(document.querySelector(`#chart-progress-policy-area`), options);
          chart.render();
        
    }

    const chartProgressVsPerformance = (years, target , performance) => {
      $("#indicator-key-performance-chart").html("")
      var options = {
        series: [{
        name: 'Target',
        data: target
      }, {
        name: 'Performance',
        data: performance
      }],
        chart: {
        type: 'bar',
        height: 350,
        parentHeightOffset: 0,
        toolbar: {
          show: false
        }
      },
      grid: {
        show: true
    },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '85%',
          endingShape: 'rounded'
        },
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: years,
      },
      yaxis: {
      },
      fill: { colors: ["#2ca87f", "#A0D683"]},
      colors: ["#2ca87f", "#A0D683;"],
      stroke: { show: !0, width: 3, colors: ["transparent"] },
        title: {
          text: "Target Vs Performance",
          align: 'left',
          margin: 15,
          offsetX: 0,
          offsetY: 0,
          floating: false,
          style: {
            fontSize:  '14px',
            fontWeight:  'bold',
            color:  '#263238'
          },
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return  val 
          }
        }
      }
      };

      var chart = new ApexCharts(document.querySelector("#indicator-key-performance-chart"), options);
      chart.render();
    }

    const modalIndicatorAnnualPlan = (data) => {
      let previous = 0
        let table = data.map((item) =>{
          let diff = Math.floor(item.annual_performance - previous)
          let direction = diff > 1 ? 'fa-arrow-up' : diff >= 0 &&  diff == 0 ? 'fa-arrow-right': 'fa-arrow-down'
          let directionColor = diff > 1 ? 'text-success' : diff >= 0 &&  diff == 0 ? 'text-dark': 'text-danger'

          return `
            <tr>
              <td>${item.year}</td>
              <td>${item.annual_target || 'None'}</td>
              <td>${item.annual_performance || 'None' }</td>
              <td class="fw-bold" style="color: ${item.scorecard || 'red'}" >${item.score}</td>
              <td class="${directionColor} fw-bold"> <i class="fas ${direction} fa-sm "></i> ${diff}</td>
              <td class="${directionColor} fw-bold">${Math.floor((diff/previous)*100, 2) | "-"}%</td>
            </tr>
            ${previous = item.annual_performance}
          `
        })

        $("#modalAnnualPlanTable").html(table)
    }

    const policyAreaCard = async() =>{

      let type = $("#dataType").val()
      let typeValue = $("#dataTypeLists").val()
      let url = `/api/policy-area/${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`

      preLoading('policyAreaCardLists', 12, 2)  //loading -> htmlId, num of repeat, num of column 
      let data = await fetchData(url)


        const card = data.map((area, index)=>{
            let color = randomColor()
            let avgScore = Math.floor(area?.policy_area_score_card?.avg_score) 
            let direction = avgScore > 60 ? 'fa-arrow-up' : avgScore >= 50 &&  avgScore <= 60 ? 'fa-arrow-right': 'fa-arrow-down'
            return`
            <div class="col-6 col-sm-4 col-xl-2">
            <div class="card card-shadow  m-1 " data-policy-area="${area.id}" data-score="${avgScore}" data-color="${color}" name="policy-area-card">
                <div class="row ">
                    <div class="col-8 rounded-start bg-${color}-700 rounded-start" >
                        <div class="row justify-content-center  mt-3 text-white">
                            <div class="col-2  p-0 m-0">
                                <p class="fw-bold   p-0 m-0 ms-2" style="font-size: 10px;">${index+1}</p>
                            </div>
                            <div class="col-10 p-0 m-0 ">
                                <p class="font-monospace p-0 m-0  text-start"  data-bs-toggle="tooltip" data-bs-placement="top" title="${area.policyAreaEng}" style="font-size: 9px;">${area.policyAreaEng.slice(0,25)}...</p>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <i class="fas ${area.icon ? 'fa-'+area.icon.split(',')[1]:'fas fa-tractor'} fa-2x text-center text-white pb-4"></i>
                        </div>

                    </div>
                    <div class="col-4 align-items-center d-flex">
                        <div>
                            <i class="fas ${direction}  fa-2x  text-center" style="color: ${area?.policy_area_score_card?.scorecard_color} "></i>
                            <div class="text-center mt-2 p-1 " style="border-style: solid;  border-width: 1px; border-color: var(--bs-${color})">${Math.floor(area?.policy_area_score_card?.avg_score)}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
            `
        })

        $("#policyAreaCardLists").html(card)
    }

    const goalListCard = (goals, color) =>{

        let card = goals.map((goal) =>{
            return `
            <div class="col-6 col-lg-4">
                <div class="card card-shadow " name="goal-card" data-goal-name="${goal.goal_name_eng}" data-goal="${goal.id}" style="height : 200px; border-style: solid;  border-width: 1px; border-color: var(--bs-${color})">
                    <div class="card-body">
                      <div class="mb-2 row justify-content-between">
                        <div class="col-6 text-start fw-bold">${goal?.responsible_ministries?.code}</div>
                        <div class="col-6 text-end"><img src="${goal?.responsible_ministries?.image}" alt="" style="width: 30px; height: 30px" class="img-fluid"></div>
                      </div>    
                      <h6 class="mb-2 f-w-400  data-bs-toggle="tooltip" data-bs-placement="top" title="${goal.goal_name_eng}" text-muted">${goal.goal_name_eng.length > 45 ? goal.goal_name_eng.slice(0,45)+'...' : goal.goal_name_eng}</h6>
                    </div>

                    <div class="card-footer border-0">
                      <div class="w-100 progress border border-2 " style="height: 20px">
                          <div class="progress-bar" role="progressbar" style="width: ${Math.floor(goal.goal_score_card.avg_score) || 0}%; background-color : ${goal.goal_score_card.scorecard_color};)" aria-valuenow="${Math.floor(goal.goal_score_card.avg_score) || 0}" aria-valuemin="0" aria-valuemax="100">${Math.floor(goal.goal_score_card.avg_score) || 0}%</div>
                      </div>
                     
                    </div>

                </div>
            </div>
            `
        })

        $("#goalListCard").html(card)
    }

    const indicatorList = (indicators) =>{
        return indicators.map((indicator) =>{
    
          let previousIndicator = indicator?.annual_indicators?.find((item) => item.year == (indicator?.annual[0].year-1) )
          let diff = Math.floor(indicator?.annual[0]?.annual_performance - previousIndicator.annual_performance)
          let direction = diff > 1 ? 'fa-arrow-up' : diff >= 0 &&  diff == 0 ? 'fa-arrow-right': 'fa-arrow-down'
          let directionColor = diff > 1 ? 'text-success' : diff >= 0 &&  diff == 0 ? 'text-dark': 'text-danger'
      
          let hasTarget = indicator?.annual[0]?.annual_target ? 'primary' : 'secondary'
          let score = indicator?.annual[0]?.score || 0
          
          return `
              <div name="indicator-lists" class="col-lg-4 mt-1 d-none">
                  <div>
                      <div class="d-flex align-items-center">
                          <div class="flex-shrink-0">
                            <span class="p-2 d-block rounded-circle"  style=" font-size: 22px; background-color: ${indicator?.annual[0]?.scorecard || 'red'}"></span>
                          </div>
                          <div class="ml-3"> &nbsp <i class="fas ${direction}  ${directionColor}  " style=" font-size: 22px;"></i></div>
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

    const goalWithKraList = (goal) =>{        
        let kra_lists = goal.kra_goal.map((kra) =>{
          return `
          <h6 name="kra-lists" class="pt-3" >${kra.activity_name_eng} - AVG SCORE (<span class="badge" style="background-color: ${kra?.kra_score_card?.scorecard_color};"> ${Math.floor(kra?.kra_score_card?.avg_score) || 0} </span>)</h6>
          ${indicatorList(kra.indicators).join('') || '<p name="indicator-lists"  class="d-none fw-bold text-danger" >No indicators</p>'}
          `
        })

        let goalHtml = `
           <div class="row mt-5">
              <h3>${goal.goal_name_eng}</h3>
              <p class="fw-bold">Key Result Areas</p>
              ${kra_lists.join('')}
          </div> `


       $("#goalWithKraList").html(`

       <div class="form-check mb-2">
          <input class="form-check-input" type="checkbox" value="" id="showIndicator"> 
          <label class="form-check-label" for="showIndicator">Show with Indicator</label>
       </div>
 

       <h1 name="indicator-lists" class="d-none">Indicators</h1>
       <p name="indicator-lists" class="d-none fw-bold" >Click on an indicator for values, time series, and metadata.</p>

        <div name="indicator-lists" class="d-none d-flex align-items-center">
            <div class="flex-shrink-0">
              <span class="p-2 d-block rounded-circle" style="background-color: #28A745; "></span>
            </div>
            <div class="pe-5"> &nbsp Very Good Performance</div>

            <div class="flex-shrink-0">
              <span class="p-2 d-block rounded-circle " style="background-color: #8BC34A; "></span>
            </div>
            <div class="pe-5"> &nbsp Good Performance</div>

            <div class="flex-shrink-0">
              <span class="p-2 d-block rounded-circle " style="background-color: #FFC107; "></span>
            </div>
            <div class="pe-5"> &nbsp Average Performance</div>

            <div class="flex-shrink-0">
              <span class="p-2 d-block rounded-circle " style="background-color: #FF9800; "></span>
            </div>
            <div class="pe-5"> &nbsp Low Performance</div>

            <div class="flex-shrink-0">
              <span class="p-2 d-block rounded-circle " style="background-color: #DC3545; "></span>
            </div>
            <div class="pe-5"> &nbsp Very Poor Performance</div>
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

    const selectedPolicyAreaCard = (data, color, score) =>{
       let card = `
        <div class="col-md-6 col-lg-4 ">
            <div class="card bg-${color}-700 h-100 dropbox-card ">
                <div class="card-body">
                    <div class="d-flex align-items-center justify-content-between">
                        <h5 class="text-white">${data.policyAreaEng}</h5>
                            <div> <i class="fas ${data.icon ? 'fa-'+data.icon.split(',')[1]:'fas fa-tractor'} text-white" style="font-size:80px"></i></div>
                    </div>
                    <div class="d-flex align-items-center h-75">
                         <div class="col" id="chart-progress-policy-area"></div> 
                    </div>
                    
                </div>
            </div>
        </div>
        ` 
        $("#policyAreaMainCard").html(card)
        


        $("#policyAreaMainCard").append(`
            <div class="col-md-6 col-lg-8">
                <h3>Goals</h3>
                <div class="row h-100 mt-3" id="goalListCard">
                </div>
            </div>
        `)
       chartProgress(score)
       goalListCard(data?.policy_area_goal, color) //goal list 
      
        
    }

    const indicatorModal = (title, data) =>{
      $('#indicatorModalLabel').html(title)
      $('#kpi-unit').html(data.kpi_measurement_units || 'None')
      $('#kpi-char').html(data.kpi_characteristics)
      $('#kpi-weight').html(data.kpi_weight || 'None')
      $('#kpi-kra').html(data.keyResultArea > 5 ? data.keyResultArea.slice(0, 5) : data.keyResultArea)
      $('#kpi-ministry').html(data?.responsible_ministries?.code || 'None')

      let years = data.annual_indicators.map((year) => year.year)
      let performance = data.annual_indicators.map((performance) => performance.annual_performance || 0)
      let target = data.annual_indicators.map((target) => target.annual_target || 0)

      chartProgressVsPerformance(years, target, performance) //modal chart
      modalIndicatorAnnualPlan(data.annual_indicators)

     


    }

    const dashboardCard = async() =>{

      preLoading('dashboardInfo', 4, 3)  //loading -> htmlId, num of repeat, num of column
      let data = await fetchData('/api/dashboard/')

      const icon = ['briefcase', 'bullseye', 'suitcase', 'chart-line']
      let color = randomColor()

      let card = data.dashboard.map((card, index) =>{
        return`
        <div class="col-md-6 col-xl-3">
            <div  class="card social-widget-card bg-${color}-500">
                <div class="card-body">
                    <h2 class="text-white m-0">${card.value}</h2>
                    <span class="fw-bold">Number of ${card.title}</span>
                    <i style="font-size: 80px;" class="fas fa-${icon[index]}"></i>
                </div>
            </div>
        </div>
        `
      })

      $("#dashboardInfo").html(card)
    }

    const scrollToDiv = (id) =>{
       //scroll to the target div
       const element = document.getElementById(id);
       element.scrollIntoView({ behavior: 'smooth' });
       
    }


    const filterDataOption = async() =>{
      let data = await fetchData(`/api/time_series_year/`)

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
    
    const policyAreaDashboard = (data, color) =>{
      let card = data?.map((dashboard) =>{
        
        return `
        <div class="col-md-2 card  available-balance-card bg-${color}-700">
        <div class="card-body p-3">
            <div class="d-flex align-items-center justify-content-between">
                <div>
                    <p class="mb-0  text-white text-opacity-75">${dashboard?.title}</p>
                </div>
                <div class="avtar">
                    <h4 class="mb-0 text-white">${dashboard?.value}</h4>
                </div>
            </div>
        </div>
    </div>`
      })
     
  $("#policyAreaDashboard").html(card)
    }

    const policyAreaDashboard2 = (data) =>{

      let card = data?.map((item) =>{
        return  `
        <div class="card">
        <div class="card-body">
            <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                    <div class="avtar bg-light-${item.color}">
                        <i class="${item.icon} f-24"></i>
                    </div>
                </div>

                <div class="text-start ms-4">
                    <p class="mb-1 fw-bold">${item?.title}</p>
                      <h4 class="mb-0 text-${item?.color}">${item?.value}</h4>
                </div>

            </div>
        </div>
    </div>`
  
      })
      
     
  $("#overAllPerformanceAnalysis").html(card)}

    const policyAreaWithSDGGraph = async() =>{
      let data = await fetchData('/api/policy_area_SDG/')
      let node = []

      data.policy_areas.forEach((item) => {
        node.push({ id: 'pa-'+item.id, title: item.policyAreaEng})
      })

      data.sdgs.forEach((item) => {
        node.push(
          { id: 'sdg-'+item.code, title: `${item.title} (${item.code})`})
      })

      data.agendas.forEach((item) => {
        node.push({
          id : `agenda-${item.id}`,
          title : item.title,
        })
      })

 


      let edge = []
      data.policy_areas.forEach((item) =>{
        item.sdg.forEach((sdg) =>{
          edge.push( {
            source : 'pa-'+item.id,
            target : 'sdg-'+sdg,
            value : item.num_of_goals * 2 > 5 ? item.num_of_goals * 2 : 5 || 5
          })
        })
      })

      data.agendas.forEach((item) =>{
        item.sdg.forEach((sdg) =>{
          edge.push( {
            source : 'sdg-'+sdg,
            target : 'agenda-'+item.id,
            value : item.num_of_sdg * 10 > 5 ? item.num_of_sdg * 10 : 5 || 5
          })
        })
      })



      const chardData = {
        nodes: node,
        edges: edge,
    };
    const graphOptions = {
      nodeWidth: 30,
      fontWeight: 600,
      width: 1300,
      fontSize: '13px',
      height: 1100,
    
    };
    const s = new ApexSankey(document.getElementById('goalShareTreeMapUpdated'), graphOptions);
    s.render(chardData);


      
    }


    const ministrySharesPyramid = async (data) => {
      const dataChart = [];
      const categories = [];
    
      for (const [key, value] of Object.entries(data)) {
        let sum = 0;
        let len = 0;
        let weight = 0
        data[key].map((item) => {
          sum += item?.goal_score_card?.avg_score ? item?.goal_score_card?.avg_score : 0;
          weight+=item?.goal_weight
          len++;
        });

        let avg = Math.floor((sum * weight)/(len*100));

        dataChart.push({
          data: avg || 0,
          categories: `${key} (${avg || 0 })%`,
        })
      }


      dataChart.sort((a,b) =>{
        if(a.data < b.data) return -1
        return 1
      })

    
      // Check if the chart already exists
      if (window.ministrySharesChart) {
        // Update the series and categories dynamically
        window.ministrySharesChart.updateOptions({
          series: [
            {
              name: "",
              data: dataChart.map((item) => item.data),
            },
          ],
          xaxis: {
            categories:  dataChart.map((item) => item.categories),
          },
        });
      } else {
        // Initial chart rendering
        var options = {
          series: [
            {
              name: "",
              data: dataChart.map((item) => item.data),
            },
          ],
          chart: {
            type: 'bar',
            height: 350,
            toolbar: {
              show: false,
            },
          },
          plotOptions: {
            bar: {
              borderRadius: 0,
              horizontal: true,
              distributed: true,
              barHeight: '80%',
              isFunnel: true,
            },
          },
          colors: [
            '#F44F5E',
            '#E55A89',
            '#D863B1',
            '#CA6CD8',
            '#B57BED',
            '#8D95EB',
            '#62ACEA',
            '#4BC3E6',
          ],
          dataLabels: {
            enabled: true,
            formatter: function (val, opt) {
              return opt.w.globals.labels[opt.dataPointIndex];
            },
            dropShadow: {
              enabled: true,
            },
          },
          title: {
            text: 'Ministries Shares',
            align: 'middle',
          },
          xaxis: {
            categories: dataChart.map((item) => item.categories),
          },
          legend: {
            show: false,
          },
        };
    
        window.ministrySharesChart = new ApexCharts(
          document.querySelector("#ministrySharesPyramid"),
          options
        );
        window.ministrySharesChart.render();
      }
    };
    

    const main = async() =>{
       await filterDataOption()
       dashboardCard()
       policyAreaCard()
       policyAreaWithSDGGraph()
    }

    main()
    
    
    


    $(document).on('click', "[name='policy-area-card']", async function() {
      $("#goalPerformanceAnalysisName").html('')
      $("#policyAreaMainCard").html('')
      $("#overAllPerformanceAnalysis").html('')
      $("#goalWithKraList").html('')
      $("#performanceAnalysis").html('')


      const policyAreaId = $(this).data('policyArea');
      const score = $(this).data('score');
      const color = $(this).data('color');

    
      try {

        let type = $("#dataType").val()
        let typeValue = $("#dataTypeLists").val()

        //check is year or quarter
        let url = `/api/policy-area/${policyAreaId}/${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
       

        preLoading('policyAreaMainCard', 4, 3)  //loading -> htmlId, num of repeat, num of column
        let data = await fetchData(url); //fetch data


        const ministriesShare = Object.groupBy(data.policy_area_goal, ({responsible_ministries})=>{
          return responsible_ministries.code
        });



        let policyAreaDashboardData = [
          {
          title : 'Number Of Goal',
          value : data.count_goal
         },
         {
          title : 'Number Of Key Result Area',
          value : data.count_kra
         },
         {
          title : 'Number Of Indicator',
          value : data.count_indicator
         },
        ]

        let policyAreaDashboardData2 = [
          {
            title : '(Num) Indicator have target',
            value : data.count_indicator_target,
            icon : 'fas fa-bullseye',
            color : 'primary'
          },
          {
            title : '(Num) Indicator have Target and Performance',
            value : data.count_indicator_have_performance,
            icon : 'fas fa-chart-bar',
            color : 'success'
          },
          {
            title : '(Num) Indicator have Target and No Performance',
            value : data.count_indicator_have_target_and_no_performance,
            icon : 'fas fa-sort-amount-down',
            color : 'danger'
          },
        ]


        function normalizeTo100(arr) {
          const sum = arr.reduce((acc, val) => acc + parseFloat(val), 0); // Calculate the sum of the array
          const multiplier = 100 / sum; // Find how much we need to multiply each value to make the total 100
      
          // Adjust each value proportionally to make the total sum 100
          const normalized = arr.map(val => parseFloat(val) * multiplier);
      
          // Optional: Round to 2 decimal places
          return normalized.map(val => Math.round(val * 100) / 100);
      }

      
        let shareGoalNameLists = data?.policy_area_goal?.map((goal)=> goal.goal_name_eng.slice(0,15)+"...")
        let shareGoalValueLists = data?.policy_area_goal?.map((goal)=>goal.goal_weight || 0)

           //ministries share for policy area
           ministrySharesPyramid(ministriesShare)

        
        //policy area dashboard
        policyAreaDashboard(policyAreaDashboardData, color)
        policyAreaDashboard2(policyAreaDashboardData2)


        //pie chart goal share
        goalSharePieChart(shareGoalNameLists,normalizeTo100(shareGoalValueLists), color)

        // Render selected policy area card and goal list
        selectedPolicyAreaCard(data, color, score);

     

      } catch (error) {
          console.error("Error fetching or rendering data:", error);
      }

      //scroll to the target div
      scrollToDiv('scroll')

       
  });
  

    $(document).on('click', "[name='goal-card']", async function() {
      const goalId = $(this).data('goal')
      const goalName = $(this).data('goalName')


      let type = $("#dataType").val()
      let typeValue = $("#dataTypeLists").val()
      let url = `/api/goal_with_kra/${goalId}/${type == 'year' ? '?year='+typeValue : '?year='+typeValue.split('-')[0]+'&quarter='+typeValue.split('-')[1]}`
    


      preLoading('goalWithKraList', 4, 3)  //loading -> htmlId, num of repeat, num of column
      let data = await fetchData(url)

     
      goalWithKraList(data, goalName)

      //performance analysis card

      //scroll to the target div
      scrollToDiv('scrollIndicator')

      const performanceData = [{
        title : 'Good Performance',
        value : data?.good_performance?.performance || 0,
        percentage : data?.good_performance?.percentage || 0,
        
        color : '#2ca87f'
      },
      {
        title : 'Average Performance',
        value : data?.average_performance?.performance || 0,
        percentage : data?.average_performance?.percentage || 0,
        color : '#fd7e14'
      },
      {
        title : 'Poor Performance',
        value : data?.poor_performance?.performance || 0,
        percentage : data?.poor_performance?.percentage || 0,
        color : '#dc2626'
      }
    ]

      performanceAnalysisCard(performanceData) 
      $("#goalPerformanceAnalysisName").html(goalName + " Performance Analysis") // change performance title by goal name
    })


    $(document).on('click', "[name='indicator-btn']", async function() {
      const indicatorId = $(this).data('indicatorId')
      const indicatorName = $(this).data('indicatorName')
      const goal = $(this).data('goal')

      let data = await fetchData(`/api/indicator/${indicatorId}/`)

      $('#kpi-goal').html(goal || 'None')
      indicatorModal(indicatorName, data)

  
    })


    $("#dataTypeLists").on('change', ()=>{
      $("#selectedDataValue").html($("#dataTypeLists").val())

      $("#policyAreaDashboard").html('')
      $("#policyAreaDashboard2").html('')
      $("#piechart").html('')
      
      $("#goalPerformanceAnalysisName").html('')
      $("#policyAreaMainCard").html('')
      $("#overAllPerformanceAnalysis").html('')

      $("#goalWithKraList").html('')
      $("#performanceAnalysis").html('')



      policyAreaCard()
     
    })

    $('#dataType').on('change', ()=>{

      $("#policyAreaDashboard").html('')
      $("#policyAreaDashboard2").html('')
      $("#piechart").html('')
      
      $("#goalPerformanceAnalysisName").html('')
      $("#policyAreaMainCard").html('')
      $("#overAllPerformanceAnalysis").html('')

      $("#goalWithKraList").html('')
      $("#performanceAnalysis").html('')


      policyAreaCard()      
    })


    const AnnualIndicatorModalTable = (indicators, years) => {
      let tableDataIndicator =  indicators.map((indicator, index)=>{
        return `
        <tr>
          <td> ${index + 1} </td>
          <td class="text-wrap"> ${indicator.kpi_name_eng} </td>
          <td class="text-wrap"> ${indicator.responsible_ministries}</td>
          ${years.map((year) =>{
            let value = indicator.annual_indicators.find((item) => item.year == year.year_amh)
            return`
            <td>
                <div class="d-grid gap-2">                                      
                  <button type="button" title="Annual Target" class="btn btn-success d-block btn-sm rounded-1">${value?.annual_target || '-'}</button>
                  <button type="button" title="Anuual Performance" class="btn btn-info d-block  btn-sm rounded-1">${value?.annual_performance || '-'}</button>
                </div>
            </td>
            `
          } 
          
          ).join('')}
        </tr>
        `
      })


      return `<thead>
            <tr>
              <th style="width:50px; scope="col">#</th>
              <th  style="width:300px; scope="col">Name</th>
              <th style="width:200px; scope="col">Responsible Ministry</th>
              ${years.map(year => {
                return (
                  `<th style="width:100px; scope="col">${year.year_amh}</th>`
                  )
              } ).join('')}
            </tr>
         </thead> 
          <tbody> 
              ${tableDataIndicator.join('')} 
         </tbody>`
      

    }


    $("#search").on('submit', async(e)=>{
      e.preventDefault()
      let value = $("#searchValue").val()

      //pre loader
      $("#searchResult").html(`
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>`)


      let search = await fetchData(`/api/search/?q=${value}`)


      if(search){
        $("#searchResult").html(
        `
        <h3 class="fw-bold">Search results</h3>
        <p class="mt-5 fw-bold" id="goal_result_count">Goals - total result (16)</p>
        <div class="scrollable card table-responsive table-hover">
            <table style="table-layout: fixed;" class="table" id="tableGoal">
            </table>
          </div>

          <p class="mt-5 fw-bold" id="kra_result_count">Key Result Area - total result (16)</p>
          <div class="scrollable card table-responsive table-hover">
            <table style="table-layout: fixed;" class="table" id="tablekra">
            </table>
          </div>


          <p class="mt-5 fw-bold" id="indicator_result_count" >Indicator - total result (16)</p>
          <div class="scrollable card table-bordered table-responsive table-hover">
            <table style="table-layout: fixed;" class="table" id="tableIndicator">
            </table>
          </div>
        `)

         //Goal Search
         let tableDataGoal =  search.goals.map((kra, index)=>{
          return `
          <tr>
            <td> ${index + 1} </td>
            <td class="text-wrap "> ${kra.goal_name_eng} 
             <a type="button" data-id="${kra.id}" name="search-goal" class="text-success" data-bs-toggle="modal" data-bs-target="#searchGoalDetail"> <i class="fas fa-eye"></i>
             </a> 
             </td>
            <td class="text-wrap"> ${kra.policy_area}</td>
          </tr>
          `
        })

        $("#tableGoal").html(
          `<thead>
              <tr>
                <th style="width:50px; scope="col">#</th>
                <th  style="width:300px; scope="col">Name</th>
                <th  style="width:100px; scope="col">Policy Area</th>
              </tr>
           </thead> 
            <tbody> 
                ${tableDataGoal} 
           </tbody>`
        )

        $("#goal_result_count").html(`Goals - total result (${search.goals.length})`)


         //Kra Search
         let tableDataKra =  search.kras.map((kra, index)=>{
          return `
          <tr>
            <td> ${index + 1} </td>
            <td class="text-wrap"> ${kra.activity_name_eng}  
              <a type="button" name="search-kra" class="text-success" data-id="${kra.id}" data-bs-toggle="modal" data-bs-target="#searchKraDetail">  <i class="fas fa-eye"></i>  </a>  
            </td>
            <td class="text-wrap"> ${kra.activity_name_amh}</td>
            <td class="text-wrap"> ${kra.goal}</td>
          </tr>
          `
        })


        $("#tablekra").html(
          `<thead>
              <tr>
                <th style="width:50px; scope="col">#</th>
                <th style="width:300px; scope="col">Name</th>
                <th style="width:100px; scope="col">Characteristics</th>
                <th style="width:200px; scope="col">Goal</th>
              </tr>
           </thead> 
            <tbody> 
                ${tableDataKra} 
           </tbody>`
        )

        $("#kra_result_count").html(`Key Result Area - total result (${search.kras.length})`)

       

        //Indicator Search
        $("#tableIndicator").html(AnnualIndicatorModalTable(search.indicators, search.years))

        $("#indicator_result_count").html(`Indicator - total result (${search.indicators.length})`)


        
       




      //handle on modal open for detail
      $("[name=search-kra]").on("click", async function () {
        let kraId  = $(this).data("id")

        let data = await fetchData(`/api/search/kra/${kraId}/`)
        //update modal title
        $("#searchKraDetailLabel").html('Key Result Area Details - ' + data.kra.activity_name_eng)

        //create table
        $("#searchKeyResultAreaDetails").html(`
        <div class="table-responsive">
         <table class="table-bordered table-hover">
           ${AnnualIndicatorModalTable(data.kra.indicators, data.years)}
         </table>
         </div>
        `)
      })


      $("[name=search-goal]").on('click', async function () {
        let goalId = $(this).data("id")

        let data = await(fetchData(`/api/search/goal/${goalId}/`))

        data?.goal?.kra_goal?.forEach((kra) => {
           //create table
        $("#searchGoalDetails").append(`
        <h4 class="mt-5 mb-2">${kra.activity_name_eng}</h4>
        <div class="table-responsive">
         <table class="table-bordered table-hover">
           ${AnnualIndicatorModalTable(kra.indicators, data.years)}
         </table>
         </div>
        `)
      }
      
      )          
        })




      }

    })



    const handleAutoComplete = () => {
      $('#searchValue').on('keydown', async()=>{
       let value = $("#searchValue").val()
       let data = await fetchData(`/api/search_auto_complete/?q=${value}`)


       $("#datalistOptions").html('') //update list to empty

       let indicators = data.indicators.map(item => ` <option value="${item}"></option>`).join('')
       let kras = data.kras.map(item => ` <option value="${item}"></option>`).join('')
       let goals = data.goals.map(item => ` <option value="${item}"></option>`).join('')

       $("#datalistOptions").append(indicators + kras + goals)
      })
    }

    handleAutoComplete()

    $(document).on('change', '#showIndicator', async function () {
      let value = $('#showIndicator').prop('checked')
      value ? $("[name='indicator-lists']").removeClass('d-none') :  $("[name='indicator-lists']").addClass('d-none')
      value ? $("[name='kra-lists']").addClass('mt-3') :  $("[name='kra-lists']").removeClass('mt-3')
    })
   
    

})