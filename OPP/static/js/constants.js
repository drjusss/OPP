const appealCardHtmlTemplate = `
    <div class="justify-between flex items-center mb-4 text-xl">
        <div class="appeal-id text-m font-medium text-gray-900 dark:text-gray-400">{{ appeal_id }}</div>
        <div class="text-xl font-medium text-gray-700 dark:text-gray-400">{{ worker_id }}</div>
        <div class="">{{ is_completed }}</div>
    </div>
    <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
            <span class="text-m font-medium text-gray-900 dark:text-gray-400">ФИО ученика</span>
            <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ name }}</p>
        </div>
        <div class="flex flex-col gap-1">
            <span class="text-m font-medium text-gray-900 dark:text-gray-400">Скайп ученика</span>
            <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ skype }}</p>
        </div>
        <div class="flex justify-between items-end gap-4">
            <div class="flex flex-col gap-1 flex-1">
                <span class="text-m font-medium text-gray-900 dark:text-gray-400">Гарнитура/микрофон</span>
                <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ headset }}</p>
            </div>
            <div class="flex flex-col gap-1 flex-1">
                <span class="text-m font-medium text-gray-900 dark:text-gray-400">Звук</span>
                <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ sound_is_ok }}</p>
            </div>
            <div class="flex flex-col gap-1 flex-1">
                <span class="text-m font-medium text-gray-900 dark:text-gray-400">Дата старта</span>
                <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ date_of_group_start }}</p>
            </div>
        </div>
        <div class="flex justify-between items-end gap-4">
            <div class="flex flex-col gap-1 flex-1">
                <span class="text-m font-medium text-gray-900 dark:text-gray-400">Наличие камеры</span>
                <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ camera }}</p>
            </div>
            <div class="flex flex-col gap-1 flex-1">
                <span class="text-m font-medium text-gray-900 dark:text-gray-400">Тест скорости</span>
                <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ speed_test }}</p>
            </div>
        </div>
        <div class="flex flex-col gap-1n">
            <span class="text-m font-medium text-gray-900 dark:text-gray-400">Текст обращения</span>
            <p class="rounded-lg text-center text-lg text-ellipsis overflow-x-hidden p-3 dark:bg-gray-700 dark:text-gray-300">{{ message }}</p>
        </div>
    </div>
`

