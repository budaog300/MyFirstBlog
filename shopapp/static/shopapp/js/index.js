/* --------------------Отображение постов каждой категории----------------- */
var postsVisible = {};

function togglePosts(index) {
    var posts = document.getElementById("posts-" + index);
    if (postsVisible[index]) {
        closePosts(posts, index);
    } else {
        openPosts(posts, index);
    }
}

function openPosts(posts, index) {
    posts.style.position = "relative";
    posts.style.visibility = "visible";
    postsVisible[index] = true;
}

function closePosts(posts, index) {
    posts.style.position = "fixed";
    posts.style.visibility = "hidden";
    postsVisible[index] = false;
}
/* ----------------------------------------------------------------------- */



