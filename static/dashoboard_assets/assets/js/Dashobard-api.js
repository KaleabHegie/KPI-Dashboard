let projectHtml = (dashboardItem,roadSummaryItem,energyCard,irrigationCard) => {
  let html = `
  <div class="row">
    <div class="col-12">
      <div class="card">
  `
  let cardHeader = () =>{
    return`
    <div class="card-header pb-0 pt-2">
    <ul class="nav nav-tabs analytics-tab" id="myTab" role="tablist">
        <li class="nav-item" role="presentation"><button class="nav-link active"
                id="analytics-tab-1" data-bs-toggle="tab" data-bs-target="#analytics-tab-1-pane"
                type="button" role="tab" aria-controls="analytics-tab-1-pane"
                aria-selected="true">Road</button></li>
        <li class="nav-item" role="presentation"><button class="nav-link" id="analytics-tab-2"
                data-bs-toggle="tab" data-bs-target="#analytics-tab-2-pane" type="button"
                role="tab" aria-controls="analytics-tab-2-pane"
                aria-selected="false">Energey</button></li>
        <li class="nav-item" role="presentation"><button class="nav-link" id="analytics-tab-3"
                data-bs-toggle="tab" data-bs-target="#analytics-tab-3-pane" type="button"
                role="tab" aria-controls="analytics-tab-3-pane" aria-selected="false">Irrigation</button></li>
        <li class="nav-item" role="presentation"><button class="nav-link" id="analytics-tab-4"
                data-bs-toggle="tab" data-bs-target="#analytics-tab-4-pane" type="button"
                role="tab" aria-controls="analytics-tab-4-pane"
                aria-selected="false">Water</button></li>
        </ul>
    </div>
    `
  }

  let section1 = () =>{


    let cardProject = ``
    roadSummaryItem.project.forEach((item) => {
      cardProject+= `
    <!--Start Cards -->
            <div class="col-12 col-lg-4">
                <div class="card">
                    <div class="card-body">
                        <div
                            class="d-flex align-items-center justify-content-between mb-3">
                            <h5 class="mb-0">${item[0]}</h5>
                        </div>
                        <div class="card rounded-4 overflow-hidden" style="
                          background-image: url('https://files.ekmcdn.com/reedycdboy/images/true-green-a4-card-290gsm-select-pack-size-40-sheets-5701-p.jpg');
                          background-size: cover;
                        ">
                            <div class="card-body">
                                <div class="d-flex">
                                    <div class="flex-grow-1 me-3">
                                        <p
                                            class="text-white text-sm text-opacity-50 mb-0">
                                            Number of Projects
                                        </p>
                                        <h5 class="text-white">${item[1]}</h5>
                                    </div>
                                </div>
                                <div class="flex-grow-1 me-3">
                                    <p
                                        class="text-white text-sm text-opacity-50 mb-0">
                                        Total Cost of the project in billion
                                        birr
                                    </p>
                                    <h5 class="text-white">${item[2]}</h5>
                                </div>
                                <div class="row">
                                    <div class="col-auto">
                                        <p
                                            class="text-white text-sm text-opacity-50 mb-0">
                                            Total Length in Thousand KM
                                        </p>
                                        <h6 class="text-white mb-0">${item[3]}
                                        </h6>
                                    </div>
                                    <div class="col-auto">
                                        <p
                                            class="text-white text-sm text-opacity-50 mb-0">
                                            Expenditure to date in billion birr
                                        </p>
                                        <h6 class="text-white mb-0">${item[4]}
                                        </h6>
                                    </div>
                                    <div class="flex-grow-1 me-3">
                                        <p
                                            class="text-white text-sm text-opacity-50 mb-0">
                                            Total Cost of the project in billion
                                            birr
                                        </p>
                                        <h5 class="text-white">${item[5]}</h5>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="text-center mt-3">
                            <h3 class="mb-1">${item[6]}</h3>
                            <p class="text-muted mb-0">Total Cost Share in %</p>
                        </div>
                    </div>
                </div>
            </div>
            <!--End Cards-->
    `
    })
    
    return `
    <div class="tab-pane fade show active" id="analytics-tab-1-pane" role="tabpanel"
    aria-labelledby="analytics-tab-1" tabindex="0">
    <div id="overview-content-1">
        <div class="row">

            <!--Card Part -->
            ${cardProject}
            <!--Table Start-->
            <div class="card">
                <h2 class="p-3">Road Projects</h2>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Road Project Category</th>
                                    <th>Number of Projects</th>
                                    <th>Total Cost of the project in billion
                                        birr</th>
                                    <th>Total Length in Thousand KM</th>
                                    <th>Expenditure to date in billion birr</th>
                                    <th>Budget request for 2017 FY in billion
                                        birr</th>
                                    <th>Total Cost Share in %</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Total</td>
                                    <td>380</td>
                                    <td>562.8</td>
                                    <td>27.2</td>
                                    <td>240.6</td>
                                    <td>78.7</td>
                                    <td>72.1</td>
                                </tr>
                                <tr>
                                    <td>Trunk Road Rehabilitation</td>
                                    <td>4</td>
                                    <td>2.7</td>
                                    <td>0.2</td>
                                    <td>2.9</td>
                                    <td>1.3</td>
                                    <td>0.3</td>
                                </tr>
                                <tr>
                                    <td>Trunk Road Upgrading</td>
                                    <td>81</td>
                                    <td>152.0</td>
                                    <td>6.1</td>
                                    <td>43.6</td>
                                    <td>18.6</td>
                                    <td>19.5</td>
                                </tr>
                                <tr>
                                    <td>New Road Project</td>
                                    <td>238</td>
                                    <td>392.3</td>
                                    <td>16.2</td>
                                    <td>115.1</td>
                                    <td>54.2</td>
                                    <td>50.2</td>
                                </tr>
                                <tr>
                                    <td>Road Heavy Maintenance</td>
                                    <td>51</td>
                                    <td>15.8</td>
                                    <td>4.6</td>
                                    <td>2.3</td>
                                    <td>2.6</td>
                                    <td>2.0</td>
                                </tr>
                                <tr>
                                    <td>Bridge Construction and Rehabilitation
                                    </td>
                                    <td>6</td>
                                    <td>0.0</td>
                                    <td>0.0</td>
                                    <td>76.7</td>
                                    <td>2.0</td>
                                    <td>0.0</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <!--Table End-->

            <!--Table Start-->
            <div class="card">
                <h2 class="p-3">Road projects Regional Distribution</h2>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Region</th>
                                    <th>Number of Road Project</th>
                                    <th>Total Road Project Budget (in billion
                                        birr)</th>
                                    <th>% share</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Afar</td>
                                    <td>13</td>
                                    <td>20</td>
                                    <td>3.6</td>
                                </tr>
                                <tr>
                                    <td>Amhara</td>
                                    <td>87</td>
                                    <td>130</td>
                                    <td>23.1</td>
                                </tr>
                                <tr>
                                    <td>Benishangul Gumuz</td>
                                    <td>8</td>
                                    <td>10</td>
                                    <td>1.8</td>
                                </tr>
                                <tr>
                                    <td>Dire Dawa</td>
                                    <td>2</td>
                                    <td>0</td>
                                    <td>0.1</td>
                                </tr>
                                <tr>
                                    <td>Gambella</td>
                                    <td>15</td>
                                    <td>23</td>
                                    <td>4.1</td>
                                </tr>
                                <tr>
                                    <td>Oromia</td>
                                    <td>95</td>
                                    <td>153</td>
                                    <td>27.2</td>
                                </tr>
                                <tr>
                                    <td>Sidama</td>
                                    <td>2</td>
                                    <td>2</td>
                                    <td>0.3</td>
                                </tr>
                                <tr>
                                    <td>Somale</td>
                                    <td>27</td>
                                    <td>37</td>
                                    <td>6.6</td>
                                </tr>
                                <tr>
                                    <td>South Ethiopia</td>
                                    <td>48</td>
                                    <td>72</td>
                                    <td>12.7</td>
                                </tr>
                                <tr>
                                    <td>South West</td>
                                    <td>3</td>
                                    <td>5</td>
                                    <td>0.9</td>
                                </tr>
                                <tr>
                                    <td>Tigray</td>
                                    <td>32</td>
                                    <td>33</td>
                                    <td>5.9</td>
                                </tr>
                                <tr>
                                    <td>Addis Ababa</td>
                                    <td>1</td>
                                    <td>0</td>
                                    <td>-</td>
                                </tr>
                                <tr>
                                    <td>Interregional</td>
                                    <td>47</td>
                                    <td>77</td>
                                    <td>13.7</td>
                                </tr>
                                <tr>
                                    <td>Grand Total</td>
                                    <td>380</td>
                                    <td>563</td>
                                    <td>100.0</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <!--Table End-->


        </div>
    </div>
</div>
    `
  }

  let section2 = () =>{
    let eneCard = ``
    energyCard.energey.forEach((item) =>{
      eneCard+=`<!--Start Cards -->
      <div class="col-12 col-lg-4">
          <div class="card">
              <div class="card-body">
                  <div
                      class="d-flex align-items-center justify-content-between mb-3">
                      <h5 class="mb-0">${item[0]} : ${item[1]} </h5>
                  </div>
                  <div class="card rounded-4 overflow-hidden" style="
                    background-image: url('https://files.ekmcdn.com/reedycdboy/images/true-green-a4-card-290gsm-select-pack-size-40-sheets-5701-p.jpg');
                    background-size: cover;
                  ">
                      <div class="card-body text-white">
                          <h5 class="text-start text-white">Project Life
                          </h5>
                          <div class="row justify-content-between">
                              <div class="col-6">
                                  <p class="text-white fw-bold"> <br>
                                      Started Date: ${item[2]} </p>
                              </div>
                              <div class="col-6">
                                  <p class="text-white fw-bold"> <br>
                                      Expected Date: ${item[3]} </p>
                              </div>
                          </div>
                          <p class="text-white fw-bold">Capacity: ${item[4]}
                          </p>
                          <p class="text-white fw-bold">2015 performance:
                          ${item[5]} </p>

                          <h6 class="text-start text-white pt-1">
                              Performance up to 2016 9 months</h6>
                          <div class="row justify-content-between">
                              <div class="col-6">
                                  <p class="text-white fw-bold">Plan <br>
                                  ${item[6]} </p>
                              </div>
                              <div class="col-6">
                                  <p class="text-white fw-bold">
                                      Performance <br> ${item[7]} </p>
                              </div>
                          </div>

                          <p class="text-white fw-bold p-0 m-1">Total
                              allocated budget: ${item[8]} </p>
                          <p class="text-white fw-bold p-0 m-1">
                              Expenditure Upto 2016 9 mth (Billion Birr):
                              ${item[9]}</p>
                      </div>
                  </div>
                  <div class="text-center mt-3">
                      <h3 class="mb-1"> ${item[10]}</h3>
                      <p class="text-muted mb-0"> Budget for remaining Work (Billion Birr):</p>
                  </div>
              </div>
          </div>
      </div>
      <!--End Cards-->`
    })
    
   
    return `
    <div class="tab-pane fade" id="analytics-tab-2-pane" role="tabpanel"
    aria-labelledby="analytics-tab-2" tabindex="0">
    <div id="overview-content-2">
        <div class="row">
            <!--Card Place-->
            ${eneCard}
            <!--Table Start-->
            <div class="card">
                <h2 class="p-2">የሀይል ልማት የፕሮጀክቶች አጠቃላይ ያሉበትን ደረጃ የሚያሳይ ቅፅ</h2>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover">
                            <thead>
                                <tr>
                                    <th colspan="3"></th>
                                    <th colspan="2" class="text-center">ፕሮጀክቱ
                                    </th>
                                    <th colspan="2"></th>
                                    <th colspan="3">2016 ዘጠነኛ ወር እቅድ አፈፃፀም </th>
                                    <th></th>
                                    <th colspan="3">2016 ዘጠነኛ ወር እቅድ አፈፃፀም
                                        (በቢሊዮን ብር)</th>
                                    <th></th>
                                    <th>እስከ 2016 ዘጠነኛ ወር የወጣ ወጪ በቢሊዮን ብር</th>
                                    <th>ፕሮጀክቱን ለማጠናቀቅ የሚያስፈልግ ወጪ</th>
                                </tr>
                                <tr>
                                    <th>ተ.ቁ</th>
                                    <th>የፕሮጀክቱ ስም</th>
                                    <th>የሚገኝበት</th>
                                    <th>የተጀመረበት ጊዜ</th>
                                    <th>የሚጠናቀቅበት ጊዜ</th>
                                    <th>የማምረት አቅም</th>
                                    <th>2015 የአፈፃፀም ደረጃ</th>
                                    <th>እቅድ</th>
                                    <th>ክንውን</th>
                                    <th>አፈፃፀም</th>
                                    <th>እስከ 2016 ዘጠነኛ ወር የተደረሰበት አፈፃፀም </th>
                                    <th>እቅድ</th>
                                    <th>ክንውን</th>
                                    <th>አፈፃፀም</th>
                                    <th>ለፕሮጀክቱ አጠቃላይ የተመደበ በጀት በተከለሰው መሰረት</th>
                                    <th>እስከ 2016 ዘጠነኛ ወር የወጣ ወጪ በቢሊዮን ብር</th>
                                    <th>ፕሮጀክቱን ለማጠናቀቅ የሚያስፈልግ ወጪ</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr>
                                    <td>1</td>
                                    <td>ህዳሴ</td>
                                    <td>ቤ.ጉ</td>
                                    <td>12/30/10</td>
                                    <td>09/08/25</td>
                                    <td>5150 MW</td>
                                    <td>92.15</td>
                                    <td>4</td>
                                    <td>3.64</td>
                                    <td>91.05</td>
                                    <td>95.79</td>
                                    <td>8.455</td>
                                    <td>6.457</td>
                                    <td>76.37</td>
                                    <td>234.97</td>
                                    <td>193.30</td>
                                    <td>48.89</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>ኮይሻ</td>
                                    <td>ደ . ም</td>
                                    <td>03/28/16</td>
                                    <td>05/18/28</td>
                                    <td>1800MW</td>
                                    <td>61.39</td>
                                    <td>5.74</td>
                                    <td>5.03</td>
                                    <td>87.6</td>
                                    <td>66.42</td>
                                    <td>5.754</td>
                                    <td>4.672</td>
                                    <td>81.2</td>
                                    <td>143.90</td>
                                    <td>50.13</td>
                                    <td>78.20</td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>አይሻ</td>
                                    <td>ሶማሊ</td>
                                    <td>02/25/16</td>
                                    <td>09/27/25</td>
                                    <td>120 MW</td>
                                    <td>82.05</td>
                                    <td>2.09</td>
                                    <td>1.36</td>
                                    <td>65</td>
                                    <td>83.41</td>
                                    <td>0.016</td>
                                    <td>0.01</td>
                                    <td>66.7</td>
                                    <td>10.32</td>
                                    <td>4.18</td>
                                    <td>4.02</td>
                                </tr>
                                <tr>
                                    <td>4</td>
                                    <td>አሉቶ</td>
                                    <td>ኦሮሚያ</td>
                                    <td>10/01/14</td>
                                    <td>09/30/24</td>
                                    <td>72 MW</td>
                                    <td>98.58</td>
                                    <td>1.64</td>
                                    <td>0.81</td>
                                    <td>50</td>
                                    <td>99.39</td>
                                    <td>1.668</td>
                                    <td>1.049</td>
                                    <td>62.92</td>
                                    <td>5.91</td>
                                    <td>5.38</td>
                                    <td>1.71</td>
                                </tr>
                                <tr>
                                    <td>5</td>
                                    <td>አሰላ</td>
                                    <td>ኦሮሚያ</td>
                                    <td>12/17/20</td>
                                    <td>01/13/25</td>
                                    <td>100MW</td>
                                    <td>39.75</td>
                                    <td>20.66</td>
                                    <td>12.49</td>
                                    <td>60.49</td>
                                    <td>52.24</td>
                                    <td>2.458</td>
                                    <td>0.515</td>
                                    <td>21</td>
                                    <td>8.08</td>
                                    <td>4.53</td>
                                    <td>4.58</td>
                                </tr>
                                <tr>
                                    <td>6</td>
                                    <td>ባህርዳር - ወልዲያ - ኮምቦልቻ</td>
                                    <td>አማራ</td>
                                    <td>08/30/19</td>
                                    <td>02/28/25</td>
                                    <td>400kv</td>
                                    <td>89.49</td>
                                    <td>7.8</td>
                                    <td>4.39</td>
                                    <td>56.3</td>
                                    <td>91.6</td>
                                    <td>1.56</td>
                                    <td>0.489</td>
                                    <td>31</td>
                                    <td>13.47</td>
                                    <td>6.80</td>
                                    <td>6.78</td>
                                </tr>
                                <tr>
                                    <td>7</td>
                                    <td>በቆጂ እና ደብረ ታቦር</td>
                                    <td>አማራና ኦሮሚያ</td>
                                    <td>03/03/23</td>
                                    <td>08/31/24</td>
                                    <td>230kv</td>
                                    <td>39.03</td>
                                    <td>37.69</td>
                                    <td>34.34</td>
                                    <td>91.11</td>
                                    <td>73.37</td>
                                    <td>1</td>
                                    <td>1.062</td>
                                    <td>114</td>
                                    <td>1.94</td>
                                    <td>1.30</td>
                                    <td>0.61</td>
                                </tr>
                                <tr>
                                    <td>8</td>
                                    <td>የኤሌክትሪክ ግሪድ ደቡባዊ</td>
                                    <td>ደቡብ/ሶዳማ</td>
                                    <td>11/29/22</td>
                                    <td>11/28/25</td>
                                    <td>132kv</td>
                                    <td>22.11</td>
                                    <td>26.51</td>
                                    <td>23.34</td>
                                    <td>88.04</td>
                                    <td>45.45</td>
                                    <td>1</td>
                                    <td>0.392</td>
                                    <td>28</td>
                                    <td>10.62</td>
                                    <td>4.15</td>
                                    <td>6.76</td>
                                </tr>
                                <tr>
                                    <td>9</td>
                                    <td>የጫካ ፓርክ</td>
                                    <td>አዲስ አበባ</td>
                                    <td>07/04/23</td>
                                    <td>08/31/24</td>
                                    <td>132kv/230kv</td>
                                    <td>0</td>
                                    <td>99.2</td>
                                    <td>89.6</td>
                                    <td>90.32</td>
                                    <td>89.6</td>
                                    <td>0</td>
                                    <td>0.137</td>
                                    <td>96</td>
                                    <td>0.20</td>
                                    <td>0.14</td>
                                    <td>0.38</td>
                                </tr>
                                <tr>
                                    <td>10</td>
                                    <td>የኮተቤ ግቢ</td>
                                    <td>አዲስ አበባ</td>
                                    <td>10/05/22</td>
                                    <td>05/08/24</td>
                                    <td></td>
                                    <td>78.46</td>
                                    <td>20</td>
                                    <td>18.12</td>
                                    <td>90.6</td>
                                    <td>96.58</td>
                                    <td>0</td>
                                    <td>0.298</td>
                                    <td>82</td>
                                    <td>0.74</td>
                                    <td>0.60</td>
                                    <td>0.43</td>
                                </tr>
                                <tr>
                                    <td>11</td>
                                    <td>ህዳሴው ማስተባበሪያ</td>
                                    <td>ቤንሻንጉል</td>
                                    <td>11/03/23</td>
                                    <td>06/27/24</td>
                                    <td></td>
                                    <td>0</td>
                                    <td>51.6</td>
                                    <td>57.2</td>
                                    <td>110.8</td>
                                    <td>57.2</td>
                                    <td>61</td>
                                    <td>109.18</td>
                                    <td>180</td>
                                    <td>0.15</td>
                                    <td>0.11</td>
                                    <td>0.15</td>
                                </tr>

                            </tbody>

                        </table>
                    </div>
                </div>
            </div>
            <!--Table End-->

        </div>
    </div>
</div>
    `
  }

  let section3 = () =>{
    let card = ``
    irrigationCard.irrigation.forEach((item) =>{
      card+=`
      <!--Start Cards -->
      <div class="col-12 col-lg-4">
          <div class="card">
              <div class="card-body">
                  <div
                      class="d-flex align-items-center justify-content-between mb-3">
                      <h5 class="mb-0">${item[0]}</h5>
                  </div>
                  <div class="card rounded-4 overflow-hidden" style="
                    background-image: url('https://files.ekmcdn.com/reedycdboy/images/true-green-a4-card-290gsm-select-pack-size-40-sheets-5701-p.jpg');
                    background-size: cover;
                  ">
                      <div class="card-body">
                          <div class="d-flex">
                          </div>
                          <div class="row">
                              <div class="col-auto">
                                  <p
                                      class="text-white text-sm text-opacity-50 mb-0">
                                      Total Investment Cost (Billion Birr) 
                                  </p>
                                  <h6 class="text-white mb-0">${item[2]}
                                  </h6>
                              </div>
                              <div class="col-auto">
                                  <p
                                      class="text-white text-sm text-opacity-50 mb-0">
                                      Expenditure Upto 2016 9 month (Billion Birr)
                                  </p>
                                  <h6 class="text-white mb-0">${item[3]}
                                  </h6>
                              </div>
                              <div class="flex-grow-1 me-3">
                                  <p
                                      class="text-white text-sm text-opacity-50 mb-0">
                                      Required Budget for remaining Work (Billion Birr)
                                  </p>
                                  <h5 class="text-white">${item[4]}</h5>
                              </div>
                          </div>
                      </div>
                  </div>
                  <div class="text-center mt-3">
                      <h3 class="mb-1">${item[1]}</h3>
                      <p class="text-muted mb-0">Number of Project</p>
                  </div>
              </div>
          </div>
      </div>
      <!--End Cards-->
  
      `
    })
    return `
    <div class="tab-pane fade" id="analytics-tab-3-pane" role="tabpanel"
    aria-labelledby="analytics-tab-3" tabindex="0">
    <div id="overview-content-3">
       <div class="row"> 
       ${card}
       <div>   
        <!--Table Start-->
        <div class="card">
            <h2 class="p-2">Irrigation Development project Spatial Distribution</h2>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <tr>
                            <th>Region</th>
                            <th>Number of Projects
                            </th>
                            <th>Total Project cost (Billion Birr)</th>
                        </tr>
                        <tr>
                            <td>Somali </td>
                            <td>4</td>
                            <td>8</td>
                        </tr>
                        <tr>
                            <td>Tigrayi</td>
                            <td>2</td>
                            <td>12</td>
                        </tr>
                        <tr>
                            <td>Amhara</td>
                            <td>13</td>
                            <td>20</td>
                        </tr>
                        <tr>
                            <td>Afar</td>
                            <td>6</td>
                            <td>10</td>
                        </tr>
                        <tr>
                            <td>Oromiya</td>
                            <td>34</td>
                            <td>20</td>
                        </tr>
                        <tr>
                            <td>Oromiya and Sidama</td>
                            <td>3</td>
                            <td>4</td>
                        </tr>
                        <tr>
                            <td>South Ethiopia</td>
                            <td>4</td>
                            <td>7.516</td>
                        </tr>
                        <tr>
                            <td>South West</td>
                            <td>2</td>
                            <td>1.49</td>
                        </tr>
                        <tr>
                            <td>South Ethiopia and South west</td>
                            <td></td>
                            <td>2</td>
                        </tr>
                        <tr>
                            <td>Grand Total</td>
                            <td>54</td>
                            <td>101</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        <!--Table End -->
</div>
</div>
</div>
    `
  }

  let section4 = () =>{
    return `

    <div class="tab-pane fade" id="analytics-tab-4-pane" role="tabpanel"
    aria-labelledby="analytics-tab-4" tabindex="0">
    <div id="overview-content-4">
        <!--Card Start-->
        <div class="card">
            <div class="card-body">
                
                <div class="row justify-content-center">

                <!--Start Cards -->
                <div class="col-12 col-lg-6">
                    <div class="card">
                   
                        <div class="card-body">
                            <div
                                class="d-flex align-items-center justify-content-between mb-3">
                                <h5 class="mb-0"></h5>
                            </div>
                            <div class="card rounded-4 overflow-hidden" style="
                              background-image: url('https://files.ekmcdn.com/reedycdboy/images/true-green-a4-card-290gsm-select-pack-size-40-sheets-5701-p.jpg');
                              background-size: cover;
                            ">
                                <div class="card-body">
                                    <div class="d-flex">
                                        <div class="flex-grow-1 me-3">
                                            <p
                                                class="text-white text-sm text-opacity-50 mb-0">
                                                Number of Projects
                                            </p>
                                            <h5 class="text-white">10</h5>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 me-3">
                                        <p
                                            class="text-white text-sm text-opacity-50 mb-0">
                                            Average Performance
                                        </p>
                                        <h5 class="text-white">25.179</h5>
                                    </div>
                                    <div class="row">
                                        <div class="col-auto">
                                            <p
                                                class="text-white text-sm text-opacity-50 mb-0">
                                                Allocated Budget (Million Birr)
                                            </p>
                                            <h6 class="text-white mb-0">17,376.71
                                            </h6>
                                        </div>
                                        <div class="col-auto">
                                            <p
                                                class="text-white text-sm text-opacity-50 mb-0">
                                                Expenditure Upto 2016 9 Mth (Million Birr)
                                            </p>
                                            <h6 class="text-white mb-0">18,354.01
                                            </h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!--End Cards-->


              


                </div>
            </div>
        </div>
        <!--Card End-->

        <div class="card">
            <div class="card-body">
            <h3 class="p-3">Water and sanitation projects.</h3>
                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead>
                            <tr>
                                <th colspan="3"></th>
                                <th colspan="2" class="text-center">Project life
                                </th>
                                <th colspan="1" class="text-center">Performance
                                    up to 2016 9 months </th>
                                <th colspan="2"></th>
                            </tr>
                            <tr>
                                <th>#</th>
                                <th>Project Name</th>
                                <th>Project Location</th>
                                <th>Started Date</th>
                                <th>Expected Completion Date</th>
                                <th>Performance</th>
                                <th>Total allocated budget (Billion)</th>
                                <th>Expenditure Upto 2016 9 month (Billion Birr)
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                                <tr>
                                    <td>1</td>
                                    <td>National Potable water access
                                        alternative strategy studyn project</td>
                                    <td>National</td>
                                    <td>2,015</td>
                                    <td>2,018</td>
                                    <td>12.5</td>
                                    <td>32.76</td>
                                    <td>8.41920972</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Rain fall harvesting project</td>
                                    <td>National</td>
                                    <td>2,016</td>
                                    <td>2,020</td>
                                    <td>5.11</td>
                                    <td>5936</td>
                                    <td>6.84</td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>Study and Design of 30 urban cities
                                        project</td>
                                    <td>National</td>
                                    <td>2,015</td>
                                    <td>2,020</td>
                                    <td>1</td>
                                    <td>32.194</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>4</td>
                                    <td>Drought affected Regions water supply
                                        access project</td>
                                    <td>All regions and Diredawa</td>
                                    <td>2,010</td>
                                    <td>2,017</td>
                                    <td>66.07</td>
                                    <td>5000</td>
                                    <td>3528.080021</td>
                                </tr>
                                <tr>
                                    <td>5</td>
                                    <td>Sustanable Dirinking water project</td>
                                    <td>National</td>
                                    <td>2,015</td>
                                    <td>2,017</td>
                                    <td>3</td>
                                    <td>3400</td>
                                    <td>2.91</td>
                                </tr>
                                <tr>
                                    <td>6</td>
                                    <td>Borena sustainable water development for
                                        livelihood project</td>
                                    <td>Oromiya Borena</td>
                                    <td>2,015</td>
                                    <td>2,018</td>
                                    <td>6</td>
                                    <td>754.34</td>
                                    <td>0.019</td>
                                </tr>
                                <tr>
                                    <td>7</td>
                                    <td>Horn of Africa ground water project</td>
                                    <td>All regions and Diredawa</td>
                                    <td>2,015</td>
                                    <td>2,020</td>
                                    <td>0</td>
                                    <td>125.475</td>
                                    <td>29.13</td>
                                </tr>
                                <tr>
                                    <td>8</td>
                                    <td>One Drinkable water and sanitation
                                        project</td>
                                    <td>All regions and Diredawa</td>
                                    <td>2,011</td>
                                    <td>2,017</td>
                                    <td>70.85</td>
                                    <td>634.94</td>
                                    <td>5318.33754</td>
                                </tr>
                                <tr>
                                    <td>9</td>
                                    <td>23 curban cities drianage Inistitution
                                        construction project</td>
                                    <td>National</td>
                                    <td>2,009</td>
                                    <td>2,016</td>
                                    <td>52.86</td>
                                    <td>538</td>
                                    <td>9390.78</td>
                                </tr>
                                <tr>
                                    <td>10</td>
                                    <td>ODF projects</td>
                                    <td>All Urban Areas</td>
                                    <td>2,012</td>
                                    <td>2,017</td>
                                    <td>34.4</td>
                                    <td>923</td>
                                    <td>69.49</td>
                                </tr>
                                <tr>
                                    <td colspan="6"></td>
                                    <td class="table-primary"> 17.3</td>
                                    <td class="table-primary"> 18.35 </td>
                                </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

    `
  }



  html+=cardHeader()
  html+=`
  <div class="card-body">
    <div class="row">
      <div class="col-sm-12 col-xl-9">
       <div class="tab-content" id="myTabContent">
  `
  html+=section1()
  html+=section2()
  html+=section4()
  html+=section3()
  html += `
  </div> 
   </div>
    </div>

    <div class="col-sm-12 col-xl-3">
    <h3 class="text-center text-success">General Overview</h3>
    <hr/>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">
          <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                  <div class="avtar avtar-s bg-light-secondary"><i class="bi bi-gear"></i></div>
              </div>
              <div class="flex-grow-1 ms-3">
                  <div class="row g-1">
                      <div class="col-12">
                          <p class="text-muted mb-1">Number of Projects</p>
                          <h6 class="mb-0">455</h6>
                      </div>
                  </div>
              </div>
          </div>
      </li>

      <li class="list-group-item">
          <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                  <div class="avtar avtar-s bg-light-secondary"><i class="bi bi-cash"></i></div>
              </div>
              <div class="flex-grow-1 ms-3">
                  <div class="row g-1">
                      <div class="col-12">
                          <p class="text-muted mb-1">Total Cost of the project (Billion Birr)</p>
                          <h6 class="mb-0">18,471.49</h6>
                      </div>
                  </div>
              </div>
          </div>
      </li>

      <li class="list-group-item">
          <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                  <div class="avtar avtar-s bg-light-secondary"><i class="bi bi-wallet2"></i></div>
              </div>
              <div class="flex-grow-1 ms-3">
                  <div class="row g-1">
                      <div class="col-12">
                          <p class="text-muted mb-1">Expenditure to date (Trillion Birr)</p>
                          <h6 class="mb-0">18,896</h6>
                      </div>
                  </div>
              </div>
          </div>
      </li>


    </ul>

    </div>
  
    </div>
    </div>
    </div>
  `
  return html
}
let randomColor = () => {
  const borderColors = [
    'primary', 'secondary', 'success', 
    'danger', 'warning', 'info'
  ];

  return borderColors[Math.floor(Math.random() * borderColors.length)];
}

