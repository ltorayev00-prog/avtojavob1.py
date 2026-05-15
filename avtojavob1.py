import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

API_TOKEN = "8784968001:AAHLBYoMh53CAJ3X_M-I4BbdgLulHgHDzFQ"
ADMIN_ID = 7822366507   # Admin Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Adminning reply rejimini saqlash
reply_mode = {}

@dp.message()
async def handle_user_message(message: Message):
    if message.from_user.id != ADMIN_ID:
        user_id = message.from_user.id
        user_name = message.from_user.full_name

        # Tugma yaratish
        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Javob yozish", callback_data=f"reply_{user_id}")]
        ])

        # Admin’ga xabar yuborish tugma bilan
        await bot.send_message(
            ADMIN_ID,
            f"📩 Yangi xabar:\n👤 {user_name} (ID: {user_id})\n✉️ {message.text}",
            reply_markup=buttons
        )

        await message.answer("✅ Xabaringiz admin ga yuborildi.")
    else:
        # Agar admin reply rejimida bo'lsa → foydalanuvchiga yuboradi
        if message.from_user.id == ADMIN_ID and message.from_user.id in reply_mode:
            target_id = reply_mode[ADMIN_ID]
            await bot.send_message(target_id, f"📨 Admin javobi: {message.text}")
            await message.answer("✅ Javob foydalanuvchiga yuborildi.")
            del reply_mode[ADMIN_ID]  # rejimni o'chiramiz
        else:
            await message.answer("❌ Reply rejimi yoqilmagan. Tugmani bosing.")

@dp.callback_query()
async def process_callback(callback: CallbackQuery):
    if callback.from_user.id == ADMIN_ID and callback.data.startswith("reply_"):
        target_id = int(callback.data.split("_")[1])
        reply_mode[ADMIN_ID] = target_id
        await callback.message.answer("✍️ Endi xabar yozing, u foydalanuvchiga yuboriladi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
