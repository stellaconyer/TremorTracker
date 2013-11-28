var n = 100,
  random = d3.random.normal(0, 20),


  //Create separate data arrays for x,y,z
  data = [];
 
var margin = {top: 20, right: 20, bottom: 20, left: 40},
    width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
 
var x = d3.scale.linear()
    .domain([1, 50])
    .range([0, width]);
 
var y = d3.scale.linear()
    .domain([-15, 15])
    .range([height, 0]);
 
var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d, i) { return x(i); })
    .y(function(d, i) { return y(d); });
 
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
svg.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);
 
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + y(0) + ")")
    .call(d3.svg.axis().scale(x).orient("bottom"));
 
svg.append("g")
    .attr("class", "y axis")
    .call(d3.svg.axis().scale(y).orient("left"));
 

 // path for x recording 
var path = svg.append("g")
    .attr("clip-path", "url(#clip)")
  .append("path")
    .datum(data) //modify for y,z
    .attr("class", "line")
    .attr("d", line);
    //set stroke attribute

  //draw y,z path
 


function tick(x_coord) {
 
//call these for each x,y,z

  // push a new data point onto the back
  data.push(x_coord);
  console.log("tick");
  console.log(data);
 
  // redraw the line, and slide it to the left
  path
      .attr("d", line)
      .attr("transform", null)
    .transition()
      .duration(500)
      .ease("linear")
      .attr("transform", "translate(" + x(0) + ",0)");
      // .each("end", tick);
 
  // pop the old data point off the front

    if (data.length > 50) {
        data.shift();}
 
}