//Loading
let renderRoadProject = () => {

  var options = {
    series: [{
    name: 'Total',
    data: [360, 781.0, 20.5, 306.8, 78.7, 100.0]
  }, {
    name: 'Trunk Road Rehabilitation',
    data: [781.0, 6.5, 237.1, 523.5, 13.8, 0.1]
  },
  {
    name: 'Trunk Road Upgrading',
    data: [20.5, 0.2, 1.6, 15.3, 3.4, 0.0]
  },
  {
    name: 'New Road Project',
    data: [306.8, 1.9, 48.9, 134.2, 121.8, 0.0]
  },
  {
    name: 'Road Heavy Maintenance',
    data: [78.7, 1.3, 18.6, 54.2, 2.6, 2.0]
  },
  {
    name: 'Bridge Construction and Rehabilitation',
    data: [100.0, 0.8, 30.4, 67.0, 1.8, 0.0]
  },
],
    chart: {
    type: 'bar',
    height: 900
  },
  plotOptions: {
    bar: {
      horizontal: true,
      dataLabels: {
        position: 'top',
      },
    }
  },
  dataLabels: {
    enabled: true,
    offsetX: -6,
    style: {
      fontSize: '12px',
      colors: ['#fff']
    }
  },
  stroke: {
    show: true,
    width: 1,
    colors: ['#fff']
  },
  tooltip: {
    shared: true,
    intersect: false
  },
  xaxis: {
    categories: ["Total", "Trunk Road Rehabilitation", "Trunk Road Upgrading", "New Road Project", "Road Heavy Maintenance", "Bridge Construction and Rehabilitation"],
  },
  };

  var chart = new ApexCharts(document.querySelector("#monthly-report-graph"), options);
  chart.render();
} 

