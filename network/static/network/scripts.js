window.addEventListener("DOMContentLoaded", (event) => {
       document.querySelectorAll('#edit-button').forEach((x) => {
            x.addEventListener('click', toggleEdit);
       });
       document.querySelectorAll('#edit-form').forEach((x) => {
           x.addEventListener("submit", savePost);
       })       
});


function savePost(event) {
    event.preventDefault();
    const content = document.getElementById(`${this.post_id.value}edit-content`).value;
    console.log(content);  
    const csrftoken = getCookie('csrftoken');
    
    // Call the API
    fetch("/savePost", {
       method: "POST",
       body: JSON.stringify({
          content: content,
          post_id: this.post_id.value
      }),
      headers: { "X-CSRFToken": csrftoken },
    })
    .then((response) => {
        document.getElementById(`${this.post_id.value}content`).style.display = "block";
        document.getElementById(`${this.post_id.value}edit-content`).style.display = "none";
        document.getElementById(`${this.post_id.value}edit`).style.display = "block";
        document.getElementById(`${this.post_id.value}save`).style.display = "none";
        document.getElementById(`${this.post_id.value}content`).innerHTML = content;
    })
    .catch((error) => console.log(error));

    return false;
}

function toggleEdit() {
    console.log(this.value)
    document.getElementById(`${this.value}content`).style.display = "none";
    document.getElementById(`${this.value}edit-content`).style.display = "block";
    document.getElementById(`${this.value}edit`).style.display = "none";
    document.getElementById(`${this.value}save`).style.display = "block";
 }    

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
