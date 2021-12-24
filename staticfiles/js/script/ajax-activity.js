define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-accounting.js OK");



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





    });

});
 

 
 

 
 
 