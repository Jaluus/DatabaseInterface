import { createModal, createTabelRow, getDataFromServerAndDisplay } from "./functions.js";

var backend_URL = "http://192.168.0.220:5000/flakes";
var currentFilter = {};

//add a click listener to the filter button of the filter Modal
$("#filter_button").click(function (event) {
  currentFilter = {};
  // getting the current status of the filter, set it to -1 if its not selected
  currentFilter.userName =
    $("#userInput").val() != "" ? $("#userInput").val() : undefined;
  currentFilter.minSize =
    $("#sizeInput").val() != "" ? $("#sizeInput").val() : undefined;
  currentFilter.thickness =
    $("#thicknessSelect").val() != "" ? $("#thicknessSelect").val() : undefined;
  currentFilter.exfoliated_material =
    $("#materialSelect").val() != "" ? $("#materialSelect").val() : undefined;
  currentFilter.flake_limit =
    $("#flakeLimit").val() != "" ? $("#flakeLimit").val() : undefined;

  getDataFromServerAndDisplay(backend_URL, currentFilter);
});

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

// first creation

//display the data
getDataFromServerAndDisplay(backend_URL, currentFilter);

