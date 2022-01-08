define(['jquery', 'asynchrone'], function ($) {
 $(document).ready(function () {
  console.log("chargement JS rt-sequence.js OK");



        
      console.log($('#activity_id').val());    
 
		$("body").on('change', '#activity_id' , function () { 
			
			alert("activité changée");
		});
 
  
	});	    
 
});