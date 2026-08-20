import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.environ.get("GEMINI_API_KEY")
print(f"Загруженный ключ: {key[:5]}...{key[-5:] if key else 'КЛЮЧ НЕ НАЙДЕН'}")

try:
    client = genai.Client(api_key=key)
    # Используем обновленную модель
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Ответь одним словом: Работает?"
    )
    print("Ответ от Gemini:", response.text)
    print("✅ Ключ валиден и работает отлично!")
except Exception as e:
    print("❌ Ошибка при запросе к Gemini:")
    print(e)