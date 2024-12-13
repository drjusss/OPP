const appealCardHtmlTemplate = `
    <div class="justify-between flex-items-center mb-4 text-5">
        <div class="appeal-id">{{ appeal_id }}</div>
        <div>{{ worker_id }}</div>
        <div>{{ is_completed }}</div>
    </div>
    <div class="appeal-card-body">
        <div class="appeal-card-option">
            <span class="appeal-card-label">ФИО ученика</span>
            <p class="appeal-item">{{ name }}</p>
        </div>
        <div class="appeal-card-option">
            <span class="appeal-card-label">Скайп ученика</span>
            <p class="appeal-item">{{ skype }}</p>
        </div>
        <div class="flex justify-between items-end gap-4">
            <div class="appeal-card-option flex-1">
                <span class="appeal-card-label">Гарнитура/микрофон</span>
                <p class="appeal-item">{{ headset }}</p>
            </div>
            <div class="appeal-card-option flex-1">
                <span class="appeal-card-label">Звук</span>
                <p class="appeal-item">{{ sound_is_ok }}</p>
            </div>
            <div class="appeal-card-option flex-1">
                <span class="appeal-card-label">Дата старта</span>
                <p class="appeal-item">{{ date_of_group_start }}</p>
            </div>
        </div>
        <div class="flex justify-between items-end gap-4">
            <div class="appeal-card-option flex-1">
                <span class="appeal-card-label">Наличие камеры</span>
                <p class="appeal-item">{{ camera }}</p>
            </div>
            <div class="appeal-card-option flex-1">
                <span class="appeal-card-label">Тест скорости</span>
                <p class="appeal-item">{{ speed_test }}</p>
            </div>
        </div>
        <div class="appeal-card-option">
            <span class="appeal-card-label">Текст обращения</span>
            <p class="appeal-item">{{ message }}</p>
        </div>
    </div>
`

//const appealDetailWindowHTMLTemplate = `
//    <div style="top: 0; right: 0; bottom: 0; left: 0; background-color: rgb(107 114 128); position: fixed; z-index: 10; opacity: 50%;"></div>
//    <div style="height: 100%; width: 100%; position: fixed; top: 0; right: 0; left: 0; z-index: 20; display: flex; align-items: center; justify-content: center;">
//        <div id="appeal">
//            <div class="appeal-card-large overflow-y-scroll">
//                <div class="justify-between flex-items-center mb-4 text-5">
//                    <div id="appeal-card-id">{{ appeal_id }}</div>
//                    <div>
//                        <select name="fixik" id="appeal-card-fixik-choice" class="text-5 border-gray br-2"></select>
//                    </div>
//                    <div class="check-box">
//                        <button id="is-spam-button" type="button" class="text-5 w-100">Спам</button>
//                    </div>
//                    <div class="check-box">
//                        <label for="appeal-card-is-complete" class="appeal-card-label mr-2">Выполненные</label>
//                        <input type="checkbox" id="appeal-card-is-complete" class="w-8 h-8">
//                    </div>
//                </div>
//                <div class="appeal-card-body">
//                    <div class="appeal-card-option">
//                        <span class="appeal-card-label">ФИО ученика</span>
//                        <p id="appeal-card-name" class="appeal-item bg-read-only-input">{{ student_name }}</p>
//                    </div>
//                    <div class="appeal-card-option">
//                        <span class="appeal-card-label">Скайп ученика</span>
//                        <p id="appeal-card-skype" class="appeal-item bg-read-only-input">{{ skype }}</p>
//                    </div>
//                    <div class="appeal-card-option">
//                        <span class="appeal-card-label">Текст обращения</span>
//                        <p id="appeal-card-content" class="appeal-item bg-read-only-input">{{ message }}</p>
//                    </div>
//                    <div class="flex justify-between items-end gap-4">
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-headset" class="appeal-card-label">Гарнитура</label>
//                            <select name="headset" id="appeal-card-headset" class="text-5 border-gray">
//                                <option value="USB">USB</option>
//                                <option value="3.5">3.5</option>
//                                <option value="USB/3.5">USB/3.5</option>
//                                <option value="3.5/USB">3.5/USB</option>
//                            </select>
//                        </div>
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-sound-is-ok" class="appeal-card-label">Звук</label>
//                            <select name="sound-is-ok" id="appeal-card-sound-is-ok" class="text-5 border-gray">
//                                <option value="true">ОК</option>
//                                <option value="false">Не ОК</option>
//                            </select>
//                        </div>
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-date-of-start" class="appeal-card-label">Дата старта</label>
//                            <input id="appeal-card-date-of-start" type="date" class="text-5 border-gray">
//                        </div>
//                    </div>
//                    <div class="flex-items-center justify-between gap-4">
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-camera" class="appeal-card-label">Наличие камеры</label>
//                            <select name="camera" id="appeal-card-camera" class="text-5 border-gray">
//                                <option value="true">OK</option>
//                                <option value="false">Не ОК</option>
//                            </select>
//                        </div>
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-type" class="appeal-card-label">Тип обращения</label>
//                            <select name="type" id="appeal-card-type" class="text-5 border-gray">
//                                <option value="check">Проверка</option>
//                                <option value="incident">Инцидент</option>
//                            </select>
//                        </div>
//                        <div class="appeal-card-option flex-1">
//                            <label for="appeal-card-speed-test" class="appeal-card-label">Тест скорости</label>
//                            <input  id="appeal-card-speed-test" type="text" class="text-5 border-gray">
//                        </div>
//                    </div>
//                    <div class="appeal-card-option">
//                        <label for="appeal-card-speed-test-comment" class="appeal-card-label">Комментарий к тесту</label>
//                        <textarea id="appeal-card-speed-test-comment" class="text-5 border-gray" rows="2"></textarea>
//                    </div>
//                    <div class="appeal-card-option">
//                        <label for="appeal-card-student-comment" class="appeal-card-label">Комментарий к ученику</label>
//                        <textarea id="appeal-card-student-comment" class="text-5 border-gray" rows="2"></textarea>
//                    </div>
//                    <div class="flex-items-center justify-between gap-4">
//                        <button id="save-button" type="button" class="text-5 w-100">Сохранить</button>
//                        <button id="not-save-button" type="button" class="text-5 w-100">Не сохранять</button>
//                    </div>
//                </div>
//            </div>
//        </div>
//    </div>
//`

