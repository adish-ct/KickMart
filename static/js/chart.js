let sales = []
let elements = document.getElementsByClassName("salesData");
// Loop through the elements and extract their values
for (let i = 0; i < elements.length; i++) {
    sales.push(elements[i].textContent);
}

let years = []
let yElements = document.getElementsByClassName("yearData");
// Loop through the elements and extract their values
for (let i = 0; i < yElements.length; i++) {
    years.push(yElements[i].textContent);
}

var options = {
    chart: {
        type: 'line'
    },
    series: [{
        name: 'sales',
        data: sales
    }],
    xaxis: {
        categories: years
    }
}

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();



// order

let months = []
let xelements = document.getElementsByClassName("monthData");
// Loop through the elements and extract their values
for (let i = 0; i < xelements.length; i++) {
    months.push(xelements[i].textContent);
}

let order = []
let xyElements = document.getElementsByClassName("orderData");
// Loop through the elements and extract their values
for (let i = 0; i < xyElements.length; i++) {
    order.push(xyElements[i].textContent);
}
var options = {
    series: [{
        name: 'Net Profit',
        data: order
    }],
    chart: {
        type: 'bar',
        height: 350
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: months,
    },
    yaxis: {
        title: {
            text: '$ (thousands)'
        }
    },
    fill: {
        opacity: 1
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return "$ " + val + " thousands"
            }
        }
    }
};

var chart = new ApexCharts(document.querySelector("#barChart"), options);
chart.render();

// py chart

// let payment = []
// let count = document.getElementsById("payment_count");
// // Loop through the elements and extract their values
// for (let i = 0; i < elements.length; i++) {
//     sales.push(elements[i].textContent);
// }

// let payment_count = []
// let payment_methods = document.getElementsByClassName("payment_method");
// // Loop through the elements and extract their values
// for (let i = 0; i < yElements.length; i++) {
//     years.push(yElements[i].textContent);
// }

