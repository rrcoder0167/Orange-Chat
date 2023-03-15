const oopsText = document.querySelector(".oops");
const oopsTextContent = oopsText.textContent;
oopsText.textContent = "";

let i = 0;
const typeEffect = setInterval(() => {
  oopsText.textContent += oopsTextContent.charAt(i);
  i++;
  if (i > oopsTextContent.length - 1) {
    clearInterval(typeEffect);
  }
}, 30);

const dots = document.querySelectorAll('.dot');
const error_msg = document.querySelector('.error-message');

setTimeout(() => {
  dots.forEach(dot => {
    dot.style.animation = 'none';
    dot.style.backgroundColor = '#f03a49';
    dot.style.transform = 'translateY(-20px)';
    dot.style.animation = 'orangeDisappear 1s linear forwards';
  });
  error_msg.innerHTML = "Sorry, we can't find this page.";
  error_msg.style.color = '#f03a49';
}, 5000);