const appealDetailWindowHTMLTemplate = `
    <div style="top: 0; right: 0; bottom: 0; left: 0; background-color: rgb(107 114 128); position: fixed; z-index: 10; opacity: 50%;"></div>
    <div style="height: 100%; width: 100%; position: fixed; top: 0; right: 0; left: 0; z-index: 20; display: flex; align-items: center; justify-content: center;">
        <div id="appeal">
            <div class="appeal-card-large overflow-y-scroll">
                <div class="justify-between flex-items-center mb-4 text-5">
                    <div id="appeal-card-id">{{ appeal_id }}</div>
                    <div>
                        <select name="fixik" id="appeal-card-fixik-choice" class="text-5 border-gray br-2"></select>
                    </div>
                    <div class="check-box">
                        <button id="is-spam-button" type="button" class="text-5 w-100">Спам</button>
                    </div>
                    <div class="check-box">
                        <label for="appeal-card-is-complete" class="appeal-card-label mr-2">Выполненные</label>
                        <input type="checkbox" id="appeal-card-is-complete" class="w-8 h-8">
                    </div>
                </div>
                <div class="appeal-card-body">
                    <div class="appeal-card-option">
                        <span class="appeal-card-label">ФИО ученика</span>
                        <p id="appeal-card-name" class="appeal-item bg-read-only-input">{{ student_name }}</p>
                    </div>
                    <div class="appeal-card-option">
                        <span class="appeal-card-label">Скайп ученика</span>
                        <p id="appeal-card-skype" class="appeal-item bg-read-only-input">{{ skype }}</p>
                    </div>
                    <div class="appeal-card-option">
                        <span class="appeal-card-label">Текст обращения</span>
                        <p id="appeal-card-content" class="appeal-item bg-read-only-input">{{ message }}</p>
                    </div>
                    <div class="flex justify-between items-end gap-4">
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-headset" class="appeal-card-label">Гарнитура</label>
                            <select name="headset" id="appeal-card-headset" class="text-5 border-gray">
                                <option value="USB">USB</option>
                                <option value="3.5">3.5</option>
                                <option value="USB/3.5">USB/3.5</option>
                                <option value="3.5/USB">3.5/USB</option>
                            </select>
                        </div>
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-sound-is-ok" class="appeal-card-label">Звук</label>
                            <select name="sound-is-ok" id="appeal-card-sound-is-ok" class="text-5 border-gray">
                                <option value="true">ОК</option>
                                <option value="false">Не ОК</option>
                            </select>
                        </div>
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-date-of-start" class="appeal-card-label">Дата старта</label>
                            <input id="appeal-card-date-of-start" type="date" class="text-5 border-gray">
                        </div>
                    </div>
                    <div class="flex-items-center justify-between gap-4">
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-camera" class="appeal-card-label">Наличие камеры</label>
                            <select name="camera" id="appeal-card-camera" class="text-5 border-gray">
                                <option value="true">OK</option>
                                <option value="false">Не ОК</option>
                            </select>
                        </div>
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-type" class="appeal-card-label">Тип обращения</label>
                            <select name="type" id="appeal-card-type" class="text-5 border-gray">
                                <option value="check">Проверка</option>
                                <option value="incident">Инцидент</option>
                            </select>
                        </div>
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-time-to-complete" class="appeal-card-label">Время на выполненние</label>
                            <input  id="appeal-card-time-to-complete" type="text" class="text-5 border-gray">
                        </div>
                    </div>
                    <div class="flex-items-center justify-between gap-4">
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-speed-test" class="appeal-card-label">Тест скорости</label>
                            <input  id="appeal-card-speed-test" type="text" class="text-5 border-gray">
                        </div>
                        <div class="appeal-card-option flex-1">
                            <label for="appeal-card-type-of-connection" class="appeal-card-label">Тип подключения</label>
                            <select name="type-of-connection" id="appeal-card-type-of-connection" class="text-5 border-gray">
                                <option value="wi-fi">wi-fi</option>
                                <option value="cable">Кабель</option>
                            </select>
                        </div>
                    </div>
                    <div class="appeal-card-option">
                        <label for="appeal-card-speed-test-comment" class="appeal-card-label">Комментарий к тесту</label>
                        <textarea id="appeal-card-speed-test-comment" class="text-5 border-gray h-6" rows="2"></textarea>
                    </div>
                    <div class="appeal-card-option">
                        <label for="appeal-card-student-comment" class="appeal-card-label">Комментарий к ученику</label>
                        <textarea id="appeal-card-student-comment" class="text-5 border-gray" rows="2"></textarea>
                    </div>
                    <div class="flex-items-center justify-between gap-4">
                        <button id="save-button" type="button" class="text-5 w-100">Сохранить</button>
                        <button id="not-save-button" type="button" class="text-5 w-100">Не сохранять</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
`