let indicatorCards = (item, seasonType, value, randomBgColor) =>{


  return `<div class="col-md-6 col-xxl-4 col-12">
            <div class="card border-${randomBgColor} ">
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
                            <h6 class="mb-0">${item.indicator__title_ENG} (${seasonType == 'Month' ? 'Mth' : 'Annual'}) </h6>
                        </div>
                        <div class="flex-shrink-0 ms-3">
                            <div class="dropdown"><a
                                    class="avtar avtar-s btn-link-primary dropdown-toggle arrow-none" href="#"
                                    data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i
                                        class="ti ti-dots-vertical f-18"></i></a>
                                <div class="dropdown-menu dropdown-menu-end">
                                ${seasonType == 'monthly' ? `
                                <a class="dropdown-item" href="#">Month</a>
                                <a class="dropdown-item" href="#">Year</a>
                                ` : ''}
                                   
                                    <button data-id="${item.id}"  data-type-of = "${item.indicator__type_of}" class=" detail-category  detail-category dropdown-item" data-bs-toggle="modal" data-bs-target="#exampleModal" > <svg class="pc-icon"> <use xlink:href="#custom-flash"></use></svg> Detail</button>
                                    </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-body p-3 mt-3 rounded" style="height: 100px;">
                        <div class="mt-3 row align-items-center">
                            <div class="col-7">
                                <div id="all-earnings-graph${item.indicator__id}"></div>
                            </div>
                            <div class="col-5" style="margin: -15px;">
                                    <h4 class="mb-3 ms-3 float-sm-start float-xl-end ">
                                    <span class="badge bg-light-${randomBgColor} border border-${randomBgColor} border border-success">${value[value.length - 1] ? value[value.length - 1].for_datapoint_id__year_GC : ''}  <hr>${value[value.length - 1] ? value[value.length - 1].value.toLocaleString() : ''} </span>
                                    </h4>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
          </div>`;
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

let showLoadingSkeleton = () => {
  $("#loading-skeleton-category").html("")
  for (let i = 0; i < 6; i++) {
    $("#loading-skeleton-category").append(`
        <div class="col-md-4 col-xxl-4 container loading-skeleton">
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
  $("#loading-skeleton-category").html("");
};


let renderCategoryGraph = (id, dataArray, bootstrapColorsCode) => {
  const ColorsCode = {
    "primary" : "#0d6efd",
    "secondary" : "#6610f2",
    "success" : "#198754",  // Corrected closing quotation mark
    "danger": "#dc3545",
    "warning" : "#ffc107",
    "info" : "#20c997",
};


  
  const seriesData = dataArray.map((dataPoint) => {
    return {
      x: dataPoint[0], // Year
      y: dataPoint[1], // Value
    };
  });
$(`#all-earnings-graph${id}`).html("")
new ApexCharts(document.querySelector(`#all-earnings-graph${id}`), {
  series: [
    {
      data: [
        { x: "", y: [1, 6] },
        { x: "", y: [3, 7] },
        { x: "", y: [4, 8] },
        { x: "", y: [5, 9] },
        { x: "", y: [4, 8] },
        { x: "", y: [4, 7] },
        { x: "", y: [2, 5] },
      ],
    },
  ],
  chart: {
    type: "rangeBar",
    height: 80,
    sparkline: { enabled: !0 },
    toolbar: { show: !1 },
  },
  colors: ["#E58A00"],
  plotOptions: {
    bar: { columnWidth: "30%", borderRadius: 5, horizontal: !1 },
  },
  yaxis: { tickAmount: 2, min: 0, max: 10 },
  grid: { show: !1, padding: { top: 0, right: 0, bottom: 0, left: 0 } },
  xaxis: {
    labels: { show: !1 },
    axisBorder: { show: !1 },
    axisBorder: { show: !1 },
    axisTicks: { show: !1 },
  },
  dataLabels: { enabled: !1 },
}).render();
var e = {
chart: { height: 250, type: "bar", toolbar: { show: !1 } },
plotOptions: {
  bar: {
    horizontal: !1,
    columnWidth: "55%",
    borderRadius: 4,
    borderRadiusApplication: "end",
  },
},
legend: { show: !0, position: "top", horizontalAlign: "left" },
dataLabels: { enabled: !1 },
colors: ["#4680FF", "#4680FF"],
stroke: { show: !0, width: 3, colors: ["transparent"] },
fill: { colors: ["#4680FF", "#4680FF"], opacity: [1, 0.5] },
grid: { strokeDashArray: 4 },
series: [
  { name: "Net Profit", data: [76, 85, 101, 98, 87, 105, 91] },
  { name: "Revenue", data: [44, 55, 57, 56, 61, 58, 63] },
],
xaxis: { categories: ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"] },
tooltip: {
  y: {
    formatter: function (e) {
      return "$ " + e + " thousands";
    },
  },
},
};
};



let renderHalfPieChart = (data, html, max) => {
  Highcharts.chart(`${html}`, {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: `Indicator<br>shares<br>${max}`,
        align: 'center',
        verticalAlign: 'middle',
        y: 60,
        style: {
            fontSize: '1.1em'
        }
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Indicators share',
        innerSize: '50%',
        data: data
    }]
});

}


let lineGraph = (graphData, min, html) => {
  Highcharts.chart(`${html}`, {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Indicators Relation'
    },
    yAxis: {
        title: {
            text: 'Value'
        }
    },
    tooltip: {
        pointFormat: '{series.name} had stockpiled <b>{point.y:,.0f}</b><br/>' +
            'warheads in {point.x}'
    },
    plotOptions: {
        area: {
            pointStart: Number(min),
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        }
    },
    series: graphData
  });
}

let barChart = (graphData, indicators) => {
  Highcharts.chart('barChart', {
    chart: {
        type: 'bar'
    },
    title: {
        text: `Last 3 Year's `,
        align: 'left'
    },
    xAxis: {
        categories: indicators,
        title: {
            text: null
        },
        gridLineWidth: 1,
        lineWidth: 0
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Values',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        },
        gridLineWidth: 0
    },
    tooltip: {
        valueSuffix: ' '
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
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        shadow: true
    },
    credits: {
        enabled: false
    },
    series: graphData,
  });
}

let pieChart = (graphData, max) => {
  // Data retrieved from https://netmarketshare.com/
// Build the chart
Highcharts.chart('pieChart', {
  chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
  },
  title: {
      text: `Indicator shares in ${max}`,
      align: 'left'
  },
  tooltip: {
      pointFormat: '{series.name} <b>{point.percentage:.1f}%</b>'
  },
  accessibility: {
      point: {
          valueSuffix: '%'
      }
  },
  plotOptions: {
      pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
              enabled: false
          },
      }
  },
  series: [{
      name: 'Values',
      colorByPoint: true,
      data: graphData,
  }]
});

}

