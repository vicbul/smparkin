$(document).ready(function(){
//    $(".level0").css("background-color", "yellow");
//    $(".level1").css("background-color", "red");
//    $(".level2").css("background-color", "green");
//    $(".level3").css("background-color", "blue");
//    $(".level4").css("background-color", "orange");
    $('<span class="collapsible"><</span>').insertBefore('.level_up');

    var levels = [];
    $('.level-block').each(function() {
        levels.push(+$(this).data('level'));
    })
    var max_level = Math.max.apply(Math, levels);

    $('<div class="levels-display"></div>').insertAfter('.expand-levels');
    $.each(new Array(+max_level+1), function(index) { // for (var n = 0; n <= max_level; ++ n)
        $('<b>&nbsp;&nbsp;>&nbsp;</b><button class="hide-level" data-level='+index+'>Level '+index+'</button>').insertBefore('.levels-display');
    });

    $('.hide-level').on('click', function(event) {
        event.preventDefault();
        var level_cut = +$(this).data('level')
        $('.hide-level').each(function(i) {
            if (i <= level_cut) {
                $(this).addClass('highlight'); //css({'font-weight':'bold', 'background-color':'green','color':'white'});
                $('.level'+i).closest('ul').slideDown();
                $('.level'+i).closest('ul').prev('.collapsible').text('<');
            } else {
                $(this).removeClass('highlight'); //css({'font-weight':'normal', 'background-color':'white','color':'black'});
                $('.level'+i).closest('ul').slideUp();
                $('.level'+i).closest('ul').prev('.collapsible').text('>');
            }
        });

    });

    $('.collapsible').on('click', function(event) {
        event.preventDefault();
        $('.hide-level').removeClass('highlight');
        $(this).closest('li').find('.level_up').first().slideToggle('fast');
        if ($(this).text() == '<') {
            $(this).text('>');
        } else {
            $(this).text('<');
        }
    });

});