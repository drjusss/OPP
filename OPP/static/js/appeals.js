let filteredAppeals = [];

function filterAppeals() {
    filteredAppeals = structuredClone(appeals);  //глубокая копия (чтобы можно было менять без изменения изначального объекта)

    let filterIsCompleted = document.querySelector('#only-complete').value;
    const filterWorker = document.querySelector('#filter-fixik').value;
    const filterAppealType = document.querySelector('#appeal-type').value;
    const filterAppealDate = document.querySelector('#filter-date-input').value;
    const filterSearch = document.querySelector('#search-field').value.toLowerCase();

    if (filterIsCompleted != 'any') {
        filterIsCompleted = filterIsCompleted == 'true';
        filteredAppeals = filteredAppeals.filter(appeal => appeal.is_completed == filterIsCompleted);
    }
    if (filterWorker != '') {
        filteredAppeals = filteredAppeals.filter(appeal => appeal.worker && appeal.worker.id == Number(filterWorker));
    }
    if (filterAppealType != 'any') {
        filteredAppeals = filteredAppeals.filter(appeal => appeal.type == filterAppealType);
    }
    if (filterAppealDate != '') {
        filteredAppeals = filteredAppeals.filter(appeal => appeal.date_of_group_start == filterAppealDate);
    }
    if (filterSearch != '') {
        filteredAppeals = filteredAppeals.filter(appeal => appeal.message.toLowerCase().includes(filterSearch) ||
                                                           String(appeal.pk).includes(filterSearch) ||
                                                           appeal.skype.toLowerCase().includes(filterSearch) ||
                                                           appeal.name.toLowerCase().includes(filterSearch))
    };
    displayAppeals(filteredAppeals);
}

function filterAppealsToExport() {
    let filterWorkerId = document.querySelector('#filter-fixik').value || null;
    let filterAppealType = document.querySelector('#appeal-type').value || null;
    let isCompleted = document.querySelector('#only-complete').value || null;
    const filterAppealDate = document.querySelector('#filter-date-input').value || null;
    const filterSearch = document.querySelector('#search-field').value.toLowerCase() || null;

    if (filterWorkerId == 'any') {
        filterWorkerId = null;
    }

    if (filterAppealType == 'any') {
        filterAppealType = null;
    }

    if (isCompleted == 'any') {
        isCompleted = null;
    }

    return {
        isCompleted: isCompleted,
        workerId: filterWorkerId,
        appealType: filterAppealType,
        appealDate: filterAppealDate,
        search: filterSearch,
    }
}


function addFilterHandler() {
    const onlyCompleted = document.querySelector('#only-complete');
    const fixik = document.querySelector('#filter-fixik');
    const appealType = document.querySelector('#appeal-type');
    const filterDate = document.querySelector('#filter-date-input');
    const searchField = document.querySelector('#search-field');

    onlyCompleted.addEventListener('change', filterAppeals);
    fixik.addEventListener('change', filterAppeals);
    appealType.addEventListener('change', filterAppeals);
    filterDate.addEventListener('change', filterAppeals);
    searchField.addEventListener('input', filterAppeals);
}

function displayAppeals(appealsData) {
    const appealList = document.querySelector('#appeal-list');
    appealList.innerHTML = ''

    for (const appealData of appealsData) {
        const appealCard = document.createElement('div');  //создаем тег div
        appealCard.classList.add('border-2')
        appealCard.classList.add('appeal-card')
        appealCard.classList.add('border-solid')
        appealCard.classList.add('dark:bg-gray-900')
        appealCard.classList.add('dark:border-gray-500')
        appealCard.classList.add('px-6')
        appealCard.classList.add('py-4')
        appealCard.classList.add('rounded-2xl')

        let worker;
        if (appealData.worker) {
            worker = appealData.worker.name;
        } else {
            worker = '';
        }

        let soundIsOk;
        if (appealData.sound_is_ok == null) {
            soundIsOk = '-';
        } else if (appealData.sound_is_ok == false) {
            soundIsOk = 'Не ОК';
        } else {
            soundIsOk = 'OK'
        }

        let camera;
        if (appealData.camera == null) {
            camera = '-';
        } else if (appealData.camera == false) {
            camera = 'Не ОК';
        } else {
            camera = 'OK'
        }

        let appealStatus;
        if (appealData.is_completed) {
            appealStatus = 'completed';
        } else if (worker) {
            appealStatus = 'in progress';
        } else {
            appealStatus = 'not completed';
        }

        appealCard.innerHTML = appealCardHtmlTemplate.replace('{{ appeal_id }}', appealData.pk)
                                                     .replace('{{ worker_id }}', worker)
                                                     .replace('{{ name }}', appealData.name)
                                                     .replace('{{ skype }}', appealData.skype)
                                                     .replace('{{ headset }}', appealData.headset || '-')
                                                     .replace('{{ sound_is_ok }}', soundIsOk)
                                                     .replace('{{ date_of_group_start }}', appealData.date_of_group_start || '-')
                                                     .replace('{{ camera }}', camera)
                                                     .replace('{{ speed_test }}', appealData.speed_test || '-')
                                                     .replace('{{ message }}', appealData.message)
                                                     .replace('{{ is_completed }}', appealCompletionIcons[appealStatus]);
        appealList.append(appealCard);
    }
    addOpenAppealCardHandler()
}

