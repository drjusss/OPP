function displayAppealsToDashboard(appealsData) {
    const appealList = document.querySelector('#appeal-table-body');
    appealList.innerHTML = ''

    for (const appealData of appealsData) {
        const appealRow = document.createElement('tr');
        appealRow.classList.add('bg-white')
        appealRow.classList.add('border-b')
        appealRow.classList.add('border-x-2')
        appealRow.classList.add('dark:bg-gray-800')
        appealRow.classList.add('dark:border-gray-600')
        appealRow.classList.add('hover:bg-gray-50')
        appealRow.classList.add('dark:hover:bg-gray-900')

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

        let connectionType;
        if (appealData.type_of_connection == 'cable') {
            connectionType = 'Кабель'
        } else if (appealData.type_of_connection == 'wi-fi') {
            connectionType = 'wi-fi'
        } else {
            connectionType = '-'
        }

        appealRow.innerHTML = dashboardHTMLTemplate.replace('{{ name }}', appealData.name)
                                                    .replace('{{ skype }}', appealData.skype)
                                                    .replace('{{ headset }}', appealData.headset || '-')
                                                    .replace('{{ type_of_connection }}', connectionType)
                                                    .replace('{{ sound_is_ok }}', soundIsOk)
                                                    .replace('{{ camera }}', camera)
                                                    .replace('{{ speed_test }}', appealData.speed_test || '-')
                                                    .replace('{{ date_of_group_start }}', appealData.date_of_group_start || '-')
                                                    .replace('{{ worker }}', worker)
                                                    .replace('{{ time_to_complete }}', appealData.time_to_complete || '-')
        appealList.append(appealRow);

    }

    if (appealsData.length == 0) {
        const appealRow = document.createElement('tr');
        appealRow.innerHTML = '<td colspan="10" class="text-center px-6 py-3">По выбранному фильтру не найдено ни одного обращения</td>';
        appealList.append(appealRow);
    }

    const tableRowElements = appealList.querySelectorAll('tr')
    const lastTableRow = tableRowElements[tableRowElements.length - 1]

    const tableDataElements = lastTableRow.querySelectorAll('td')

    for (const tableDataElement of tableDataElements) {
        tableDataElement.classList.add('border-b-2')
        tableDataElement.classList.add('dark:border-gray-600')
    }

    const firstTableData = tableDataElements[0]
    const lastTableData = tableDataElements[tableDataElements.length - 1]

    firstTableData.classList.add('rounded-bl-lg')
    lastTableData.classList.add('rounded-br-lg')
}

function getPersonalData() {
    sendRequestToGetPersonalData((data) => {
        const engineerName = document.querySelector('#engineer-name');
        engineerName.textContent = data.name;
    })
}

function fillTableByAppeals() {
    const startDate = document.querySelector('#start-date').value;
    const endDate = document.querySelector('#end-date').value;

    sendRequestToGetAppeals(() => {
        displayAppealsToDashboard(appeals)
    }, startDate, endDate)
}

function filterStartDate() {
    filteredAppeals = structuredClone(appeals);
    const filterAppealDate = document.querySelector('#group-start-date').value;

    if (filterAppealDate != '') {
            filteredAppeals = filteredAppeals.filter(appeal => appeal.date_of_group_start == filterAppealDate);
        }

    displayAppealsToDashboard(filteredAppeals);
}

function addStartDateFilterHandler() {
    const startDate = document.querySelector('#group-start-date');

    startDate.addEventListener('change', filterStartDate)
}

autoFillDateInputs()
addDateFilterHandler(fillTableByAppeals)
addStartDateFilterHandler()

initRequestToGetAppeals(fillTableByAppeals)
fillTableByAppeals()
getPersonalData()

