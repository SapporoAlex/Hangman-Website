// JavaScript logic for updating the image zoom level
const imageElement = document.querySelector("#stick-figure-box img"); // Your image element




// Function to update image class based on wrong guesses
function updateImageZoom() {
    // Remove any existing zoom class
    for (let i = 0; i <= 5; i++) {
        imageElement.classList.remove(`zoomed-image-${i}`);
    }
    // Add the correct zoom class
    imageElement.classList.add(`zoomed-image-${wrongGuesses}`);
}

// Example function that handles wrong guesses
function handleWrongGuess() {
    if (wrongGuesses < 5) { // Increment until max zoom out level
        wrongGuesses++;
        updateImageZoom();
    }
}

// Reset game (optional)
function resetGame() {
    wrongGuesses = 0;
    updateImageZoom();
}

// Initialize the zoom level
updateImageZoom();
