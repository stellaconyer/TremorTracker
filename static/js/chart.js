
var dataset = [{'timestamp': '1385407616347', 'data': [2.4728413708669374, 1.0213275879824053, 0.6079034848067788, 0.77700792781258421]}, {'timestamp': '1385407617347', 'data': [0.5159543321896326, 0.30089637877501274, 0.29576087039073845, 0.17047443811929824]}, {'timestamp': '1385407615180', 'data': [0.22355068543427009, 0.1828661683728921, 0.27317129983999899, 0.25205675288116147]}, {'timestamp': '1385407613180', 'data': [0.27430178945792527, 0.17270123904337203, 0.16406304991091852, 0.18666311418691917]}, {'timestamp': '1385407614180', 'data': [0.24340115857097588, 0.13899838286602154, 0.17379015269958525, 0.16380843391672484]}];



// SVG width and height
var margin = {top: 30, right: 20, bottom: 30, left: 20},
    w = 500 - margin.left - margin.right,
    h = 500 - margin.top - margin.bottom;

//Create array of data to determine max and min values
    function createArrayFromJSON (dataset) {
      var endArray = [];
      for (var i = 0; i < dataset.length; i++) {
        endArray = endArray.concat(dataset[i].data);
      }
      
      return endArray;
    }

    var datasetArray = createArrayFromJSON(dataset);

    var max = d3.max(datasetArray);
    var min = d3.min(datasetArray);

    var colorScale = d3.scale.linear()
      .domain([min, max])
      .range(["#fdd", "#f00"]);

    var colorScaleInverted = d3.scale.linear()
      .domain([max, min])
      .range(["#fdd", "#f00"]);


//Create an SVG element
    var chart = d3.select("#chart")
      .append("svg")
      .attr("width", w + margin.left + margin.right)
      .attr("height", h + margin.top + margin.bottom);



//Create a column for each entry
    var columns = chart.selectAll("g")
      .data(dataset)
      .enter()
      .append("g")
      .attr("transform", function (d, i) { return translate((i * 60)+60, 0); });


//Create rows for each value in "data"
    var rows = columns.selectAll("g")
      .data(function (d, i) { return d.data; })
      .enter()
      .append("g")
      .attr("transform", function (d, i) { return translate(0, i * 20+20); });

    //Create a rectangle each of the four PSD readings 
    rows
      .append("rect")
      .attr("width", 58)
      .attr("height", 18)
      .attr("fill", colorScale);

    // Overlay "data" value
    rows
      .append("text")
      .text(function (d, i) { return d.toPrecision(3); })
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


// Create x and y axis labels
  //Take in timestamp as string, convert to JS Date object
  var convertTimestamp = function (timestamp) {
    return new Date(parseInt(timestamp, 10));
  };

  //Format a timestamp to H:M:S
  var formatTime = d3.time.format("%X");

  //Format a timestamp to "%a %b %e %H:%M:%S %Y"
  var formatDate = d3.time.format("%c");


  //x labels as H:M:S
  var xLabels = columns.append("g")
    .append("text")
    .text(function(d){return formatTime(convertTimestamp(d.timestamp));})
    .attr("width", 58)
    .attr("height", 18)
    .attr("font-family", "sans-serif")
    .attr("font-size", "12px")
    .attr("transform", function (d, i) {
      return translate(0, d.data.length*20 + 12+20); });


  var chartTitle = ['1385407614180'];

  var chartLabel = chart.selectAll("g")
    .append("g")
    .data(chartTitle, function(d) {return d; })
    .enter()
    .append("text")
    .attr("font-family", "sans-serif")
    .attr("font-size", "12px")
    .text(function (d,i) {return d; })
    .attr("transform", function (d, i) {return translate(0, i+15); });

  //y labels

  var yValues = ["1hz", "3hz", "6hz", "10hz"];

  var yLabels = chart.selectAll("g")
    .append("g")
    .data(yValues, function(d) {return d; })
    .enter()
    .append("text")
    .attr("font-family", "sans-serif")
    .attr("font-size", "12px")
    .text(function (d) {console.log(d); return d;});



 // helper function for translating
    function translate (x, y) {
      return ['translate(', x, ',', y, ')'].join('');
    }