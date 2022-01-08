define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-dashboard.js OK");

 

    $('body').on('click', ".update_folder_button" , function () { 

        let folder_id    = $(this).data("folder_id"); 
        let folder_title = $(this).data("folder_title");

        var rg = /^[a-zA-Z0-9]+$/.test(folder_title) ; 

        if (!(rg)) 
            {
            alert("Votre titre ne doit contenir que des caractères ou des nombres.");
            return  false ;
            }
 
        if  (folder_title.length > 20) {
            alert("Votre titre doit contenir un maximum de 20 caractères."); 
            return false ;
        }

        $("#id_title_modal").val(folder_title); 
        $("#id_folder_modal").val(folder_id); 

    });


    function sorter_sequences($div_class , $sequence_class, $item_id, $url) {

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
                        var sequences = [];

                        $($sequence_class).each(function() {

                            let sequence_id = $(this).data($item_id);
                            sequences.push(sequence_id);
 
                        });



                        $(ui.item).css("box-shadow", "0px 0px 0px transparent");

                        $.ajax({
                                data: { 'sequences': sequences ,  csrfmiddlewaretoken: csrf_token  } ,    
                                type: "POST",
                                dataType: "json",                
                                traditional: true,
                                url: $url ,
                            }); 
                        }
                    });
        }
    
    sorter_sequences('#sequences_sorter_div' , ".sequences_sorter", "sequence_id", "sequence/ajax_sort_sequences");
    sorter_sequences('#folders_sorter_div' , ".folders_sorter", "folder_id", "sequence/ajax_sort_folders");

    sorter_sequences('.collapse' , ".list_sequence_index_padding15", "sequence_id", "sequence/ajax_sort_sequences");


        $( ".folders_sorter" ).droppable({

            accept: ".sequences_sorter",
            drop: function( event, ui ) {

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let new_nb    = parseInt($( this ).data("nbinit" )) + 1;
                let folder_id = $( this ).data("folder_id" );

                if (new_nb>1) { texte = "séquences";} else { texte = "séquence";}
                $("#nbs"+folder_id ).html(new_nb + " " +texte) ;
                 $("#list_folder_index"+folder_id ) .addClass( "list_sequence_index_padding15") ;

                        
                $.ajax({
                        data:   { 'sequence_id': ui.draggable.data("sequence_id") , 'folder_id' : folder_id ,   csrfmiddlewaretoken: csrf_token  } ,    
                        type: "POST",
                        dataType: "json",                
                        traditional: true,
                        url: "sequence/ajax_include_folders" ,
                        success: function (data) {
                                $("#list_folder_index"+folder_id ).append(  ui.draggable.html() ) ;
                                deleteImage( ui.draggable );
                           }
                    });


              }
        });
 
        function deleteImage( $item ) {
          $item.fadeOut(function() {
          });
        }

 


    $('body').on('click', ".open_folder_button", function () { 
 

        $(this).find("i").addClass("fa fa-folder-open"); 
 

    });





});

});

