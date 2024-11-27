function sendRequestToSignOut() {
    fetch(`${domain}/api/auth/sign-out/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        alert('Вы успешно вышли из системы.');
        window.location.href = loginUrl  // redirect который не заменяет и по которому можно вернуться на предыдущую страницу
    })
    .catch(error => {
        console.error(error.stack);
    })
}

function addClickButtonHandler() {
    const button = document.querySelector('#sign-out-button');
    button.addEventListener('click', sendRequestToSignOut);
}

addClickButtonHandler()


