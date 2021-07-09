import { BACKEND_URL, IMAGE_URL } from "../constants.js";

// Saving the Current State
var current_scan_data = undefined;
var current_flakes = [];
var current_flake_index = 0;
var current_mag = 1;
const MAG_DICT = {
  1: "2.5x",
  2: "5x",
  3: "20x",
  4: "50x",
  5: "100x",
};

function updateQuickInspectModal() {
  // swap the Image and the heading
  $("#quick_inspect_image").attr(
    "src",
    `${IMAGE_URL}/${current_flakes[current_flake_index]?.flake_path}/${MAG_DICT[current_mag]}.png`
  );
  $("#quick_inspect_overview").attr(
    "src",
    `${IMAGE_URL}/${current_flakes[current_flake_index]?.flake_path}/overview_marked.jpg`
  );
  $("#quick_inspect_heading").text(
    `Currently inspecting "${current_scan_data?.scan_name}" | Flake ID : ${
      current_flakes[current_flake_index]?.flake_id
    } | Current Flake ${current_flake_index + 1} / ${
      current_flakes.length
    } | current Magnification ${MAG_DICT[current_mag]}`
  );

  $("#quick_inspect_eval").attr(
    "src",
    `${IMAGE_URL}/${current_flakes[current_flake_index]?.flake_path}/eval_img.png`
  );

  //Update every Table Row
  $("#flake_id").text(current_flakes[current_flake_index]?.flake_id);
  $("#flake_thickness").text(
    current_flakes[current_flake_index]?.flake_thickness
  );
  $("#flake_used").text(current_flakes[current_flake_index]?.flake_used);
  $("#scan_exfoliated_material").text(
    current_flakes[current_flake_index]?.scan_exfoliated_material
  );
  $("#flake_size").text(
    Math.round(current_flakes[current_flake_index]?.flake_size) + " μm²"
  );
  $("#flake_width").text(
    Math.round(current_flakes[current_flake_index]?.flake_width) + " μm"
  );
  $("#flake_height").text(
    Math.round(current_flakes[current_flake_index]?.flake_height) + " μm"
  );
  $("#flake_aspect_ratio").text(
    current_flakes[current_flake_index]?.flake_aspect_ratio
  );
  $("#flake_entropy").text(current_flakes[current_flake_index]?.flake_entropy);
  $("#chip_id").text(current_flakes[current_flake_index]?.chip_id);
  $("#chip_thickness").text(
    current_flakes[current_flake_index]?.chip_thickness
  );
  $("#chip_used").text(current_flakes[current_flake_index]?.chip_used);
  $("#scan_id").text(current_flakes[current_flake_index]?.scan_id);
  $("#scan_name").text(current_flakes[current_flake_index]?.scan_name);
  $("#scan_user").text(current_flakes[current_flake_index]?.scan_user);
  $("#scan_time").text(current_flakes[current_flake_index]?.scan_time);
  $("#scan_exfoliation_method").text(
    current_flakes[current_flake_index]?.scan_exfoliation_method
  );
}

function deleteCurrentFlake() {
  if (
    confirm(`Delete Flake ${current_flakes[current_flake_index]?.flake_id}?`)
  ) {
    $.ajax({
      url: `${BACKEND_URL}/flakes?flake_id=${current_flakes[current_flake_index]?.flake_id}`,
      type: "DELETE",
      success: function (result) {
        //removes the Flake from the Array
        current_flakes.splice(current_flake_index, 1);
        updateQuickInspectModal();
      },
    });
  }
}

function deleteHandler(event) {
  var scan_id = event.data.id;
  if (confirm(`Do you wish to delete Scan ${scan_id}?`)) {
    if (
      confirm(
        `Are you REALLY Sure, this is permanent\nYou are about to delete all associated files and entries in the Database`
      )
    ) {
      $.ajax({
        url: `${BACKEND_URL}/scans?scan_id=${scan_id}`,
        type: "DELETE",
        success: function (result) {
          // we need to rebuild the table
          $(`#${scan_id}`).addClass("table-danger");
          $(`#view_button${scan_id}`).remove();
          $(`#delete_button${scan_id}`).remove();
        },
      });
    }
  }
}

