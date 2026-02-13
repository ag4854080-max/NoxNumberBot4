import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

BOT_TOKEN = os.getenv("8153568939:AAEm69ANJFiqJ-7Ym3tOFF1B8vRdBh7WNi4")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ساخت دکمه شیشه‌ای
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛒 ورودی سیستم خرید",
                callback_data="enter_buy_system"
            )
        ]
    ])
    return keyboard


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "به ربات خوش اومدی 👋",
        reply_markup=main_menu()
    )


@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "enter_buy_system":
        await callback.answer()
        await callback.message.edit_text(
            "شما وارد سیستم خرید شدید ✅",
            reply_markup=main_menu()
        )


# بخش Webhook برای Render
async def handle(request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()


async def on_startup(app):
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)
    print("Bot started")


app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=int(os.environ.get("PORT", 10000)))
