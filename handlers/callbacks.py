import json
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()
STATS_FILE = "data/stat.json"


def update_stat(key: str):
    try:
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"total_generations": 0, "likes": 0, "dislikes": 0}

    data[key] += 1
    with open(STATS_FILE, "w") as f:
        json.dump(data, f)


@router.callback_query(F.data.in_(["like", "dislike", "delete"]))
async def handle_feedback(callback: CallbackQuery):
    action = callback.data

    if action == "like":
        update_stat("likes")
        await callback.answer("❤️ Rahmat! Fikringiz muhim.", show_alert=False)
    elif action == "dislike":
        update_stat("dislikes")
        await callback.answer("👎 Afsus, fikringiz uchun rahmat.", show_alert=False)
    elif action == "delete":
        await callback.message.delete()


@router.message(Command("stats"))
async def stats_cmd(message: Message):
    if int(message.from_user.id) != ADMIN_ID:
        return await message.reply("❌ Siz admin emassiz.")

    try:
        with open("data/stat.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"total_generations": 0, "likes": 0, "dislikes": 0}

    await message.reply(
        f"📊 Statistika:\n"
        f"🖼 Generatsiyalar: {data['total_generations']}\n"
        f"❤️ Like: {data['likes']}\n"
        f"👎 Dislike: {data['dislikes']}"
    )


@router.message(Command("panel"))
async def admin_panel(message: Message):
    if int(message.from_user.id) != int(ADMIN_ID):
        return await message.reply("❌ Ushbu bo‘lim faqat admin uchun.")

    await message.reply(
        "🛠 <b>Admin Panel:</b>\n"
        "/stats – Statistika ko‘rish\n"
        "(Kelajakda): /broadcast – Xabar yuborish\n"
        "(Kelajakda): /users – Foydalanuvchilar ro‘yxati\n"
        "(Kelajakda): /logs – So‘rovlar tarixi"
    )
