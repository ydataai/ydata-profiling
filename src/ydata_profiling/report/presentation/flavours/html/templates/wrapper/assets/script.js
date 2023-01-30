$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$("a").not("[href^='#']").attr('target', '_blank');

$("a[href^='#']").not("[role='tab']").on('click', function (e) {

    // prevent default anchor click behavior
    e.preventDefault();

    // store hash
    var hash = this.hash;

    // animate
    $('html, body').animate({
        scrollTop: $(hash).offset().top
    }, 300, function () {

        // when done, add hash to url
        // (default click behaviour)
        window.location.hash = hash;
    });

});

$("select#variables-dropdown").on("change", function (e) {
    var searchText = $("select#variables-dropdown").val().toLowerCase();
    var variables = $(".variable");
    variables.each(function (index) {
        var isMatch = $(this.firstChild.firstChild).attr("title").toLowerCase() == (searchText);
        if(searchText == ""){isMatch = true};
        $(this).parent().toggle(isMatch);
    });
});
