$(document).on("click", ".Id_submit", function (event) {
    event.preventDefault();
    var selector = $(this).closest(".productID")
    console.log(selector.find("form").attr('action'))
    $.ajax({
        type: 'POST',
        url: selector.find("form").attr('action'),
        success: function () {
            alert("Product added to cart")
        }
    });
})