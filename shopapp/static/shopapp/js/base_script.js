/* ----------------------Кнопка скролла по странице---------------------- */
mybutton = document.getElementById("myBtn");

// Когда пользователь прокручивает вниз 20px от верхней части документа, покажите кнопку
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 100) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// Когда пользователь нажимает на кнопку, прокрутите до верхней части документа
function topFunction() {
  document.body.scrollTop = 0; // Для Safari
  document.documentElement.scrollTop = 0; // Для Chrome, Firefox, IE и Opera
}
/* ---------------------------------------------------------------------- */

/* ----------------------------Дата и время------------------------------ */
function updateTime() {
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    document.getElementById('current-time').innerText = now.toLocaleDateString('ru-RU', options);
}

setInterval(updateTime, 1000);
updateTime();  // Initial call to display the time immediately
/* ---------------------------------------------------------------------- */