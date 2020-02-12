// GENERATE RESULTS //
function stars(score){
  var roundedScore = Math.floor(score);
  var htmlstr = `<span style="font-size:300%;color:lightskyblue;"><i class="fa fa-star"></i></span>`;
  var value = htmlstr.repeat(roundedScore);
  if (score - roundedScore > .3) {
    value = value.concat(`<span style="font-size:300%;color:lightskyblue;"><i class="fa fa-star-half"></i></span>`);
  }
  console.log(roundedScore);
  d3.select("#test")
  .html(value)
}
stars(8.4);
//stars()

// GENERATE CHARTS //

var svgWidth1 = 1000;
var svgWidth2 = 500;
var svgHeight = 600;

var chartMargin = {
  top: 50,
  right: 50,
  bottom: 100,
  left: 80
};

var chartWidth1 = svgWidth1 - chartMargin.left - chartMargin.right;
var chartWidth2 = svgWidth2 - chartMargin.left - chartMargin.right;
var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

//app.use('/data', express.static(__dirname + '/static'));
var fp1 = 'static/data/short_tables.csv'
var fp2 = 'static/data/medium_tables.csv'
var fp3 = 'static/data/long_tables.csv'

var tip = d3.tip()
.attr('class', 'd3-tip')
.offset([-20, 0])
.html(function(d) {
  return (`<strong>${d.model}</strong><hr>CO2/mi per seat:<br>${d.co2_mi_seat} lbs`);
});

///////////////////////////////////////////////////////////////////////

d3.select("#graph1")
.append("div")
.classed("special", true);

d3.select(".special")
.html(
  `<div class=row>
    <div class = col-4>
      <h4 class = 'writing'>CO2 Emissions Per Seat Per Mile:</h4>
      <select id='options' class = 'select'>
        <option value=${fp1} selected='selected'>Short Range</option>
        <option value=${fp2}>Medium Range</option>
        <option value=${fp3}>Long Range</option>
      </select>
    </div>
  </div>`);

var svg = d3.select(".special")
  .append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth1);

var chartGroup = svg.append("g")
  .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);

///////////////////////////////////////////////////////////////////////

function chart1(csv){
  d3.csv(csv).then(function(flightData) {
      flightData.forEach(function(data) {
        data.first_flight = +data.first_flight;
        data.seats = +data.seats;
        data.co2_mi_seat = +data.co2_mi_seat;
        data.co2_mi = +data.co2_mi;
        });


  //console.log(flightData);

  var barSpacing = 5;

  var barWidth = (chartWidth1 - (barSpacing * (flightData.length - 1))) / flightData.length;

  var modelLabels = flightData.map(function(d) { 
    return d.model
    });
  
  var yScale = d3.scaleLinear()
  .domain([0,.75])
  .range([chartHeight, 0]);

  var xScale = d3.scaleBand()
  .domain(modelLabels)
  .range([0, chartWidth1])
  .padding(0.05);

  var yAxis = d3.axisLeft(yScale);
  var xAxis = d3.axisBottom(xScale)

  chartGroup.append("g")
  .attr("transform", `translate(0, ${chartHeight})`)
  .attr("class", "axis")
  .call(xAxis)
  .selectAll("text")
    .attr("y", 0)
    .attr("x", 9)
    .attr("dy", ".35em")
    .attr("transform", "rotate(45)")
    .style("text-anchor", "start");;
  
  chartGroup.append("g")
  .attr("class", "axis")
  .call(yAxis);

  var axisLabelX = -50;
  var axisLabelY = chartHeight / 2;

  chartGroup.append("g")
    .attr("class", "label")
    .attr('transform', 'translate(' + axisLabelX + ', ' + axisLabelY + ')')
    .append("text")
    .attr('text-anchor', 'middle')
    .attr("transform", "rotate(-90)")
    .text("Lbs of C02 emitted per mile per seat");

  //console.log(flightData);

  var barsGroup = chartGroup.selectAll(".bar")
  .data(flightData)
  .enter()
  .append("rect")
  .classed("bar", true)
  .attr("id", "fix")
  .attr("width", d => barWidth)
  .attr("height", d => (chartHeight - yScale(d.co2_mi_seat)))
  .attr("x", (d, i) => i * (barWidth + barSpacing))
  .attr("y", d => yScale(d.co2_mi_seat));

  //console.log(ageData.age);
  
  chartGroup.call(tip);

  barsGroup.on("mouseover", function(d) {
      tip.show(d, this)})
      .on("mouseout", function(d) {
        tip.hide(d);

      });
    });    
  };


//////////////////////////////////////////////////////////////////////////////////
d3.select('#options')
.on("change", function () {
  var sect = document.getElementById("options");
  var section = sect.options[sect.selectedIndex].value;

  d3.selectAll(".bar").remove();
  d3.selectAll(".axis").remove();

  console.log(section)
  console.log("as percentages")

  return chart1(section)

  
  });


  

chart1(`${fp1}`);