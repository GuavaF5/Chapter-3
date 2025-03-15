import streamlit as st
import requests
import json

st.title("Глава 3")
st.write("Вы приехали к **достопримечательности**. Вы сразу же заприметили странного мужчину в белом костюме. Он начал зазывать Вас идти с ним. Вместе вы пришли в маленькую хижину неподалёку, но как только Вы переступили через порог, подозрительный мужчина захлопнул за Вашей спиной дверь. Вы начали судорожно пытаться её открыть, но она не поддавалась. Затем вы увидел вторую дверь в противоположном конце помещения. На ней висел странный электронный замок: он выводил некое закодированное случайное послание, и для открытия двери нужно было его расшифровать.")
st.write(" **(Подсказка: ключ = secret)** ")

def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '254ee246-4b6b-49e3-b72e-29c60d84e69d',
        'Authorization': 'Basic YjA2NmI2NDAtZTU3ZC00ZDJkLTk3OWMtODRmYzkyNjAyZjI2OjczYzc1NjdkLWNjNWEtNDJmMS04ZGI3LWFhZTQxZjBlM2UxOA=='
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_token = response.json()["access_token"]
    return access_token

# Функция для отправки запроса к GigaChat
def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["message"]["content"]

# Функция для шифрования сообщения с использованием XOR
def xor_encrypt(message: str, key: str) -> str:
    encrypted_message = ""
    for i in range(len(message)):
        encrypted_message += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted_message

# Функция для генерации закодированного сообщения
def generate_encoded_message(access_token: str):
    prompt = (
        "Придумай короткое загадочное сообщение на русском языке (не более 10 слов). "
        "Выведи только это сообщение, без дополнительных пояснений."
    )
    message = send_prompt(prompt, access_token).strip()
    key = "secret"  # Ключ для XOR-шифрования
    encoded_message = xor_encrypt(message, key)
    return message, encoded_message

# Заголовок приложения

# Инициализация состояния сессии для токена
if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("Токен успешно получен")
    except Exception as e:
        st.toast(f"Не удалось получить токен: {e}")

# Инициализация состояний
if "message" not in st.session_state:
    st.session_state.message = ""
if "encoded_message" not in st.session_state:
    st.session_state.encoded_message = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "show_question" not in st.session_state:
    st.session_state.show_question = False

# Кнопка для начала игры
if st.button("Расшифровать код"):
    st.session_state.message, st.session_state.encoded_message = generate_encoded_message(st.session_state.access_token)
    st.session_state.user_answer = ""  # Сброс ответа пользователя
    st.session_state.show_question = True  # Показываем вопрос

# Если игра начата, отображаем закодированное сообщение и поле для ввода
if st.session_state.show_question:
    st.write("Закодированное сообщение:")
    st.write(st.session_state.encoded_message)

    user_answer = st.text_input("Введите расшифровку сообщения. Не забывайте, что у Вас в рюкзаке есть ноутбук, на котором можно написать код для расшифровки. Готовый код также можно взять из репозитория Третьей главы.", value=st.session_state.user_answer)

    # Если пользователь ввёл ответ, проверяем его
    if user_answer:
        st.session_state.user_answer = user_answer  # Сохраняем ответ пользователя
        if user_answer.lower() == st.session_state.message.lower():
            st.success("Правильно! Вы расшифровали сообщение! 4 глава: https://chapter-4.streamlit.app/")
        else:
            st.error(f"Неправильно. Попробуйте ещё раз")
        st.session_state.show_question = False  # Скрываем вопрос после ответа
