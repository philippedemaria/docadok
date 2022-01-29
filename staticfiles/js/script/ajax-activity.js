define(['jquery', 'bootstrap','uploader' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-activity.js OK");



        $("input[type=checkbox]").prop('checked', false); 



        $(document).on('click', '.add_more', function (event) {


                var total_form = $('#id_choices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) 
                $('#cloningZone').attr("id","cloningZone"+totalForms) 

 
                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

                $('#spanner').attr("id","spanner"+totalForms) ;
                $('#preview').attr("id","preview"+totalForms) ;
                $('#bi-image').attr("id","bi-image"+totalForms) ;
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_more', function () {
            var total_form = $('#id_choices-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });



        $('body').on('change', '.choose_imagefile' , function (event) {

            previewFile00();
         }); 



        $('body').on('change', '.choose_imageanswer' , function (event) {

            var suffix = this.id.match(/\d+/);

            previewFile(suffix) ;
         });  


        function previewFile(nb) {

            const preview = $('#preview'+nb);
            const file = $('#id_choices-'+nb+'-imageanswer')[0].files[0];
            const reader = new FileReader();

            $("#preview"+nb).val("") ;  
            $("#bi-image"+nb).addClass("preview") ;
            $("#preview"+nb).removeClass("preview") ; 
            $("#delete_img"+nb).removeClass("preview") ;
            $("#spanner"+nb).prepend("<span class='input-group-addon input-group-addon-left' id='deleter"+nb+"'><a href='#' data-id='"+nb+"' class='delete_img'><i class='bi bi-trash'></i></a></span>") 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

          }


        function previewFile00() {

            const preview = $('#preview00');
            const file = $('#id_imagefile')[0].files[0];
            const reader = new FileReader();

            $("#preview00").val("") ;  
            $("#bi-image00").addClass("preview") ;
            $("#preview00").removeClass("preview") ; 
            $("#delete_img00").removeClass("preview") ;
            $("#spanner00").prepend("<span class='input-group-addon input-group-addon-left' id='deleter00'><a href='#' data-id='00' class='delete_img'><i class='bi bi-trash'></i></a></span>") 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview00").attr("src", image );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

        }



        $('body').on('click', '.delete_img' , function (event) {

            var suffix = $(this).data('id');
            noPreviewFile(suffix) ;
         });  
  


        function noPreviewFile(nb) {  
            $("#id_choices-"+nb+"-imageanswer").attr("src", "" );
            $("#bi-image"+nb).removeClass("preview") ;
            $("#preview"+nb).addClass("preview") ; 
            $("#delete_img"+nb).addClass("preview") ;
            $("#deleter"+nb).remove() ;

          }





        makeDivAppear($("#id_is_publish"), $("#display_publish"));
        makeDivAppear($("#id_is_timer"), $("#display_timer"));
        makeDivAppear($("#id_is_score"), $("#display_score"));
        
        function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                         $item.toggle(500);
                    });
                }
 

        $(document).on('click', '#caret_activities', function () {
            $("#display_caret_activities").toggle(500);
        });


 




    });

});
 

 
 

 
 
 