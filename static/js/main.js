document.addEventListener('DOMContentLoaded', function() {

    const space_id = document.querySelector('#space_id').innerHTML;
    const link_form = document.querySelector('#link_form');

    // Show and hide rename paper form
    const header = document.querySelector('#header');
    const header_text = document.querySelector('#header-text');
    const edit_symbol = document.querySelector('#edit-title-symbol');

    header.addEventListener('mouseenter', () => {
        edit_symbol.addEventListener('click', () => {
            header_text.innerHTML = document.querySelector('#rename-space-form-div').innerHTML;
        });
        edit_symbol.style.display = 'inline-block';
    });
    header.addEventListener('mouseleave', () => edit_symbol.style.display = 'none');




    link_form.addEventListener('submit', event => {
        event.preventDefault();
        add_link(link_form, space_id);
      });
    
});

function load_and_show_source_space(source_id) {

    // Source-space view url
    const url = `/source_space/${source_id}`;

    // Send request to source-space view
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(function(response) {
        // When the page is loaded convert it to text
        return response.text()
    })
    .then(function(html) {
        // Initialize the DOM parser
        let parser = new DOMParser();

        // Parse the text
        const source_space_page = parser.parseFromString(html, "text/html");

        // Get empty div for pasting
        const source_space_div = document.querySelector(`#source-space-div-${source_id}`);

        // Past source space header
        const source_space_header = source_space_page.querySelector('#source-space-header');
        document.querySelector(`#source-space-label-${source_id}`).innerHTML = source_space_header.innerHTML;

        // Past source space body
        source_space_div.innerHTML = source_space_page.querySelector('#source-space-div').innerHTML;
        
        // Set validation for source-edit-forms
        const edit_forms = document.getElementsByClassName('edit-form');
        Array.from(edit_forms).forEach(form => {
            form.addEventListener('change', function() {
                form.classList.add('was-changed')
            })
        })
    })
}

async function submit_source_forms(source_id) {

    // Get all changed forms
    const forms = document.getElementsByClassName('was-changed');

    if (!forms.length) {
        // In case no form was changed
        return;
    }
    for await (const form of forms) {
        if (form.id === `alter-source-form-${source_id }`) {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source main info
                if (!await alter_source_info(form, source_id)) {
                    // Error case
                    return show_form_error_message();
                }
            }
        }
        else if (form.id === `add-link-form-${source_id}`) {
            // Set form validation
            if (!form.checkValidity()) {
                form.classList.add('was-validated')
                return;
            }
            else {
                // Update source link
                if (!await add_link_to_source(form, source_id)) {
                    // Error case
                    return show_form_error_message();
                }
            }
        }
        else if (form.id === `upload-file-form-${source_id}`) {
            // Save new source file
            if (!await upload_source_file(form, source_id)) {
                // Error case
                return show_form_error_message();
            }
        }
    }
    // Update source space in case of success
    load_and_show_source_space(source_id);
    document.querySelector(`#close-source-settings-button-${source_id}`).click();
}

async function alter_source_info(form, source_id) {

    // Alter-source-info view url
    const url = `/alter_source_info/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
        }
    })
}

async function add_link_to_source(form, source_id) {

    // Add-link-to-source view url
    const url = `/add_link_to_source/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
        }
    });
}

async function upload_source_file(form, source_id) {

    // Add-link-to-source view url
    const url = `/upload_source_file/${source_id}`;

    // Send POST request
    return fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            return true;
        }
        else {
            return false;
        }
    });
}

