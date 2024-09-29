// Wait until the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Get the form and submit button elements
    const form = document.querySelector('form');
    const submitButton = document.querySelector('button');

    // Form validation
    form.addEventListener('submit', function(event) {
        let valid = true;
        const inputs = document.querySelectorAll('.form-control');

        // Loop through each input and check if it's empty
        inputs.forEach(function(input) {
            if (input.value.trim() === '') {
                valid = false;
                input.style.borderColor = 'red'; // Highlight the empty field in red
                input.placeholder = 'This field is required'; // Add placeholder message
            } else {
                input.style.borderColor = '#3c3c3c'; // Reset border color if valid
            }
        });

        // If any field is invalid, prevent form submission
        if (!valid) {
            event.preventDefault();
            alert('Please fill in all the fields.'); // Alert message for incomplete form
        }
    });

    // Button animation on click
    submitButton.addEventListener('click', function() {
        submitButton.classList.add('button-clicked');
        setTimeout(function() {
            submitButton.classList.remove('button-clicked');
        }, 200); // Button animation duration
    });
    
    // Smooth scroll effect for the page
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
