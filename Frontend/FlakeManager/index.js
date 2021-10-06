import { getDataFromServerAndDisplay } from "./functions.js";

var currentFilter = {};

//add a click listener to the filter button of the filter Modal
$("#filter_button").click(function (event) {
  currentFilter = {};
  // getting the current status of the filter, set it to -1 if its not selected

  if ($("#userInput").val() != "")
    currentFilter.scan_user = $("#userInput").val();
  if ($("#sizeInput").val() != "")
    currentFilter.flake_size = $("#sizeInput").val();
  if ($("#thicknessSelect").val() != "")
    currentFilter.flake_thickness = $("#thicknessSelect").val();
  if ($("#materialSelect").val() != "")
    currentFilter.scan_exfoliated_material = $("#materialSelect").val();
  if ($("#flakeIdInput").val() != "")
    currentFilter.flake_id = $("#flakeIdInput").val();
  if ($("#queryLimit").val() != "")
    currentFilter.query_limit = $("#queryLimit").val();

  getDataFromServerAndDisplay(currentFilter);
});

// makes the table sortable as well as a paginatior
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
getDataFromServerAndDisplay(currentFilter);
