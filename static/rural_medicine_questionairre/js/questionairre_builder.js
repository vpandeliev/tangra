

function write_question(number, with_text, and_rationale) 
{
	document.write('<div class="question_container">');
	document.write('	<div class="the_question">')
	document.write('		<h3>' + with_text + "</h3>");
	document.write('	 </div>');
	
	var name = "rationale_" + number;
	document.write('<div class="rationale"><h2><a href="" onclick="return toggle_detail(\''+name+'\',$(this));" class="right">Rationale</a></h2>');
	document.write('<div id="'+name+'" style="display:none;"><p>'+and_rationale+'</p></div></div>');
	
	document.write('<div class="the_answers">');
	document.write('	<table width="100%"><tr>');
	document.write('		<th>No Answer</th>');
	document.write('		<th>Don\'t Know</th>');
	document.write('		<th>Strongly Disagree</th>');
	document.write('		<th>Disagree</th>');
	document.write('		<th>Neutral</th>');
	document.write('		<th>Agree</th>');
	document.write('		<th>Strongly Agree</th>');
	document.write('		<th>Not Applicable</th>');
	document.write('	</tr><tr>')
	document.write('		<td><input type="radio" name="q'+number+'" checked="checked" value="no_answer"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="dont_know"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="strongly_disagree"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="disagree"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="neutral"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="agree"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="strongly_agree"></td>');
	document.write('		<td><input type="radio" name="q'+number+'" value="not_applicable"></td>');
	document.write('	</tr></table>');
	
	document.write('</div>');
	
	document.write('</div>');
}
