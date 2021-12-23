define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-bibiotex.js OK");

    

    clickDivAppear($("#change_title"), $("#sequence_title_form"), $("#sequence_title"));
    clickDivAppear($("#change_code"), $("#sequence_code_form"), $("#sequence_code"));

    clickDivAppear($("#close_sequence_title_form"), $("#sequence_title_form"), $("#sequence_title"));
    clickDivAppear($("#close_sequence_code_form"), $("#sequence_code_form"), $("#sequence_code"));

    clickOneDivAppear($("#open_properties"), $("#properties"));
    clickOneDivAppear($(".close_properties"), $("#properties"));


    function clickOneDivAppear($toggle, $item ) {
                $toggle.click(function () {
                    $item.toggle("slow");
                });
            }


    function clickDivAppear($toggle, $item, $itm) {
                $toggle.click(function () {
                    $item.toggle();
                    $itm.toggle();
                });
            }

    function makeDivAppear($toggle, $item ) {
                $toggle.change(function () {
                    $item.toggle();
                });
            }



 
    $('body').on('click', '.save_sequence' , function () { 

        let champ       = $(this).data("champ"); 
        let sequence_id = $(this).data("sequence_id");
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val(); 
        let value       = $("#id_"+champ).val();  
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'value'       : value, 
                    'champ'       : champ, 
                    'sequence_id' : sequence_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_update_sequence" ,
                success: function (data) {
                    $("#new_"+champ).html(value) ;
                    $("#sequence_"+champ+"_form").toggle();
                    $("#sequence_"+champ).toggle();
                }
            }
        )
    });



    $('body').on('change', '.check_sequence' , function () { 

        let sequence_id = $("#sequence_id").val();
        let csrf_token  = $("input[name='csrfmiddlewaretoken']").val(); 
        let value       = $(this).attr("id"); 

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'value'       : value, 
                    'sequence_id' : sequence_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_update_checkbox_sequence" ,
                success: function (data) {

                    $("#"+value).addclass(data.html);
 
                }
            }
        )
    });











        function sorter_exotexs($div_class , $exercise_class ) {

                $($div_class).sortable({
                    cursor: "move",
                    swap: true,    
                    animation: 150,
                    distance: 10,
                    revert: true,
                    tolerance: "pointer" , 
                    start: function( event, ui ) { 
                           $(ui.item).css("box-shadow", "10px 5px 10px gray"); 
                       },
                    stop: function (event, ui) {

                        let bibliotex = $("#bibliotex").val();
                        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                        var relationtexs = [];
 

                        $($exercise_class).each(function() {

                            let relationtex_id = $(this).data("relationtex_id");
                            relationtexs.push(relationtex_id);
 
                        });

 
                        $(ui.item).css("box-shadow", "0px 0px 0px transparent"); 

                        console.log( 'relationtexs  ' + relationtexs +  '  bibliotex' + bibliotex )


                        $.ajax({
                                data:   { 'relationtexs': relationtexs ,  'bibliotex' : bibliotex , csrfmiddlewaretoken: csrf_token  } ,    
                                type: "POST",
                                dataType: "json",                
                                traditional: true,
                                url: "../ajax_sort_exotexs_in_bibliotex" 
                            }); 
                        }
                    });
                }

    
        sorter_exotexs('#bibliotex_sortable' , ".relationtex_sorter");

});

});

