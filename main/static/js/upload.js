(function ($) {
    function handleUpload(modalId, buttonText, formAction, formId, fileId, uploadUrl, csrfToken) {
        const formUploadDataHTML = `<form id="${formId}" enctype="multipart/form-data" action="${formAction}">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            <input type="file" name="file" id="${fileId}">
            <button type="button" class="btn btn-outline-info btn-block mt-3" id="upload-button">${buttonText}</button>
            <div id="upload-message" style="margin-top: 10px;"></div>
        </form>`

        document.addEventListener('DOMContentLoaded', function () {
            let uploadModal = document.getElementById(modalId);

            uploadModal.addEventListener('click', function () {
                showModal(buttonText, formUploadDataHTML, { 'data': { 'lookup': null } });

                let form = document.getElementById(formId);
                let fileInput = document.getElementById(fileId);
                let uploadButton = document.getElementById('upload-button');
                let uploadMessage = document.getElementById('upload-message');

                uploadButton.addEventListener('click', function () {
                    console.log('upload data');
                    uploadMessage.innerText = 'Uploading file...';
                    uploadMessage.style.color = '#000';

                    let formData = new FormData(form);

                    fetch(uploadUrl, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken
                        },
                        body: formData
                    })
                        .then(function (response) {
                            if (response.ok) {
                                // Success message
                                console.log('File uploaded successfully.');
                                uploadMessage.innerText = 'File uploaded successfully.';
                                uploadMessage.style.color = 'green';
                                // Clear file input
                                fileInput.value = '';
                            } else {
                                // Error message
                                console.log('File upload failed.');
                                uploadMessage.innerText = 'File upload failed.';
                                uploadMessage.style.color = 'red';
                            }
                        })
                        .catch(function (error) {
                            // Error message
                            console.log('File upload failed:', error);
                            uploadMessage.innerText = 'File upload failed: ' + error;
                            uploadMessage.style.color = 'red';
                        });
                });
            });
        });
    }

    window.handleUpload = handleUpload;
})(jQuery);
