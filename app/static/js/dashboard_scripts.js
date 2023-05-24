document.addEventListener('DOMContentLoaded', function() {
    var apiKeysLink = document.querySelector('.left-nav a');
    var apiKeysSection = document.querySelector('.api-keys-section');

    apiKeysLink.addEventListener('click', function(event) {
        event.preventDefault();
        apiKeysSection.style.display = 'block';
    });
});
