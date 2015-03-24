$(function() {
	var agingOption = {};
	var offsetTop = 0;
	var offsetLeft = 0;
	var agingCounter = 0;
	
	$("#showArea").hide();
	var IP = "http://127.0.0.1:5000/";
	var url = IP + "upload";
	var imgPath = IP + "static/img/";
	$('#file').attr("data-url", url);
	$('#file').on('success.tools.upload', function(json) {
		if (json.code == 0) {
			json = json.data;
			$("#showArea").show();
			$("#uploadArea").hide();
			$("#uploadFace").attr("src", imgPath + json.path);
			
			agingOption.pointX = json.pointX;
			agingOption.pointY = json.pointY;
			
			var obj = $("#imgArea");
			offsetTop = obj.offset().top - 5;
			offsetLeft = obj.offset().left - 5;
			
			var html = [];		
			var css = {
				width: json.width,
				height: json.height
			};
			obj.css(css);
			
			for (var i = 0; i < json.pointSize; i++) {
				var tmpLeft = offsetLeft + json.pointX[i];
				var tmpTop = offsetTop + json.pointY[i];			
				html.push('<a class="blackPoint" y="' + json.pointY[i] + '" x="' + json.pointX[i] + '" index="' + i 
					+ '" href="#" style="left:' + tmpLeft + 'px; top:' + tmpTop + 'px;"></a>');
			}
			html = html.join("");		
			obj.append(html);
			$("#newFace").hide();
			$(".blackPoint").draggable({
				containment: "parent",
			  	cursor: "crosshair",
			  	stop: function(event, ui) {
			  		var index = parseInt(ui.helper.attr("index"));
			  		agingOption.pointX[index] = ui.position.left - offsetLeft;
			  		agingOption.pointY[index] = ui.position.top - offsetTop;
			  	}
			});
			
			$("#curAge").val(Math.floor(json.curAge));
		} else {
			alert(json.mess);
		}
	});
	
	$("#Aging").on("click", function(){
		agingOption.curAging = $("#curAge").val();
		agingOption.forecastAge = $("#forecastAge").val();		
		
		var cAge = parseInt(agingOption.curAging);
		var pAge = parseInt(agingOption.forecastAge);
		// if (cAge === pAge) {
			// alert("Current Age equal to prective Age");			
		// } else if (cAge > 15 || pAge > 15) {
			// alert("Age large than 15.\n Application couldn't support so far.");			
		// } else {		
			var pointX = [];
			var pointY = [];
			$(".blackPoint").each(function(){
				var i = $(this).attr("index");
				pointX[i] = $(this).position().left - offsetLeft;
				pointY[i] = $(this).position().top - offsetTop;
			});
			
			var points = [];
			var index = 0;
			for (var i = 0; i < pointX.length; i++) {
				points[index] = pointX[i];
				index++;
				points[index] = pointY[i];
				index++;
			}
			
			var str = $("#uploadFace").attr("src");
			index = str.lastIndexOf("/") + 1;
			agingOption.image = str.substr(index);
			agingOption.points = points.join(" ");	
			agingOption.times = agingCounter;
			agingCounter++;	
			$.post("/age", agingOption, function(data) {
				if (data.code === 0) {
					var html = [];
					html.push('<div class="agingFace">');
						html.push('<img id="newFace' + agingCounter + '" src=" ' + imgPath + data.newImage + ' " alt="face" />');
						html.push('<br />');
						html.push('<span>Current Age:' + data.curAge + '</span>');
						html.push('<br />');
						html.push('<span>predictive Age:' + data.forecastAge + '</span>');
					html.push('</div>');
					html = html.join("");
					
					$("#agingFaceShow").append(html);
				}
			});			
		// }
		return false;
	});
});