from aiogram import Bot
from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
from database import queries
from services.attend import attend
from database.queries import delete_user, get_all_users
import asyncio

from utils.exceptions import EtuAuthException

load_dotenv(".env")

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery_app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")
celery_app.conf.timezone = "Europe/Moscow"
celery_app.conf.beat_schedule = {
    "attend_users": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=50,
            hour="8, 9, 11, 13, 15, 17",
            day_of_week="mon,tue,wed,thu,fri,sat",
        ),
    }
}
celery_app.autodiscover_tasks()


async def attend_users_async():
    print("checking users...")
    bot = Bot(os.environ.get("BOT_TOKEN", ""))
    for user in await get_all_users():
        cookies = await queries.get_cookies_by_user(user.email)
        try:
            subjects = attend(cookies)
            subjects_string = ""
            for subject in subjects:
                subjects_string += f"{subject}\n"
            if len(subjects) > 0:
                await bot.send_message(
                    chat_id=user.id,
                    text=f"Отметились на предметах✅\n{subjects_string} ",
                )
        except EtuAuthException:
            await bot.send_message(
                chat_id=user.id,
                text="Сессия личного кабинета истекла❌\nПожалуйста, авторизуйтесь заново с помощью команды /login.",
            )
            await delete_user(user.id)
    await bot.session.close()


@celery_app.task
def attend_users():
    asyncio.run(attend_users_async())