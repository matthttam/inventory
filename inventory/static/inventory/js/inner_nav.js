$(document).ready(function(){
    
    // Auto hide innernav based on size and orientation changes.
    $(window).on('resize orientationChanged', function(e) {
        var breakpoint = 1300
        var windowWidth = $(window).width();
        inventoryInnerNav = $('.inventory-innernav').first()
        is_hidden = inventoryInnerNav.hasClass('inventory-innernav-toggled')
        if(windowWidth < breakpoint && !is_hidden){
            $("a[data-inv-toggle='collapse']").trigger('click')
        }else if(windowWidth > breakpoint && is_hidden){
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
       }
    }

    // Try really hard to scroll to the top of a tab when it is hiding or after it is shown or when the tab is clicked
    $('.inventory-innernav a[data-bs-toggle="tab"]').on('hide.bs.tab shown.bs.tab click', e => {
        $(this).scrollTop(0)
    })
    // Set URL Fragment for clicked link.
    $('.inventory-innernav a[data-bs-toggle="tab"]').on('shown.bs.tab', event => {
        window.location.hash = $(event.target).attr('href');
    })
})