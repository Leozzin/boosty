var Quagga = window.Quagga;
var App = {
  _scanner: null,
  init: function () {
    this.attachListeners();
  },
  decode: function (file) {
    Quagga.decoder({ readers: ["ean_reader"] })
      .locator({ patchSize: "medium" })
      .fromSource(file, { size: 800 })
      .toPromise()
      .then(function (result) {
        document.querySelector("#barcodeText1").value = result.codeResult.code;
      })
      .catch(function () {
        document.querySelector("#barcodeText1").value = "Not Found";
      })
      .then(
        function () {
          this.attachListeners();
        }.bind(this)
      );
  },
  attachListeners: function () {
    var self = this,
      button = document.querySelector("#barcodeBtn1"),
      fileInput = document.querySelector("#barcodeFile1");

    button.addEventListener("click", function onClick(e) {
      e.preventDefault();
      button.removeEventListener("click", onClick);
      document.querySelector("#barcodeFile1").click();
    });

    fileInput.addEventListener("change", function onChange(e) {
      e.preventDefault();
      fileInput.removeEventListener("change", onChange);
      if (e.target.files && e.target.files.length) {
        self.decode(e.target.files[0]);
      }
    });
  },
};

App.init();

var App2 = {
  _scanner: null,
  init: function () {
    this.attachListeners();
  },
  decode: function (file) {
    Quagga.decoder({ readers: ["ean_reader"] })
      .locator({ patchSize: "medium" })
      .fromSource(file, { size: 800 })
      .toPromise()
      .then(function (result) {
        document.querySelector("#barcodeText2").value = result.codeResult.code;
      })
      .catch(function () {
        document.querySelector("#barcodeText2").value = "Not Found";
      })
      .then(
        function () {
          this.attachListeners();
        }.bind(this)
      );
  },
  attachListeners: function () {
    var self = this,
      button = document.querySelector("#barcodeBtn2"),
      fileInput = document.querySelector("#barcodeFile2");

    button.addEventListener("click", function onClick(e) {
      e.preventDefault();
      button.removeEventListener("click", onClick);
      document.querySelector("#barcodeFile2").click();
    });

    fileInput.addEventListener("change", function onChange(e) {
      e.preventDefault();
      fileInput.removeEventListener("change", onChange);
      if (e.target.files && e.target.files.length) {
        self.decode(e.target.files[0]);
      }
    });
  },
};

App2.init();

function insertCard(data, parentElement) {
  const card = `
   <div class="card shadow mt-2 border-0 height="400">
        <h5 class="card-header bg-info text-light border-0">
          ${data["product_name"]}
        </h5>
    <div class="card-body">
     <p class="card-text">
       <ul>
          <li><strong>Nutrition:</strong> ${data["grade"]}</li>
          <li><strong>Sugar:</strong> ${data["sugar"]}</li>
          <li><strong>Lipide:</strong> ${data["lipids"]}</li>
          <li><strong>Salt:</strong> ${data["salt"]}</li>
          <li><strong>Fat:</strong> ${data["fat"]}</li>
          <li><strong>Saturated Fat:</strong> ${data["saturated_fat"]}</li>
       </ul>
     </p>
    </div>
   </div>
`;
  parentElement.innerHTML += card;
}

const HIGH = "High";
const MEDIUM = "Medium";
const LOW = "Low";

function getLevel(dc, big, small) {
  let result = null;
  if (dc >= big) {
    result = HIGH;
  } else if (dc > small && dc < big) {
    result = MEDIUM;
  } else if (dc <= small) {
    result = LOW;
  }
  return result;
}

function generateData(data) {
  let sugar = (salt = fat = lipids = saturated_fat = null);
  sugar = getLevel(parseFloat(data["sugar"]), 15, 5);
  salt = getLevel(parseFloat(data["salt"]), 1.5, 0.3);
  lipids = getLevel(parseFloat(data["lipids"]), 20, 3);
  fat = getLevel(parseFloat(data["fat"]), 20, 3);
  saturated_fat = getLevel(parseFloat(data["saturated_fat"]), 5, 1.5);
  return {
    sugar: sugar,
    salt: salt,
    lipids: lipids,
    fat: fat,
    saturated_fat: saturated_fat,
    grade: data["nutrition_grade"],
    product_name: data["product_name"],
  };
}

let compareBtn = document.getElementById("compareBtn");
compareBtn.addEventListener("click", function (e) {
  e.preventDefault();
  // get input value
  const productCard1 = document.querySelector("#productCard1");
  const productCard2 = document.querySelector("#productCard2");

  const code1 = document.querySelector("#barcodeText1").value;
  const code2 = document.querySelector("#barcodeText2").value;

  $.ajax({
    url: "http://127.0.0.1:8000/p/compare",
    type: "POST",
    contentType: "application/json; charset=utf-8",
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
    data: JSON.stringify({ barcode1: code1, barcode2: code2 }),
    success: function (response) {
      console.log(response);
      let data1 = generateData(response[0]);
      let data2 = generateData(response[1]);
      insertCard(data1, productCard1);
      insertCard(data2, productCard2);
    },
    error: function (response) {
      console.log(response.text);
    },
  });
});