let fetchIndicatorDetail = () =>{
  $(".indicator-detail").click(function(){
    const buttonData = $(this).data()

      $("#analytics-tab-2")[0].click(); //Trigger to detail button clicked automatically 
  
    $.ajax({
      type: "GET",
      url: `/dashboard-api/indicator-detail/${buttonData.indicatorId}`,
      success: function(data){
        const graphData = []
        const dataValue = []
        const childData = []
        let min = data.values[0].for_datapoint_id__year_EC
        let max = data.values[data.values.length - 1].for_datapoint_id__year_EC

        let table = `
        <div class="table-responsive">
        <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Indicator</th>
            
        `
        for (let i = min; i <= max; i++) {
          table += `<th scope="col">${i}</th>`
        }

        table += `
      </tr>
        </thead>
        <tbody>`

        let counter = 1
        let parentIndicator = data.indicators[0]

        table += `<tr>
        <th scope="row">${counter}</th>
        <td class="fw-bold">  ${parentIndicator.title_ENG}</td>
      `
      let values = data.values.filter((value) => value.for_indicator_id == parentIndicator.id)



      for (let yr = min; yr <= max; yr++) {
        let checkedYear = false

        let yearValue = values.find((item) => item.for_datapoint_id__year_EC == yr)

          if(yearValue){
            checkedYear = true
            table += `<td>${yearValue.value}</td>`
            dataValue.push(yearValue.value)
          }
      
      if(checkedYear  == false ){
        dataValue.push(0)
        table += `<td> - </td>`
      }
    }



      graphData.push(
        {
          name: parentIndicator.title_ENG,
          data : dataValue
        }
      )

      table+=`</tr>`
       

        let filterChildIndicatorTable = (parent, space) =>{
          let spaceChild = space+"&nbsp;&nbsp;&nbsp;&nbsp;"

          let childLists = data.indicators.filter((children) => children.parent_id == parent.id )
          for(let child of  childLists){   
            if(child.parent_id == parent.id){
              counter++;
              table += `<tr>
              <th scope="row">${counter}</th>
              <td> ${space} ${child.title_ENG}</td>
            `
            let values = data.values.filter((value) => value.for_indicator_id == child.id)
            let valueYear = values.filter((value) =>value.for_datapoint_id__year_EC )
            for (let yr = min; yr <= max; yr++) {
              let checkedYear = false
      
              let yearValue = values.find((item) => item.for_datapoint_id__year_EC == yr)
      
                if(yearValue){
                  checkedYear = true
                  table += `<td>${yearValue.value}</td>`
                  dataValue.push(yearValue.value)
                }
            
            if(checkedYear  == false ){
              dataValue.push(0)
              table += `<td> - </td>`
            }
          }
            childData.push(
              [child.title_ENG, values[values.length-1].value]
            )

            table+=`</tr>`
            filterChildIndicatorTable(child, spaceChild)
            }
          }
        }
        
        filterChildIndicatorTable(parentIndicator, "&nbsp;&nbsp;")

        table += `</tbody>
        </table>
      </div>
        `

      
        $('#indicator-detail-table').html(table)
        lineGraph(graphData, min, 'lineGraph-detail')

        if(childData.length > 0){
          $('#lineGraph-detail-parent-html').removeClass('col-12').addClass('col-md-6')
          renderHalfPieChart(childData, 'half-pie-chart-detail', max)
        }else{
          $('#lineGraph-detail-parent-html').removeClass('col-md-6').addClass('col-12')

          $('#half-pie-chart-detail').html('')
        }
       
      }
    })
  })
}

