$(document).ready(function() {
    $("#addbtn").click(function() {
	$("#contactdiv").css("display", "block");
    });
    $("#contact #cancel").click(function() {
	$(this).parent().parent().hide();
    });
    // Contact form popup send-button click event.
    $("#send").click(function() {
	var first_name = $("#first_name").val();
	if (first_name == "" ){
	    alert("Please specify name");
	}
	else{
	    add_person(first_name);
	    function validateEmail(email) {
		var filter = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
		if (filter.test(email)) {
		    return true;
		}  else {
		    return false;
		}
	    }
	    $(this).parent().parent().hide();
	}
    });
    
});