const appealDetailWindowHTMLTemplate = `
    <div style="top: 0; right: 0; bottom: 0; left: 0; background-color: rgb(107 114 128); position: fixed; z-index: 10; opacity: 50%;"></div>
    <div style="height: 100%; width: 100%; position: fixed; top: 0; right: 0; left: 0; z-index: 20; display: flex; align-items: center; justify-content: center;">
        <div id="appeal" class="w-[50rem] justify-around flex m-auto">
            <div class="scrollbar-none max-h-[90vh] w-[65rem] rounded-2xl px-6 py-4 border-2 border-solid dark:border-gray-600 overflow-y-scroll dark:bg-gray-900">
                <div class="justify-between grid grid-cols-4 grid-span-6 mb-4 text-xl gap-10">
                    <div class="flex items-center dark:text-gray-300">
                        <span id="appeal-card-id">{{ appeal_id }}</span>
                    </div>
                    <div class="col-span-2 relative">
                        <select name="fixik" id="appeal-card-fixik-choice" required class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-left text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" "></select>
                        <label for="appeal-card-headset" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4">Инженер</label>
                    </div>
                    <div class="flex items-center justify-end gap-4">
                        <label for="appeal-card-is-complete" class="cursor-pointer text-base dark:text-gray-400">Выполненно</label>
                        <input type="checkbox" id="appeal-card-is-complete" class="w-8 h-8 cursor-pointer appearance-none dark:bg-gray-600 rounded-lg">
                    </div>
                </div>
                <div class="grid grid-cols-6 gap-6">
                    <div class="flex flex-col gap-1 col-span-3">
                        <span class="dark:text-gray-400">ФИО ученика</span>
                        <p id="appeal-card-name" class="p-2 rounded-lg font-xl text-ellipsis text-center overflow-hidden whitespace-nowrap dark:bg-gray-800 dark:text-gray-300">{{ student_name }}</p>
                    </div>
                    <div class="flex flex-col gap-1 col-span-3">
                        <span class="dark:text-gray-400">Скайп ученика</span>
                        <p id="appeal-card-skype" class="p-2 rounded-lg font-xl text-ellipsis text-center overflow-hidden whitespace-nowrap dark:bg-gray-800 dark:text-gray-300">{{ skype }}</p>
                    </div>
                    <div class="flex flex-col gap-1 col-span-6">
                        <span class="dark:text-gray-400">Текст обращения</span>
                        <p id="appeal-card-content" class="resize-none text-center break-words p-2 min-h-[4.625rem] rounded-lg font-xl dark:bg-gray-800 dark:text-gray-300">{{ message }}</p>
                    </div>
                    <div class="gap-4 col-span-6 grid grid-cols-3 relative">
                        <div class="">
                            <select name="headset" id="appeal-card-headset" required class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-left text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                                <option value="USB">USB</option>
                                <option value="3.5">3.5</option>
                                <option value="USB/3.5">USB/3.5</option>
                                <option value="3.5/USB">3.5/USB</option>
                            </select>
                            <label for="appeal-card-headset" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4">Гарнитура</label>
                        </div>
                        <div class="relative">
                            <select name="sound-is-ok" id="appeal-card-sound-is-ok" required class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                                <option value="true">ОК</option>
                                <option value="false">Не ОК</option>
                            </select>
                            <label for="appeal-card-sound-is-ok" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Звук</label>
                        </div>
                        <div class="relative">
                            <input id="appeal-card-date-of-start" type="date" class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                            <label for="appeal-card-date-of-start" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Дата старта</label>
                        </div>
                    </div>
                    <div class="gap-4 col-span-6 grid grid-cols-3">
                        <div class="flex flex-col gap-1 flex-1 relative">
                            <select name="camera" id="appeal-card-camera" required class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                                <option value="true">OK</option>
                                <option value="false">Не ОК</option>
                            </select>
                            <label for="appeal-card-camera" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Наличие камеры</label>
                        </div>
                        <div class="flex flex-col gap-1 flex-1 relative">
                            <select name="type" id="appeal-card-type" required class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                                <option value="check">Проверка</option>
                                <option value="incident">Инцидент</option>
                            </select>
                            <label for="appeal-card-type" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Тип обращения</label>
                        </div>
                        <div class="flex flex-col gap-1 flex-1 relative">
                            <input  id="appeal-card-time-to-complete" type="text" class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                            <label for="appeal-card-time-to-complete" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Время на выполненние</label>
                        </div>
                    </div>
                    <div class="flex items-center justify-between gap-4 col-span-6">
                        <div class="flex flex-col gap-1 flex-1 relative">
                            <input  id="appeal-card-speed-test" type="text" class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                            <label for="appeal-card-speed-test" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Тест скорости</label>
                        </div>
                        <div class="flex flex-col gap-1 flex-1 relative">
                            <select name="appeal-card-type-of-connection" required id="appeal-card-type-of-connection" class="scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" ">
                                <option value="wi-fi">wi-fi</option>
                                <option value="cable">Кабель</option>
                            </select>
                            <label for="appeal-card-type-of-connection" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-invalid:scale-100 peer-invalid:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Тип подключения</label>
                        </div>
                    </div>
                    <div class="flex flex-col gap-1 col-span-6 relative">
                        <textarea id="appeal-card-speed-test-comment" rows="2" class="resize-none scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" "></textarea>
                        <label for="appeal-card-speed-test-comment" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Комментарий к тесту</label>
                    </div>
                    <div class="flex flex-col gap-1 col-span-6 relative">
                        <textarea id="appeal-card-student-comment" rows="2" class="resize-none scrollbar-none block pt-4 pl-2 pb-2 w-full text-xl text-gray-900 bg-gray-50 rounded-lg border-0 border-b-2 border-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white outline-0 dark:focus:border-b-blue-500 peer" placeholder=" "></textarea>
                        <label for="appeal-card-student-comment" class="absolute text-sm text-gray-300 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Комментарий к ученику</label>
                    </div>
                    <div class="grid grid-cols-3 m-auto gap-4 col-span-6">
                        <button id="save-button" type="button" class="text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-xl px-5 py-2.5 text-center me-2 mb-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-500 dark:focus:ring-blue-800">Сохранить</button>
                        <button id="not-save-button" type="button" class="text-gray-700 hover:text-white border border-gray-700 hover:bg-gray-800 focus:ring-4 focus:outline-none focus:ring-gray-300 font-medium rounded-lg text-xl px-5 py-2.5 text-center me-2 mb-2 dark:border-gray-500 dark:text-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-900">Не сохранять</button>
                        <button id="is-spam-button" type="button" class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-xl px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">Спам</button>
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
            <select name="only-complete" id="only-complete" class="text-xl dark:border-gray-500">
                <option>Любое</option>
                <option>Да</option>
                <option>Нет</option>
            </select>
        </div>
        <div class="flex-col">
            <label for="fixik" class="mb-2">
                <span>Инженер</span>
            </label>
            <select name="fixik" id="fixik" class="text-xl dark:border-gray-500"></select>
        </div>
        <div class="flex-col">
            <label for="appeal-type" class="mb-2">
                <span>Тип</span>
            </label>
            <select name="appeal-type" id="appeal-type" class="text-xl dark:border-gray-500">
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
        <div id="modal-window-content" class="dark:bg-gray-800">
            <p class="text-[2rem] mb-6" style="text-align: center; margin-bottom: 2rem;">Вы уверены что это спам?</p>
            <div style="display: flex; align-items: center; justify-content: center;">
                <button type="button" id="spam-modal-button" class="text-2xl mr-2">Да, удалить</button>
                <button type="button" id="close-spam-modal-button" class="text-2xl rounded-lg">Нет, не удалять</button>
            </div>
        </div>
    </div>
`