let monthGraph = (data_set) =>{

  (async () => {
    /**
     * Create the chart when all data is loaded
     * @return {undefined}
     */
    function createChart(series) {
      Highcharts.stockChart("monthChart", {
        rangeSelector: {
          selected: 4,
        },

        yAxis: {
          labels: {
            format: "{#if (gt value 0)}+{/if}{value}%",
          },
          plotLines: [
            {
              value: 0,
              width: 2,
              color: "silver",
            },
          ],
        },

        plotOptions: {
          series: {
            label: {
              connectorAllowed: false,
            },
          },
        },

        tooltip: {
          pointFormat:
            '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
          valueDecimals: 2,
          split: true,
        },

        series,
      });
    }
    createChart(data_set);
  })();

}

  //Handel onclick category detail
let handelCategoryDetail = () => {
    $(".detail-category").click(function () {
      let buttonData = $(this).data();
     
      $.ajax({
        url: `/dashboard-api/category_detail_list/${buttonData.id}`,
        beforeSend: function () {
          showLoadingSpinner('spinnerLoading')
          $("#analytics-tab-1")[0].click();
          $("#monthChart").hide()
          $("#analytics-tab-2").hide()
          $("#indicator-detail-table").hide()
          $("#category-detail-chart-lists").hide()
          $("#analytics-tab-2").hide()
          $("#indicator-detail-table").hide()
          $("#category-detail-chart-lists").hide()
          $('#category-detail-table').hide()
        },
        complete: function () {
          hideLoadingSpinner('spinnerLoading')
          $('#category-detail-table').show()
        },
        success: function (data) {
          data.year = data.year.sort()
          let min = data.year[0]
          let max = data.year[data.year.length - 1]

          if(buttonData.typeOf == 'yearly'){
            const graphData = []
            const barChartData = []
            const pieChartData = []
  
  
            let tableYear = `
            <div class="table-responsive">
            <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Indicator</th>
            `
            for (let i = min; i <= max; i++) {
              tableYear += `<th scope="col">${i}</th>`
            }
  
            tableYear += `
          <th scope="col">Action</th>    
          </tr>
            </thead>
            <tbody>`
            let counter = 1
            const dataValueChart1 = []
            const dataValueChart2 = []
            const dataValueChart3 = []
  
            const indicatorName = []
  
            data.indicators.forEach((item) => {
              indicatorName.push(item.title_ENG)
  
              let values = data.values.filter((value) => value.for_indicator_id == item.id)
  
  
  
  
              tableYear += `<tr>
                 <th scope="row">${counter}</th>
                  <td>${item.title_ENG}</td>
                 `
              const dataValue = []
              
  
              for (let yr = min; yr <= max; yr++) {
                let checkedYear = false

                let yearValue = values.find((item) => item.for_datapoint_id__year_EC == yr)

                  if(yearValue){
                    checkedYear = true
                    tableYear += `<td>${yearValue.value}</td>`
                    dataValue.push(yearValue.value)
                  }
              
              if(checkedYear  == false ){
                dataValue.push(0)
                tableYear += `<td> - </td>`
              }
            }
              
            tableYear+=`
              <td> <button data-indicator-id = ${item.id} class="btn btn-sm btn-primary indicator-detail" ><i class="bi bi-eye"></i></button> </td>
              </tr>`
             
  
              graphData.push(
                {
                  name: item.title_ENG,
                  data : dataValue
                }
              )
  
              dataValueChart1.push(dataValue[dataValue.length -  1])
              dataValueChart2.push(dataValue[dataValue.length -  2])
              dataValueChart3.push(dataValue[dataValue.length -  3])
  
              pieChartData.push({
                name: item.title_ENG,
                y : dataValue[dataValue.length -  1]
              })
            
  
              counter++;
            
            })
  
            barChartData.push(
              {
                name: `Year ${max}`,
                data: dataValueChart1,
              }
            )
            barChartData.push(
              {
                name: `Year ${max-1}`,
                data: dataValueChart2,
              }
            )
            barChartData.push(
              {
                name: `Year ${max-2}`,
                data: dataValueChart3,
              }
            )
  
            tableYear += `</tbody>
                </table>
              </div>
                `
            $("#analytics-tab-1")[0].click();
            $("#monthChart").hide()
            $('#category-detail-table').html(tableYear)
            $("#analytics-tab-2").show()
            $("#indicator-detail-table").show()
            $("#category-detail-chart-lists").show()
            lineGraph(graphData, min, 'lineGraph')
            barChart(barChartData,indicatorName)
            pieChart(pieChartData, max)
            fetchIndicatorDetail()
          }
          else if (buttonData.typeOf == 'monthly'){
            let data_set = []

            let table = `
            <div class="table-responsive">
            <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Year</th>
                <th scope="col">Month</th>
            `

            let counter = 1;
            for(indicator of data.indicators){
              table += `<th scope="col">${indicator.title_ENG}</th>`
            }

            table += `
          </tr>
            </thead>
            <tbody>`

            //For table creation
            for (let i = min; i <= max; i++) {
              let yearPrint = false
              

              for(let month of data.months){
                table += `
                <tr>`
                if(!yearPrint){
                  table += `
                  <th scope="col">${counter}</th>
                  <td class="fw-bold">${i}</td>
                  `
                  counter++;
                }else{
                  table += `
                  <th scope="col"></th>
                  <td> </td>
                  `
                }

                table+=`
                <td>${month.month_AMH}</td>
                `
              
                yearPrint = true


                for(indicator of data.indicators){
                   let value = data.values.find((value) => value.for_datapoint_id__year_EC == i && value.for_month_id__number == month.number && value.for_indicator_id == indicator.id)
                   if(value){
                      table+=` <td>${value.value}</td>`
                   }else{
                    table+=` <td> - </td>`
                   }
                }

                
                table+= `
                </tr>
                `
              }
              
            }


            //for chart
            let arr = [];
            for(indicator of data.indicators){
              for(let year=min; year<=max; year++){
                for(month of data.months){
                  let value = data.values.find((value) => value.for_datapoint_id__year_EC == year && value.for_month_id__number == month.number && value.for_indicator_id == indicator.id)
                  if(value){
                    arr.push([Date.UTC(parseInt(year), parseInt(month.number), 1), (value.value)]);
                  }
                }
              }
              data_set.push({'name' : indicator.title_ENG, 'data' : arr})
              arr = []
            }  

            table += `</tbody>
                  </table>
                </div>
                  `


            monthGraph(data_set) // set Chart datas
            $("#monthChart").show()
            $("#analytics-tab-1")[0].click();
            $("#analytics-tab-2").hide()
            $("#indicator-detail-table").hide()
            $("#category-detail-chart-lists").hide()
            $('#category-detail-table').html(table)
          }else if (buttonData.typeOf == 'quarterly'){s
            let data_set = []

            let table = `
            <div class="table-responsive">
            <table class="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Year</th>
                <th scope="col">Quarter</th>
            `

            let counter = 1;
            for(indicator of data.indicators){
              table += `<th scope="col">${indicator.title_ENG}</th>`
            }

            table += `
          </tr>
            </thead>
            <tbody>`

            //For table creation
            for (let i = min; i <= max; i++) {
              let yearPrint = false
              

              for(let quarter of data.quarters){
                table += `
                <tr>`
                if(!yearPrint){
                  table += `
                  <th scope="col">${counter}</th>
                  <td class="fw-bold">${i}</td>
                  `
                  counter++;
                }else{
                  table += `
                  <th scope="col"></th>
                  <td> </td>
                  `
                }

                table+=`
                <td>${quarter.title_ENG}</td>
                `
              
                yearPrint = true


                for(indicator of data.indicators){
                   let value = data.values.find((value) => value.for_datapoint_id__year_EC == i && value.for_quarter__number == quarter.number && value.for_indicator_id == indicator.id)
                   if(value){
                      table+=` <td>${value.value}</td>`
                   }else{
                    table+=` <td> - </td>`
                   }
                }

                
                table+= `
                </tr>
                `
              }
              
            }


            //for chart
            let arr = [];
            for(indicator of data.indicators){
              for(let year=min; year<=max; year++){
                for(quarter of data.quarters){
                  let value = data.values.find((value) => value.for_datapoint_id__year_EC == year && value.for_quarter__number == quarter.number && value.for_indicator_id == indicator.id)
                  if(value){
                    arr.push([Date.UTC(parseInt(year), parseInt(quarter.number), 1), (value.value)]);
                  }
                }
              }
              data_set.push({'name' : indicator.title_ENG, 'data' : arr})
              arr = []
            }  

            table += `</tbody>
                  </table>
                </div>
                  `


            monthGraph(data_set) // set Chart datas
            $("#monthChart").show()
            $("#analytics-tab-1")[0].click();
            $("#analytics-tab-2").hide()
            $("#indicator-detail-table").hide()
            $("#category-detail-chart-lists").hide()
            $('#category-detail-table').html(table)
          }

        

        }

      })
    })
  }


