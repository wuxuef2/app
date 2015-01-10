$(function() {
	var url = location.href + "/upload";
	var imgPath = location.href + "/static/img/";
	$('#file').attr("data-url", url);
	$('#file').on('success.tools.upload', function(json) {
		alert(json.path);
		$("#uploadArea").empty();
		$("#uploadArea")
		
		//console.log(this, json);
	});
});