function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
  return null;
}

const domain = 'http://localhost:8000';
const loginUrl = `${domain}/auth/sign-in/`

function showPassword() {
    const passwordInput = document.querySelector('#password');
    const showPasswordIcon = document.querySelector('#show-password');
    const hidePasswordIcon = document.querySelector('#hide-password');

    passwordInput.type = 'text';
    showPasswordIcon.classList.add('hidden');
    hidePasswordIcon.classList.remove('hidden');
}

function addShowPasswordHandler() {
    const showPasswordIcon = document.querySelector('#show-password');

    showPasswordIcon.addEventListener('click', showPassword);
}

function hidePassword() {
    const passwordInput = document.querySelector('#password');
    const showPasswordIcon = document.querySelector('#show-password');
    const hidePasswordIcon = document.querySelector('#hide-password');

    passwordInput.type = 'password';
    showPasswordIcon.classList.remove('hidden');
    hidePasswordIcon.classList.add('hidden');
}

function addHidePasswordHandler() {
    const hidePasswordIcon = document.querySelector('#hide-password');

    hidePasswordIcon.addEventListener('click', hidePassword);
}

function isDateWithinOneYear(inputDate) {
    const currentDate = new Date();
    const oneYearAgo = new Date();
    const oneYearAhead = new Date();

    // Устанавливаем диапазон: год назад и год вперед от текущей даты
    oneYearAgo.setFullYear(currentDate.getFullYear() - 1);
    oneYearAhead.setFullYear(currentDate.getFullYear() + 1);

    // Преобразуем введенную дату в объект Date
    const dateToCheck = new Date(inputDate);

    // Проверяем, находится ли дата в диапазоне
    return dateToCheck >= oneYearAgo && dateToCheck <= oneYearAhead;
}

function convertDateFormat(dateString) {
    if (dateString == '') {
        return dateString
    }
    const dateStringArray = dateString.split('-');
    const year = dateStringArray[0]
    const month = dateStringArray[1]
    const day = dateStringArray[2]

    const result = `${day}.${month}.${year}`
    return result
}

function getVerboseNow() {
    const now = new Date();
    const year = String(now.getFullYear());
    const month = String(now.getMonth() + 1).padStart(2, '0');  // padStart - метод строк, который добавляет нужное количество символов (1 значние) и заполняет их из 2 значения
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    const result = `${day}-${month}-${year} ${hours}-${minutes}-${seconds}`
    return result
}

function addMessageInputHandler(selector) {
    const messageInput = document.querySelector(selector)
    messageInput.addEventListener('input', () => {
        messageInput.setCustomValidity('')
        autoResizeHandler(messageInput);
    })
}

function autoResizeHandler(element) {
    element.style.height = 'auto';
    element.style.height = `${element.scrollHeight}px`;
}

function isCyrillicWithDash(str) {
    return /^[а-яА-ЯёЁ\s-]+$/.test(str);
}
const a = 5
const test = a > 10 ? 'true' : 'false'