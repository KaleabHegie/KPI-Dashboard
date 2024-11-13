let tableToExcel = (function () {
  // Define the base URI for Excel export
  let uri = 'data:application/vnd.ms-excel;base64,';

  // Define the HTML template for the Excel file
  let template = `
    <html xmlns:o="urn:schemas-microsoft-com:office:office"
          xmlns:x="urn:schemas-microsoft-com:office:excel"
          xmlns="http://www.w3.org/TR/REC-html40">
      <head>
        <!--[if gte mso 9]>
          <meta charset="UTF-8">
          <xml>
            <x:ExcelWorkbook>
              <x:ExcelWorksheets>
                <x:ExcelWorksheet>
                  <x:Name>{worksheet}</x:Name>
                  <x:WorksheetOptions>
                    <x:DisplayGridlines/>
                  </x:WorksheetOptions>
                </x:ExcelWorksheet>
              </x:ExcelWorksheets>
            </x:ExcelWorkbook>
          </xml>
        <![endif]-->
      </head>
      <body>
        <table>{table}</table>
      </body>
    </html>`;

  // Function to convert a string to base64
  let base64 = function (s) {
    return window.btoa(unescape(encodeURIComponent(s)));
  };

  // Function to format the template with provided context
  let format = function (s, c) {
    return s.replace(/{(\w+)}/g, function (m, p) {
      return c[p];
    });
  };

  // Main function to export the specified table
  return function (table, name, filename) {
    // Get the table element by ID if a string is provided
    if (!table.nodeType) {
      table = document.getElementById(table);
    }
    // Create the context object for formatting
    var ctx = {
      worksheet: name || 'Worksheet',
      table: table.innerHTML
    };
    
    // Create a link element to trigger the download
    let link = document.createElement('a');
    link.href = uri + base64(format(template, ctx));
    link.download = filename || 'export.xls'; // Set the dynamic filename

    // Programmatically click the link to trigger the download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
})();
