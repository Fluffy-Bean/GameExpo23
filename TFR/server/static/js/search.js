function showHint() {
    const search = document.querySelector('#search');
    const searchPos = search.getBoundingClientRect();
    const hint = document.querySelector('.search-hint');

    hint.style.width = `${search.offsetWidth}px`;
    hint.style.left = `${searchPos.left}px`;
    hint.style.top = `${searchPos.bottom}px`;

    hint.style.display = 'flex';
}


function hideHint() {
    const hint = document.querySelector('.search-hint');
    hint.style.display = 'none';
}


function updateHint() {
    const search = document.querySelector('#search');
    const searchPos = search.getBoundingClientRect();
    const hint = document.querySelector('.search-hint');

    hint.style.width = `${search.offsetWidth}px`;
    hint.style.left = `${searchPos.left}px`;
    hint.style.top = `${searchPos.bottom}px`;
}


function getSearch() {
    let search = document.querySelector('#search').value;
    const hint = document.querySelector('.search-hint');

    if (search.length === 0) {
        hint.innerHTML = '<p>Start typing to see results...</p>';
        return;
    }

    fetch(`/api/search?q=${search}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            hint.innerHTML = '<p>No results found...</p>';
            return;
        }

        hint.innerHTML = '';

        data.forEach(user => {
            const el = document.createElement('button');
            el.innerHTML = user;
            el.onmousedown = function (event) {
                event.preventDefault();
                search = user.toString();
                search.blur();
            }
            hint.appendChild(el);
        });
    })
    .catch(() => {
        hint.innerHTML = '<p>Something went wrong...</p>';
    });
}


window.onload = () => {
    let typingTimer;
    const search = document.querySelector('#search');

    if (search === null) {
        return;
    }

    window.addEventListener('resize', updateHint);

    search.addEventListener('focus', showHint);
    search.addEventListener('blur', hideHint);
    search.addEventListener('keydown', () => {
        clearTimeout(typingTimer);
    });
    search.addEventListener('keyup', () => {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(getSearch, 250);
    });
}
