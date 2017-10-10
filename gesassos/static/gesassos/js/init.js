(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('ul:not(.collapsible) > li.active').addClass("amber");

    $('input.autocomplete').autocomplete({
        data: {
            "Apple": null,
            "Microsoft": null,
            "Google": 'https://placehold.it/250x250'
        },
        limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
        onAutocomplete: function(val) {
            // Callback function when value is autcompleted.
        },
        minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
    });

    $('li.collection-item.expandable a').click(function () {
        $( this ).parent().toggleClass("expanded");
        console.log($( this ).children("div"));
        $( this ).parent().children("div").slideToggle();
    });

    $(".btn-new").click(function() {
        $(".new-form").fadeIn();
        return false;
    });


    $(".new-form").css("display", "flex").hide().css("opacity", 1);
    $(".new-form").click(function() {
        $(".new-form").fadeOut();
        return false;
    });
    $(".new-form-container").on("click", function(evt) {
        evt.stopPropagation();
    });

    $('.passwd-confirm').click(function() {
        confirmText = "announcement";
        if ($( this ).children('i').text() == confirmText) {
            return true;
        } else {
            $( this ).children('span').text("Confirmer");
            $( this ).children('i').text(confirmText);
            return false;
        }
    })

  }); // end of document ready
})(jQuery); // end of jQuery name space