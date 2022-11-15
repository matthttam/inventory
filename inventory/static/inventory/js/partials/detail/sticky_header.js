$(document).ready(function(){
    
    // Auto hide innernav based on size and orientation changes.
    $(window).on('resize orientationChanged', function(e) {
        console.log('here')
        var header = $('.detail-sticky-header')
        var height = header.height() + 15;//take the header height
        header.next().css({'margin-top':height});//alter the margin of the wrapped content
    }).trigger('resize');//trigger the margin resize when page is loaded

})