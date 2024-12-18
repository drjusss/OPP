function displayAppealsToDashboard(appealsData) {
    const appealList = document.querySelector('#appeal-table-body');
    appealList.innerHTML = ''

    for (const appealData of appealsData) {
        const appealRow = document.createElement('tr');
        appealRow.classList.add('bg-white')
        appealRow.classList.add('border-b')
        appealRow.classList.add('dark:bg-gray-800')
        appealRow.classList.add('dark:border-gray-700')
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
}

function fillTableByAppeals() {
    sendRequestToGetAppeals(() => {
        displayAppealsToDashboard(appeals)
    })
}

fillTableByAppeals()