function downloadCurrentFlake(event) {
  // Quick and Dirty way to download the File from my server
  window.location = `${BACKEND_URL}/downloadFlake?flake_id=${current_flakes[current_flake_index]?.flake_id}`;
}

function quickViewHandler(event) {
  current_scan_data = event.data.scan_data;
  let query_url =
    BACKEND_URL + `/flakes?scan_id=${current_scan_data.scan_id}&query_limit=-1`;

  // Query the DB for the Flakes belonging to the Scan
  $.getJSON(query_url, function (data) {
    // set the state of the App
    current_flakes = data;
    current_flake_index = 0;
    current_mag = 1;
    updateQuickInspectModal();
  });
}

function createTabelRow(data_dict) {
  //modalIDs
  var view_modal_id = `modalview${data_dict.scan_id}`;

  // create an empth row to populate later
  var row = $("<tr>").attr("id", data_dict.scan_id);

  //time to nicer look
  var Unix = data_dict.scan_time;
  var dateObject = new Date(Unix * 1000);
  const humanDateFormat = dateObject.toLocaleString();

  // create each cell
  var index_cell = $("<td>").text(data_dict.scan_id).css("font-weight", "bold");
  var name_cell = $("<td>").text(data_dict.scan_name);
  var user_cell = $("<td>").text(data_dict.scan_user);
  var material_cell = $("<td>").text(data_dict.scan_exfoliated_material);
  var time_cell = $("<td>").text(humanDateFormat);

  // this is for the Buttons
  var button_cell = $("<td>");
  var button_div = $("<div>").css("text-align", "center");
  var view_button = $("<a>")
    .attr("data-bs-toggle", "modal")
    .attr("data-bs-target", `#${view_modal_id}`)
    .addClass("btn btn-primary btn-xs")
    .text("View")
    .attr("id", `view_button${data_dict.scan_id}`);
  var quickview_button = $("<a>")
    .addClass("btn btn-warning btn-xs")
    .attr("data-bs-toggle", "modal")
    .attr("data-bs-target", `#modalquick`)
    .text("Quick Inspect")
    .css("color", "black")
    .click({ scan_data: data_dict }, quickViewHandler);
  var delete_button = $("<a>")
    .addClass("btn btn-danger btn-xs")
    .text("Delete")
    .attr("id", `delete_button${data_dict.scan_id}`)
    .click({ id: data_dict.scan_id }, deleteHandler);

  //append the buttons to the button cell
  button_div.append(view_button);
  button_div.append(quickview_button);
  button_div.append(delete_button);

  button_cell.append(button_div);
  //finally populate the row
  row.append(index_cell);
  row.append(name_cell);
  row.append(user_cell);
  row.append(material_cell);
  row.append(time_cell);
  row.append(button_cell);

  return row;
}

