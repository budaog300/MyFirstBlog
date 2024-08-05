/* ----------------------Чтобы галочка оставалась в "Запомнить меня"---------------------- */
document.addEventListener('DOMContentLoaded', function() {
    const rememberMeCheckbox = document.getElementById('rememberMe');
    if (localStorage.getItem('rememberMe') === 'true') {
        rememberMeCheckbox.checked = true;
    }

    rememberMeCheckbox.addEventListener('change', function() {
        localStorage.setItem('rememberMe', rememberMeCheckbox.checked);
    });
});
/* -------------------------------------------------------------------- */

/* ----------------------Показать пароль---------------------- */
function myFunction(index) {
    var x = document.getElementById(index);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
/* ----------------------------------------------------------- */