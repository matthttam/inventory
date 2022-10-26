$(document).ready(function(){
    $('#sidebarToggle').on('click', event => {
        event.preventDefault();
        document.body.classList.toggle('sb-sidenav-toggled');
        value = document.body.classList.contains('sb-sidenav-toggled')
        localStorage.setItem('sb|sidenav-toggle', value);
        document.cookie="sb_sidenav_toggle="+value+"; path=/;expires="
    })
})