function createQuickInspectModal() {
  var modal_id = `modalquick`;

  // creating the Modal
  var quickInspectModal = $("<div>")
    .attr({ role: "dialog", id: modal_id, tabindex: -1, "aria-modal": true })
    .addClass("modal fade viewer");
  var modal_dialog = $("<div>").addClass("modal-dialog modal-fullscreen");
  var modal_content = $("<div>").addClass("modal-content");
  var modal_header = $("<div>").addClass("modal-header");
  var modal_body = $("<div>").addClass("modal-body");
  var modal_footer = $("<div>").addClass("modal-footer");

  //header design
  var heading = $("<h4>")
    .attr("id", "quick_inspect_heading")
    .addClass("modal-title");
  modal_header.append(heading);

  //body design

  var overview = /*html*/ `
  <div class="row">
    <div class="col-3">
      <table class="table table-hover table-sm">
        <thead>
          <tr>
            <th style="width:50%" scope="col">Flake Key</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Flake ID</th>
            <td id="flake_id"></td>
          </tr>
          <tr>
            <th scope="row">Flake Thickness</th>
            <td id="flake_thickness"></td>
          </tr>
          <tr>
            <th scope="row">Flake Used</th>
            <td id="flake_used"></td>
          </tr>
          <tr>
            <th scope="row">Flake Material</th>
            <td id="scan_exfoliated_material"></td>
          </tr>
          <tr>
            <th scope="row">Flake Size</th>
            <td id="flake_size"></td>
          </tr>
          <tr>
            <th scope="row">Flake Width</th>
            <td id="flake_width"></td>
          </tr>
          <tr>
            <th scope="row">Flake Length</th>
            <td id="flake_height"></td>
          </tr>
          <tr>
            <th scope="row">Flake Aspect Ratio</th>
            <td id="flake_aspect_ratio"></td>
          </tr>
          <tr>
            <th scope="row">Flake Entropy</th>
            <td id="flake_entropy"></td>
          </tr>
        </tbody>
      </table>

      <table class="table table-hover table-sm">
        <thead>
          <tr>
            <th style="width:50%" scope="col">Chip Key</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Chip ID</th>
            <td id="chip_id"></td>
          </tr>
          <tr>
            <th scope="row">Chip Thickness</th>
            <td id="chip_thickness"></td>
          </tr>
          <tr>
            <th scope="row">Chip Used</th>
            <td id="chip_used"></td>
          </tr>
        </tbody>
      </table>

      <table class="table table-hover table-sm">
        <thead>
          <tr>
            <th style="width:50%" scope="col">Scan Key</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Scan ID</th>
            <td id="scan_id"></td>
          </tr>
          <tr>
            <th scope="row">Scan Name</th>
            <td id="scan_name"></td>
          </tr>
          <tr>
            <th scope="row">Scan User</th>
            <td id="scan_user"></td>
          </tr>
          <tr>
            <th scope="row">Scan Time</th>
            <td id="scan_time"></td>
          </tr>
          <tr>
            <th scope="row">Scan Exfoliation Method</th>
            <td id="scan_exfoliation_method"></td>
          </tr>
        </tbody>
      </table>

    </div>

    <div class="col-6 mx-auto text-center">
      <img id="quick_inspect_image" class="img-thumbnail" loading="lazy"> 
    </div>

  <div class="col-3 mx-auto text-center">
    <img id="quick_inspect_overview" class="img-thumbnail" loading="lazy"> 
    <img id="quick_inspect_eval" class="img-thumbnail" loading="lazy">
  </div>
</div>
  `;

  modal_body.append(overview);

  // buttons for exititng
  var dismiss_button = $("<button>")
    .attr({ type: "button", "data-bs-dismiss": "modal" })
    .addClass("btn btn-secondary")
    .text("Close");
  var delete_button = $("<button>")
    .attr({ type: "button", "data-bs-dismiss": "modal" })
    .addClass("btn btn-danger")
    .text("Delete")
    .click(deleteCurrentFlake);
  var download_button = $("<button>")
    .attr("type", "button")
    .addClass("btn btn-primary")
    .text("Download as ZIP")
    .click(downloadCurrentFlake);

  //footer Design
  modal_footer.append(delete_button);
  modal_footer.append(download_button);
  modal_footer.append(dismiss_button);

  // build the final modal
  modal_content.append(modal_header);
  modal_content.append(modal_body);
  modal_content.append(modal_footer);
  modal_dialog.append(modal_content);
  quickInspectModal.append(modal_dialog);

  // adding a Keylistener into the Modal to listen Change to current state
  quickInspectModal.on("keydown", function (e) {
    //W
    if (e.key == "w" || e.key == "W" || e.key == "ArrowUp") {
      current_mag += 1;
    }
    //A
    else if (e.key == "a" || e.key == "A" || e.key == "ArrowLeft") {
      current_flake_index -= 1;
    }
    //S
    else if (e.key == "s" || e.key == "S" || e.key == "ArrowDown") {
      current_mag -= 1;
    }
    //D
    else if (e.key == "d" || e.key == "D" || e.key == "ArrowRight") {
      current_flake_index += 1;
    }
    //Q
    else if (e.key == "q" || e.key == "Q") {
      deleteCurrentFlake();
    } else if (e.key == "e" || e.key == "E") {
      downloadCurrentFlake();
    }

    // clamping the Values
    current_flake_index = Math.min(
      Math.max(current_flake_index, 0),
      current_flakes.length - 1
    );
    current_mag = Math.min(Math.max(current_mag, 1), 5);

    updateQuickInspectModal();
  });
  return quickInspectModal;
}

