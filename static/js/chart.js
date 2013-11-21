// var dataset = [{'timestamp': '2013-11-20 17:55:12.230717', 'data': [0.27150600768698541, 0.54700389736808952, 0.27989681432545555, 0.18541747897096902]}, {'timestamp': '2013-11-20 17:55:12.233453', 'data': [0.35556553756610387, 0.727923757748143, 0.33010381286315599, 0.40916634448091921]}, {'timestamp': '2013-11-20 17:55:12.236541', 'data': [19.338538240923686, 2.1949874472044155, 0.4380670714493568, 4.3758447446434445]}, {'timestamp': '2013-11-20 17:55:12.239399', 'data': [21.196379030531169, 3.777768138898761, 4.4018123520780961, 0.80592773951603691]}, {'timestamp': '2013-11-20 17:55:12.242423', 'data': [21.516699704212019, 7.022255372721288, 4.444317647253766, 5.6401802798604752]}, {'timestamp': '2013-11-20 17:55:12.245820', 'data': [25.484850519772159, 7.5519101111519316, 3.3555483970960713, 13.896023738566782]}, {'timestamp': '2013-11-20 17:55:12.248807', 'data': [34.021843050565003, 13.126449669911736, 4.3648375279657721, 2.6099755867796492]}, {'timestamp': '2013-11-20 17:55:12.250508', 'data': [9.4481706003953949, 18.263146137069551, 9.7734644339328494, 5.519340125385285]}, {'timestamp': '2013-11-20 17:55:12.252107', 'data': [9.6858943705876381, 6.5843575719315384, 6.1970465294932424, 2.0610351062877115]}, {'timestamp': '2013-11-20 17:55:12.254665', 'data': [9.2890874653255242, 4.3791773605999547, 6.0395110595226829, 2.8085162463256625]}, {'timestamp': '2013-11-20 17:55:12.257270', 'data': [10.264069340901374, 4.6327588912326698, 9.3969823016854352, 5.2161808429740351]}, {'timestamp': '2013-11-20 17:55:12.259347', 'data': [8.664378473473862, 5.3933796254996356, 6.0537448295123992, 7.7738247224704615]}, {'timestamp': '2013-11-20 17:55:12.262110', 'data': [14.263800240278158, 11.945346467046743, 7.4353657460026659, 2.1003655018854901]}, {'timestamp': '2013-11-20 17:55:12.265213', 'data': [7.9200867552981498, 1.6793879453282741, 2.9017750353315948, 5.0710219189982846]}];

    var w = 1000;
    var h = 500;

    function array_from_dataset (dataset) {
      var end_array = [];
      for (var i = 0; i < dataset.length; i++) {
        end_array = end_array.concat(dataset[i].data);
      }
      return end_array;
    }

    var max = d3.max(array_from_dataset(dataset));
    var min = d3.min(array_from_dataset(dataset));

    var colorScale = d3.scale.linear()
      .domain([min, max])
      .range(["#fdd", "#f00"]);

    var colorScaleInverted = d3.scale.linear()
      .domain([max, min])
      .range(["#fdd", "#f00"]);

//Create an SVG element
    var chart = d3.select("#chart")
      .append("svg")
      .attr("width", w)
      .attr("height", h);

//Create a column for each entry
    var columns = chart.selectAll("g")
      .data (dataset)
      .enter()
      .append("g")
      .attr("transform", function (d, i) { return translate(i * 60, 0); });


//Create rows for each value in "data"
    var rows = columns.selectAll("g")
      .data(function (d, i) { return d.data; })
      .enter()
      .append("g")
      .attr("transform", function (d, i) { return translate(0, i * 20); });

    //Create a rectangle each of the four PSD readings 
    rows
      .append("rect")
      .attr("width", 58)
      .attr("height", 18)
      .attr("fill", colorScale);


    // Overlay "data" value
    rows
      .append("text")
      .text(function (d, i) { return d.toPrecision(5); })
      .attr("dx", "20px")
      .attr("dy", "14px")
      .attr("font-family", "sans-serif")
      .attr("font-size", "12px")
      .attr("fill", colorScaleInverted)
      .style({opacity:'0'})
      .on('mouseover', function(d){
          var nodeSelection = d3.select(this).style({opacity:'1.0'});
      })
      .on('mouseout', function(d){
          var nodeSelection = d3.select(this).style({opacity:'0'});
      });


 // helper functions are super useful with d3
    function translate (x, y) {
      return ['translate(', x, ',', y, ')'].join('');
    }