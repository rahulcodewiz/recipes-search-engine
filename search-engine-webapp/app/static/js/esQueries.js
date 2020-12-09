//Ready function when page is loaded
$(document).ready(function() {
    $("#query").click(function(e) {
        var results = $.map([0], function() {
            //Get text from the input field
            var searchQuery = document.getElementById('typeahead').value;
            var request = $.ajax({
                type: "POST",
                url: "/search",
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
            searchResultToDiv(response)
        });
    });

    var searchResultToDiv =
        function searchResultToDiv(esDocs) {
            var table = document.createElement('table');
            //table.classList.add("styled-table");




            //table.className = "styled-table"
            //Table Header
            var row = document.createElement('thead');
            var title = document.createElement('th');
            title.appendChild(document.createTextNode("Title"));
            row.appendChild(title);
            var ingredients = document.createElement('th');
            ingredients.appendChild(document.createTextNode("Ingredients"));
            row.appendChild(ingredients);
            var instructions = document.createElement('th');
            instructions.appendChild(document.createTextNode("Instructions"));
            row.appendChild(instructions);
            table.appendChild(row);

            //Table Body
            var tableBody = document.createElement('tbody');
            esDocs.hits.hits.forEach(function(rowData) {
                source = rowData._source
                hlTitle = rowData.highlight.title
                var row = document.createElement('tr');

                var title = document.createElement('td');
                var titleDiv = document.createElement('div');
                titleDiv.innerHTML = hlTitle[0];
                //titleDiv = titleDiv.firstChild;
                title.appendChild(titleDiv)
                row.appendChild(title);
                var ingredients = document.createElement('td');
                ingredients.appendChild(document.createTextNode(source.ingredients));
                row.appendChild(ingredients);
                tableBody.appendChild(row);
                var instructions = document.createElement('td');
                instructions.appendChild(document.createTextNode(source.instructions));
                row.appendChild(instructions);
            });

            table.appendChild(tableBody);
            document.getElementById("searchResults").innerHTML = "";
            $("#searchResults").append(table);
        };

    //TODO(Jon) Identify correct ajax function to post to 'ESresults' 
    //TODO(Jon) Parse the json for title field text, generate link
    //TODO(Jon) Store the document id for all click events
    //TODO(Jon) call to Retreive recipe id $('#element_id').data('extra_tag');
    //TODO(Jon) datapull = $(document).data();   pull the ESResults down
    var postRecommend = function(esResults) {
        request = $.ajax({
            type: "POST",
            url: "/recommend",
            async: false,
            data: doc['title'],
            contentType: "text/plain; charset=utf-8",
            dataType: "json",
            success: function(data) {
                return (data);
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }


    //TODO(Jon) Test, bug fix
    //multipost function to dynamically update page with search results 
    var multipost = function(esDocs) {
        //store the full results from esQuery
        $(document).data(esDocs);

        var i = 0;
        //Parse ESsearch results and dynamically publish links with title text and hidden recipe id
        $.each(esDoc, function(key, value) {
            i = i + 1;
            var tag_id = "#link" + i.toString();
            var doc_title = value['title'];
            $.ajax(tag_id).html(doc_title.link('recipe.html'));
            $.ajax(tag_id).attr(target, "_blank");
            $(tag_id).data('extra_tag', key);
        });
    };


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