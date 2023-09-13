function validate(){

    let productName = document.getElementById("productName").value
    let originalPrice = document.getElementById("originalPrice").value
    let sellingPrice = document.getElementById("sellingPrice").value


    const originalPriceError = document.getElementById("originalPriceError")
    const sellingPriceError = document.getElementById("sellingPriceError")
    const productNameError = document.getElementById("productNameError")

    if (productName.length === 0) {
        productNameError.innerHTML = "* Product name required"
        return false
    }
    if (originalPrice.length === 0){
        originalPriceError.innerHTML = "* Price required"
        return false
    }
    if (sellingPrice.length === 0){
        sellingPriceError.innerHTML = "* Selling price required"
        return false
    }

    productNameError.innerHTML = ""
    originalPriceError.innerHTML = ""
    sellingPrice.innerHTML = ""

    return true
}



// coupon validation
function couponValidate(){
        console.log("working")
        let couponCode = document.getElementById("addCoupon").value
        let couponTitle = document.getElementById("couponTitle").value
        let discountAmount = document.getElementById("discountAmount").value
        let discount = document.getElementById("discount").value
        let minAmount = document.getElementById("minAmount").value
        let description = document.getElementById("productDesc").value

        const couponCodeError = document.getElementById("couponCodeError")
        const couponTitleError = document.getElementById("couponTitleError")
        const discountAmountError = document.getElementById("discountAmountError")
        const minAmountError = document.getElementById("minAmountError")
        const descriptionError = document.getElementById("descriptionError")

        if (couponCode.length === 0){
            couponCodeError.innerHTML = "* coupon code required"
            return false
        }
        couponCodeError.innerHTML = ""
        if (couponTitle.length === 0){
            couponTitleError.innerHTML = "* coupon title required"
            return false
        }
        couponTitleError.innerHTML = ""
        if (discountAmount.length === 0 && discount.length === 0){
            discountAmountError.innerHTML = "*  provide discount amount or discount"
            return false
        }
        discountAmountError.innerHTML = ""
        if (minAmount.length === 0){
            minAmountError.innerHTML = "* minimum amount required"
            return false
        }
        minAmountError.innerHTML = ""
        if (description.length === 0){
            descriptionError.innerHTML = "* coupon description required"
            return false
        }
        descriptionError.innerHTML = ""

        return true
}