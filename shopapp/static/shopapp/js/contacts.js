/* ------------------Закрыть сообщение об успешной отправке--------------- */
function hideMessage(id) {
    var element = document.getElementById(id);
    if (element) {
        element.style.display = 'none';
    }
    else {
        console.error("Element with id " + id + " not found.");
    }
}
/* ----------------------------------------------------------------------- */