let handleTopicClicked = () =>{
  //Handel on Click topic card
  $(".topic-card").click(function () {
    $("#bigPieChartParent").html('')
    const buttonData = $(this).data();

    $("#category-card-list").html("");
    $("#sidebarHtml").addClass("d-none")
    $(".selected-card").removeClass("border border-secondary shadow-lg border-4")
    $("#category-card-list").html("");
    $.ajax({
      type: "GET",
      url: `/key_area_list/${buttonData.id}`,
      beforeSend: function () {
        hideLoadingSkeletonCategory();
        showLoadingSkeleton();
      },
      complete: function () {
        hideLoadingSkeletonCategory();
      }, success: function (data) {
        if (data.goal_list.length > 0) {
          $("#choose_goal").html("");
          $("#category-card-list").html("");
    
          data.goal_list.forEach((goal) => {
            let color = randomColor();
            $("#choose_goal").append(`<option id="${goal.id}">${goal.goal_name_eng}</option>`);
    
            let filteredKeyResultAreas = data.KeyResultArea_list.filter(
              (item) => item.goal_id === goal.id
            );
    
            $("#category-card-list").append(`
              <div class="card">
                <div class="card-header">${goal.goal_name_eng}</div>
                <div class="card-body">
                  ${filteredKeyResultAreas
                    .map((item) => `<p>${item.activity_name_eng}</p>`)
                    .join("")}
                </div>
              </div>
            `);
          });
        }
        else{
          $("#category-title").html('<p class="text-center text-danger h3">No Data Found</p>')
        }
      },

    });
   
   
  });
  
}

