$(document).ready(function(){
    //$($("a[data-inv-toggle='collapse']").attr('data-inv-target')).hide()
    //$($("a[data-inv-toggle='collapse']").attr('data-inv-target')).addClass('inventory-inner-nav-text-hidden')
    $("a[data-inv-toggle='collapse']").on("click", function(e){
        inventoryInnerNav = $('.inventory-inner-nav').first()
        $(this).toggleClass('inventory-icon-rotate-180 inventory-icon-rotate-360', 1000)
        $($(this).attr('data-inv-target')).animate({'width': 'toggle'})
        inventoryInnerNav.toggleClass('inventory-sidenav-toggled');
        value = inventoryInnerNav.hasClass('inventory-sidenav-toggled')
        localStorage.setItem('inventory|sidenav-toggle', value);
        document.cookie="inventory_sidenav_toggle="+value+"; path=/;expires="
    })
})