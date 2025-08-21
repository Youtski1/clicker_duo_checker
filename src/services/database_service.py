from aiohttp.client import ClientSession
from dotenv import load_dotenv
from os import environ
from typing import List
import logging

from ..type_models import (
    User,
    Duo
)

load_dotenv()

API_URL = environ.get("API_URL")
API_KEY = environ.get("API_KEY")

logger = logging.getLogger(__name__)


class DatabaseService: 

    def __init__(
        self,
        session: ClientSession
    ):
        self.session = session


    async def get_all_duo(self):
        async with self.session.get(
            url=f"{API_URL}/duo/get_all_duo",
            headers={'api-key': API_KEY}
        ) as response:
            
            logger.info(f"Get all duos status: {response.status}")

            if response.status == 200:
                all_duo: List[Duo] = await response.json()
                return [Duo(**duo) for duo in all_duo["duos"]]
            else:
                return 
        
    async def set_stage_duo(
        self,
        owner_id: int ,
        new_stage: int
    ):
        async with self.session.post(
            url=f"{API_URL}/duo/set_stage",
            json={
                'owner_id': owner_id,
                'new_stage': new_stage
            },
            headers = {
                'api-key': API_KEY,
                "Content-Type": "application/json"
            }
        ) as response:
            return response.status
        
    async def full_recovery_duo(
        self,
        owner_id: int
    ): 
        async with self.session.post(
            url=f"{API_URL}/duo/recovery_duo",
            json={
                'owner_id': owner_id,
            },
            headers = {
                'api-key': API_KEY,
                "Content-Type": "application/json"
            }
            
        ) as response:
            return response.status
    
    async def get_user(
        self,
        telegram_id: int
    ):
        async with self.session.get(
            url=f"{API_URL}/user/{telegram_id}",
            headers={"api-key": API_KEY}
        ) as response:
            
            logger.info(f"Get user status: {response.status} {await response.text()}")

            if response.status == 200:
                data = await response.json()
                return User(**data["user"])
            else:
                return
