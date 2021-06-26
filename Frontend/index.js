import { createModal, createTabelRow } from "./functions.js";

var backend_URL = "http://192.168.0.220:5000/flakes";

function buildURL(backend_URL, filter) {
  let full_URL = backend_URL;
  let first_value = true;
  for (const [key, value] of Object.entries(filter)) {
    if (value != "-1") {
      if (first_value) {
        full_URL += "?";
        first_value = false;
      } else {
        full_URL += "&";
      }
      full_URL += `${key}=${value}`;
    }
  }

  return full_URL;
}

function getDataFromServerAndDisplay(filter) {
  // Clear the Table first
  $("#flake_table > tbody").empty();

  let full_URL = buildURL(backend_URL, filter);

  // repopulate the table with data
  $.getJSON(full_URL, function (data) {
    $.each(data, function (key, value) {
      var row = createTabelRow(value);
      var view_modal = createModal(value);

      // Append to to the table
      $("#flake_table > tbody").append(row);
      $("#flake_table").append(view_modal);
    });
    $("#flake_table").trigger("update");
  });
}
//add a click listener to the filter button of the filter Modal
$("#filter_button").click(function (event) {
  var currentFilter = {};
  // getting the current status of the filter, set it to -1 if its not selected
  currentFilter.userName =
    $("#userInput").val() != "" ? $("#userInput").val() : "-1";
  currentFilter.minSize =
    $("#sizeInput").val() != "" ? $("#sizeInput").val() : "-1";
  currentFilter.thickness =
    $("#thicknessSelect").val() != "" ? $("#thicknessSelect").val() : "-1";
  currentFilter.material =
    $("#materialSelect").val() != "" ? $("#materialSelect").val() : "-1";
  currentFilter.flake_limit =
    $("#flakeLimit").val() != "" ? $("#flakeLimit").val() : "-1";

  getDataFromServerAndDisplay(currentFilter);
});

// first creation
// define a default filter

var currentFilter = {
  userName: "-1",
  minSize: "-1",
  thickness: "-1",
  material: "-1",
  flake_limit: "-1",
};
//display the data
getDataFromServerAndDisplay(currentFilter);

// makes the table sortable
$(function () {
  $("#flake_table")
    .tablesorter({
      theme: "bootstrap",
    })
    .tablesorterPager({
      // target the pager markup - see the HTML block below
      container: $(".ts-pager"),

      // target the pager page select dropdown - choose a page
      cssGoto: ".pagenum",

      // remove rows from the table to speed up the sort of large tables.
      // setting this to false, only hides the non-visible rows; needed if you plan to add/remove rows with the pager enabled.
      removeRows: false,

      // Number of visible rows
      size: 15,
      // output string - default is '{page}/{totalPages}';
      // possible variables: {page}, {totalPages}, {filteredPages}, {startRow}, {endRow}, {filteredRows} and {totalRows}
      output: "{startRow} - {endRow} / {totalRows}",
    });
});
