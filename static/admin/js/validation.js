function validate(){

    let productName = document.getElementById("productName").value
    let originalPrice = document.getElementById("originalPrice").value
    let sellingPrice = document.getElementById("sellingPrice").value

    const originalPriceError = document.getElementById("originalPriceError")
    const sellingPriceError = document.getElementById("sellingPriceError")
    const productNameError = document.getElementById("productNameError")

    if (productName.length === 0){

        productNameError.innerHTML = "* Product name required"
        return false
    }else {
        console.log(productName)
        productNameError.innerHTML = ""
    }
    if (originalPrice.length === 0){
        originalPriceError.innerHTML = "* Price required"
        return false
    }else{
        originalPriceError.innerHTML = ""
    }
    if (sellingPrice.length === 0){
        sellingPriceError.innerHTML = "* Selling price required"
        return false
    }else {
        sellingPrice.innerHTML = ""
    }

    return true
}