function addClickButtonHandler() {
    const button = document.querySelector('#sign-out-button');
    button.addEventListener('click', () => {
        sendRequestToSignOut(() => {
            window.location.href = loginUrl // redirect который не заменяет и по которому можно вернуться на предыдущую страницу
        })
    })
}

addClickButtonHandler()

