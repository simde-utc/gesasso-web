(function($){
  $(function(){

    $('.button-collapse').sideNav();

    // Style TODO: move this to a clean place
    $('ul:not(.collapsible) > li.active').addClass("amber");

    autocompleteValues = JSON.parse($("#autocomplete-values").text());
    $('input.autocomplete').autocomplete({
        data: autocompleteValues,
        limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
        onAutocomplete: function(val) {
            // Callback function when value is autcompleted.
            goToUrl = window.location.origin + window.location.pathname + "?s=" + val
            window.location.href = goToUrl;
        },
        minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
    });

    // Expandable click events
    $('li.collection-item.expandable > a').click(function (evt) {
        $( this ).parent().toggleClass("expanded");
        $( this ).parent().children("div").slideToggle();
        evt.stopPropagation();
        return false;
    });
    $('li.collection-item.expandable').click(function (evt) {
        evt.stopPropagation();
    });
    $('main').click(function () {
        $(".expanded").children("div").slideUp();
        $(".expanded").toggleClass("expanded");
    });


    // Hidden form
    $(".new-form:not(.visible)").css("display", "flex").hide().css("opacity", 1);

    // Visible form
    $(".new-form.visible").css("display", "flex").css("opacity", 1);
    $(".new-form.visible").fadeIn();

    // Form click events
    $(".new-form").click(function() {
        $(".new-form").fadeOut();
        return false;
    });
    $(".new-form-container").on("click", function(evt) {
        evt.stopPropagation();
    });
    $(".btn-new").click(function() {
        showStdForm();
        return false;
    });
    $('.confirm').click(function() {
        confirmText = "announcement";
        if ($( this ).children('i').text() == confirmText) {
            return true;
        } else {
            $( this ).children('span').text("Confirmer");
            $( this ).children('i').text(confirmText);
            $( this ).removeClass("amber").addClass("red");
            return false;
        }
    })

    // Messages animations and actions
    messageAnimationInterval = 200; // ms
    messageWaitInterval = 5000; // ms
    function toggleMessages() {
        $( ".messages" ).children().each(function(i) {
            setTimeout(()=>{
                $(this).toggleClass("visible");
            }, i*messageAnimationInterval)
        });
    }
    function hideMessages() {
        $( ".messages" ).children().each(function(i) {
            setTimeout(()=>{
                $(this).removeClass("visible");
            }, i*messageAnimationInterval)
        });
    }
    toggleMessages()
    setTimeout(hideMessages, messageWaitInterval)
    $("#toggleMessages").click(toggleMessages)

    // Edit
    initForm = "";
    $(" .edit-item ").click(function (evt) {
        showStdForm($( this ).parent().children(".hidden-form").first().html());
        return false;
    });

    function showStdForm(editForm = false){
        if(!editForm) {
            if (initForm != ""){
                $("#std-form").html(initForm);
            }
        } else {
            if (initForm == ""){
                initForm = $("#std-form").html();
            }

            $("#std-form").html( editForm );
        }
        Materialize.updateTextFields();
        $("#std-form").find("select").material_select();
        $(".new-form").fadeIn();
    }

  }); // end of document ready
})(jQuery); // end of jQuery name space
