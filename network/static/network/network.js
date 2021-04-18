document.addEventListener('DOMContentLoaded', function() {
    /* For all elements with class of like, add event listener for processing
    liking and unliking posts */
    const likes = document.querySelectorAll('.like');
    likes.forEach(function(post) {
        post.addEventListener("click", () => like_request(post))
    });

    const edit = document.querySelectorAll(".edit");
    edit.forEach(function(post) {
        post.addEventListener("click", () => edit_post(post))
    });
});

// Calls function to like / unlike a post
function like_request(post) {
    fetch(`like/${post.dataset.postId}`, {
        method: 'PUT'
    })
    .then(response => response.json())
	.then(data => {
        if (data.liked === true) {
		    post.innerHTML = "UNLIKE " + "Total Likes: " + data.total_likes
        } else {
            post.innerHTML = "LIKE " + "Total Likes: " + data.total_likes
        }
	});
}

function edit_post(post) {
    let newText = document.createElement("textarea");
    let saveBtn = document.createElement("button");
    saveBtn.innerHTML = "Save Changes";
    newText.value = post.innerHTML;
    // save.addEventListener('click', () => save_edit(post, newText))
    post.innerHTML = ''
    post.parentElement.append(newText);
    post.parentElement.append(saveBtn);

    saveBtn.addEventListener('click', () => {
        console.log(post, newText.value);
        fetch(`save_edit/${post.dataset.editId}/${newText.value}`, {
        method: 'PUT'
        })
        .then(response => response.json())
	    .then(data => {
            console.log(data);
            newText.remove();
            post.append(data.content);
            saveBtn.remove();
	    });
    });
}
