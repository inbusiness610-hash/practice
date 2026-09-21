const element = document.getElementById('title');

const words = ['Created by: Melikyan', 'Created by: Babkeni', 'Created by: Phyhsmath', 'Created by: 10E', 'Created by: Number 14', 'Created by: Narek'];
let currentWordIndex = 0;

setInterval(() => {
    if (element) {
        element.textContent = words[currentWordIndex];
        currentWordIndex = (currentWordIndex + 1) % words.length;
    }
}, 1000);

// Slot Machine Logic (3x3 grid)
const SYMBOLS = ['🍒', '🍋', '🍇', '🔔', '💎', '7️⃣'];
const SYMBOL_HEIGHT = 80;
const REEL_COUNT = 3;

let balance = 100;
let bet = 10;

const reelStrips = document.querySelectorAll('.strip');
const spinBtn = document.getElementById('spin-btn');
const ibetBtn = document.getElementById('ibet');
const sbetBtn = document.getElementById('sbet');
const balanceEl = document.getElementById('balance');
const betEl = document.getElementById('bet');
const resultEl = document.getElementById('result');

function updateUI() {
    balanceEl.textContent = `$${balance}`;
    betEl.textContent = `$${bet}`;
}
function generateStripSymbols(strip) {
    strip.innerHTML = '';
    // Создаем длинный массив из случайно перемешанных иконок
    for (let i = 0; i < 40; i++) {
        const symbol = document.createElement('div');
        symbol.classList.add('symbol');
        // Берем случайный символ из перетасованного набора
        symbol.textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
        strip.appendChild(symbol);
    }
}
function initReels() {
    reelStrips.forEach(strip => generateStripSymbols(strip));
}

function setButtonsState(disabled) {
    spinBtn.disabled = disabled;
    ibetBtn.disabled = disabled;
    sbetBtn.disabled = disabled;
}
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function spin() {
    if (balance < bet) {
        resultEl.textContent = '❌ Not enough balance!';
        return;
    }

    balance -= bet;
    updateUI();
    setButtonsState(true);
    resultEl.textContent = 'Spinning...';

    const reelResults = [];

    reelStrips.forEach((strip, index) => {
        // 1. Мгновенно сбрасываем анимацию и позицию в 0
        strip.style.transition = 'none';
        strip.style.transform = 'translateY(0px)';
        
        // 2. Генерируем совершенно НОВЫЙ порядок символов для этой ленты
        generateStripSymbols(strip);

        // Принудительно обновляем DOM, чтобы сброс сработал мгновенно
        void strip.offsetWidth;

        // 3. Выбираем случайную точку остановки ближе к концу ленты
        const targetIndex = Math.floor(Math.random() * (SYMBOLS.length)) + 25;
        
        const reelSymbols = [
            strip.children[targetIndex].textContent,
            strip.children[targetIndex + 1].textContent,
            strip.children[targetIndex + 2].textContent
        ];
        reelResults.push(reelSymbols);

        const offset = -(targetIndex * SYMBOL_HEIGHT);

        // 4. Возвращаем плавную анимацию и запускаем быстрый крутёж
        setTimeout(() => {
            strip.style.transition = 'transform 1.5s cubic-bezier(0.1, 0.9, 0.2, 1)';
            strip.classList.add('spinning');
            strip.style.transform = `translateY(${offset}px)`;
        }, index * 150);

        // Убираем размытие перед самой остановкой
        setTimeout(() => {
            strip.classList.remove('spinning');
        }, 1200 + index * 150);
    });

    setTimeout(() => {
        checkWin(reelResults);
        setButtonsState(false);
    }, 1800 + (REEL_COUNT - 1) * 150);
}
function checkWin(reelResults) {

    const topRow = [reelResults[0][0], reelResults[1][0], reelResults[2][0]];
    const middleRow = [reelResults[0][1], reelResults[1][1], reelResults[2][1]];
    const bottomRow = [reelResults[0][2], reelResults[1][2], reelResults[2][2]];

    const reel1Col = [reelResults[0][0], reelResults[0][1], reelResults[0][2]];
    const reel2Col = [reelResults[1][0], reelResults[1][1], reelResults[1][2]];
    const reel3Col = [reelResults[2][0], reelResults[2][1], reelResults[2][2]];

    const lines = [
        topRow, middleRow, bottomRow, // Horizontal
        reel1Col, reel2Col, reel3Col  // Vertical
    ];

    let totalWin = 0;
    let winningLinesCount = 0;

    lines.forEach((line) => {
        if (line[0] === line[1] && line[1] === line[2]) {
            totalWin += bet * 5;
            winningLinesCount++;
        }
    });

    if (winningLinesCount > 0) {
        balance += totalWin;
        resultEl.textContent = `🎉 WIN! Hit ${winningLinesCount} line(s) for +$${totalWin}!`;
    } else {
        resultEl.textContent = 'Try Again!';
    }
    updateUI();
}

ibetBtn.addEventListener('click', () => {
    if (bet + 5 <= balance) {
        bet += 5;
        updateUI();
    }
});

sbetBtn.addEventListener('click', () => {
    if (bet - 5 >= 5) {
        bet -= 5;
        updateUI();
    }
});

spinBtn.addEventListener('click', spin);

initReels();
updateUI();