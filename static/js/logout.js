var logoutUrl = "{{ url_for('logout') }}"; // Define logout URL using Jinja
document.getElementById("logout-link").addEventListener("click", confirmLogout);

function confirmLogout(event) {
    event.preventDefault(); // Prevent the default link behavior
    var confirmLogout = confirm("Are you sure you want to logout?");
    if (confirmLogout) {
        window.location.href = logoutUrl; // Redirect to logout URL
    }
}