const filterHTMLTemplate = `
    <div class="flex-items-stretch justify-between mr-8 gap-10">
        <div class="flex-col">
            <label for="only-complete" class="mb-2">
                <span>Выполненные</span>
            </label>
            <select name="only-complete" id="only-complete" class="text-5 border-gray">
                <option>Любое</option>
                <option>Да</option>
                <option>Нет</option>
            </select>
        </div>
        <div class="flex-col">
            <label for="fixik" class="mb-2">
                <span>Инженер</span>
            </label>
            <select name="fixik" id="fixik" class="text-5 border-gray"></select>
        </div>
        <div class="flex-col">
            <label for="appeal-type" class="mb-2">
                <span>Тип</span>
            </label>
            <select name="appeal-type" id="appeal-type" class="text-5 border-gray">
                <option>Любое</option>
                <option>Инцидент</option>
                <option>Проверка</option>
            </select>
        </div>
    </div>
    <div class="flex-items-stretch">
        <input type="text" id="search-field">
        <button type="button" id="search-button">Найти</button>
    </div>
    `

const spamModalWindowHTMLTemplate = `
    <div style="top: 0; right: 0; bottom: 0; left: 0; background-color: rgb(107 114 128); position: fixed; z-index: 30; opacity: 50%;"></div>
    <div style="height: 100%; width: 100%; position: fixed; top: 0; right: 0; left: 0; z-index: 40; display: flex; align-items: center; justify-content: center;">
        <div id="modal-window-content" style="background-color: white; border-radius: 1rem; width: 40rem; height: 10rem; padding: 2rem;">
            <p class="text-8 mb-6" style="text-align: center; margin-bottom: 2rem;">Вы уверены что это спам?</p>
            <div style="display: flex; align-items: center; justify-content: center;">
                <button type="button" id="spam-modal-button" class="text-6 mr-2">Да, удалить</button>
                <button type="button" id="close-spam-modal-button" class="text-6 br-2">Нет, не удалять</button>
            </div>
        </div>
    </div>
`

const dashboardHTMLTemplate = `
    <td>{{ name }}</td>
    <td>{{ skype }}</td>
    <td>{{ headset }}</td>
    <td>{{ type_of_connection }}</td>
    <td>{{ sound_is_ok }}</td>
    <td>{{ camera }}</td>
    <td>{{ speed_test }}</td>
    <td>{{ date_of_group_start }}</td>
    <td>{{ worker }}</td>
    <td>{{ time_to_complete }}</td>
`

const appealCompletionIcons = {
    'completed': '<svg xmlns="http://www.w3.org/2000/svg" height="2rem" viewBox="0 -960 960 960" width="2rem" fill="green"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>',
    'not completed': '',
    'in progress': '<svg xmlns="http://www.w3.org/2000/svg" height="2rem" viewBox="0 -960 960 960" width="2rem" fill="blue"><path d="M441-82Q287-97 184-211T81-480q0-155 103-269t257-129v120q-104 14-172 93t-68 185q0 106 68 185t172 93v120Zm80 0v-120q94-12 159-78t79-160h120q-14 143-114.5 243.5T521-82Zm238-438q-14-94-79-160t-159-78v-120q143 14 243.5 114.5T879-520H759Z"/></svg>',
}