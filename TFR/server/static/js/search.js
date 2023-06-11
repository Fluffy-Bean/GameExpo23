function showHint() {
    let search = document.querySelector('.search > input');
    let searchPos = search.getBoundingClientRect();
    let hint = document.querySelector('.search-hint');

    hint.style.width = search.offsetWidth + 'px';
    hint.style.left = searchPos.left + 'px';
    hint.style.top = searchPos.bottom + 'px';

    hint.style.display = 'flex';
}


function hideHint() {
    let hint = document.querySelector('.search-hint');
    hint.style.display = 'none';
}


function updateHint() {
    let search = document.querySelector('.search > input');
    let searchPos = search.getBoundingClientRect();
    let hint = document.querySelector('.search-hint');

    hint.style.width = search.offsetWidth + 'px';
    hint.style.left = searchPos.left + 'px';
    hint.style.top = searchPos.bottom + 'px';
}


function getSearch() {
    let search = document.querySelector('.search > input').value;
    let hint = document.querySelector('.search-hint');

    if (search.length === 0) {
        hint.innerHTML = '<p>Start typing to see results...</p>';
        return;
    }

    fetch('/api/users?search=' + search.toString(), {
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
            let el = document.createElement('button');
            el.innerHTML = user;
            el.onmousedown = function (event) {
                event.preventDefault();
                search = document.querySelector('.search > input');
                search.value = user.toString();
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
    let search = document.querySelector('.search > input');

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
