
$('.payWithRazorpay').click(function (e) {
    e.preventDefault();
    var paymentMethod = $("[name = 'paymentMode']").val();
    var token = $("[name='csrfmiddlewaretoken']").val();
    // fetch values

    $.ajax({
        url: "proceed-to-pay/",
        method: "GET",
        success: function (response) {
            // console.log(response)
            var options = {
                "key": "rzp_test_i0ukiADffB9XqG", // Enter the Key ID generated from the Dashboard
                "amount": response.payable_amount * 100, // `Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "currency": "INR",
                "name": "Kick Mart Pvt",
                "description": "sample",
                "image": "https://example.com/your_logo",
                // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response_a) {
                    // alert(response_a.razorpay_payment_id);
                    data = {
                        'paymentMethod': paymentMethod,
                        'payment_id': response_a.razorpay_payment_id,
                        csrfmiddlewaretoken: token,
                    }

                    $.ajax({
                        type: "POST",
                        url: "order-confirmed/",
                        data: data,
                        success:(res)=>{
                            console.log('success')
                            console.log(res.status);
                            alert('ok')
                            location.href='order-confirmed/'
                            
                        }                       
                    });
                },
                "prefill": {
                    "name": "Gaurav Kumar",
                    "email": "gaurav.kumar@example.com",
                    "contact": "9000090000"
                },
                "notes": {
                    "address": "Razorpay Corporate Office"
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);

            rzp1.open();
        }
    });

});