function createViewModal(data_dict) {
  var modal_id = `modalview${data_dict.scan_id}`;
  var image_directory = `${IMAGE_URL}/${data_dict.scan_name}`;

  // creating the Modal
  var view_modal = $("<div>")
    .attr({ role: "dialog", id: modal_id, tabindex: -1, "aria-modal": true })
    .addClass("modal fade viewer");
  var modal_dialog = $("<div>").addClass("modal-dialog modal-fullscreen");
  var modal_content = $("<div>").addClass("modal-content");
  var modal_header = $("<div>").addClass("modal-header");
  var modal_body = $("<div>").addClass("modal-body");
  var modal_footer = $("<div>").addClass("modal-footer");

  // buttons for exititng
  var delete_button = $("<button>")
    .attr({ type: "button", "data-bs-dismiss": "modal" })
    .addClass("btn btn-danger")
    .text("Delete")
    .click({ id: data_dict.scan_id }, deleteHandler);
  var download_button = $("<button>")
    .attr("type", "button")
    .addClass("btn btn-primary")
    .text("Download as ZIP");
  var dismiss_button = $("<button>")
    .attr({ type: "button", "data-bs-dismiss": "modal" })
    .addClass("btn btn-secondary")
    .text("Close");

  //header design
  var heading = $("<h4>")
    .addClass("modal-title")
    .text(`Viewing Scan ${data_dict.scan_id}`);
  modal_header.append(heading);

  //body design
  var overview = `
        <div class="row bg-faded">
            <div class="col-6 mx-auto text-center">
                <img src="${image_directory}/overview.png" class="img-thumbnail" loading="lazy"> 
            </div>
        </div>
    `;

  modal_body.append(overview);

  //footer Design
  modal_footer.append(delete_button);
  modal_footer.append(download_button);
  modal_footer.append(dismiss_button);

  // build the final modal
  modal_content.append(modal_header);
  modal_content.append(modal_body);
  modal_content.append(modal_footer);
  modal_dialog.append(modal_content);
  view_modal.append(modal_dialog);

  return view_modal;
}

function createScanTable() {
  // What to add
  // Number Chips, Number Flakes, mono bi tri etc..
  // User, name, Material, time
  var table = $("<table>");
}

function getDataFromServerAndDisplay(filter) {
  // Clear the Table first
  $("#flake_table > tbody").empty();

  // we need to remove all the modals
  $(".viewer").remove();

  // build the Query URL from the given Filter
  // This is Querying for all the Scans
  let query_url = BACKEND_URL + "/scans?" + $.param(filter);

  // repopulate the table with data
  $.getJSON(query_url, function (data) {
    $.each(data, function (key, value) {
      var row = createTabelRow(value);
      var view_modal = createViewModal(value);

      // Append to to the table
      $("#flake_table > tbody").append(row);
      $("body").append(view_modal);
    });
    $("#flake_table").trigger("update");
  });

  var quick_inspect_modal = createQuickInspectModal();
  $("body").append(quick_inspect_modal);
}

export { getDataFromServerAndDisplay };
