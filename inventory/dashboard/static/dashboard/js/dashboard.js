$(document).ready(function(){
    $('#sidebarToggle').on('click', event => {
        event.preventDefault();
        document.body.classList.toggle('sb-sidenav-toggled');
        value = document.body.classList.contains('sb-sidenav-toggled')
        localStorage.setItem('sb|sidenav-toggle', value);
        document.cookie="sb_sidenav_toggle="+value+"; path=/;expires="
    })

    $(window).on('resize orientationChanged', function(e) {
        var breakpoint = 994
        var windowWidth = $(window).width();
        sbSideNav = $('.sb-nav-fixed').first()
        is_hidden = sbSideNav.hasClass('sb-sidenav-toggled')
        if(windowWidth < breakpoint && !is_hidden){
            $("#sidebarToggle").trigger('click')
        }else if(windowWidth > breakpoint && is_hidden){
            $("#sidebarToggle").trigger('click')
        }
    })
})