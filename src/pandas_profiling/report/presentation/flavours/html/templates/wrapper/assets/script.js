$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$("a[href^='#'].anchor").on('click', function (e) {

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

$("#variables-dropdown").on("change", function (e) {
    var searchText = $("#variables-dropdown").val();
    var variables = $(".variable");

    variables.each(function (index) {
        if(!($(this.firstChild.firstChild).attr("title").toLowerCase().includes(searchText))){
            $(this).parent().hide();
        }
        else{
            $(this).parent().show();
        }
    })
})