let defaultCategoryLists = ( search = null) => {
  //Default 
  $("#category-card-list").html("");
  $.ajax({
    type: "GET",
    url: `/goal_list/1${search ? '?'+search : '' }`,
    beforeSend: function () {
      showLoadingSkeleton();
    },
    complete: function () {
      hideLoadingSkeletonCategory();
    },
    success: function (data) {
      console.log(data)

      if(data.goal_list.length > 0){
        $("#choose_goal").html("")
              data.goal_list.forEach((cat) => {
                let color = randomColor()
                  $("#choose_goal").append(
                    `<option selected>${cat.goal_name_eng}</option>
                    `
                  )
          })
         
        let category = ``;
        try{ $("#category-title").html(data.goal_list[0].goal_name_eng);}
        catch{ null}


        $("#category-card-list").append(indicatorCards(item, seasonType, value,color));
        renderCategoryGraph(item.indicator__id, valueItem , color);
        handelCategoryDetail()
        
      }else{
        $("#category-title").html('<p class="text-center text-danger h3">No Data Found</p>')
      }
    },
  });
}


let handleOnSearch = () =>{
  $("#searchItemForm").submit(function(e){
    let form = $("#searchItemForm")
    e.preventDefault()
    let searchItem  = this.q.value
    defaultCategoryLists(`q=${searchItem}`)
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
      url: "/dashboard-api/search_category_indicator/",
      data: { search: searchValue },
      success: function(data) {
        let a = data.indicators.map((item) => `<option value="${item.indicator__title_ENG}">${item.indicator__title_ENG}</option>`)
        $("#autocomplete").html(a)
      },
    })
    
  })
}


