from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot import bot
from services.modelslab import query_img2img_modelslab
from keyboards.default import result_buttons

router = Router()

class EditState(StatesGroup):
    waiting_photo = State()
    waiting_prompt = State()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await message.reply("👋 Salom! Rasmni o'zgartirish uchun /edit deb yozing.")
    await state.clear()

@router.message(Command("edit"))
async def edit_cmd(message: Message, state: FSMContext):
    await state.set_state(EditState.waiting_photo)
    await message.reply("📷 Iltimos, rasm yuboring.")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.reply("📩 Yordam uchun: @httpswnx")

@router.message(F.photo, EditState.waiting_photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    await state.update_data(file_id=photo.file_id)
    await state.set_state(EditState.waiting_prompt)
    await message.reply("✅ Rasm qabul qilindi! Endi prompt kiriting.")

@router.message(F.text, EditState.waiting_prompt)
async def handle_prompt(message: Message, state: FSMContext):
    prompt = message.text.strip()
    data = await state.get_data()

    if 'file_id' not in data:
        await message.reply("⚠️ Avval rasm yuboring.")
        await state.set_state(EditState.waiting_photo)
        return

    try:
        await message.reply("🧠 AI rasm ustida ishlamoqda, kuting...")

        file = await bot.get_file(data['file_id'])
        image_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"

        result_bytes = query_img2img_modelslab(image_url, prompt)
        photo = BufferedInputFile(result_bytes, filename="ai_result.jpg")

        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption="💬 Izohingiz uchun rahmat!",
            reply_markup=result_buttons()
        )
    except Exception:
        await message.reply(
            "⚠️ Rasm generatsiya bo‘lmadi. Iltimos, promptni aniq va ingliz tilida yozing.\n"
            "Masalan: <i>futuristic robot in neon city</i>"
        )
    finally:
        await state.clear()
