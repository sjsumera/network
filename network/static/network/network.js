document.addEventListener('DOMContentLoaded', function() {
    // Update likes in DB 
    let element = document.querySelector('#like').addEventListener('click');
    console.log(element);
    document.querySelector('#unlike').addEventListener('click', () => like_request(decrement));
});

function like_request(type) {
    console.log(element, type);
}