function addClickButtonHandler() {
    const button = document.querySelector('#sign-out-button');
    button.addEventListener('click', () => {
        sendRequestToSignOut(() => {
            alert('Вы успешно вышли из системы.');
            window.location.href = loginUrl // redirect который не заменяет и по которому можно вернуться на предыдущую страницу
        })
    })
}

addClickButtonHandler()

