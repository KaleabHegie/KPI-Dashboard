let randomColor = () => {
  const borderColors = [
    'primary', 'secondary', 
    'danger', 'warning', 'info'
  ];

  return borderColors[Math.floor(Math.random() * borderColors.length)];
}

let showLoadingSpinner = (div) => {
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

let hideLoadingSpinner = (div) =>{
  $(`#${div}`).html('')
}

let showLoadingSkeletonTopic = () => {
  for (let i = 0; i < 8; i++) {
    $("#loading-skeleton-topic").append(
      `
            <div class="col-md-6 col-xl-3 d-none d-md-block container loading-skeleton ">
               <div class="card social-widget-card">
                   <div class="card-body d-flex justify-content-between align-items-center p-2">
                    <div class="bg-body p-3 mt-3 rounded" style="height: 40px; width: 100%;">
                    </div>
                   </div>
               </div>
            </div>
            `
    );
  }
};

let hideLoadingSkeletonTopic = () => {
  $("#loading-skeleton-topic").html("");
};

let showLoadingSkeletonCategory = () => {
  $("#kra-card-list").html("")
  for (let i = 0; i < 6; i++) {
    $("#kra-card-list").append(`
        <div class="col-md-6 col-xxl-4 col-12 container loading-skeleton">
            <div class="card" >
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="flex-shrink-0">
                        </div>
                        <div class="flex-grow-1 ms-3" >
                            <h6 class="mb-0"></h6>
                        </div>
                    </div>
                    <div class="bg-body p-3 mt-3 rounded" style="height: 190px;">
                    <div class="text-center mt-5">
                        <div class="spinner-grow text-success" role="status">
                          <span class="visually-hidden">Loading...</span>
                          </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);
  }
};

let hideLoadingSkeletonCategory = () => {
  $("#kra-card-list").html("");
};

let renderCategoryGraph = (id, dataArray, color1) => {
  const ColorsCode = {
    "primary" : "#0d6efd",
    "secondary" : "#6610f2",
    "success" : "#198754",  // Corrected closing quotation mark
    "danger": "#dc3545",
    "warning" : "#ffc107",
    "info" : "#20c997",
};

console.log(dataArray)


  
let year = dataArray.map((yr) => {
  return "" + yr[2]
})

let target = dataArray.map((tgt) => {
  return "" + tgt[0]
})

let performance = dataArray.map((perf) => {
  return "" + perf[1]
})


$(`#all-earnings-graph${id}`).html("")

  var options = {
    series: [{
    name: 'Target',
    data: target,
  },{
    name: 'Performance',
    data: performance
  }],
    chart: {
    type: 'bar',
    height: 150,
    toolbar: {
      show: false
    }
  },
  grid: {
    show: false
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '90%',
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
  colors:[ColorsCode[color1],'#198754'],
  xaxis: {
    labels: {
      rotate: -45
    },
    categories: year,
  },
  yaxis: {
    labels: {
      show: false,
    }
  },
  fill: {
    opacity: 1,
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return val
      }
    }
  }
  };

  var chart = new ApexCharts(document.querySelector(`#all-earnings-graph${id}`), options);
  chart.render();

  
};

function indicatorCards (item, score, score_card) {
  
  let performance = null
  try{
    performance =  score.annual_performance ? score.annual_performance :( score.month_performance ? score.month_performance : (score.quarter_performance ? score.quarter_performance : null ))
  }catch{
    null
  }
  let target = null
  try{
    target = score.annual_target ?  score.annual_target :( score.month_target ? score.month_target : (score.quarter_target ? score.quarter_target : null ) )
  }catch{
    null
  }

  
  let scoreResult = ''
  if(performance != null && target !=null){
   
    if(item.kpi_characteristics == 'inc'){
      //For increasing KPIs, a higher score is better
      scoreResult = (Number(performance) / Number(target)) * 100
    }else if (item.kpi_characteristics == 'dec'){
      // For decreasing KPIs, a lower score is better
      scoreResult = (Number(target) / Number(performance)) * 100
    }else{
      // For constant KPIs, the score is based on achieving the target exactly
      scoreResult = (Number(performance) / Number(target)) * 100
    }

    // Ensure score is between 0 and 100
    scoreResult = Math.min(Math.max(scoreResult, 0), 100)
  }
  let colorCode = null
   try{
    colorCode = score_card.find((colorCode) => scoreResult >= colorCode.starting && scoreResult <= colorCode.ending)
   }catch{
    null
   }
   return `<div class="col-md-6 col-xxl-4 col-12">
   <div class="card border-{randomBgColor} ">
       <div class="card-body">
           <div class="d-flex align-items-center">
               <div class="flex-shrink-0">
                   <div class="avtar avtar-s  bg-light-primary">
                       <svg  width="24" height="24"
                           viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                           <path opacity="0.4" d="M13 9H7" stroke="#4680FF" stroke-width="1.5"
                               stroke-linecap="round" stroke-linejoin="round" />
                           <path
                               d="M22.0002 10.9702V13.0302C22.0002 13.5802 21.5602 14.0302 21.0002 14.0502H19.0402C17.9602 14.0502 16.9702 13.2602 16.8802 12.1802C16.8202 11.5502 17.0602 10.9602 17.4802 10.5502C17.8502 10.1702 18.3602 9.9502 18.9202 9.9502H21.0002C21.5602 9.9702 22.0002 10.4202 22.0002 10.9702Z"
                               stroke="#4680FF" stroke-width="1.5" stroke-linecap="round"
                               stroke-linejoin="round" />
                           <path
                               d="M17.48 10.55C17.06 10.96 16.82 11.55 16.88 12.18C16.97 13.26 17.96 14.05 19.04 14.05H21V15.5C21 18.5 19 20.5 16 20.5H7C4 20.5 2 18.5 2 15.5V8.5C2 5.78 3.64 3.88 6.19 3.56C6.45 3.52 6.72 3.5 7 3.5H16C16.26 3.5 16.51 3.50999 16.75 3.54999C19.33 3.84999 21 5.76 21 8.5V9.95001H18.92C18.36 9.95001 17.85 10.17 17.48 10.55Z"
                               stroke="#4680FF" stroke-width="1.5" stroke-linecap="round"
                               stroke-linejoin="round" />
                       </svg>
                       </div>
               </div>
               <div class="flex-grow-1 ms-3" >
                   <h6 class="mb-0">${item.kpi_name_eng} </h6>
               </div>
               <div class="flex-shrink-0 ms-3">
                   <div class="dropdown"><a
                           class="avtar avtar-s btn-link-primary dropdown-toggle arrow-none" href="#"
                           data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i
                               class="ti ti-dots-vertical f-18"></i></a>
                       <div class="dropdown-menu dropdown-menu-end">
                          
                           <button data-id="${item.id}"  class="detail-category  detail-category dropdown-item" data-bs-toggle="modal" data-bs-target="#exampleModal" > <svg class="pc-icon"> <use xlink:href="#custom-flash"></use></svg> Detail</button>
                           </div>
                   </div>
               </div>
           </div>
           <div class="bg-body p-3 mt-3 rounded" style="height: 190px;">
               <div class="mt-3 row ">
                   <div class="col-9">
                       <div id="all-earnings-graph${item.id}"></div>
                   </div>

                  ${
                    scoreResult ? ` <div class="col-3 ">
                    <span class="badge rounded-pil p-3 text-dark" style="background-color:${colorCode.color};">${parseFloat(scoreResult).toFixed(2)}</span>
                   </div>` : '' 
                  }


               </div>
           </div>
       </div>
   </div>
 </div>`;  
}

let keyResultArea = () =>{
  $("#goalDropDownOption").change(function(){
    let goalId = this.value
    $.ajax({
      type: "GET",
      url: `/indicator_lists/${goalId}/`,
      beforeSend: function () {
        showLoadingSkeletonCategory();
     },
     complete: function () {
    
     },
     success: function(data){
      if(data.kra.length > 0){
        $("#kra-card-list").html("")
        data.kra.forEach((kra) =>{
          $("#kra-card-list").append(`
            <h4 class="fw-bold  text-center pt-3" ></h4>
            <hr class="shadow-lg p-1 rounded ">`) // Append Single KRA


            let filterKraIndicators = data.indicators.filter((indicator) => indicator.keyResultArea_id == kra.id)  //filter Indicator 

            let color = randomColor()
            filterKraIndicators.forEach((item) => {
              let chartData = []
              let dashboardSetting = data.dashboardSetting.filter((dashboard) => dashboard.indicator_id.includes(item.id))
              let score = ''
              for (setting of dashboardSetting){

                if(setting.quarter_id == null && setting.month_id == null ){
                  let filterindicatorValue = data.value_annual.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                  if(filterindicatorValue){
                    for(value of filterindicatorValue){
                     if(value.annual_target != null ||  value.annual_performance != null ){
                      chartData.push(
                        [
                          setting.target ? value.annual_target : null, 
                          setting.performance ? value.annual_performance : null, 
                          value.year__year_amh,
                          value.year__year_eng
                       ]
                      )

                      //Calculate Score Card
                     if(setting.is_score_card){
                      score = value
                      }


                     }
                  }
                  }
                }



                if (setting.quarter_id && setting.month_id == null ){
                  let filterindicatorValue = data.value_quarter.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                  if(filterindicatorValue){
                    for(value of filterindicatorValue){
                        chartData.push(
                          [
                            setting.target ? value.quarter_target : null, 
                            setting.performance ? value.quarter_performance : null, 
                            value.year__year_amh + " " + value.quarter__quarter_eng,
                            value.year__year_eng + " " + value.quarter__quarter_eng,
                        ]
                        )


                        //Calculate Score Card
                     if(setting.is_score_card){
                      score = value
                      }


                  }
                  }
                }

                
                if (setting.month_id && setting.quarter_id == null ){
                  let filterindicatorValue = data.value_month.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                  if(filterindicatorValue){
                    for(value of filterindicatorValue){
                        chartData.push(
                          [
                            setting.target ? value.month_target : null, 
                            setting.performance ? value.month_performance : null, 
                            value.year__year_amh + " " + value.month__month_english,
                            value.year__year_eng + " " + value.month__month_english
                        ]
                        )

                        //Calculate Score Card
                     if(setting.is_score_card){
                      score = value
                      }
                  }
                  }
                }                
              }  


            

              $("#kra-card-list").append(indicatorCards(item, score, data.score_card)); // append Card
              renderCategoryGraph(item.id, chartData,color, randomColor()); //render graph

              


            })
 
        })

      
      }else{
        $("#kra-title").html('<p class="text-center text-danger h3">No Data Found</p>')
      }
    }
    }) 
    
  })

}

let indicatorSearchResult = (search) =>{
  $.ajax({
    type: "GET",
    url: `/indicator_lists/1${search ? '?'+search : '' }`,
    beforeSend: function () {
      showLoadingSkeletonCategory();
   },
   complete: function () {
    $("#kra-title").html("Search Result")
    $("#goalDropDownOption").hide()
    $("#goalDropDownOptionLabel").hide()
   },
   success: function(data){
    if(data.kra.length > 0){
      $("#kra-card-list").html("")
      data.kra.forEach((kra) =>{
        $("#kra-card-list").append(`
          <h4 class="fw-bold  text-center pt-3"></h4>
          <hr class="shadow-lg p-1 rounded ">`) // Append Single KRA


          let filterKraIndicators = data.indicators.filter((indicator) => indicator.keyResultArea_id == kra.id)  //filter Indicator 

          let color = randomColor()
          filterKraIndicators.forEach((item) => {
            let chartData = []
            let dashboardSetting = data.dashboardSetting.filter((dashboard) => dashboard.indicator_id.includes(item.id))
            let score = ''
            for (setting of dashboardSetting){

              if(setting.quarter_id == null && setting.month_id == null ){
                let filterindicatorValue = data.value_annual.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                if(filterindicatorValue){
                  for(value of filterindicatorValue){
                   if(value.annual_target != null ||  value.annual_performance != null ){
                    chartData.push(
                      [
                        setting.target ? value.annual_target : null, 
                        setting.performance ? value.annual_performance : null, 
                        value.year__year_amh
                     ]
                    )

                    //Calculate Score Card
                   if(setting.is_score_card){
                    score = value
                    }


                   }
                }
                }
              }



              if (setting.quarter_id && setting.month_id == null ){
                let filterindicatorValue = data.value_quarter.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                if(filterindicatorValue){
                  for(value of filterindicatorValue){
                      chartData.push(
                        [
                          setting.target ? value.quarter_target : null, 
                          setting.performance ? value.quarter_performance : null, 
                          value.year__year_amh + " " + value.quarter__quarter_eng
                      ]
                      )


                      //Calculate Score Card
                   if(setting.is_score_card){
                    score = value
                    }


                }
                }
              }

              
              if (setting.month_id && setting.quarter_id == null ){
                let filterindicatorValue = data.value_month.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                if(filterindicatorValue){
                  for(value of filterindicatorValue){
                      chartData.push(
                        [
                          setting.target ? value.month_target : null, 
                          setting.performance ? value.month_performance : null, 
                          value.year__year_amh + " " + value.month__month_english
                      ]
                      )

                      //Calculate Score Card
                   if(setting.is_score_card){
                    score = value
                    }
                }
                }
              }                
            }  


          

            $("#kra-card-list").append(indicatorCards(item, score, data.score_card)); // append Card
            renderCategoryGraph(item.id, chartData,color, randomColor()); //render graph

            


          })

      })

    
    }else{
      $("#kra-title").html('<p class="text-center text-danger h3">No Data Found</p>')
    }
  }
  }) 
}



let handleDropDown = (ministryId) => {
  $.ajax({
    type: "GET",
    url: `/ministry-goal/${ministryId}/`,
    beforeSend: function () {
      showLoadingSkeletonCategory();
   },
    success: function(data){
      let goalLists =  data.ministry_goal.map((item)=>`<option value="${item.id}">${item.goal_name_eng}</option>`)
      $("#goalDropDownOption").html(goalLists)


      //For the default one
      if(goalLists.length > 0 ){
        $.ajax({
          type: "GET",
          url: `/indicator_lists/${data.ministry_goal[0].id}/`,
          beforeSend: function () {
            showLoadingSkeletonCategory();
         },
          complete: function () {
            //hideLoadingSkeletonCategory();
          },     success: function(data){
            if(data.kra.length > 0){
              $("#kra-card-list").html("")
              data.kra.forEach((kra) =>{
                $("#kra-card-list").append(`
                  <h4 class="fw-bold  text-center pt-3" ></h4>
                  <hr class="shadow-lg p-1 rounded ">`) // Append Single KRA
      
      
                  let filterKraIndicators = data.indicators.filter((indicator) => indicator.keyResultArea_id == kra.id)  //filter Indicator 
      
                  let color = randomColor()
                  filterKraIndicators.forEach((item) => {
                    let chartData = []
                    let dashboardSetting = data.dashboardSetting.filter((dashboard) => dashboard.indicator_id.includes(item.id))
                    let score = ''
                    for (setting of dashboardSetting){
      
                      if(setting.quarter_id == null && setting.month_id == null ){
                        let filterindicatorValue = data.value_annual.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                        if(filterindicatorValue){
                          for(value of filterindicatorValue){
                           if(value.annual_target != null ||  value.annual_performance != null ){
                            chartData.push(
                              [
                                setting.target ? value.annual_target : null, 
                                setting.performance ? value.annual_performance : null, 
                                value.year__year_amh
                             ]
                            )
      
                            //Calculate Score Card
                           if(setting.is_score_card){
                            score = value
                            }
      
      
                           }
                        }
                        }
                      }
      
      
      
                      if (setting.quarter_id && setting.month_id == null ){
                        let filterindicatorValue = data.value_quarter.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                        if(filterindicatorValue){
                          for(value of filterindicatorValue){
                              chartData.push(
                                [
                                  setting.target ? value.quarter_target : null, 
                                  setting.performance ? value.quarter_performance : null, 
                                  value.year__year_amh + " " + value.quarter__quarter_eng
                              ]
                              )
      
      
                              //Calculate Score Card
                           if(setting.is_score_card){
                            score = value
                            }
      
      
                        }
                        }
                      }
      
                      
                      if (setting.month_id && setting.quarter_id == null ){
                        let filterindicatorValue = data.value_month.filter((value) => value.indicator__id == item.id && value.year__year_eng == setting.year__year_eng)
                        if(filterindicatorValue){
                          for(value of filterindicatorValue){
                              chartData.push(
                                [
                                  setting.target ? value.month_target : null, 
                                  setting.performance ? value.month_performance : null, 
                                  value.year__year_amh + " " + value.month__month_english
                              ]
                              )
      
                              //Calculate Score Card
                           if(setting.is_score_card){
                            score = value
                            }
                        }
                        }
                      }                
                    }  
      
      
                  
      
                    $("#kra-card-list").append(indicatorCards(item, score, data.score_card)); // append Card
                    renderCategoryGraph(item.id, chartData,color, randomColor()); //render graph
      
                    
      
      
                  })
       
              })
      
            
            }else{
              $("#kra-title").html('<p class="text-center text-danger h3">No Data Found</p>')
            }
          }

          
        }) 
      }else{
        hideLoadingSkeletonCategory();
        $("#kra-title").html('<p class="text-center text-danger h3">No Data Found</p>')
      }
    }

  })
}

let handleOnMinistryClicked = () =>{
  $('.ministry-card').click(function(){
    const buttonData = $(this).data();

    $("#kra-title").html(buttonData.name)
    $("#goalDropDownOption").show()
    $("#goalDropDownOptionLabel").show()
    handleDropDown(buttonData.id)  //update drop down lists
    keyResultArea()

  })
}

let handleOnSearch = () =>{
  $("#searchItemForm").submit(function(e){
    let form = $("#searchItemForm")
    e.preventDefault()
    let searchItem  = this.q.value
    indicatorSearchResult(`q=${searchItem}`)
  })

  $("#searchItemValue").on("keydown", function(event){
    let searchValue = $(this).val()
    // Prevent default form submission if enter is pressed (optional)
    if (event.keyCode === 13) {
      event.preventDefault();
    }

    // Minimum characters to trigger search (optional)
    if (searchValue.length < 2) {
      return; // Exit if not enough characters entered
    }

    $.ajax({
      type: "GET",
      dataType: "json",
      url: "/search_autocomplete_indicator_list/",
      data: { search: searchValue },
      success: function(data) {
        let a = data.indicators.map((item) => `<option value="${item.kpi_name_eng}">${item.kpi_name_eng}</option>`)
        $("#autocomplete").html(a)
      },
    })
    
  })
}

$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/ministries_lists/",
    beforeSend: function () {
       showLoadingSkeletonTopic();
    },
    complete: function () {
      hideLoadingSkeletonTopic();
    },
    success: function (data) {
      const bootstrapColors = [
        "primary",
        "secondary",
        "success",
        "warning",
        "info",
        "dark",
      ];
      let cardMinistry = ``
      let sideNav = ``;
      let selectedCard = ''
      data.ministries.forEach((item) => {
        cardMinistry += `
        <!-- custom cards -->
          <div class="col-md-3 col-xl-1 d-none d-md-block ministry-card"
             data-id = ${item.id}
             data-name = "${item.code}"
             >
                <div class="card ${ item.id == 3 ? selectedCard : '' } selected-card social-widget-card text-dark">
                    <div class="card-body d-flex justify-content-start align-items-center p-2">
                    <img src="${item.image}" class="img-fluid rounded-circle"  style="width: 37px; height: 37spx;" alt="ministry image">
                    <span class=" ">${item.code}</span>
                    </div>
                </div>
            </div>`;

        sideNav += `<li class="pc-item ministry-card" data-id = ${item.id} data-category-name = "${item.responsible_ministry_eng}">
            <a href="#" class="pc-link">
  
                <span class="pc-mtext">${item.responsible_ministry_eng}</span>   
                </a>
        </li>
        `

        
      });

   
      $("#mobile-collapse").click(function(){
        $("#sidebarHtml").removeClass("d-none")
      })

      goals_list = `
      
      `
      $("#ministry-card-lists").html(cardMinistry);
      //$("#topic-card-lists").append(goals_list);
      //$("#sidebar-topic-list").html(sideNav);

      handleOnMinistryClicked() 

    },error: function(response) {
      // hideLoadingSkeletonTopic();
      // hideLoadingSkeletonCategory();
    }
  
  });

  //Default 
  handleOnSearch() //Search
  handleDropDown(3)
  $("#kra-title").html("MoT")
  keyResultArea()
  
});



