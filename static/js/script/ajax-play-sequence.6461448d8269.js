define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-sequence.js OK");





     var i = 0;
        setInterval(function(){
            $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
        }, 4000);



    function sorter_choices($div_class , $exercise_class) {

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
                        var choices    = [];

                        $($exercise_class).each(function() {

                            let choice_id = $(this).data("choice_id");
                            choices.push(choice_id);
 
                        });

                        $(ui.item).css("box-shadow", "0px 0px 0px transparent");

                        // $.ajax({
                        //         data:   { 'choices': choices ,  csrfmiddlewaretoken: csrf_token  } ,    
                        //         type: "POST",
                        //         dataType: "json",                
                        //         traditional: true,
                        //         url: "../ajax_sort_choices" ,
                        //         success: function (data) {
                        //                 i=1;
                        //                 $(".number_list").each(function() {
                        //                     $(this).html(i);
                        //                     i++;
                        //                 });
                        //            }
                        //     }); 
                        }
                    });
                }

        sorter_choices('.activity_sorter' , ".move_div");
});

});

