const SYMBOLS = ['🍒', '🍋', '🍇', '🔔', '💎', '7️⃣'];
const SYMBOL_HEIGHT = 80;
const REEL_COUNT = 3;

// Локальные переменные UI (не бизнес-логика!)
let currentBalance = 0;
let bet = 10;

const reelStrips = document.querySelectorAll('.strip');
const spinBtn = document.getElementById('spin-btn');
const ibetBtn = document.getElementById('ibet');
const sbetBtn = document.getElementById('sbet');
const balanceEl = document.getElementById('balance');
const betEl = document.getElementById('bet');
const resultEl = document.getElementById('result');

function updateUI() {
    balanceEl.textContent = `$${currentBalance}`;
    betEl.textContent = `$${bet}`;
}

// Запрашиваем баланс у Flask при старте
async function syncBalanceWithServer() {
    try {
        const res = await fetch('/api/state');
        const data = await res.json();
        currentBalance = data.balance; // Обновляем локальное отображение
        updateUI();
    } catch (e) {
        resultEl.textContent = 'Server connection error!';
    }
}

function generateStripSymbols(strip, finalSymbols = null) {
    strip.innerHTML = '';
    for (let i = 0; i < 40; i++) {
        const symbol = document.createElement('div');
        symbol.classList.add('symbol');
        symbol.textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
        strip.appendChild(symbol);
    }

    if (finalSymbols) {
        const targetIndex = 25;
        strip.children[targetIndex].textContent = finalSymbols[0];
        strip.children[targetIndex + 1].textContent = finalSymbols[1];
        strip.children[targetIndex + 2].textContent = finalSymbols[2];
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

async function spin() {
    setButtonsState(true);
    resultEl.textContent = 'Spinning...';

    try {
        // Просто слаем ставку на бэкенд, а бэкенд сам решит, хватает ли баланса
        const response = await fetch('/api/spin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bet })
        });

        const data = await response.json();

        // Если сервер вернул ошибку (например, 400 Bad Request — не хватило денег)
        if (!response.ok) {
            resultEl.textContent = `❌ ${data.error}`;
            if (data.balance !== undefined) currentBalance = data.balance;
            updateUI();
            setButtonsState(false);
            return;
        }

        const { balance: newBalance, totalWin, winningLinesCount, reelResults } = data;

        // Запускаем визуальную крутилку под присланный с бэкенда результат
        reelStrips.forEach((strip, index) => {
            strip.style.transition = 'none';
            strip.style.transform = 'translateY(0px)';
            
            generateStripSymbols(strip, reelResults[index]);

            void strip.offsetWidth;

            const targetIndex = 25;
            const offset = -(targetIndex * SYMBOL_HEIGHT);

            setTimeout(() => {
                strip.style.transition = 'transform 1.5s cubic-bezier(0.1, 0.9, 0.2, 1)';
                strip.classList.add('spinning');
                strip.style.transform = `translateY(${offset}px)`;
            }, index * 150);

            setTimeout(() => {
                strip.classList.remove('spinning');
            }, 1200 + index * 150);
        });

        // В конце анимации устанавливаем новый баланс, который дал Flask
        setTimeout(() => {
            currentBalance = newBalance;
            if (winningLinesCount > 0) {
                resultEl.textContent = `🎉 WIN! Hit ${winningLinesCount} line(s) for +$${totalWin}!`;
            } else {
                resultEl.textContent = 'Try Again!';
            }
            updateUI();
            setButtonsState(false);
        }, 1800 + (REEL_COUNT - 1) * 150);

    } catch (err) {
        resultEl.textContent = 'Server connection error!';
        setButtonsState(false);
    }
}

// Кнопки изменения ставки
ibetBtn.addEventListener('click', () => {
    bet += 5;
    updateUI();
});

sbetBtn.addEventListener('click', () => {
    if (bet - 5 >= 5) {
        bet -= 5;
        updateUI();
    }
});

spinBtn.addEventListener('click', spin);

// Старт
initReels();
syncBalanceWithServer();