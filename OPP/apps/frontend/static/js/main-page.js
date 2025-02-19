function getValuesToCreateAppeal() {
    event.preventDefault()
    const nameInput = document.querySelector('#user-name');
    const skypeInput = document.querySelector('#skype');
    const messageInput = document.querySelector('#appeal-content');

    const name = nameInput.value;
    const skype = skypeInput.value;
    const message = messageInput.value;

    if (!validateAppealContent(nameInput, skypeInput, messageInput)) {
        console.log('Validation Failed')
        return
    }
    return {
        name: name,
        skype: skype,
        message: message,
    }
}

function addSubmitFormHandler() {
    const sendAppealForm = document.querySelector('#send-appeal-form');
    sendAppealForm.addEventListener('submit', () => {
        const dataToCreateAppeal = getValuesToCreateAppeal()

        if (!dataToCreateAppeal) {
            return
        }

        sendRequestToCreateAppeal(
            () => {
                showModalWindow()
                clearInputValues()
            },
            () => {alert('Ошибка валидации')},
            dataToCreateAppeal,
        )
    });
}

function validateAppealContent(nameInput, skypeInput, messageInput) {

    if (nameInput.value.length < 5) {
        nameInput.setCustomValidity('Длина ФИО должна быть не менее 5 символов.')  // кастомизация ошибки
        nameInput.reportValidity()  // отображение ошибки
        return false;
    }

    if (!isCyrillicWithDash(nameInput.value)) {
        nameInput.setCustomValidity('ФИО может состоять только из букв кириллицы(может использоваться дефис).')
        nameInput.reportValidity()
        return False
    }

    if (skypeInput.value.length < 5) {
        skypeInput.setCustomValidity('Длина скайпа должна быть не менее 5 символов.')
        skypeInput.reportValidity()
        return false;
    }

    if (messageInput.value.length < 19) {
        messageInput.setCustomValidity('Напишите вопрос, более информативно.')
        messageInput.reportValidity()
        return false;
    }
    return true
}

function addNameInputHandler() {
    const nameInput = document.querySelector('#user-name')
    nameInput.addEventListener('input', () => {
        nameInput.setCustomValidity('')
    })
}

function addSkypeInputHandler() {
    const skypeInput = document.querySelector('#skype')
    skypeInput.addEventListener('input', () => {
        skypeInput.setCustomValidity('')
    })
}

function addMessageInputHandler() {
    const messageInput = document.querySelector('#appeal-content')
    messageInput.addEventListener('input', () => {
        messageInput.setCustomValidity('')
    })
}

function autoResizeHandler() {
    const appealContentElement = document.querySelector('#appeal-content');
    appealContentElement.style.height = 'auto';
    console.log(`${appealContentElement.scrollHeight}`)
    appealContentElement.style.height = `${appealContentElement.scrollHeight}px`;
}

function autoResize() {
    const appealContentElement = document.querySelector('#appeal-content');
    appealContentElement.addEventListener('input', autoResizeHandler)
}

function addHideModalWindowHandler() {
    const modalButton = document.querySelector('#notification-model-window-close-button');
    modalButton.addEventListener('click', hideModalWindow);
}

function showModalWindow() {
    const modalWindow = document.querySelector('#modal-window');
    modalWindow.classList.remove('hidden');
}

function hideModalWindow() {
    const modalWindow = document.querySelector('#modal-window');
    modalWindow.classList.add('hidden');
}

function clearInputValues() {
    const nameInput = document.querySelector('#user-name')
    const skypeInput = document.querySelector('#skype')
    const messageInput = document.querySelector('#appeal-content')

    nameInput.value = '';
    skypeInput.value = '';
    messageInput.value = '';
}

function addAutoCloseModalWindow() {
    const modalWindow = document.querySelector('#modal-window');
    modalWindow.addEventListener('click', autoCloseModalWindow)
}

function autoCloseModalWindow(event) {
    const modalWindowContent = document.querySelector('#modal-window-content');
    if (!modalWindowContent.contains(event.target)) {
        hideModalWindow();
    }
}

addSubmitFormHandler()
addNameInputHandler()
addSkypeInputHandler()
addMessageInputHandler()
addHideModalWindowHandler()
addAutoCloseModalWindow()
autoResize()