// let homePieChart = () => {
//   $.ajax({
//     url: "/dashboard-api/pie_chart_data",
//     type: "GET",

//     success: function (dataMain) {
//       let chartData = [
//         {
//           id: '0.0',
//           parent: '',
//           name: "National Topic",
//         },
//       ];

//       // Assign topics with their corresponding parent
// for (const topic of dataMain.topics) {
//     const newObj = {
//       id: `1.${topic.id}`,
//       parent: '0.0',
//       name: topic.title_ENG,
//       value: topic.category_count,
//     };
//     chartData.push(newObj);
//   }
  
//   // Assign categories with their corresponding parent
//   for (const cat of dataMain.category) {
//     const newObj = {
//       id: `2.${cat.id}`,
//       parent: `1.${cat.dashboard_topic__id}`,
//       name: cat.name_ENG,
//       value: cat.category_count,
//     };
//     chartData.push(newObj);
//   }
  
//   // Assign indicators with their corresponding parent
//   for (const indicator of dataMain.indicators) {
//     const obj = {
//       id: `3.${indicator.id}`,
//       parent: `2.${indicator.for_category__id}`,
//       name: indicator.title_ENG,
//       value: 3,
//     };
//     chartData.push(obj);
//   }



//   Highcharts.chart('bigPieChart', {

//     chart: {
//         height: '100%'
//     },

//     // Let the center circle be transparent
//     colors: ['transparent'].concat(Highcharts.getOptions().colors),

//     title: {
//         text: 'National Topic'
//     },

//     series: [{
//         type: 'sunburst',
//         data: chartData,
//         name: 'National Level',
//         allowDrillToNode: true,
//         borderRadius: 3,
//         cursor: 'pointer',
//         dataLabels: {
//             format: '{point.name}',
//             filter: {
//                 property: 'innerArcLength',
//                 operator: '>',
//                 value: 16
//             }
//         },
//         levels: [{
//             level: 1,
//             levelIsConstant: false,
//             dataLabels: {
//                 filter: {
//                     property: 'outerArcLength',
//                     operator: '>',
//                     value: 64
//                 }
//             }
//         }, {
//             level: 2,
//             colorByPoint: true
//         },
//         {
//             level: 3,
//             colorVariation: {
//                 key: 'brightness',
//                 to: -0.5
//             }
//         }, {
//             level: 4,
//             colorVariation: {
//                 key: 'brightness',
//                 to: 0.5
//             }
//         }]

//     }],

//     tooltip: {
//         headerFormat: '',
//         pointFormat: '<b>{point.name}</b>' 
//     }
// });
//     },
//     error: function (xhr, status, error) {
//       console.error("AJAX request failed:", error);
//     },
//   });
// }

$(document).ready(function () {

  $.ajax({
    type: "GET",
    url: "/ministries_lists/",
    beforeSend: function () {
      showLoadingSkeletonTopic();
      showLoadingSkeleton();
    },
    complete: function () {
      hideLoadingSkeletonTopic();
      hideLoadingSkeletonCategory();
    },
    success: function (data) {
      console.log(data)
      handleOnSearch()
      const bootstrapColors = [
        "primary",
        "secondary",
        "success",
        "warning",
        "info",
        "dark",
      ];
      let cardTopic = ``
      let sideNav = ``;
      let selectedCard = ''
      data.ministries.forEach((item) => {
        cardTopic += `
        <!-- custom cards -->
          <div class="col-md-6  col-xl-3 d-none d-md-block topic-card"
             data-id = ${item.id}
             data-category-name = "${item.responsible_ministry_eng}"
             >
                <div class="card ${ item.id == 3 ? selectedCard : '' } selected-card social-widget-card bg-${bootstrapColors[Math.floor(Math.random() * bootstrapColors.length)]}">
                    <div class="card-body d-flex justify-content-between align-items-center p-2">
                        <div class="d-flex flex-column">
                            <h3 class="text-white m-0">${Number(item.goal_count)} +</h3>
                            <span class="m-t-10">${item.responsible_ministry_eng}</span>
                        </div>
                        
                    </div>
                </div>
            </div>`;

        sideNav += `<li class="pc-item topic-card" data-id = ${item.id} data-category-name = "${item.responsible_ministry_eng}">
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
      <div class="row justify-content-center">
        <div class="col-5">
          <label for="choose_goal" class="form-label h5">Select a goal</label>
          <select id="choose_goal" class="form-select form-select-md" aria-label=".form-select-sm example">
            <option selected>Open this select menu</option>
            <option value="1">One</option>
            <option value="2">Two</option>
            <option value="3">Three</option>
          </select>
        </div>
      </div>
      `
      
      $("#topic-card-lists").html(cardTopic);
      $("#topic-card-lists").append(goals_list);
      $("#sidebar-topic-list").html(sideNav);

      handleTopicClicked() 

    },error: function(response) {
      hideLoadingSkeletonTopic();
      hideLoadingSkeletonCategory();
    }
  
  });

  //Default 
  defaultCategoryLists()

  
});



