from aiohttp import ClientSession
import logging
import asyncio
from datetime import datetime
from aiogram import Bot
from os import environ
from dotenv import load_dotenv
import schedule
import time

from .kbs import *

from .services import DatabaseService


load_dotenv()

TOKEN = environ.get("TOKEN")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)


logger.info("Start checker!")

async def main():
    async with ClientSession() as session:
        database_service = DatabaseService(session=session)
        duos = await database_service.get_all_duo()

        if not duos:
            logger.info("Not data duos")
            return
        
        for duo in duos:
            if not duo.recovery_time:
                logger.info(f"Duo {duo.owner_id} not recovery_time")
                continue
            
            logger.info(f"{duo.recovery_time} {datetime.now()}")
            
            if datetime.strptime(duo.recovery_time, '%Y-%m-%d %H:%M:%S') < datetime.now():
                status_query = await database_service.full_recovery_duo(owner_id=duo.owner_id)
                
                if status_query == 200:
                    logger.info(f"Duo {duo.owner_id} recovery successfully")
                    user = await database_service.get_user(telegram_id=duo.owner_id)
            
                    return await bot.send_photo(
                        chat_id=user.telegram_id,
                        caption=f"@{user.username} как же хорошо, что меня больше не бьют )))",
                        photo="AgACAgIAAxkBAAIBmGigUQGtMGKzBXJdvFHpp9-gwWoIAAJVBDIb2HoJSRB4tPnJNT4TAQADAgADeAADNgQ",
                        reply_markup=kb_start_webapp()
                    )
                
                logger.info(f"Duo {duo.owner_id} recovery error status: {status_query}")
            
            else:
                recovery_time = datetime.strptime(duo.recovery_time, '%Y-%m-%d %H:%M:%S') - datetime.now()
                recovery_time_in_hours = int(recovery_time.total_seconds()) // 3600
                new_stage = 7 - (6 - recovery_time_in_hours)
                
                if new_stage == duo.stage or new_stage == 1:
                    continue

                status_query = await database_service.set_stage_duo(
                    owner_id=duo.owner_id,
                    new_stage=new_stage
                )

                logger.info(f"Update stage duo {duo.owner_id} on {new_stage} status: {status_query}")



def start_main():
    asyncio.run(main=main())


schedule.every(1).minutes.do(start_main)

while True:
  schedule.run_pending()
  time.sleep(1)