function show_or_hide_source_settings(source_id) {

    const source_div = document.querySelector(`#source-space-${source_id}`);
    const source_settings_div = document.querySelector(`#source-settings-${source_id}`);

    // Get all buttons
    const btn_close_button = document.querySelector(`#btn-close-${source_id}`);
    const close_modal_button = document.querySelector(`#close-source-modal-button-${source_id}`);
    const edit_button = document.querySelector(`#show-source-settings-button-${source_id}`);
    const close_settings_button = document.querySelector(`#close-source-settings-button-${source_id}`);
    const delete_button = document.querySelector(`#delete-source-button-${source_id}`);
    const link_button = document.querySelector(`#source-link-button-${source_id}`);
    const open_file_button = document.querySelector(`#open-source-file-button-${source_id}`);
    const expand_button = document.querySelector(`#expand-button-${source_id}`);

    // Open source settings
    if (source_settings_div.style.display === 'none') {
        source_div.style.display = 'none';
        source_settings_div.style.display = 'block';

        // Change all buttons
        edit_button.style.display = 'none';
        close_modal_button.style.display = 'none';
        btn_close_button.style.display = 'none';
        expand_button.style.display = 'none';
        close_settings_button.style.display = 'inline-block';
        delete_button.style.display = 'inline-block';

        if (open_file_button) {
            open_file_button.style.display = 'none';
        }

        if (link_button) {
            link_button.style.display = 'none';
        }        
    }
    // Close source settings
    else {
        source_settings_div.style.display = 'none';
        source_div.style.display = 'block';

        // Change all buttons
        close_settings_button.style.display = 'none';
        delete_button.innerHTML = 'Delete source';
        delete_button.style.display = 'none';
        edit_button.style.display = 'inline-block';
        close_modal_button.style.display = 'inline-block';
        expand_button.style.display = 'inline-block';
        btn_close_button.style.display = 'block';

        if (open_file_button) {
            open_file_button.style.display = 'inline-block';
        }

        if (link_button) {
            link_button.style.display = 'inline-block';
        }
    }
}

function delete_source(source_id) {

    // Get delete button and ask user for conformation
    const delete_button = document.querySelector(`#delete-source-button-${source_id}`);
    delete_button.innerHTML = "Are you sure?";

    delete_button.addEventListener('click', () => {

        // Rename-space url
        const url = `/delete_source/${source_id}`;

        // Send POST request
        fetch(url)
        .then(response => handleErrors(response, url))
        .then(response => response.json())
        .then(result => {
            if (result.status === 'ok') {

                // TODO
                // redirect somewhere?
            }
        });
    })
}

function show_form_error_message() {
    document.querySelector('.form-error-message').style.display = 'block';
}

function invite_to_work_space(space_id) {

    // Get invitation code and link
    const answer = get_invitation_code(space_id);
    const invitation_code = answer.invitation_code;
    const invitation_link = answer.invitation_link;

    // Render results on page
    // TODO

}

function share_space_sources(space_id) {

    // Get sharing code and link
    const answer = get_share_space_source_code(space_id);
    const sources_code = answer.share_sources_code;
    const sources_link = answer.share_sources_link;

    // Render results on page

}



function get_invitation_code(space_id) {

    // Invitation API route
    const url = `/invite_to_space/${space_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        // Return new link to invitation page
        return result;
    });
}

function get_share_space_source_code(space_id) {

    // Invitation API route
    const url = `/share_sources/${space_id}`;

    // Send request
    fetch(url)
    .then(response => handleErrors(response, url))
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            // Return new link to invitation page
            return result;
        }
        else {
            // Error case (empty workspace)
            return false;
        }
    });
}

function add_link(form, space_id) {

    // Add-link view url
    const url = `/add_link_to_space/${space_id}`;

    // Send POST request
    fetch(url, {
        method: 'POST',
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            console.log(result.link_name);
            // TODO!
            // What to do?
        }
        else {
            redirect(result.url)
        }
    });
}

function alter_link(link_id) {

    // Alter-link view url
    const url = `/alter_link/${link_id}`;

    // TODO

}

function delete_link(link_id) {

    // Delete-link view url
    const url = `/delete_link/${link_id}`;

    // Send request to delete_link view
    fetch(url)
    .then(response => response.json())
    .then(result => {
        if (result.status === 'ok') {
            
            document.querySelector(`#link_${link_id}`).remove();
        }
        else {
            console.log("error")
        }
    });
    // TODO: animation!
}

function handleErrors(response, url) {
    if (!response.ok) {
        redirect(url)
    }
    return response;
}

function redirect(url) {
    // Imitate django redirect func
    window.location.replace(url)
}
