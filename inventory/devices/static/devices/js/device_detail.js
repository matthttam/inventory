$(document).ready(function(){
    console.log('loaded')
    $("#minimize-inner-nav").on("click", function(){
        $(this).toggleClass('inventory-icon-rotate-180 inventory-icon-rotate-360', 1000)
        $(".inner-nav-text").toggle()
    })
})