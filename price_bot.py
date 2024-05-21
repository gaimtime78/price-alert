import requests
import schedule
import time
import asyncio
from telegram import Bot, error

# Fungsi untuk mendapatkan harga terkini
def get_current_price(crypto, vs_currency):
    url = f'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': crypto,
        'vs_currencies': vs_currency
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data[crypto][vs_currency]

# Fungsi untuk mengirim peringatan melalui Telegram secara asynchronous
async def send_telegram_alert(token, chat_id, message):
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except error.TimedOut:
        print("Request timed out. Retrying...")
    except Exception as e:
        print(f"An error occurred: {e}")

# Fungsi untuk memeriksa harga dan mengirim pesan
async def check_and_send_price_alert():
    crypto = 'bitcoin'
    vs_currency = 'idr'
    telegram_token = '6971571599:AAFzqXlOizhxNUFxB06PIYu0k6sB7eRMHHU'  # API token Anda
    chat_id = '@hellofromherebro/3'  # Ganti dengan username grup/chat Anda

    current_price = get_current_price(crypto, vs_currency)
    print(f"Current {crypto} price: Rp{current_price}")
    message = f"{crypto.capitalize()} price is currently Rp{current_price}."
    await send_telegram_alert(telegram_token, chat_id, message)

# Fungsi untuk menjalankan schedule di event loop
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Mengatur schedule untuk menjalankan check_and_send_price_alert setiap 10 detik
def schedule_job():
    asyncio.run(check_and_send_price_alert())

schedule.every(10).seconds.do(schedule_job)

# Menjalankan schedule
if __name__ == "__main__":
    run_schedule()
