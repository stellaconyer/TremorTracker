// SVG width and height

    var w = 1000;
    var h = 500;

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


 // helper functions are super useful with d3
    function translate (x, y) {
      return ['translate(', x, ',', y, ')'].join('');
    }