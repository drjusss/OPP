let appeals = [];
let fixiks = [];


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

function sendRequestToGetAppeals(successfulHandler) {
    fetch(`${domain}/api/appeals/`)
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

function sendRequestToUpdateAppeal(successfulHandler, errorHandler, appealPk, data) {
    const {headset, soundIsOk, dateOfGroupStart, workerId, toComplete, camera, appealType} = data;
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
            appeal_type: appealType,
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