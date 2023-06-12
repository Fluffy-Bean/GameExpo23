function addFlashMessage(message, type='success') {
    let flask = document.createElement('p');
    flask.onclick = () => flask.remove();
    flask.classList.add(type);
    flask.innerHTML = message;

    let close = document.createElement('span');
    close.innerHTML = '<i class="ph-bold ph-x"></i>';

    flask.appendChild(close);
    document.querySelector('.flash').appendChild(flask);
}

function yeetSession(id) {
    let form = new FormData();
    form.append('session_id', id);

    fetch('/api/tokens', {
        method: 'POST',
        body: form,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addFlashMessage(data.success, 'success');
            document.querySelector(`#sess-${id}`).remove();
        } else {
            addFlashMessage(data.error, 'error');
        }
    })
    .catch(error => addFlashMessage(error.error, 'error'));
}