const dashboardHTMLTemplate = `
    <td scope="col" class="px-6 py-3">{{ name }}</td>
    <td scope="col" class="px-6 py-3">{{ skype }}</td>
    <td scope="col" class="px-6 py-3">{{ headset }}</td>
    <td scope="col" class="px-6 py-3">{{ type_of_connection }}</td>
    <td scope="col" class="px-6 py-3">{{ sound_is_ok }}</td>
    <td scope="col" class="px-6 py-3">{{ camera }}</td>
    <td scope="col" class="px-6 py-3">{{ speed_test }}</td>
    <td scope="col" class="px-6 py-3">{{ date_of_group_start }}</td>
    <td scope="col" class="px-6 py-3">{{ worker }}</td>
    <td scope="col" class="px-6 py-3">{{ time_to_complete }}</td>
`

const appealCompletionIcons = {
    'completed': '<svg xmlns="http://www.w3.org/2000/svg" height="2rem" viewBox="0 -960 960 960" width="2rem" fill="green"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>',
    'not completed': '',
    'in progress': '<svg xmlns="http://www.w3.org/2000/svg" height="2rem" viewBox="0 -960 960 960" width="2rem" fill="blue"><path d="M441-82Q287-97 184-211T81-480q0-155 103-269t257-129v120q-104 14-172 93t-68 185q0 106 68 185t172 93v120Zm80 0v-120q94-12 159-78t79-160h120q-14 143-114.5 243.5T521-82Zm238-438q-14-94-79-160t-159-78v-120q143 14 243.5 114.5T879-520H759Z"/></svg>',
}