function validateUpdateAppealData(headsetInput, soundIsOkInput, dateOfGroupStartInput, workerIdInput, cameraInput, isCompletedCheckBox, appealTypeSelect, timeToCompleteInput, connectionTypeInput) {
    if (isCompletedCheckBox.checked) {
        if (!headsetInput.value) {
            headsetInput.setCustomValidity('Поле гарнитуры должно быть заполнено до закрытия обращения.');
            headsetInput.reportValidity();
            return false
        }
        if (!soundIsOkInput.value) {
            soundIsOkInput.setCustomValidity('Поле звука должно быть заполнено до закрытия обращения.');
            soundIsOkInput.reportValidity();
            return false
        }
        if (!dateOfGroupStartInput.value) {
            dateOfGroupStartInput.setCustomValidity('Поле даты должно быть заполнено до закрытия обращения.');
            dateOfGroupStartInput.reportValidity();
            return false
        }
        if (!workerIdInput.value) {
            workerIdInput.setCustomValidity('Поле инженера должно быть заполнено до закрытия обращения.');
            workerIdInput.reportValidity();
            return false
        }
        if (!cameraInput.value) {
            cameraInput.setCustomValidity('Поле камеры должно быть заполнено до закрытия обращения.');
            cameraInput.reportValidity();
            return false
        }
        if (!appealTypeSelect.value) {
            appealTypeSelect.setCustomValidity('Поле типа обращения должно быть заполнено до закрытия обращения.');
            appealTypeSelect.reportValidity();
            return false
        }
        if (!timeToCompleteInput.value) {
            timeToCompleteInput.setCustomValidity('Поле время выполнения должно быть заполнено до закрытия обращения');
            timeToCompleteInput.reportValidity();
            return false
        }
        if (!connectionTypeInput.value) {
            connectionTypeInput.setCustomValidity('Поле типа подключения должно быть заполнено до закрытия обращения');
            connectionTypeInput.reportValidity();
            return false
        }
    }

//    if (!['1', '2', '3'].includes(workerIdInput.value)) {
//    let searchedFixiksById = fixiks.filter(fixik => workerIdInput.value == fixik.id);
//    if (searchedFixiksById.length == 0) {

    if (workerIdInput.value == null) {
        workerIdInput.setCustomValidity('Поле инженера - обязательное.')
        workerIdInput.reportValidity();
        return false
    }

    if (!fixiks.find(fixik => workerIdInput.value == fixik.id)) {
        workerIdInput.setCustomValidity('Поле инженера заполнено неверно');
        workerIdInput.reportValidity();
        return false
    }

    if (headsetInput.value != '' && !['USB', '3.5', 'USB/3.5', '3.5/USB'].includes(headsetInput.value)) {
        headsetInput.setCustomValidity('Поле гарнитуры заполнено неверно.');
        headsetInput.reportValidity();
        return false
    }

    if (soundIsOkInput.value != '' && !['true', 'false'].includes(soundIsOkInput.value)) {
        soundIsOkInput.setCustomValidity('Поле звука заполнено неверно.');
        soundIsOkInput.reportValidity();
        return false
    }

    if (dateOfGroupStartInput.value != '' && !isDateWithinOneYear(dateOfGroupStartInput.value)) {
        dateOfGroupStartInput.setCustomValidity('Дата старта группы, должна быть в диапазоне +- год от текущей.')
        dateOfGroupStartInput.reportValidity();
        return false
    }

    if (cameraInput.value != '' && !['true', 'false'].includes(cameraInput.value)) {
        cameraInput.setCustomValidity('Поле камеры заполнено неверно.');
        cameraInput.reportValidity();
        return false
    }

    if (appealTypeSelect.value != '' && !['check', 'incident'].includes(appealTypeSelect.value)) {
        appealTypeSelect.setCustomValidity('Поле типа обращения заполнено неверно.');
        appealTypeSelect.reportValidity();
        return false
    }

    if (connectionTypeInput.value != '' && !['wi-fi', 'cable'].includes(connectionTypeInput.value)) {
        connectionTypeInput.setCustomValidity('Поле типа подключения заполнено неверно.')
        connectionTypeInput.reportValidity();
        return false
    }


    return true
}

