var g1Val = g2Val = g3Val =g4Val = 0;



var opts = {
  angle: -0.2, // The span of the gauge arc
  lineWidth: 0.2, // The line thickness
  radiusScale: 1, // Relative radius
  pointer: {
    length: 0.6, // // Relative to gauge radius
    strokeWidth: 0.035, // The thickness
    color: '#000000' // Fill color
  },
  limitMax: false,     // If false, max value increases automatically if value > maxValue
  limitMin: false,     // If true, the min value of the gauge will be fixed
  colorStart: '#6FADCF',   // Colors
  colorStop: '#8FC0DA',    // just experiment with them
  strokeColor: '#E0E0E0',  // to see which ones work best for you
  generateGradient: true,
  highDpiSupport: true,     // High resolution support
  // renderTicks is Optional
  renderTicks: {
    divisions: 5,
    divWidth: 1.6,
    divLength: 0.7,
    divColor: '#111111',
    subDivisions: 6,
    subLength: 0.5,
    subWidth: 0.4,
    subColor: '#111111'
  },
  
};

let opts1 = Object.assign({}, opts);

opts1.staticZones = [
    {strokeStyle: "rgb(20,200,100)", min: 0, max: 2000, height: 1.2},
    {strokeStyle: "rgb(240,80,10)", min: 2001, max: 4000, height: 1.2},
    {strokeStyle: "rgb(200,30,30)", min: 4001, max: 6000, height: 1.2},
  ];

opts1.staticLabels = {
  font: "10px sans-serif",  // Specifies font
  labels: [0, 1000, 2000, 3000, 4000, 5000, 6000],  // Print labels at these values
  color: "#000000",  // Optional: Label text color
  fractionDigits: 0  // Optional: Numerical precision. 0=round off.
};


var g1 = document.getElementById('g1'); // your canvas element
var gauge1 = new Gauge(g1).setOptions(opts1); // create sexy gauge!
// gauge.percentColors = [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]];
gauge1.maxValue = 6000; // set max gauge value
gauge1.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gauge1.animationSpeed = 32; // set animation speed (32 is default value)
gauge1.set(g1Val); // set actual deserializer.readValue()




let opts2 = Object.assign({}, opts);

opts2.staticZones = [
    {strokeStyle: "rgb(20,200,100)", min: 0, max: 100, height: 1.2},
    {strokeStyle: "rgb(240,80,10)", min: 101, max: 250, height: 1.2},
    {strokeStyle: "rgb(200,30,30)", min: 251, max: 500, height: 1.2},
  ];

opts2.staticLabels = {
  font: "10px sans-serif",  // Specifies font
  labels: [0, 100, 200, 300, 400, 600],  // Print labels at these values
  color: "#000000",  // Optional: Label text color
  fractionDigits: 0  // Optional: Numerical precision. 0=round off.
};


var g2 = document.getElementById('g2'); // your canvas element
var gauge2 = new Gauge(g2).setOptions(opts2); // create sexy gauge!
gauge2.maxValue = 500; // set max gauge value
gauge2.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gauge2.animationSpeed = 32; // set animation speed (32 is default value)
gauge2.set(g2Val); // set actual deserializer.readValue()



let opts3 = Object.assign({}, opts);

opts3.staticZones = [
    {strokeStyle: "rgb(20,200,100)", min: 0, max: 50, height: 1.2},
    {strokeStyle: "rgb(240,80,10)", min: 51, max: 100, height: 1.2},
    {strokeStyle: "rgb(200,30,30)", min: 101, max: 200, height: 1.2},
  ];

opts3.staticLabels = {
  font: "10px sans-serif",  // Specifies font
  labels: [0, 50, 100, 150, 200],  // Print labels at these values
  color: "#000000",  // Optional: Label text color
  fractionDigits: 0  // Optional: Numerical precision. 0=round off.
};

var g3 = document.getElementById('g3'); // your canvas element
var gauge3 = new Gauge(g3).setOptions(opts3); // create sexy gauge!
gauge3.maxValue = 200; // set max gauge value
gauge3.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gauge3.animationSpeed = 32; // set animation speed (32 is default value)
gauge3.set(g3Val); // set actual deserializer.readValue()


