import { BACKEND_URL, IMAGE_URL } from "./constants.js"

// Saving the Current State
var current_scan_data = undefined
var current_flakes = []
var current_flake_index = 0
var current_mag = 1
const MAG_DICT = {
    1: "2.5x",
    2: "5x",
    3: "20x",
    4: "50x",
    5: "100x",
}

function deleteCurrentFlake() {
    confirm(`Delete Flake ${current_flakes[current_flake_index]?.flake_id}?`)
}

function deleteHandler(event) {
    var scan_id = event.data.id
    if (confirm(`Do you wish to delete Scan ${scan_id}?`)) {
        if (confirm(`Are you REALLY Sure, this is permanent\nYou are about to delete all associated files and entries in the Database`)) {
            $.ajax({
                url: `${BACKEND_URL}/scans?id=${scan_id}`,
                type: 'DELETE',
                success: function (result) {
                    // we need to rebuild the table
                    $(`#${scan_id}`).addClass("table-danger")
                    $(`#view_button${scan_id}`).remove();
                    $(`#delete_button${scan_id}`).remove();
                }
            });
        }
    }
}

function quickViewHandler(event) {
    current_scan_data = event.data.scan_data
    let query_url = BACKEND_URL + `/flakes?scan_id=${current_scan_data.scan_id}&query_limit=-1`;

    // Query the DB for the Flakes belonging to the Scan
    $.getJSON(query_url, function (data) {
        // set the state of the App
        current_flakes = data
        current_flake_index = 0
        current_mag = 1
        $("#quick_inspect_image").attr("src", `${IMAGE_URL}/${current_flakes[current_flake_index]?.flake_path}/${MAG_DICT[current_mag]}.png`)
        $("#quick_inspect_heading").text(`Current Scan: ${current_scan_data.scan_id}, current Flake ID: ${current_flakes[current_flake_index]?.flake_id}, current Flake ${current_flake_index + 1} / ${current_flakes.length}`)
    });

}

function createTabelRow(data_dict) {
    //modalIDs
    var view_modal_id = `modalview${data_dict.scan_id}`

    // create an empth row to populate later
    var row = $('<tr>').attr('id', data_dict.scan_id);

    //time to nicer look
    var Unix = data_dict.scan_time
    var dateObject = new Date(Unix * 1000)
    const humanDateFormat = dateObject.toLocaleString()

    // create each cell
    var index_cell = $("<td>").text(data_dict.scan_id).css("font-weight", "bold")
    var name_cell = $("<td>").text(data_dict.scan_name)
    var user_cell = $("<td>").text(data_dict.scan_user)
    var material_cell = $("<td>").text(data_dict.scan_exfoliated_material)
    var time_cell = $("<td>").text(humanDateFormat)

    // this is for the Buttons
    var button_cell = $('<td>')
    var button_div = $('<div>').css("text-align", "center")
    var view_button = $('<a>').attr("data-bs-toggle", "modal").attr("data-bs-target", `#${view_modal_id}`).addClass("btn btn-primary btn-xs").text("View").attr('id', `view_button${data_dict.scan_id}`);
    var quickview_button = $('<a>').addClass("btn btn-warning btn-xs").attr("data-bs-toggle", "modal").attr("data-bs-target", `#modalquick`).text("Quick Inspect").css("color", "black").click({ 'scan_data': data_dict }, quickViewHandler)
    var delete_button = $('<a>').addClass("btn btn-danger btn-xs").text("Delete").attr('id', `delete_button${data_dict.scan_id}`).click({ 'id': data_dict.scan_id }, deleteHandler)

    //append the buttons to the button cell
    button_div.append(view_button)
    button_div.append(quickview_button)
    button_div.append(delete_button)

    button_cell.append(button_div)
    //finally populate the row
    row.append(index_cell)
    row.append(name_cell)
    row.append(user_cell)
    row.append(material_cell)
    row.append(time_cell)
    row.append(button_cell)

    return row
}

