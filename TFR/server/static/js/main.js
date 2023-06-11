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

function ajax(url, form, callback, method='POST') {
    console.log(form)
    fetch(url, {
        method: method,
        body: form,
    })
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => addFlashMessage(error.error, 'error'));
}

function deleteToken(id) {
    let form = new FormData();
    form.append('token_id', id);

    ajax('/api/tokens', form, (data) => {
        if (data.success) {
            addFlashMessage(data.success, 'success');
            document.querySelector(`#token-${id}`).remove();
        } else {
            addFlashMessage(data.error, 'error');
        }
    }, 'DELETE');
}

function addToken() {
    ajax('/api/tokens', null, (data) => {
        if (data.success) {
            window.location.reload();
        } else {
            addFlashMessage(data.error, 'error');
        }
    });
}

function viewToken(id) {
    let token = document.querySelector(`#token-${id}`);
    let hidden = token.children[2];

    hidden.classList.toggle('hidden');
}
