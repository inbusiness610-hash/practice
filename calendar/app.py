import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from google import genai

# Загружаем переменные окружения из файла .env (если он есть)
load_dotenv()

# template_folder='.' и static_folder='.' позволяют держать файлы рядом
app = Flask(__name__)
CORS(app)

DATA_FILE = "plans.json"


ai_client = None
if os.environ.get("GEMINI_API_KEY"):
    ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def load_plans():
    """Загрузка планов из JSON-файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_plans_to_file(plans):
    """Сохранение планов в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)


# ==========================================================================
# Main Routes
# ==========================================================================

@app.route("/")
def index():
    weekdays = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
    return render_template(
        "index.html", 
        weekdays=weekdays, 
        page_title="Планировщик и Календарь"
    )


# ==========================================================================
# API Endpoints for Plan Management
# ==========================================================================

@app.route("/api/plans", methods=["GET"])
def get_plans():
    """Получить все сохраненные планы."""
    return jsonify(load_plans())


@app.route("/api/plans", methods=["POST"])
def add_plan():
    """Добавить один план вручную."""
    data = request.json
    date_key = data.get("dateKey")
    text = data.get("text")

    if not date_key or not text:
        return jsonify({"error": "Некорректные данные"}), 400

    plans = load_plans()
    if date_key not in plans:
        plans[date_key] = []

    plans[date_key].append(text)
    save_plans_to_file(plans)

    return jsonify({"message": "Успешно добавлено", "plans": plans[date_key]}), 201


@app.route("/api/plans/edit", methods=["POST"])
def edit_plan():
    """Изменить текст существующего плана."""
    data = request.json
    date_key = data.get("dateKey")
    index = data.get("index")
    new_text = data.get("text")

    if not date_key or index is None or not new_text:
        return jsonify({"error": "Некорректные данные"}), 400

    plans = load_plans()

    if date_key in plans and 0 <= index < len(plans[date_key]):
        plans[date_key][index] = new_text
        save_plans_to_file(plans)
        return jsonify({"message": "План успешно обновлен", "plans": plans[date_key]}), 200

    return jsonify({"error": "План не найден"}), 404


@app.route("/api/plans/delete", methods=["POST"])
def delete_plan():
    """Удалить выбранный план."""
    data = request.json
    date_key = data.get("dateKey")
    index = data.get("index")

    plans = load_plans()

    if date_key in plans and 0 <= index < len(plans[date_key]):
        plans[date_key].pop(index)
        if len(plans[date_key]) == 0:
            del plans[date_key]
        save_plans_to_file(plans)
        return jsonify({"message": "Успешно удалено"}), 200

    return jsonify({"error": "План не найден"}), 404


# ==========================================================================
# API Endpoints for Gemini AI Integration
# ==========================================================================

@app.route("/api/generate-plans", methods=["POST"])
def generate_plans():
    """Автоматическая генерация списка планов с помощью Gemini AI."""
    if not ai_client:
        return jsonify({
            "error": "GEMINI_API_KEY не установлен. Проверьте ваш .env файл или переменные окружения."
        }), 500

    data = request.json
    date_key = data.get("dateKey")
    user_prompt = data.get("prompt", "Спланируй продуктивный рабочий день")

    if not date_key:
        return jsonify({"error": "Дата не указана"}), 400

    system_instruction = (
        "Ты — умный персональный ассистент-планировщик. "
        "Пользователь дает тему или цель дня, а ты генерируешь список из 3–5 четких, коротких и практичных задач. "
        "Твой ответ должен содержать ТОЛЬКО валидный JSON-массив строк без каких-либо вводных слов, пояснений или разметки Markdown. "
        "Пример ответа: [\"Сделать утреннюю зарядку\", \"Разобрать рабочую почту\", \"Прочитать 1 главу книги\"]"
    )

    try:
        response = ai_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Сгенерируй задачи на день по цели/теме: {user_prompt}",
            config={"system_instruction": system_instruction}
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            if raw_text.endswith("```"):
                raw_text = raw_text.rsplit("\n", 1)[0]
        
        generated_tasks = json.loads(raw_text.strip())

        if not isinstance(generated_tasks, list):
            return jsonify({"error": "ИИ вернул неверный формат данных"}), 500
        
        plans = load_plans()
        if date_key not in plans:
            plans[date_key] = []

        plans[date_key].extend(generated_tasks)
        save_plans_to_file(plans)

        return jsonify({
            "message": "Планы успешно сгенерированы", 
            "plans": plans[date_key]
        }), 201

    except json.JSONDecodeError:
        return jsonify({"error": "Не удалось распарсить ответ от ИИ как JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Ошибка генерации: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)