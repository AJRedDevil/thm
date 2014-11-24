



function fullheights()
{
	$('.fullpage').css('min-height',$(window).height() + "px");
}


$(function(){

	fullheights();
	devices();

	popupInit();

})

$(window).resize(function() {

	fullheights();
})

// Handheld test 
function devices(){
if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
	console.log("device")
	$('head').append('<link rel="stylesheet" href="css/devices.css" type="text/css" />');

}
}

function toogleCheck(a){
	if(a.hasClass('checked'))
	{
		// console.log('Pee')
		a.removeClass('checked');
		a.attr('data','unchecked');
		// uncheck(a);
	}
	else
	{
		// check(a);
		// console.log('Dee')
		a.addClass('checked');
		a.attr('data','checked');
	}

}





