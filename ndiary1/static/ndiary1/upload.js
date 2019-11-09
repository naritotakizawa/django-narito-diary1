const insertText = (textarea, text) => {
    const cursorPos      = textarea.selectionStart;
    const last      = textarea.value.length;
    const before   = textarea.value.substr(0, cursorPos);
    const after    = textarea.value.substr(cursorPos, last);
    textarea.value = before + text + after;
};

const upload = (uploadFile, textarea) => {
    const formData = new FormData();
    formData.append('file', uploadFile);
    fetch(textarea.dataset.url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        const extension = response.url.split('.').pop().toLowerCase();
        insertText(textarea, response.url);

    }).catch(error => {
        console.log(error);
    });
};


document.addEventListener('DOMContentLoaded', e => {
    for (const textarea of document.querySelectorAll('textarea.uploadable')) {
        textarea.addEventListener('dragover', e => {
            e.preventDefault();
        });

        textarea.addEventListener('drop', e => {
            e.preventDefault();
            upload(e.dataTransfer.files[0], textarea);
        });
    }
});
