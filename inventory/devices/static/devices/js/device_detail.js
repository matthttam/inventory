$(document).ready(function(){

    
    $(window).on('resize orientationChanged', function(e) {
        var windowWidth = $(window).width();
        inventoryInnerNav = $('.inventory-innernav').first()
        is_toggled = inventoryInnerNav.hasClass('inventory-innernav-toggled')
        if(windowWidth < 960 && !is_toggled){
            $("a[data-inv-toggle='collapse']").trigger('click')
        }else if(windowWidth > 960 && is_toggled){
            $("a[data-inv-toggle='collapse']").trigger('click')
        }
    })
    $("a[data-inv-toggle='collapse']").on("click", function(e){
        inventoryInnerNav = $('.inventory-innernav').first()
        $($(this).attr('data-inv-target')).animate({'width': 'toggle'})
        inventoryInnerNav.toggleClass('inventory-innernav-toggled');
        value = inventoryInnerNav.hasClass('inventory-innernav-toggled')
        localStorage.setItem('inventory|innernav-toggled', value);
        document.cookie="inventory_innernav_toggled="+value+"; path=/;expires="

    })

    var hash = window.location.hash;
    if(hash != ''){
       tab = $("a[href='"+hash+"']")
       if(tab){
        tab.tab('show')
        $(window).scrollTop(0)
       }
    }
    $('.inventory-innernav a[data-bs-toggle="tab"]').on('shown.bs.tab', event => {
        console.log('shown.bs.tab')
        $(window).scrollTop(0)
        window.location.hash = $(event.target).attr('href');
    })
})