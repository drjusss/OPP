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