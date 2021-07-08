import { BACKEND_URL, IMAGE_URL } from "../constants.js";

function deleteHandler(event) {
  var flake_id = event.data.id;
  if (confirm(`Do you wish to delete flake ${flake_id}?`)) {
    $.ajax({
      url: `${BACKEND_URL}/flakes?id=${flake_id}`,
      type: "DELETE",
      success: function (result) {
        // we need to rebuild the table
        $(`#${flake_id}`).addClass("table-danger");
        $(`#view_button${flake_id}`).remove();
        $(`#delete_button${flake_id}`).remove();
      },
    });
  }
}

function createTabelRow(data_dict) {
  //modalID
  var modal_id = `modalview${data_dict.flake_id}`;

  // create an empth row to populate later
  var row = $("<tr>").attr("id", data_dict.flake_id);

  // create each cell
  var index_cell = $("<td>")
    .text(data_dict.flake_id)
    .css("font-weight", "bold");
  var material_cell = $("<td>").text(data_dict.scan_exfoliated_material);
  var thickness_cell = $("<td>").text(data_dict.flake_thickness);
  var size_cell = $("<td>").text(data_dict.flake_size);
  var used_cell = $("<td>").text(data_dict.flake_used);

  // this is for the Buttons
  var button_cell = $("<td>");
  var button_div = $("<div>").css("text-align", "center");
  var view_button = $("<a>")
    .attr("data-bs-toggle", "modal")
    .attr("data-bs-target", `#${modal_id}`)
    .addClass("btn btn-primary btn-xs")
    .text("View")
    .attr("id", `view_button${data_dict.flake_id}`);
  //var toggle_button = $('<a>').addClass("btn btn-warning btn-xs").text("Toggle used")
  var delete_button = $("<a>")
    .addClass("btn btn-danger btn-xs")
    .text("Delete")
    .attr("id", `delete_button${data_dict.flake_id}`)
    .click({ id: data_dict.flake_id }, deleteHandler);

  //append the buttons to the button cell
  //button_div.append(toggle_button)
  button_div.append(view_button);
  button_div.append(delete_button);

  button_cell.append(button_div);
  //finally populate the row
  row.append(index_cell);
  row.append(material_cell);
  row.append(thickness_cell);
  row.append(size_cell);
  row.append(used_cell);
  row.append(button_cell);

  return row;
}

function createModal(data_dict) {
  var modal_id = `modalview${data_dict.flake_id}`;
  var image_directory = `${IMAGE_URL}/${data_dict.flake_path}`;

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
    .click({ id: data_dict.flake_id }, deleteHandler);
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
    .text(`Viewing Flake ${data_dict.flake_id}`);
  modal_header.append(heading);

  //body design "${image_directory}/5x.png"
  var gallery = `
  <div style="width:50%; margin:auto;">
    <div id="carousel${data_dict.flake_id}" class="carousel slide" data-bs-ride="false">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide-to="0" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide-to="2" class="active" aria-current="true" aria-label="Slide 3"></button>
            <button type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide-to="3" aria-label="Slide 4"></button>
            <button type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide-to="4" aria-label="Slide 5"></button>
        </div>

    <div class="carousel-inner" data-bs-interval="false">
    <div class="carousel-item">
        <img src="${image_directory}/2.5x.png" class="d-block w-100" loading="lazy" data-bs-interval="flase">
        <div class="carousel-caption d-none d-md-block">
        <h5>2.5x Image</h5>
        </div>
    </div>

    <div class="carousel-item">
        <img src="${image_directory}/5x.png" class="d-block w-100" loading="lazy" data-bs-interval="flase">
        <div class="carousel-caption d-none d-md-block">
            <h5>5x Image</h5>
        </div>
    </div>

    <div class="carousel-item active">
        <img src="${image_directory}/20x.png" class="d-block w-100" loading="lazy" data-bs-interval="flase">
        <div class="carousel-caption d-none d-md-block">
            <h5>20x Image</h5>
        </div>
    </div>

    <div class="carousel-item">
        <img src="${image_directory}/50x.png" class="d-block w-100" loading="lazy" data-bs-interval="flase">
        <div class="carousel-caption d-none d-md-block">
            <h5>50x Image</h5>
        </div>
    </div>

    <div class="carousel-item">
        <img src="${image_directory}/100x.png" class="d-block w-100" loading="lazy" data-bs-interval="flase">
        <div class="carousel-caption d-none d-md-block">
            <h5>100x Image</h5>
        </div>
    </div>
    </div>

    <button class="carousel-control-prev" type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carousel${data_dict.flake_id}" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
    </button>
    </div>
</div>
`;

  //modal_body.append(overview)
  modal_body.append(gallery);

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

function getDataFromServerAndDisplay(filter) {
  // Clear the Table first
  $("#flake_table > tbody").empty();

  // we need to remove all the modals
  $(".viewer").remove();

  // build the Query URL from the given Filter
  let query_url = BACKEND_URL + "/flakes?" + $.param(filter);

  // repopulate the table with data
  $.getJSON(query_url, function (data) {
    $.each(data, function (key, value) {
      var row = createTabelRow(value);
      var view_modal = createModal(value, IMAGE_URL);

      // Append to to the table
      $("#flake_table > tbody").append(row);
      $("body").append(view_modal);
    });
    $("#flake_table").trigger("update");
  });
}

export { getDataFromServerAndDisplay };