let opts4 = Object.assign({}, opts);

opts4.staticZones = [
    {strokeStyle: "rgb(20,200,100)", min: 0, max: 50, height: 1.2},
    {strokeStyle: "rgb(240,80,10)", min: 51, max: 90, height: 1.2},
    {strokeStyle: "rgb(200,30,30)", min: 91, max: 180, height: 1.2},
  ];

opts4.staticLabels = {
  font: "10px sans-serif",  // Specifies font
  labels: [0, 40, 80, 140, 180],  // Print labels at these values
  color: "#000000",  // Optional: Label text color
  fractionDigits: 0  // Optional: Numerical precision. 0=round off.
};

var g4 = document.getElementById('g4'); // your canvas element
var gauge4 = new Gauge(g4).setOptions(opts4); // create sexy gauge!
gauge4.maxValue = 180; // set max gauge value
gauge4.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gauge4.animationSpeed = 32; // set animation speed (32 is default value)
gauge4.set(g4Val); // set actual deserializer.readValue()





const productList = document.querySelector("#productList");
const searchBtn = document.querySelector("#searchBtn");
const searchInput = document.querySelector("#searchInput");
const energyTable = document.querySelector("#energyTable");


function insertCard(data, parentElement) {
  let htmlString = `<div class="col col-md-3 col-sm-10 col-xs-12">
                    <div class="card rounded m-2">
                      <img src="${["image"]}" alt="product image" class="card-img rounded img-230">
                      <div class="card-body p-1 mt-2">
                        <div class="input-group mb-3">
                          <input type="text" class="form-control" placeholder="amount" aria-label="Recipient's username" aria-describedby="button-addon2">
                          <div class="input-group-append">
                          <button class="btn btn-outline-success add-btn p-9" type="button" id="addBtn" data-id="${data["product_id"]}" data-energy="${data["product_energy"]}">Add</button>
                          </div>
                        </div>
                      </div>
                          <div class="card-footer">
                              <h6 class="text-black-50 text-center">
                                  ${data["product_name"]}
                              </h6>
                          </div>
                      </div>
                      </div>`

  parentElement.appendChild(htmlString);};

$("#searchInput").on("input", function() {
  let value = $(this).val().toLowerCase();
  if (value != "") {
    $("#productList").removeClass("hidden-list");
    $("#productList .col").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  } else if (value == "") {
    $("#productList").addClass("hidden-list")
  }
});

function updateGauge(data) {
  gauge1.set(data["energy"]);
  gauge2.set(data["sugar"]);
  gauge3.set(data["lipid"]);
  gauge4.set(data["protein"]);
}

const addBtnList = Array.from(document.getElementsByClassName("add-btn"));

function insertToTable(data, parentElement) {
  const d = `
            <tr>
              <td>${data["product"]}</td>
              <td>
                  <span class="float-right badge badge-pill badge-secondary">
                      ${data["energy"]}
                  </span>
              </td>
          </tr>`;


    parentElement.innerHTML += d;
};


addBtnList.forEach(function(btn) {
  btn.addEventListener("click" , function(e) {
    const amount = parseInt(btn.parentNode.previousElementSibling.value, 10);
    const productId = parseInt(btn.getAttribute("data-id"), 10);
    $.ajax({
      url: "http://127.0.0.1:8000/h/add",
      type: "GET",
      data: {
        "id": productId,
        "amount": amount,
      },
      success: function(response) {
        console.log(response.content);
        updateGauge(response.content);
        insertToTable(response.content, energyTable);
      },
      error: function(response) {
        console.log(response.content);
      },
    })
  })
})


/*
function search(query) {
  $.ajax({
    url:"http://127.0.0.1:8000/p/search",
    type:"GET",
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
    data: {
      "q": String(query).trim(),
    },
    success: function(response) {
      console.log(response.content)
    },
    error: function(response) {
      console.log(response.content)
    }
  })}

searchBtn.addEventListener("click", function() {
  console.log(searchInput.value);
  search(searchInput.value);})
*/