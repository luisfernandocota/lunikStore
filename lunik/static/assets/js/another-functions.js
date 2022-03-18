$(document).ready(function () {


	if(getCookieValue('showModal') !==  'show')
	{
		writeCookie ("showModal", "show", 24);
		// Show 4shop Intro Modal 
		$('#intro-modal-user-guide').modal('show')
	}
});


function writeCookie (key, value, hours) {
    var date = new Date();
    date.setTime(+ date + (hours * 3600000)); //60 * 60 * 1000
    window.document.cookie = key + "=" + value + "; expires=" + date.toGMTString() + "; path=/";
    return value;
};


function getCookieValue(name){
	return document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
}