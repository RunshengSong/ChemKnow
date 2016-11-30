/**
 * Created by Andre on 13/07/2015.
 */

var API_URL = "http://localhost:5000/annotate"


function makeid(){
    //http://stackoverflow.com/a/1349426/3605086
    var text = "";
    //var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var possible = "0123456789";
    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function options(){
    if($("#options").is(":visible") ){
        $("#options").hide();
        $("#optionsbutton").text("Show Options")
    } else {
        $("#options").show();
        $("#optionsbutton").text("Hide Options")
    }
}

function chemInSent(sent, chemList){
    // indexList = [];
    console.log("In class chemInSent...");
    console.log(sent);
    console.log(chemList);
    for(var i=0; i<chemList.length; i++){
        if(sent.includes(chemList[i])){
            index = sent.indexOf(chemList[i]);
            console.log(index);
            console.log(sent.charAt(index-1));
            if(sent.charAt(index-1) === " " || index==0){
                // indexList.push([index, chemList[i].length]);
                sent = sent.substring(0, index)
                        + "<span class='hightlight'>"
                        + chemList[i]    
                        + "</span>"
                        + sent.substring(index+chemList[i].length, sent.lenth);
            }
                
        }
    }
    console.log(sent);
    return sent;
}


function process(){
    //alert($("#combined").parent().children("#ths").text())
    $('#progressbar').css('display','inline');
    $("#results").html("");
    $("#submitbutton").text("Processing...");
    $("#submitbutton").prop("disabled",true);
    console.log($('#inputtext').val());

    // url = "http://localhost:5000/annotate?text=" + $('#inputtext').val();
    // console.log(url);
    // $.getJSON(url)
    //         .done(function(data){

    //             console.log(data);

    //         })
    //         .fail(function(jqxhr){
    //                 if(jqxhr.status === 404)
    //                 {
    //                         console.log("error 404");           }
    //                 else
    //                 {
    //                         console.log(jqxhr);
    //                 }
    //         });
    var hidingChem = 0;
    // console.log($("#checkHideChem"));
    // console.log($("#checkHideChem")[0].checked);
    if($("#checkHideChem")[0].checked){
        hidingChem = 1
        // console.log(hidingChem);
    }

    $.ajax({
        url: API_URL,
        type: 'POST',
        headers: {'Access-Control-Allow-Origin': 'http://localhost'},
        //dataType: "html",
        data: {text: $('#inputtext').val(),
                chem: $('#inputChem').val(),
                hideChem: hidingChem},
        error: function (xhr, ajaxOptions, thrownError) {
            $('#progress').text("Server Error");
        },
        cache: false
    })
        .done(function( msg ) {
            $("#submitbutton").text("Analyze")
            $("#submitbutton").prop("disabled",false);
            $('#progressbar').css('display','none');
            $('#resultsrow').css('display','inline');
            $('#results').css('display','inline');
            console.log(msg);
            var result = msg;
            console.log(result["results"]);
            var sentList = result["results"]["sentList"];
            var chemList = result["results"]["chemList"];
            console.log(sentList);
            console.log(chemList);
            //var result = msg;
            outputHTML = "<br/><h3>Results</h3><br/><table style=''><tr><th>Sentences</th></tr><tr>";
            for(var i=0; i<sentList.length; i++)
            {
                // if (chemList.length >= i+1){
                //     outputHTML += ("<td>" + chemList[i] + "</td>");
                // }
                // else{
                //     outputHTML += ("<td style='width: 20px'>" + "  " + "</td>");
                // }
                sent = sentList[i];

                sent = chemInSent(sent, chemList);

                outputHTML += ("<td>" + sent + "</td>");
                outputHTML += "</tr>";
            }
            outputHTML += "</table><br/><br/><br/>";
            // console.log(outputHTML);
            $("#options").append(outputHTML);

            //$.scrollTo("#results");
            // $('html, body').animate({
            //     scrollTop: $("#resultsrow").offset().top - $("#navbar").height()
            // }, 1000);
            //console.log(msg);
            // $.getScript('js/process_annotations.js', function()
            // {
                // var result = JSON.parse(msg);
                // //var result = msg;
                // output = $('<div></div>');

                // console.log(result);
                // script is now loaded and executed.
                // put your dependent JS here.
                // for(si=0;si<result.abstract.sentences.length;si++){
                //     sentence_div = $('<div class="panel panel-default"></div>');
                //     sentence_text = annotateText(result.abstract.sentences[si].text,
                //         result.abstract.sentences[si].entities);
                //     sentence_table = $('<div class="panel-collapse collapse in"><div class="panel-body"><h3>Chemical entities found</h3></div></div>')
                //     entities_table = getEntitiesTable(result.abstract.sentences[si].entities);
                //     sentence_table.append(entities_table)
                //     sentence_heading = $('<div class="panel-heading"></div>')
                //     sentence_heading.append(sentence_text)
                //     sentence_div.append(sentence_heading)
                //     sentence_div.append(sentence_table)
                //     output.append(sentence_div)
                    //console.log(result.abstract.sentences[si]);
                //    for(ei=0;ei<result.abstract.sentences[si].entities.length;ei++){
                        //console.log(result.abstract.sentences[si].entities[ei].text);
                //    }
                // }
                // $("#results").html(output);
            // });

            // $(document).prop('title', '(DONE) IICE - Identifying Interactions between Chemical Entities');
            // loadPopups();
        });
    //success: function(data){
    //alert(JSON.stringify(data));
    //    alert(data)
    //}
}

function loadPopups(){
    $('[data-toggle="popover"]').popover({
        trigger: 'hover',
        placement: 'auto',
        animate: true,
        container: 'body',
        html: true,

    });
};

