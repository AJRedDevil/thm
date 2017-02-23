
function popup(ppClass)
{
	console.log(ppClass);
	hidePopup();
	$('.popupSystem').show();
	
	$('.popupSystem .' + ppClass).show();
}

function hidePopup(){
	$('.popupContent > div').hide();
	$('.popupSystem').hide();
}
$(document).ready(function() {

	hidePopup();
	$('.popupSystem .close-btn').click(function(){
		hidePopup();
	})

	$('.popupSystem .back-black').click(function(){
		hidePopup();
	})

$(document).keydown(function(e) {

  if (e.keyCode == 27) { 
  	hidePopup();
   }   // esc
});

});



 
