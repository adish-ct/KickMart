$('.increseQuantity').click(function (e){
    e.preventDefault()

    let product_id = $(this).closest('.product_data').find('.product_id').val()
    let product_qty = $(this).closest('.product_data').find('.inputQuantity').val()
    let token = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        method: 'POST',
        url: 'add-cart-quandity/',
        data: {
            'product_id': product_id,
            'product_quandity': product_qty,
            csrfmiddlewaretoken: token,
        },
        
        success:(res)=>{
            console.log('increase');
            document.getElementById(product_id+"-qty").value=res.quantity
            document.getElementById(product_id+"-qtyL").innerHTML=res.quantity
            document.getElementById(product_id+"-total").innerHTML=res.total
            document.getElementById('productTotal').innerHTML=res.grant_total
            document.getElementById('cartTotal').innerHTML=res.total_amount
            document.getElementById('tax').innerHTML=res.tax
            document.getElementById('deliveryCharge').innerHTML=res.delivery_charge
            window.location.reload();

        }
    })
})



$('.decreaseQuantity').click(function (e){
    e.preventDefault()
    
    let product_id = $(this).closest('.product_data').find('.product_id').val()
    let product_qty = $(this).closest('.product_data').find('.inputQuantity').val()
    let token = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        method: 'POST',
        url: 'remove-cart-quandity/',
        data: {
            'product_id': product_id,
            'product_quandity': product_qty,
            csrfmiddlewaretoken: token,
        },
        success:(res)=>{
            console.log('decrease');
            document.getElementById(product_id+"-qty").value=res.quantity
            document.getElementById(product_id+"-qtyL").innerHTML=res.quantity
            document.getElementById(product_id+"-total").innerHTML=res.total
            document.getElementById('productTotal').innerHTML=res.grant_total
            document.getElementById('cartTotal').innerHTML=res.total_amount
            document.getElementById('tax').innerHTML=res.tax
            document.getElementById('deliveryCharge').innerHTML=res.delivery_charge
            window.location.reload();
        }
    })
})



