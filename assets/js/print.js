// stock reports -----------------------------------

function exportReportToExcel() {
    console.log("wordcount")

    // Get the table element
    const table = document.getElementById("sortTable");

    // Convert the table to a workbook
    const workbook = XLSX.utils.table_to_book(table);

    // Convert the workbook to a binary Excel file
    const excelBinary = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });

    // Create a Blob object and download the file
    const blob = new Blob([s2ab(excelBinary)], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "salesReport.xlsx";
    link.click();

    // Utility function to convert a string to an ArrayBuffer
    function s2ab(s) {
        const buf = new ArrayBuffer(s.length);
        const view = new Uint8Array(buf);
        for (let i = 0; i < s.length; i++) {
            view[i] = s.charCodeAt(i) & 0xff;
        }
        return buf;
    }
    //document.getElementById("downloadTable").hidden = true
}


function printTable() {
    var table = document.getElementById("sortTable");
    var newWin = window.open('', 'Print-Window');
    newWin.document.open();

    // Add necessary CSS styles for the table
    newWin.document.write('<html><head><style>');
    newWin.document.write('table { border-collapse: collapse; width: 100%; }');
    newWin.document.write('table, th, td { border: 1px solid black; }');
    newWin.document.write('</style></head><body onload="window.print()">');

    // Write the table HTML
    newWin.document.write(table.outerHTML);

    newWin.document.write('</body></html>');
    newWin.document.close();

    setTimeout(function () { newWin.close(); }, 10);
   // table.hidden = true;
}

// stock reports ---------------------------------------


// cancel reports -----------------------------------

function exportCancelTable() {
    console.log("wordcount")

    // Get the table element
    const table = document.getElementById("customTable");

    // Convert the table to a workbook
    const workbook = XLSX.utils.table_to_book(table);

    // Convert the workbook to a binary Excel file
    const excelBinary = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });

    // Create a Blob object and download the file
    const blob = new Blob([s2ab(excelBinary)], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "salesReport.xlsx";
    link.click();

    // Utility function to convert a string to an ArrayBuffer
    function s2ab(s) {
        const buf = new ArrayBuffer(s.length);
        const view = new Uint8Array(buf);
        for (let i = 0; i < s.length; i++) {
            view[i] = s.charCodeAt(i) & 0xff;
        }
        return buf;
    }
    //document.getElementById("downloadTable").hidden = true
}


function printCancelTable() {
    var table = document.getElementById("customTable");
    var newWin = window.open('', 'Print-Window');
    newWin.document.open();

    // Add necessary CSS styles for the table
    newWin.document.write('<html><head><style>');
    newWin.document.write('table { border-collapse: collapse; width: 100%; }');
    newWin.document.write('table, th, td { border: 1px solid black; }');
    newWin.document.write('</style></head><body onload="window.print()">');

    // Write the table HTML
    newWin.document.write(table.outerHTML);

    newWin.document.write('</body></html>');
    newWin.document.close();

    setTimeout(function () { newWin.close(); }, 10);
   // table.hidden = true;
}


// cancel reports -------------------------------------

// order reports ---------------------------------------


function exportOrderTable() {
    console.log("wordcount")

    const table = document.getElementById("orderTable");
    // Convert the table to a workbook
    const workbook = XLSX.utils.table_to_book(table);
    // Convert the workbook to a binary Excel file
    const excelBinary = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });

    // Create a Blob object and download the file
    const blob = new Blob([s2ab(excelBinary)], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "salesReport.xlsx";
    link.click();

    // Utility function to convert a string to an ArrayBuffer
    function s2ab(s) {
        const buf = new ArrayBuffer(s.length);
        const view = new Uint8Array(buf);
        for (let i = 0; i < s.length; i++) {
            view[i] = s.charCodeAt(i) & 0xff;
        }
        return buf;
    }
    //document.getElementById("downloadTable").hidden = true
}


function printOrderTable() {
    console.log('clicked');
    var table = document.getElementById("orderTable");
    var newWin = window.open('', 'Print-Window');
    newWin.document.open();

    // Add necessary CSS styles for the table
    newWin.document.write('<html><head><style>');
    newWin.document.write('table { border-collapse: collapse; width: 100%; }');
    newWin.document.write('table, th, td { border: 1px solid black; }');
    newWin.document.write('</style></head><body onload="window.print()">');

    // Write the table HTML
    newWin.document.write(table.outerHTML);

    newWin.document.write('</body></html>');
    newWin.document.close();

    setTimeout(function () { newWin.close(); }, 10);
   // table.hidden = true;
}

// order reports ---------------------------------------