function addSaveButtonHandler() {
    const saveButton = document.querySelector('#save-button');
    const startDate = document.querySelector('#start-date').value;
    const endDate = document.querySelector('#end-date').value;

    saveButton.addEventListener('click', () => {
        const dataToUpdate = getValuesToUpdateAppeal()
        if (!dataToUpdate) {return}
        const appealPk = document.querySelector('#appeal-card-id').textContent

        sendRequestToUpdateAppeal(
            () => {
                hideModalWindow();
                sendRequestToGetAppeals(filterAppeals, startDate, endDate);
            },
            () => {alert('Не сработало')},
            appealPk, dataToUpdate,
        )
    })
}

function addHideModalWindowHandler() {
    const hideButton = document.querySelector('#not-save-button');
    hideButton.addEventListener('click', hideModalWindow);
}

function addSpamModalWindowHandler() {
    const isSpamButton = document.querySelector('#is-spam-button');
    isSpamButton.addEventListener('click', openConfirmationWindowToSpamAppeal)
}

function hideModalWindow() {
    const modalWindow = document.querySelector('#modal-window');
    modalWindow.remove()
    document.body.classList.remove('overflow-hidden');
}

function hideSpamModalWindow() {
    const spamModalWindow = document.querySelector('#spam-modal-window');
    spamModalWindow.classList.add('hidden')
}

function addOpenAppealCardHandler() {
    const appeals = document.querySelectorAll('.appeal-card')
    for (const appeal of appeals) {
        appeal.addEventListener('click', openAppealCard);
    };
}

function openAppealCard(event) {
    const appealCard = event.target.closest('.appeal-card')  //поиск среди родительских тегов
    const appealID = appealCard.querySelector('.appeal-id').textContent

    const appealData = appeals.find(appeal => appeal.pk == appealID)  //метод поиска

    const modalWindow = document.createElement('div');
    modalWindow.id = 'modal-window';

    modalWindow.innerHTML = appealDetailWindowHTMLTemplate.replace('{{ appeal_id }}', appealData.pk)
                                                          .replace('{{ student_name }}', appealData.name)
                                                          .replace('{{ skype }}', appealData.skype)
                                                          .replace('{{ message }}', appealData.message);

    document.querySelector('#appeals-main-container').append(modalWindow);

    modalWindow.querySelector('#appeal-card-date-of-start').value = appealData.date_of_group_start;
    modalWindow.querySelector('#appeal-card-speed-test').value = appealData.speed_test;
    modalWindow.querySelector('#appeal-card-speed-test-comment').value = appealData.speed_test_note;
    modalWindow.querySelector('#appeal-card-student-comment').value = appealData.student_note;
    modalWindow.querySelector('#appeal-card-is-complete').checked = appealData.is_completed;
    modalWindow.querySelector('#appeal-card-camera').value = appealData.camera;
    modalWindow.querySelector('#appeal-card-sound-is-ok').value = appealData.sound_is_ok;
    modalWindow.querySelector('#appeal-card-headset').value = appealData.headset;
    modalWindow.querySelector('#appeal-card-type').value = appealData.type;
    modalWindow.querySelector('#appeal-card-time-to-complete').value = appealData.time_to_complete;
    modalWindow.querySelector('#appeal-card-type-of-connection').value = appealData.type_of_connection;

    const appealCardFixikChoiceSelect = modalWindow.querySelector('#appeal-card-fixik-choice');
    appealCardFixikChoiceSelect.innerHTML = ''

    for (const fixik of fixiks) {
        const option = document.createElement('option');
        option.value = fixik.id;
        option.textContent = fixik.name;
        appealCardFixikChoiceSelect.append(option);
    }

    if (appealData.worker) {
        appealCardFixikChoiceSelect.value = appealData.worker.id;
    } else {
        appealCardFixikChoiceSelect.value = null;
    }

    document.body.classList.add('overflow-hidden');  // Убирает скрол body
    addHideModalWindowHandler()
    addSpamModalWindowHandler()
    addSaveButtonHandler()
    addMessageInputHandler('#appeal-card-speed-test-comment')
    addMessageInputHandler('#appeal-card-student-comment')
}

function autoFillFixiksSelect() {
    const filterFixikChoiceSelect = document.querySelector('#filter-fixik');

    filterFixikChoiceSelect.innerHTML = ''

    const option = document.createElement('option')
    option.value = ''
    option.textContent = 'Любой'
    filterFixikChoiceSelect.append(option)

    for (const fixik of fixiks) {
        const option = document.createElement('option');
        option.value = fixik.id;
        option.textContent = fixik.name;
        filterFixikChoiceSelect.append(option);
    }
}

