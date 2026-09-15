const element = document.getElementById('title');

const words = [ 'Created by: Melikyan', 'Created by: Babkeni', 'Created by: Phyhsmath', 'Created by: 10E', 'Created by: Number 14', 'Created by: Narek'];
let currentWordIndex = 0;

setInterval(() => {
    element.textContent = words[currentWordIndex];
    currentWordIndex = (currentWordIndex + 1) % words.length;
}, 1000);

