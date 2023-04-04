import requests
import datetime
from config import open_hava_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Merhaba! Lütfen şehir adını İngilizce olarak yazın, size hava durumu verilerini göndereceğim')

@dp.message_handler()
async def get_hava(message: types.Message):

    code_to_smile = {
        'Clear': 'Temizle \U00002600',
        'Clouds': 'Bulutlu \U00002601',
        'Rain': 'Yağmur \U00002614',
        'Drizzle': 'Yağmur \U00002614',
        'Thunderstorm': 'Fırtına \U000026A1',
        'Snow': 'Kar \U0001F328',
        'Mist': 'Sis \U0001F32B'






    }
    try:

        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&appid={open_hava_token}&units=metric")

        data = r.json()
        # pprint(data)


        city = data['name']
        humidity = data['main']['humidity']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Dışarıdaki hava nasıl olur bilmiyorum, pencereden bakın\n'


        t = data['main']['temp']
        if 0 < t < 10:
            t = 'Dışarısı soğuk, bir şeyler giyin \U0001F62C'
        elif 10 < t < 20:
            t = 'Dış hava normal, dışarı çıkabilirsiniz \U0001F642'
        elif -10 < t < 0:
            t = 'Dışarısı çok soğuk, elbise ısıtıcı \U0001F62C'
        elif 20 < t:
            t = 'Hava çok iyi, ne isterseniz takın ve yürüyüşe gidin \U0001F44D'
        elif -20 > t:
            t = 'Çok soğuk, dışarı çıkmamak daha iyi \U0001F645'



        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
              f'Hava durumu: {city} \nSıcaklık: {cur_weather}C° {wd}\n{t}\n'
              f'Nem oranı: {humidity}%\nBaskı yapmak: {pressure}mm Hg Sanat.\nRüzgâr: {wind}м/с\n'
              f'Gün doğumu: {sunrise_timestamp}\nGün batımı: {sunset_timestamp}\nGün uzunluğu: {length_of_the_day}\n'
              f'İyi günler \U0001F91A'
              )
    except:
        await message.reply('\U0001F937 Şehir adını kontrol et \U0001F937')



if __name__ == '__main__':
    executor.start_polling(dp)