const englishText = ["A Developer", "An Engineer", "A Dreamer", "A Fighter"];
const spanishText = ["Un Desarrollador", "Un Ingeniero", "Un Soñador", "Un Luchador"];

const language = document.body.getAttribute('data-language');
const typewriterText = language === 'es' ? spanishText : englishText;

let textPosition = 0;
let index = 0;

function typeWriter() {
  if (textPosition < typewriterText.length) {
    let currentText = typewriterText[textPosition];
    let letter = currentText.slice(0, ++index);

    document.getElementById('typewriter').textContent = letter;
    if (letter.length === currentText.length) {
      textPosition++;
      index = 0;
      setTimeout(typeWriter, 5000);
    } else {
      setTimeout(typeWriter, 80);
    }
  } else {
    textPosition = 0;
    setTimeout(typeWriter, 5000);
  }
}

typeWriter();
