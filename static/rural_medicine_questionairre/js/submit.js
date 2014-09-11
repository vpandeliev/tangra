

// call this when AJAX request returns
function complete_task(response,status,xhr)
{
	if (response == "success")
	{
		$("#waiting_container").hide();
		window.location = "/study/fsess";
	} else {
		$("#waiting_container").hide();
		$("#retry_container").show();
	}
}

// Send arbitrary JSON data to /???/save_data
function submit_data()
{
	$("#submit_container").hide();
	$("#waiting_container").show();
	
	var data = $("#shipley_form").serialize();
	
	if (data.split('=').length - 1 != num_questions) {
		alert("Please answer all questions");
		$("#submit_container").show();
		$("#waiting_container").hide();
		return;
	}
	
	//data += "&custom_data=Whatever you want";
	
	$.post("/study/save_post_data", data, complete_task);
}


function toggle_visibility(id) {
       var e = document.getElementById(id);
       if(e.style.display == 'block')
          e.style.display = 'none';
       else
          e.style.display = 'block';
}

function go_to_survey() {
	$('#injury_background').toggle();
	$('#injury_questions').toggle();
	$('#injury_questions').display('block');
	
};

