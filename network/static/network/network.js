document.addEventListener('DOMContentLoaded', function() {
    // Update likes in DB 
    document.querySelector('#like').addEventListener('click', () => like_request(increment));
    document.querySelector('#unlike').addEventListener('click', () => like_request(decrement));
});