function deleteHandler(event) {
    var flake_id = event.data.id
    if (confirm(`Do you wish to delete flake ${flake_id}?`)) {
        $.ajax({
            url: `http://127.0.0.1:5000/flakes?id=${flake_id}`,
            type: 'DELETE',
            success: function (result) {
                console.log(flake_id)
                console.log(result)
            }
        });
    }
}

function createTabelRow(data_dict) {
    //modalID
    var modal_id = `modalview${data_dict.id}`

    // create an empth row to populate later
    var row = $('<tr>').attr('id', data_dict.id);

    // create each cell
    var index_cell = $("<td>").text(data_dict.id).css("font-weight", "bold")
    var material_cell = $("<td>").text(data_dict.material)
    var thickness_cell = $("<td>").text(data_dict.thickness)
    var size_cell = $("<td>").text(data_dict.size)
    var used_cell = $("<td>").text(data_dict.used)

    // this is for the Buttons
    var button_cell = $('<td>')
    var button_div = $('<div>').css("text-align", "center")
    var view_button = $('<a>').attr("data-toggle", "modal").attr("data-target", `#${modal_id}`).addClass("btn btn-primary btn-xs").text("View")
    //var toggle_button = $('<a>').addClass("btn btn-warning btn-xs").text("Toggle used")
    var delete_button = $('<a>').addClass("btn btn-danger btn-xs").text("Delete").click({ 'id': data_dict.id }, deleteHandler)

    //append the buttons to the button cell
    //button_div.append(toggle_button)
    button_div.append(view_button)
    button_div.append(delete_button)

    button_cell.append(button_div)
    //finally populate the row
    row.append(index_cell)
    row.append(material_cell)
    row.append(thickness_cell)
    row.append(size_cell)
    row.append(used_cell)
    row.append(button_cell)

    return row
}

function createModal(data_dict) {

    var modal_id = `modalview${data_dict.id}`

    // creating the Modal
    var view_modal = $('<div>').attr({ role: "dialog", 'id': modal_id }).addClass("modal fade")
    var modal_dialog = $('<div>').addClass("modal-dialog")
    var modal_content = $('<div>').addClass("modal-content")
    var modal_header = $('<div>').addClass("modal-header")
    var modal_body = $('<div>').addClass("modal-body")
    var modal_footer = $('<div>').addClass("modal-footer")

    //header design
    var heading = $('<h4>').addClass("modal-title").text("View Flake")
    modal_header.append(heading)


    //body design
    var overview = `
        <div class="row bg-faded">
            <div class="col-6 mx-auto text-center">
                <img src="assets/overview.jpg" class="img-thumbnail" > <!-- center this image within the column -->
            </div>
        </div>
    `
    var gallery = `
    <div class="row">
        <div class="col">    
            <img src="assets/5.jpg" class="img-thumbnail" >
            <img src="assets/20.jpg" class="img-thumbnail" >
        </div>
        <div class="col">
            <img src="assets/50.jpg" class="img-thumbnail" >
            <img src="assets/100.jpg" class="img-thumbnail" >
        </div>
    </div>`

    modal_body.append(overview)
    modal_body.append(gallery)

    //footer design
    var download_button = $("<button>").attr("type", "button").addClass("btn btn-primary pull-left").text("Download as ZIP")
    var dismiss_button = $("<button>").attr({ "type": "button", 'data-dismiss': "modal" }).addClass("btn btn-secondary").text("Close")
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

export { createModal, createTabelRow }