function openConfirmationWindowToSpamAppeal() {
    const spamModalWindow = document.querySelector('#spam-modal-window');
    spamModalWindow.classList.remove('hidden');
}

function addSpamModalWindowButtonsHandler() {
    const confirmSpamButton = document.querySelector('#spam-modal-button')
    const declineSpamButton = document.querySelector('#close-spam-modal-button')

    confirmSpamButton.addEventListener('click', confirmSpamButtonHandler)
    declineSpamButton.addEventListener('click', hideSpamModalWindow)
}

function confirmSpamButtonHandler() {
    const appealID = document.querySelector('#appeal-card-id').textContent;
    sendRequestToDeleteAppeal(appealID, confirmSpamButtonSuccessfulHandler)
}

function confirmSpamButtonSuccessfulHandler() {
    const startDate = document.querySelector('#start-date').value;
    const endDate = document.querySelector('#end-date').value;

    hideSpamModalWindow()
    hideModalWindow()
    sendRequestToGetAppeals(filterAppeals, startDate, endDate)
}

function getValuesToUpdateAppeal() {
    const headsetInput = document.querySelector('#appeal-card-headset')
    const soundIsOkInput = document.querySelector('#appeal-card-sound-is-ok')
    const dateOfGroupStartInput = document.querySelector('#appeal-card-date-of-start')
    const workerIdInput = document.querySelector('#appeal-card-fixik-choice')
    const cameraInput = document.querySelector('#appeal-card-camera')
    const isCompletedCheckBox = document.querySelector('#appeal-card-is-complete')
    const appealTypeSelect = document.querySelector('#appeal-card-type')
    const timeToCompleteInput = document.querySelector('#appeal-card-time-to-complete')
    const connectionTypeInput = document.querySelector('#appeal-card-type-of-connection')
    const speedTestInput = document.querySelector('#appeal-card-speed-test')
    const speedTestCommentInput = document.querySelector('#appeal-card-speed-test-comment')
    const studentCommentInput = document.querySelector('#appeal-card-student-comment')

    if (!validateUpdateAppealData(headsetInput, soundIsOkInput, dateOfGroupStartInput, workerIdInput, cameraInput, isCompletedCheckBox, appealTypeSelect, timeToCompleteInput, connectionTypeInput)) {
        return
    }

    let soundIsOk;
    if (soundIsOkInput.value == 'true') {
        soundIsOk = true
    } else if (soundIsOkInput.value == 'false') {
        soundIsOk = false
    } else {
        soundIsOk = null
    }

    let camera;
    if (cameraInput.value == 'true') {
        camera = true
    } else if (cameraInput.value == 'false') {
        camera = false
    } else {
        camera = null
    }

    const headset = headsetInput.value || null;
    const dateOfGroupStart = convertDateFormat(dateOfGroupStartInput.value) || null;
    const workerId = Number(workerIdInput.value);
    const toComplete = isCompletedCheckBox.checked;
    const appealType = appealTypeSelect.value;
    const connectionType = connectionTypeInput.value;
    const timeToComplete = timeToCompleteInput.value;
    const speedTest = speedTestInput.value;
    const speedTestComment = speedTestCommentInput.value;
    const studentComment = studentCommentInput.value;

    return {
        headset: headset,
        soundIsOk: soundIsOk,
        dateOfGroupStart: dateOfGroupStart,
        workerId: workerId,
        toComplete: toComplete,
        camera: camera,
        appealType: appealType,
        connectionType: connectionType,
        timeToComplete: timeToComplete,
        speedTest: speedTest,
        speedTestComment: speedTestComment,
        studentComment: studentComment,

    }
}

function addExportButtonHandler() {
    const exportButton = document.querySelector('#export-button')
    exportButton.addEventListener('click', () => {
        sendRequestToExportAppeals(filterAppealsToExport())
    })
}

function getPersonalData() {
    sendRequestToGetPersonalData((data) => {
        const engineerName = document.querySelector('#engineer-name');
        engineerName.textContent = data.name;
    })
}


addFilterHandler()
autoFillDateInputs()
addDateFilterHandler(filterAppeals)
addOpenAppealCardHandler()
addSpamModalWindowButtonsHandler()
addExportButtonHandler()

sendRequestToGetFixiks(autoFillFixiksSelect)
initRequestToGetAppeals(filterAppeals)
getPersonalData()




//setTimeout(filterAppeals, 2000)  // установить таймер для обработки функции, в милисекундах

// TODO убрать повторяющиеся функции в utils
// TODO
