document.addEventListener('DOMContentLoaded', function() {
    /* For all elements with class of like, add event listener for processing
    liking and unliking posts */
    const likes = document.querySelectorAll('.like');
    likes.forEach(function(post) {
        post.addEventListener("click", () => like_request(post.dataset.postId));
    });

    /* For all elements with class of edit (buttons), add event listener for processing edits */
    const edit = document.querySelectorAll(".edit");
    edit.forEach(function(post) {
        post.addEventListener("click", () => edit_post(post.dataset.postId));
    });
});

// Calls view that handles liking and unliking posts 
function like_request(post_id) {
    fetch(`like/${post_id}`, {
        method: 'PUT'
    })
    .then(response => response.json())
	.then(data => {
        const content = document.querySelector(`#total-${post_id}`);
        if (data.liked === true) {
            document.querySelector(`#like-${post_id}`).innerHTML = "Unlike";
		    content.innerHTML = " Total Likes: " + data.total_likes;
        } else {
            document.querySelector(`#like-${post_id}`).innerHTML = "Like";
            content.innerHTML = " Total Likes: " + data.total_likes;
        }
	});
}

// Function that handles editing of post 
function edit_post(post_id) {
    const editBtn = document.querySelector(`#edit-${post_id}`);
    const post = document.querySelector(`#post-${post_id}`);
    const newText = document.querySelector(`#text-${post_id}`);
    const saveBtn = document.querySelector(`#save-${post_id}`);
    editBtn.style.display = 'none';
    newText.style.display = 'block';
    saveBtn.style.display = 'inline';
    newText.value = post.innerHTML;
    post.innerHTML = '';

    /* Process saving post edits and displaying appropriate buttons / new text. 
    "../" to ensure edits can be made whether on profile page or home page */ 
    saveBtn.addEventListener('click', () => {
        fetch(`../save_edit/${post.dataset.postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: newText.value
            })
        })
        .then(response => response.json())
	    .then(data => {
            post.innerHTML = data.content;
            editBtn.style.display = 'inline';
            saveBtn.style.display = 'none';
            newText.style.display = 'none';
	    });
    });
}
