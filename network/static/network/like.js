window.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('#like').forEach((x) => {
         x.addEventListener('click', () => {
             const csrftoken = getCookie('csrftoken');

             if(x.dataset.bool === "true") 
             {
                fetch(`/dislike/${x.dataset.postid}`, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrftoken },
                 })
                 .then((response) => {
                    console.log(response);
                    x.dataset.bool = "false";
                    x.style.backgroundColor = "white";
                    let val = document.getElementById(`${x.dataset.postid}likes`).innerHTML;
                    val = parseInt(val);
                    document.getElementById(`${x.dataset.postid}likes`).innerHTML = val - 1;
                 })
                 .catch((error) => console.log(error));
             }
             else
             {
                fetch(`/like/${x.dataset.postid}`, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrftoken },
                 })
                 .then((response) => {
                    console.log(response);
                    x.dataset.bool = "true";
                    x.style.backgroundColor = "#F5D7F9";
                    let val = document.getElementById(`${x.dataset.postid}likes`).innerHTML;
                    val = parseInt(val);
                    document.getElementById(`${x.dataset.postid}likes`).innerHTML = val + 1;
                 })
                 .catch((error) => console.log(error));
             }
         });
    });
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
