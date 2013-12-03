// SVG width and height

var margin = {top: 30, right: 20, bottom: 30, left: 50},
    w = 400 - margin.left - margin.right,
    h = 500 - margin.top - margin.bottom;


    // var w = 400;
    // var h = 78;


// var valueline = d3.svg.line()
//     .x(function(d) { return x(d.timestamp); });

    var dataset = [{'timestamp': '1385407616347', 'data': [2.4728413708669374, 1.0213275879824053, 0.6079034848067788, 0.77700792781258421]}, {'timestamp': '1385407617347', 'data': [0.5159543321896326, 0.30089637877501274, 0.29576087039073845, 0.17047443811929824]}, {'timestamp': '1385407615180', 'data': [0.22355068543427009, 0.1828661683728921, 0.27317129983999899, 0.25205675288116147]}, {'timestamp': '1385407613180', 'data': [0.27430178945792527, 0.17270123904337203, 0.16406304991091852, 0.18666311418691917]}, {'timestamp': '1385407614180', 'data': [0.24340115857097588, 0.13899838286602154, 0.17379015269958525, 0.16380843391672484]}];


// function(d) { return d.date; } returns all the ‘date’ values in ‘data’
// The .extent function that finds the maximum and minimum values in the array
// The .domain function which returns those maximum and minimum values to D3 as the range for the x axis.

      // var x = d3.time.scale().range([0, w]);
      // x.domain(d3.extent(dataset, function(d) {
      //   console.log(Date(d.timestamp));
      //   return Date(d.timestamp);
      // }));

      // var xAxis = d3.svg.axis().scale(x)
      // .orient("bottom").ticks(5);



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


      var axisScale = d3.scale.linear()
        .domain([0,400])
        .range([0,400]);

      var xAxis = d3.svg.axis()
        .scale(axisScale);




//Create an SVG element
    var chart = d3.select("#chart")
      .append("svg")
      .attr("width", w)
      .attr("height", h);




//Create a column for each entry
    var columns = chart.selectAll("g")
      .data(dataset)
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

          var xAxisGroup = chart.append("g")
        .call(xAxis);

 // helper functions are super useful with d3
    function translate (x, y) {
      return ['translate(', x, ',', y, ')'].join('');
    }