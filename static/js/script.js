
var originalContentMargin; // Store the original content margin

function toggleDropdown(event, id) {
event.preventDefault(); // Prevent default behavior of the link click
var dropdown = document.getElementById(id);
var isDisplayed = dropdown.style.display === "block";
// Hide all dropdowns
var allDropdowns = document.querySelectorAll('.sub-links');
allDropdowns.forEach(function(dropdown) {
dropdown.style.display = 'none';
});
// Display the clicked dropdown if it wasn't already displayed
if (!isDisplayed) {
dropdown.style.display = 'block';
} else {
dropdown.style.display = 'none'; // Hide the dropdown if already displayed
}
}


function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('sidebar-hidden');

    // Toggle content margin based on sidebar visibility
    var content = document.querySelector('.content');
    if (!originalContentMargin) {
        originalContentMargin = getComputedStyle(content).marginLeft;
    }
    content.style.marginLeft = (sidebar.classList.contains('sidebar-hidden')) ? '0' : originalContentMargin;
}

function countCharacters(inputId, displayId, limit) {
    var input = document.getElementById(inputId);
    var characterCount = input.value.length;
    var display = document.getElementById(displayId);
    display.textContent = characterCount + "/" + limit + " characters";

    // Check if character count exceeds the limit
    if (characterCount > limit) {
        // Trim the input value to the limit
        input.value = input.value.slice(0, limit);

        // Update the character count in the display
        characterCount = limit;
        display.textContent = characterCount + "/" + limit + " characters";

        // Change the color to red
        display.style.color = 'red';
    } else {
        // Reset the color to black
        display.style.color = 'black';
    }
}