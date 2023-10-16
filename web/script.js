// script.js
const star = document.querySelector('.star');
const statsBlock = document.querySelector('.stats');

star.addEventListener('click', () => {
    if (statsBlock.style.display === 'none') {
        statsBlock.style.display = 'block';
    } else {
        statsBlock.style.display = 'none';
    }
});