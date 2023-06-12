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
