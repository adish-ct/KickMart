// handling add to cart button

let inputSize = document.getElementById("selectedValueInput")
  let addCartBtn = document.getElementById("addCartBtn")
  let alertDiv = document.getElementById("stockOut")
  console.log("start")
  console.log(inputSize)
  function checkSize(){
    if(inputSize == null){
      alertDiv.innerHTML = "choose a size"
      return false
    }
  }


// out of stock

function outOfStock() {
    const stockOut = document.getElementById("stockOut");
    stockOut.innerHTML = "Currently out of stock";
}

// size select

let selectedButton = null;
const selectedValueInput = document.getElementById("selectedValueInput");
const stockOut = document.getElementById("stockOut");
function selectButton(buttonIndex) {
  const buttonContainer = document.getElementById("buttonContainer");
  const buttons = buttonContainer.getElementsByClassName("button-size");
  stockOut.innerHTML = "";
  if (selectedButton !== null) {
    selectedButton.classList.remove("selected");
  }
  selectedButton = buttons[buttonIndex - 1];
  selectedButton.classList.add("selected");
  const selectedValue = selectedButton.getAttribute("data-value");
  selectedValueInput.value = selectedValue;
}

