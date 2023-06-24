function yeetSession(id) {
    const form = new FormData();
    form.append('session', id);

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
