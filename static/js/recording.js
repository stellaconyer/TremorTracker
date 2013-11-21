var x_samples = [];
var y_samples = [];
var z_samples = [];

var total_x_samples = [];
var total_y_samples = [];
var total_z_samples = [];


function gather_samples () {
	total_x_samples.push(x_samples);
	x_samples = [];
}

var total_x_samples_dom = $('.total_x_samples');
var x_samples_dom = $('.x_samples');
var x_dom = $('.x');
var y_dom = $('.y');
var z_dom = $('.z');

var startTracking = function () {

	window.ondevicemotion = function(event) {
		var x = event.acceleration.x;
		var y = event.acceleration.y;
		var z = event.acceleration.z;
		x_dom.html(x);
		y_dom.html(y);
		z_dom.html(z);

		x_samples.push(x);
		y_samples.push(y);
		z_samples.push(z);
		
	};

	window.gatherTimer = setInterval(gather_samples,1000);
};


 
 $(document).ready(function() {
				console.log('ready!');
			});

 $("#submit").click(function (e) {
	console.log("Things finished");
	console.log(total_x_samples);
	e.preventDefault(); //Overrides submit button defaults
	clearInterval(window.gatherTimer);
	window.ondevicemotion = undefined;
	$('.results').html("Loading...");
	$.post('/send_pkg', {x: JSON.stringify(total_x_samples)},
			function(response){
			$('.results').html(response);
	});

});

