let appeals = [];
let fixiks = [];


function sendRequestToGetPersonalData(successfulHandler) {
    fetch(`${domain}/api/engineer-personal-data/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        successfulHandler(data)
    })
    .catch(error => {
        console.error(error.stack)
    })
}


function sendRequestToDeleteAppeal(appealID, successfulHandler) {

    const options = {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            command: 'spam',
        })
    }

    fetch(`${domain}/api/appeal/${appealID}/`, options)
    .then(response => {
        return response.json()
    })
    .then(data => {
        successfulHandler()
    })
    .catch(error => {
        console.error(error.stack)
    })
}

function sendRequestToGetFixiks(successfulHandler) {
    fetch(`${domain}/api/fixiks/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        fixiks = data
        successfulHandler()
    })
    .catch(error => {
        console.error(error.stack)
    })
}

function sendRequestToGetAppeals(successfulHandler, startDate, endDate) {

    fetch(`${domain}/api/appeals/?start-date=${startDate}&end-date=${endDate}`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        appeals = data;
        successfulHandler()
    })
    .catch(error => {
        console.error(error.stack)
    })
}

function sendRequestToExportAppeals(filterAppeals) {
    const {isCompleted, workerId, appealType, appealDate, search} = filterAppeals
    let url = `${domain}/api/export/?`

    if (isCompleted) {
        url = `${url}&is-completed=${isCompleted}`
    }
    if (workerId) {
        url = `${url}&worker-id=${workerId}`
    }
    if (appealType) {
        url = `${url}&appeal-type=${appealType}`
    }
    if (appealDate) {
        url = `${url}&appeal-date=${appealDate}`
    }
    if (search) {
        url = `${url}&search=${search}`
    }

    fetch(url)
    .then(response => {
        return response.blob()
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${getVerboseNow()}.csv`
        document.body.append(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
    })
}

function sendRequestToUpdateAppeal(successfulHandler, errorHandler, appealPk, data) {
    const {headset, soundIsOk, dateOfGroupStart, workerId, toComplete, camera, appealType, connectionType, timeToComplete, speedTest, speedTestComment, studentComment} = data;
    const options = {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            headset: headset,
            sound_is_ok: soundIsOk,
            date_of_group_start: dateOfGroupStart,
            worker_id: workerId,
            to_complete: toComplete,
            camera: camera,
            type: appealType,
            connection_type: connectionType,
            time_to_complete: timeToComplete,
            speed_test: speedTest,
            speed_test_note: speedTestComment,
            student_note: studentComment,
        })
    }

    fetch(`${domain}/api/appeal/${appealPk}/`, options)
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.result == 'The appeal was successfully updated.') {
            successfulHandler()
        } else {
            errorHandler()
        }
    })
    .catch(error => {
        console.error(error.stack)
    })
}

// main-page ----------------------------

function sendRequestToCreateAppeal(successfulHandler, errorHandler, data) {
    const {name, skype, message} = data;

    const options = {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            name: name,
            skype: skype,
            message: message,
        })
    };

    //event.target возвращается то, на чем произошло событие

    fetch(`${domain}/api/appeals/`, options)
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.result == 'New appeal successfully has been created!') {
            successfulHandler()
        } else {
            errorHandler()
        }
    })
    .catch(error => {
        console.error(error.stack);
    })
}

// sign-in ----------------------------------

function sendRequestToSignIn(successfulHandler, errorHandler, data) {
    const {userName, password} = data;

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
            errorHandler()
        } else if (data.result == 'Successfully sign in.') {
            successfulHandler()
        }
    })
    .catch(error => {
        console.error(error.stack);

    })
}

// sign-out -----------------------------------

function sendRequestToSignOut(successfulHandler) {
    fetch(`${domain}/api/auth/sign-out/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        successfulHandler()
    })
    .catch(error => {
        console.error(error.stack);
    })
}

// sign-up ------------------------------------

function sendRequestToSignUp(successfulHandler, errorHandler, data) {
    const {userName, password, passwordConfirmation} = data;

    const options = {
        method: 'POST',
        headers: {
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
            successfulHandler()
        } else {
            errorHandler()
        }
    })
    .catch(error => {
        console.log(error.stack);
    })
}

