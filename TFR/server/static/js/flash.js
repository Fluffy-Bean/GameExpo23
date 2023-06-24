function addFlashMessage(message, type='success') {
    const flask = document.createElement('p');
    flask.onclick = () => flask.remove();
    flask.classList.add(type);
    flask.innerHTML = message;

    const close = document.createElement('span');
    close.innerHTML = '<i class="ph-bold ph-x"></i>';

    flask.appendChild(close);
    document.querySelector('.flash').appendChild(flask);
}
