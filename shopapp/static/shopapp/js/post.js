document.addEventListener('DOMContentLoaded', function() {
    // Получаем все кнопки "Ответить"
    const replyButtons = document.querySelectorAll('.reply-btn');

    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Находим целевую форму ответа
            const targetForm = document.querySelector(this.getAttribute('data-target'));

            // Переключаем отображение формы
            if (targetForm.style.display === 'none' || targetForm.style.display === '') {
                targetForm.style.display = 'block';
            } else {
                targetForm.style.display = 'none';
            }
        });
    });
});

/* --------------------ПОКАЗАТЬ ОТВЕТЫ К КОММЕНТАРИЯМ----------------- */
function show_replies(id) {
   var replies = document.getElementById("replies-" + id);
    if (replies.style.display === 'none' || replies.style.display === '') {
        replies.style.display = 'block';
    } else {
        replies.style.display = 'none';
    }
}
/* -------------------------------------------------------------------- */



