function sendRequestToSignIn() {
    const userName = document.querySelector('#user-name').value;
    const password = document.querySelector('#password').value;
    const errorMessage = document.querySelector('p');
    errorMessage.textContent = '';

    const options = {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')  // Обязательно необходимо отправлять csrftoken, если бэк на джанго.
        },
        body: JSON.stringify({
            username: userName,
            password: password,
        })
    };

    fetch(`${domain}/api/auth/sign-in/`, options)
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.result == 'Invalid credentials.') {
            errorMessage.textContent = 'Логин и пароль неверные.'
            showErrorLog()

        } else if (data.result == 'Successfully sign in.') {
            alert('Вы вошли в систему.');
            window.location.href = `${domain}/appeals`;
        }
    })
    .catch(error => {
        console.error(error.stack);

    })
}

function addClickButtonHandler() {
    const button = document.querySelector('#sign-in-button');
    button.addEventListener('click', sendRequestToSignIn);
}

function formSubmitHandler(event) {
    event.preventDefault();
    const dataIsValid = validateSignIn();
    if (!dataIsValid) {
        return
    };

    sendRequestToSignIn();
}

function addFormSubmitHandler() {
    const form = document.querySelector('form');
    form.addEventListener('submit', formSubmitHandler);
}

function validateSignIn() {
    const userNameInput = document.querySelector('#user-name');
    const passwordInput = document.querySelector('#password');
    const errorMessage = document.querySelector('p');
    errorMessage.textContent = '';

    if (userNameInput.value.length < 5 || passwordInput.value.length < 5) {
        errorMessage.textContent = 'Логин и пароль неверные.';
        userNameInput.focus();
        showErrorLog();
        return false
    };

    return true;
}

function showErrorLog() {
    const logInError = document.querySelector('#log-in-error');
    logInError.classList.remove('hidden');
}

function hideErrorLog() {
    const logInError = document.querySelector('#log-in-error');
    logInError.classList.add('hidden');
}

function addInputHandler() {
    const userNameInput = document.querySelector('#user-name');
    const passwordInput = document.querySelector('#password');

    userNameInput.addEventListener('input', hideErrorLog);
    passwordInput.addEventListener('input', hideErrorLog);
}

addFormSubmitHandler()
addShowPasswordHandler()
addHidePasswordHandler()
addInputHandler()

//addClickButtonHandler()
