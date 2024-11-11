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

let hideLoadingSpinner = (div) => {
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