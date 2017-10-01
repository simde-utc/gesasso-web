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