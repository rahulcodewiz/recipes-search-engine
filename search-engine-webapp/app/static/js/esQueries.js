//Ready function when page is loaded
$(document).ready(function() {
    //Autocomplete function
    var autoComplete = function(query, cb) {
        var results = $.map([0], function() {
            //Get text from the input field
            var searchQuery = document.getElementById('typeahead').value;
            var request = $.ajax({
                type: "POST",
                url: "/autosuggest",
                async: false,
                data: searchQuery,
                contentType: "text/plain; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    return (data);
                },
                failure: function(errMsg) {
                    alert(errMsg);
                }
            });

            //Parse the results and return them
            var response = JSON.parse(request.responseText);
            var resultsArray = response.suggest.recipes[0].options;
            var datum = [];
            for (var i = 0; i < resultsArray.length; i++) {
                datum.push({
                    theValue: resultsArray[i].text
                });
            }
            return datum;
        });

        cb(results);
    };

    $('.typeahead').typeahead(null, {
        displayKey: 'theValue',
        source: autoComplete
    });

});