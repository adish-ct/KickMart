// copy button 

function copy(couponId){
    let couponCode = document.getElementById(`copyContent-${couponId}`).value
    navigator.clipboard.writeText(couponCode);
    let copyAlert = document.querySelector(`#copyAlert-${couponId}`)
    copyAlert.innerHTML = "copied"
  }