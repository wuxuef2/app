$(function() {
	var agingOption = {};
	
	$("#showArea").hide();
	var url = location.href + "/upload";
	var imgPath = location.href + "static/img/";
	$('#file').attr("data-url", url);
	$('#file').on('success.tools.upload', function(json) {
		$("#showArea").show();
		$("#uploadArea").hide();
		$("#uploadFace").attr("src", imgPath + json.path);
		
		agingOption.pointX = json.pointX;
		agingOption.pointY = json.pointY;
		
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
			html.push('<a class="blackPoint" y="' + json.pointY[i] + '" x="' + json.pointX[i] + '" index="' + i + '" href="#" style="left:' + tmpLeft + 'px; top:' + tmpTop + 'px;"></a>');
		}
		html = html.join("");		
		obj.append(html);
		
		$(".blackPoint").draggable({
			containment: "parent",
		  	cursor: "crosshair",
		  	stop: function(event, ui) {
		  		var index = parseInt(ui.helper.attr("index"));
		  		agingOption.pointX[index] = ui.position.left - offsetLeft;
		  		agingOption.pointY[index] = ui.position.top - offsetTop;
		  	}
		});
	});
	
	$("#Aging").on("click", function(){
		agingOption.curAging = $("#curAge").val();
		agingOption.forecastAge = $("#forecastAge").val();
		$.post("", agingOption, function() {
			
		});
	});
});