function execute() {
  // 1. Spreadsheet with parameters
  // ss = SpreadsheetApp.openById('xxx');
  ss = SpreadsheetApp.getActiveSpreadsheet();

  // 2. Get parameters from the Spreadsheet
  sheet = ss.getSheetByName('params')
  var parameters = sheet.getDataRange().getValues()

  // 3. Call Cloud Functions
  // 3-0. Get access token of the GCP service account
  var service = checkOAuth()
  var gcp_token = ScriptApp.getOAuthToken()

  // 3-1. Create json for POST
  var data = {'parameters': parameters}
  var options = {
    'methods': 'post',
    'contentType': 'application/json',
    'headers': {'Authorization': 'Bearer '+ gcp_token},
    'payload' : JSON.stringify(data)
  }

  // 3-2. Call Cloud Functions URL and get the return
  var url = PropertiesService.getScriptProperties().getProperty('cloudFunctionsUrl'); //define propaties on GAS(file)
  var resJson = UrlFetchApp.fetch(url, options=options)
  var resJson_str = resJson.getContentText()

  // 4. Write return on Spreadsheet
  if (resJson_str != "OK"){ //null
    var res_array = JSON.parse(resJson)
    var array_index_len = res_array.length // including column row
    var array_columns_len = res_array[0].length

    sheet = ss.getSheetByName('data')
    var lastRow = sheet.getLastRow()
    if (lastRow < 2) {
      sheet.getRange(1, 1, array_index_len, array_columns_len).setValues(res_array)
      Logger.log("New data")
    }else{ //remove columns
      var res_array_values = []
      var i = 1
      while (i < array_index_len) {
        res_array_values.push(res_array[i])
        i += 1
      }
      sheet.getRange(lastRow + 1, 1, array_index_len - 1, array_columns_len).setValues(res_array_values)
      Logger.log("Add data")
    }
  }else{
    Logger.log("No data")
  }
  logWrite()
}

// logging
function logWrite(){
  sheet = ss.getSheetByName('log')
  var row = sheet.getLastRow()
  var cells = sheet.getRange(row + 1, 1, 1, 2)
  var timestamp = new Date()
  cells.setValues([[Utilities.formatDate(timestamp, "JST", "yyyy/MM/dd HH:mm:ss"), Logger.getLog()]])
}
