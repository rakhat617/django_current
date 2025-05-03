let crsf_token = document.cookie.split("=")[1];


function LikePost(postId){
    fetch(`${postId}/like`, {
        method: "POST",
        headers: {
            'X-CSRFToken': crsf_token
        },
    }).then(response => response.json())
    .then(data => {
        document.getElementById("likebtn").innerText = `👍${data.likes}`
        document.getElementById("dislikebtn").innerText = `👎${data.dislikes}`
    })
}

function DislikePost(postId){
    fetch(`${postId}/dislike`, {
        method: "POST",
        headers: {
            'X-CSRFToken': crsf_token
        },
    }).then(response => response.json())
    .then(data => {
        document.getElementById("likebtn").innerText = `👍${data.likes}`
        document.getElementById("dislikebtn").innerText = `👎${data.dislikes}`
    })
}