function createQuickInspectModal() {
    var modal_id = `modalquick`

    // creating the Modal
    var view_modal = $('<div>').attr({ role: "dialog", 'id': modal_id, 'tabindex': -1, "aria-modal": true }).addClass("modal fade viewer")
    var modal_dialog = $('<div>').addClass("modal-dialog modal-fullscreen")
    var modal_content = $('<div>').addClass("modal-content")
    var modal_header = $('<div>').addClass("modal-header")
    var modal_body = $('<div>').addClass("modal-body")
    var modal_footer = $('<div>').addClass("modal-footer")

    // buttons for exititng
    var dismiss_button = $("<button>").attr({ "type": "button", 'data-bs-dismiss': "modal" }).addClass("btn btn-secondary").text("Close")

    //header design
    var heading = $('<h4>').attr("id", "quick_inspect_heading").addClass("modal-title")
    modal_header.append(heading)

    //body design
    var overview = `
        <div class="row bg-faded">
            <div class="col-6 mx-auto text-center">
                <img id="quick_inspect_image" class="img-thumbnail"> 
            </div>
        </div>
    `

    modal_body.append(overview)

    //footer Design
    modal_footer.append(dismiss_button)

    // build the final modal
    modal_content.append(modal_header)
    modal_content.append(modal_body)
    modal_content.append(modal_footer)
    modal_dialog.append(modal_content)
    view_modal.append(modal_dialog)

    // adding a Keylistener into the Modal to listen Change to current state
    view_modal.on("keydown", function (e) {
        //W
        if (e.key == "w" || e.key == "W" || e.key == "ArrowUp") {
            current_mag += 1
        }
        //A
        else if (e.key == "a" || e.key == "A" || e.key == "ArrowLeft") {
            current_flake_index -= 1
        }
        //S
        else if (e.key == "s" || e.key == "S" || e.key == "ArrowDown") {
            current_mag -= 1
        }
        //D
        else if (e.key == "d" || e.key == "D" || e.key == "ArrowRight") {
            current_flake_index += 1
        }
        //Q
        else if (e.key == "q" || e.key == "Q") {
            deleteCurrentFlake();
        }

        // clamping the Values
        current_flake_index = Math.min(Math.max(current_flake_index, 0), current_flakes.length - 1);
        current_mag = Math.min(Math.max(current_mag, 1), 5);

        // swap the Image and the heading
        $("#quick_inspect_image").attr("src", `${IMAGE_URL}/${current_flakes[current_flake_index]?.flake_path}/${MAG_DICT[current_mag]}.png`)
        $("#quick_inspect_heading").text(`Current Scan: ${current_scan_data?.scan_id}, current Flake ID: ${current_flakes[current_flake_index]?.flake_id}, current Flake ${current_flake_index + 1} / ${current_flakes.length}`)
    });
    return view_modal
}

function createViewModal(data_dict) {

    var modal_id = `modalview${data_dict.scan_id}`
    var image_directory = `${IMAGE_URL}/${data_dict.scan_exfoliated_material}/${data_dict.scan_name}`

    // creating the Modal
    var view_modal = $('<div>').attr({ role: "dialog", 'id': modal_id, 'tabindex': -1, "aria-modal": true }).addClass("modal fade viewer")
    var modal_dialog = $('<div>').addClass("modal-dialog modal-fullscreen")
    var modal_content = $('<div>').addClass("modal-content")
    var modal_header = $('<div>').addClass("modal-header")
    var modal_body = $('<div>').addClass("modal-body")
    var modal_footer = $('<div>').addClass("modal-footer")

    // buttons for exititng
    var delete_button = $("<button>").attr({ "type": "button", 'data-bs-dismiss': "modal" }).addClass("btn btn-danger").text("Delete").click({ 'id': data_dict.scan_id }, deleteHandler)
    var download_button = $("<button>").attr("type", "button").addClass("btn btn-primary").text("Download as ZIP")
    var dismiss_button = $("<button>").attr({ "type": "button", 'data-bs-dismiss': "modal" }).addClass("btn btn-secondary").text("Close")

    //header design
    var heading = $('<h4>').addClass("modal-title").text(`Viewing Scan ${data_dict.scan_id}`)
    modal_header.append(heading)

    //body design
    var overview = `
        <div class="row bg-faded">
            <div class="col-6 mx-auto text-center">
                <img src="${image_directory}/overview_compressed.jpg" class="img-thumbnail" loading="lazy"> 
            </div>
        </div>
    `

    modal_body.append(overview)

    //footer Design
    modal_footer.append(delete_button)
    modal_footer.append(download_button)
    modal_footer.append(dismiss_button)

    // build the final modal
    modal_content.append(modal_header)
    modal_content.append(modal_body)
    modal_content.append(modal_footer)
    modal_dialog.append(modal_content)
    view_modal.append(modal_dialog)

    return view_modal
}

function createScanTable() {
    // What to add
    // Number Chips, Number Flakes, mono bi tri etc..
    // User, name, Material, time
    var table = $("<table>")
}

function getDataFromServerAndDisplay(filter) {
    // Clear the Table first
    $("#flake_table > tbody").empty();

    // we need to remove all the modals
    $(".viewer").remove()

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

export { getDataFromServerAndDisplay }
