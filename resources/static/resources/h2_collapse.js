$(document).ready(function(){
    $('table').prev().append('<span class="expand">[<b>-</b>]</span>');
    $(".expand").click(function () {
        $(this).closest('h2').nextUntil('module').slideToggle();
        if($(this).text() == '[-]') {
            $('.expand').text('[+]');
        } else {
            $('.expand').text('[-]');
        }
    });
});