$(document).ready(function(){
    console.log('loaded')
    $("a[data-inv-toggle='collapse']").on("click", function(e){
        console.log($(this))
        $(this).toggleClass('inventory-icon-rotate-180 inventory-icon-rotate-360', 1000)
        $($(this).attr('data-inv-target')).animate({'width': 'toggle'})
    })
})