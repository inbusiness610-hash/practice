const monthYearElement = document.getElementById('month-year');
const calendarDaysElement = document.getElementById('calendar-days');
const prevBtn = document.getElementById('prev-month');
const nextBtn = document.getElementById('next-month');

const selectedDateTitle = document.getElementById('selected-date-title');
const planList = document.getElementById('plan-list');
const planInput = document.getElementById('plan-input');
const addPlanBtn = document.getElementById('add-plan-btn');

// Элементы для ИИ
const aiPromptInput = document.getElementById('ai-prompt-input');
const aiGenerateBtn = document.getElementById('ai-generate-btn');

const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

const API_URL = 'http://127.0.0.1:5000/api/plans';

const today = new Date();
let currentDate = new Date();
let selectedDate = new Date();

let plans = {};

// 1. Получение планов с сервера
async function fetchPlans() {
    try {
        const response = await fetch(API_URL);
        if (response.ok) {
            plans = await response.json();
            renderCalendar();
            updatePlansPanel();
        }
    } catch (error) {
        console.error('Ошибка подключения к серверу:', error);
    }
}

function formatDateKey(date) {
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    monthYearElement.textContent = `${months[month]} ${year}`;

    const firstDayIndex = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    const prevLastDate = new Date(year, month, 0).getDate();

    calendarDaysElement.innerHTML = '';

    for (let x = firstDayIndex; x > 0; x--) {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('inactive');
        dayDiv.textContent = prevLastDate - x + 1;
        calendarDaysElement.appendChild(dayDiv);
    }

    for (let i = 1; i <= lastDate; i++) {
        const dayDiv = document.createElement('div');
        dayDiv.textContent = i;

        const thisDate = new Date(year, month, i);
        const dateKey = formatDateKey(thisDate);

        if (
            i === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            dayDiv.classList.add('today');
        }

        if (
            selectedDate &&
            i === selectedDate.getDate() &&
            month === selectedDate.getMonth() &&
            year === selectedDate.getFullYear()
        ) {
            dayDiv.classList.add('active');
        }

        if (plans[dateKey] && plans[dateKey].length > 0) {
            dayDiv.classList.add('has-plans');
        }

        dayDiv.addEventListener('click', () => {
            selectedDate = thisDate;
            renderCalendar();
            updatePlansPanel();
        });

        calendarDaysElement.appendChild(dayDiv);
    }
}

function updatePlansPanel() {
    if (!selectedDate) return;

    const dateKey = formatDateKey(selectedDate);
    selectedDateTitle.textContent = `Планы на ${selectedDate.getDate()} ${months[selectedDate.getMonth()]}`;
    
    renderPlans(dateKey);
}

function renderPlans(dateKey) {
    planList.innerHTML = '';
    const dayPlans = plans[dateKey] || [];

    if (dayPlans.length === 0) {
        const emptyLi = document.createElement('li');
        emptyLi.textContent = 'Нет планов на этот день';
        emptyLi.style.color = 'var(--text-muted)';
        emptyLi.style.background = 'transparent';
        planList.appendChild(emptyLi);
        return;
    }

    dayPlans.forEach((planText, index) => {
        const li = document.createElement('li');
        li.textContent = planText;

        const delBtn = document.createElement('button');
        delBtn.innerHTML = '&times;';
        
        delBtn.onclick = async () => {
            try {
                const response = await fetch(`${API_URL}/delete`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ dateKey, index })
                });

                if (response.ok) {
                    await fetchPlans();
                }
            } catch (error) {
                console.error('Ошибка при удалении задачи:', error);
            }
        };

        li.appendChild(delBtn);
        planList.appendChild(li);
    });
}

// Добавление плана вручную
addPlanBtn.addEventListener('click', async () => {
    const text = planInput.value.trim();
    if (!text || !selectedDate) return;

    const dateKey = formatDateKey(selectedDate);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dateKey, text })
        });

        if (response.ok) {
            planInput.value = '';
            await fetchPlans();
        }
    } catch (error) {
        console.error('Ошибка при добавлении задачи:', error);
    }
});

// Добавление планов через ИИ
aiGenerateBtn.addEventListener('click', async () => {
    if (!selectedDate) return;

    const promptText = aiPromptInput.value.trim() || 'Спланируй продуктивный рабочий день';
    const dateKey = formatDateKey(selectedDate);

    // Меняем состояние кнопки во время загрузки
    aiGenerateBtn.disabled = true;
    aiGenerateBtn.textContent = 'Думаю...';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/generate-plans', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                dateKey: dateKey, 
                prompt: promptText 
            })
        });

        const data = await response.json();

        if (response.ok) {
            aiPromptInput.value = '';
            await fetchPlans();
        } else {
            alert('Ошибка ИИ: ' + (data.error || 'Неизвестная ошибка'));
        }
    } catch (error) {
        console.error('Ошибка при генерации ИИ:', error);
        alert('Ошибка при отправке запроса к бэкенду');
    } finally {
        aiGenerateBtn.disabled = false;
        aiGenerateBtn.textContent = 'Сгенерировать';
    }
});

planInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addPlanBtn.click();
});

aiPromptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') aiGenerateBtn.click();
});

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Старт
fetchPlans();