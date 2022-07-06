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
        document.querySelector("#barcodeText").value =
          result.codeResult.code;
      })
      .catch(function () {
        document.querySelector("#barcodeText").value = "Not Found";
      })
      .then(
        function () {
          this.attachListeners();
        }.bind(this)
      );
  },
  attachListeners: function () {
    var self = this,
      button = document.querySelector("#barcodeCamera"),
      fileInput = document.querySelector("#barcodeFile");

    button.addEventListener("click", function onClick(e) {
      e.preventDefault();
      button.removeEventListener("click", onClick);
      document.querySelector("#barcodeFile").click();
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


let searchBtn = document.getElementById("barcodeSearch");
searchBtn.addEventListener("click", function (e) {
  // get input value
  const code = document.querySelector("#barcodeText").value;
  window.location.href = window.location.href + "p/search/" + code.toString();
});
