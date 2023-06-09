function addFlashMessage(message, type='success') {
    /**
     * Add a flash message to the page
     *
     * @param {string} message
     * @return {void}
     *
     * @example
     * addFlashMessage('Hello World!', 'success')
     *
     * @example
     * addFlashMessage('Oopsie!', 'error')
     */
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
    /**
     * Send a request to the server and get a response
     * Mostly a wrapper for fetch(), since most of the
     * requests are made with FormData and POST method
     *
     * @param {string} url
     * @param {FormData} form
     * @param {function} callback
     * @param {string} method
     * @return {void}
     *
     * @example
     * ajax('/api', formData, callback = (data) => { console.log(data) }, 'POST')
     */
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
    /**
     * Delete user token
     *
     * @return {void}
     * @{integer} id
     *
     * @example
     * deleteToken(id)
     */
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
    /**
     * Add a new token
     *
     * @return {void}
     *
     * @example
     * addToken()
     */
    ajax('/api/tokens', null, (data) => {
        if (data.success) {
            window.location.reload();
        } else {
            addFlashMessage(data.error, 'error');
        }
    });
}

function viewToken(id) {
    /**
     * View a token
     *
     * @return {void}
     * @{integer} id
     *
     * @example
     * viewToken(id)
     */
    let token = document.querySelector(`#token-${id}`);
    let hidden = token.children[2];

    hidden.classList.toggle('hidden');
}