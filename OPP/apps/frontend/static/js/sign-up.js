function addClickButtonHandler() {
    const button = document.querySelector('#sign-in-button');
    const valuesToSignUp = getValuesToSignUp()
    if (!valuesToSignUp) {
        return
    }

    button.addEventListener('click', () => {
        sendRequestToSignUp(
            () => {
                alert('Вы успешно зарегистрировались.');
                window.location.href = domain;
            },
            () => {alert(`${data.error}: ${data.detail}`)},
            valuesToSignUp
        )
    })
}

function getValuesToSignUp() {
    const userName = document.querySelector('#user-name').value;
    const password = document.querySelector('#password').value;
    const passwordConfirmation = document.querySelector('#password-confirmation').value;

    return {
        userName: userName,
        password: password,
        passwordConfirmation: passwordConfirmation,
    }
}

function formSubmitHandler(event) {
    event.preventDefault();
    const dataIsValid = validateSignUp();

    if (!dataIsValid) {
        return
    };

    const valuesToSignUp = getValuesToSignUp()
    if (!valuesToSignUp) {
        return
    }

    sendRequestToSignUp(
        () => {
            alert('Вы успешно зарегистрировались.');
            window.location.href = domain;
        },
        () => {alert(`${data.error}: ${data.detail}`)},
        valuesToSignUp
    );
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