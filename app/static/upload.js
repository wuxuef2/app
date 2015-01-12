$(function() {
	$("#showArea").hide();
	var url = location.href + "/upload";
	var imgPath = location.href + "static/img/";
	$('#file').attr("data-url", url);
	$('#file').on('success.tools.upload', function(json) {
		$("#showArea").show();
		$("#uploadArea").hide();
		$("#uploadFace").attr("src", imgPath + json.path);
		
		var html = [];
		var obj = $("#imgArea");
		var offsetTop = obj.offset().top;
		var offsetLeft = obj.offset().left;
		var css = {
			width: json.width,
			height: json.height
		};
		obj.css(css);
		
		for (var i = 0; i < json.pointSize; i++) {
			var tmpLeft = offsetLeft + json.pointX[i];
			var tmpTop = offsetTop + json.pointY[i];			
			html.push('<a class="blackPoint" index="' + i + '" href="#" style="left:' + tmpLeft + 'px; top:' + tmpTop + 'px;"></a>');
		}
		html = html.join("");		
		obj.append(html);
		
		$(".blackPoint").draggable({
			containment: "parent",
		  	cursor: "crosshair",
		  	stop: function(event, ui) {
		  		var index = parseInt(ui.helper.attr("index"));
		  		json.pointX[index] = ui.offset.left;
		  		json.pointY[index] = ui.offset.top;
		  	}
		});
	});
});