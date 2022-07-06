storeFilter = function(element) {
    const filtredNCardList = eshopCards.filter(function(card) {
        // filter based on the content of element
        if (element.value != "") {
            return card.getAttribute("data-product-category").toLowerCase() != element.value.toLowerCase();
        }
    });
    const filtredVCardList = eshopCards.filter(function(card) {
        // filter based on the content of element
        if (element.value != "") {
            return card.getAttribute("data-product-category") == element.value;
        }
    });
    console.log("filtredVCardList:: ", filtredVCardList);
    filtredVCardList.forEach(function(eshopCard) {
        eshopCard.style.display = "block";
    })
    console.log("filtredNCardList:: ", filtredNCardList);
    filtredNCardList.forEach(function(eshopCard) {
        eshopCard.style.display = "none";
    })
    if (element.value.toLowerCase() == "") {
        eshopCards.forEach(function(eshopCard) {
            console.log("SELECT EMPTY:: ", eshopCard);
            eshopCard.style.display = "block";
        })
    }

}


let eshopCards = Array.from(document.getElementsByClassName("eshop-card"));
let selectElements = Array.from(document.getElementsByClassName("selecta"));


selectElements.forEach(function(element) {
    element.addEventListener("change", function(event) {
        storeFilter(element)
    });
});