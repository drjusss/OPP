function sendRequestToSignUp() {
    const userName = document.querySelector('#user-name').value;
    const password = document.querySelector('#password').value;
    const passwordConfirmation = document.querySelector('#password-confirmation').value;

    const options = {
        method: 'POST',
        header: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: userName,
            password: password,
            password_confirmation: passwordConfirmation,
        })
    };

    fetch(`${domain}/api/auth/sign-up/`, options)
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.result == 'Successfully sign up.') {
            alert('Вы успешно зарегистрировались.');
            window.location.href = domain;
        } else {
            alert(`${data.error}: ${data.detail}`);
        }
    })
    .catch(error => {
        console.log(error.stack);
    })
}

function addClickButtonHandler() {
    const button = document.querySelector('#sign-in-button');
    button.addEventListener('click', sendRequestToSignUp);
}

function formSubmitHandler(event) {
    event.preventDefault();
    const dataIsValid = validateSignUp();

    if (!dataIsValid) {
        return
    };

    sendRequestToSignUp();
}

function addFormSubmitHandler() {
    const form = document.querySelector('form');
    form.addEventListener('submit', formSubmitHandler)
}


function validateSignUp() {
    const userNameInput = document.querySelector('#user-name');
    const passwordInput = document.querySelector('#password');
    const passwordConfirmationInput = document.querySelector('#password-confirmation');
    const errorMessage = document.querySelector('p');

    if (userNameInput.value.length < 5) {
        errorMessage.textContent = 'Длина логина должна быть больше 4 символов.';
        userNameInput.focus()
        return false
    };

    if (passwordInput.value.length < 5) {
        errorMessage.textContent = 'Длина пароля должна быть больше 4 символов.';
        passwordInput.focus()
        return false
    };

    if (passwordConfirmationInput.value != passwordInput.value) {
        errorMessage.textContent = 'Пароль и подтверждение пароля не совпадают.'
        passwordConfirmationInput.focus()
        return false
    };

    return true;
}

addFormSubmitHandler()
addShowPasswordHandler()
addHidePasswordHandler()