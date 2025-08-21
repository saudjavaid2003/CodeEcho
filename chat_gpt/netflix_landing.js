function subscribe() {
    var email = document.getElementById('email').value;
    var message = document.getElementById('message');
    if (email && email.includes('@') && email.includes('.')) {
        message.textContent = "Thanks for subscribing, " + email + "!";
        message.style.color = '#46d369';
    } else {
        message.textContent = "Please enter a valid email address.";
        message.style.color = '#e50914';
    }
}
