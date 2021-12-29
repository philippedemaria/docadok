define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-sequence.js OK");

    

    clickDivAppear($("#change_title"), $("#sequence_title_form"), $("#sequence_title"));
    clickDivAppear($("#change_code"), $("#sequence_code_form"), $("#sequence_code"));

    clickDivAppear($("#close_sequence_title_form"), $("#sequence_title_form"), $("#sequence_title"));
    clickDivAppear($("#close_sequence_code_form"), $("#sequence_code_form"), $("#sequence_code"));

    clickOneDivAppear($("#open_properties"), $("#properties"));
    clickOneDivAppear($(".close_properties"), $("#properties"));



    click_DivAppear($("#show_hide_menu_activities"), $(".activity_menu_li"));
    var show = 0 ;
    function click_DivAppear($toggle, $item ) {
                $toggle.click(function () {
                show++;

                if (show%2==1)
                {
                    $toggle.html('<i class="bi bi-eye-slash"></i>  Cacher les activités');
                    $("#left_col").addClass("col-md-3").addClass("col-lg-2").removeClass("col-md-1").removeClass("col-lg-1");
                    $("#right_col").addClass("col-md-9").addClass("col-lg-9").removeClass("col-md-10").removeClass("col-lg-10");
                }
                else
                {
                    $toggle.html('<i class="bi bi-plus-circle-dotted"></i>  Ajouter une activité');
                    $("#left_col").addClass("col-md-1").addClass("col-lg-1").removeClass("col-md-3").removeClass("col-lg-2");
                    $("#right_col").addClass("col-md-10").addClass("col-lg-10").removeClass("col-md-9").removeClass("col-lg-9");
                }
                $item.toggle("slow");
            });         
        }

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
 
    var reducer = 0 ;
    var augment = 0 ;
    reduce_tdb_col(  $("#reduce_left_col")  , $("#left_col")  , $("#no_visu_left_col")  );
    augment_tdb_col( $("#augment_left_col") , $("#left_col")  , $("#no_visu_left_col")  );

    reduce_tdb_col(  $("#reduce_right_col")  , $("#right_col")  , $("#no_visu_right_col")   );
    augment_tdb_col( $("#augment_right_col") , $("#right_col")  , $("#no_visu_right_col")  );

    function reduce_tdb_col($btn, $no_display ,  $display ,  $side ) {
                
            $btn.click(function () {

                    if( reducer == 0 ){
                        $("#body_col").removeClass("col-md-6").removeClass("col-lg-6").addClass("col-md-8").addClass("col-lg-8"); 
                        reducer++;                          
                    }
                    else if( reducer == 1 ){
                        $("#body_col").removeClass("col-md-8").removeClass("col-lg-8").addClass("col-md-10").addClass("col-lg-10"); 
                        reducer++; 
                    }
                    else{
                        $("#body_col").removeClass("col-md-6").removeClass("col-lg-6").addClass("col-md-8").addClass("col-lg-8"); 
                        $("#body_col").addClass($side);                           
                    }
                    $no_display.hide(500);
                    $display.show(500);
                });
        }

    function augment_tdb_col($btn, $no_display ,  $display ) {
                
            $btn.click(function () {

                    if( $("#body_col").hasClass("col-md-8") ){
                        $("#body_col").removeClass("col-md-8").removeClass("col-lg-8").addClass("col-md-10").addClass("col-lg-10"); 
                    }
                    else{
                        $("#body_col").removeClass("col-md-10").removeClass("col-lg-10").addClass("col-md-8").addClass("col-lg-8");                            
                    }
 

                    if( reducer == 2 ){
                        $("#body_col").removeClass("col-md-10").removeClass("col-lg-10").addClass("col-md-8").addClass("col-md-8"); 
                        reducer--; 
                    }
                    else if( reducer == 1 ){
                        $("#body_col").removeClass("col-md-8").removeClass("col-lg-8").addClass("col-md-6").addClass("col-lg-6"); 
                        reducer--; 
                    }
                    $no_display.show(500);
                    $display.hide(500);
                });
        }



    full_screen( $("#full_screen")  );
    function full_screen($btn, $no_display ,  $display ) {
                
            $btn.click(function () {

                    if (reducer < 2 )
                    { 
                        $("#body_col").addClass("col-md-10").addClass("col-lg-10");
                        if( $("#body_col").hasClass("col-md-8") ) {  $("#body_col").removeClass("col-md-8").removeClass("col-lg-8") ; }
                        else if( $("#body_col").hasClass("col-md-6") ) {  $("#body_col").removeClass("col-md-6").removeClass("col-lg-6") ; }
                        reducer=2; 

                        $("#left_col").hide(500);
                        $("#right_col").hide(500);
                        $("#no_visu_left_col").show(500);
                        $("#no_visu_right_col").show(500);
                        $(this).html('<i class="bi bi-chevron-bar-right"></i><i class="bi bi-chevron-bar-left"></i>') ; 
                    }
                    else 
                    { 
                        $("#body_col").addClass("col-md-6").addClass("col-lg-6");
                        reducer=0; 
                        $("#left_col").show(500);
                        $("#right_col").show(500);
                        $("#no_visu_left_col").hide(500);
                        $("#no_visu_right_col").hide(500);
                        $(this).html('<i class="bi bi-chevron-bar-left"></i><i class="bi bi-chevron-bar-right"></i>') ; 
                    }


                });
        }

 


    $('body').on('click', '.save_sequence' , function () { 

        let champ       = $(this).data("champ"); 
        let sequence_id = $(this).data("sequence_id");
        let csrf_token  = $("input[name='csrfmiddlewaretoken']").val(); 
        let value       = $("#id_"+champ).val();  
        $.ajax(
            {
                type        : "POST",
                dataType    : "json",
                traditional : true,
                data        : {
                                'value'       : value, 
                                'champ'       : champ, 
                                'sequence_id' : sequence_id,
                                csrfmiddlewaretoken : csrf_token
                            },
                url     : "../ajax_update_sequence" ,
                success : function (data) {
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





    function sorter_activities($div_class , $exercise_class) {

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

                        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                        var activities = [];

                        $($exercise_class).each(function() {

                            let activity_id = $(this).data("activity_id");
                            activities.push(activity_id);
 
                        });

                        $(ui.item).css("box-shadow", "0px 0px 0px transparent");

                        $.ajax({
                                data:   { 'activities': activities ,  csrfmiddlewaretoken: csrf_token  } ,    
                                type: "POST",
                                dataType: "json",                
                                traditional: true,
                                url: "../ajax_sort_activities" ,
                                success: function (data) {
                                        i=1;
                                        $(".number_list").each(function() {
                                            $(this).html(i);
                                            i++;
                                        });
                                   }
                            }); 
                        }
                    });
                }
    sorter_activities('#right_col' , ".activity_sorter");

});

});

