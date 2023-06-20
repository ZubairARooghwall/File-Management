let answer = document.getElementsByClassName('answer')[0];
let question = document.getElementsByClassName('question')[0];
let answerButton = document.getElementsByClassName('answer-button')[0];
let scoreButtonsDiv = document.getElementsByClassName('score')[0];
let scoreButtons = document.querySelectorAll('.score button')
function showAnswer(){
  answer.classList.add('show-answer');
  question.classList.add('question-show-answer');
  answerButton.classList.add('show-answer-button');
  scoreButtonsDiv.classList.add('show-score');
  
}


scoreButtons.forEach((scoreButton) => {
  scoreButton.addEventListener('click', () => {
    let flashcard = scoreButton.closest('.flashcard');
    let flashcardId = flashcard.dataset.flashcardId;
    let score = scoreButton.textContent.toLowerCase().replace(/\s/g, '_');
    updateFlashcardIndex();
  });
});

function updateFlashcardIndex() {
  fetch('/update_flashcard_index/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then((response) => {
      if (response.ok) {
        window.location.reload();
      } else {
        console.log('Error updating flashcard index.');
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}