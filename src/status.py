#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.10

import asyncio
import os
import time

import aiohttp
import dotenv
from json import loads
from loguru import logger


class MyVk:
    def __init__(self):
        """
        Class for simple use vk api
        """

        self.token = dotenv.dotenv_values(f"{os.getcwd()}/.env")['token']
        self.session = aiohttp.ClientSession()

    async def get_all_friends(self) -> list:
        """
        Get all friends
        :return: list of friends
        """

        url = 'https://api.vk.com/method/friends.get'
        params = {'access_token': self.token, 'v': '5.131'}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            logger.debug(data)
            return data['response']['items']

    async def get_all_online_friends(self) -> list:
        """
        Get all online friends
        :return: list of online friends
        """

        url = 'https://api.vk.com/method/friends.getOnline'
        params = {'access_token': self.token, 'v': '5.131'}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            logger.debug(data)
            return data['response']

    async def get_recent_friend(self) -> str:
        """
        Get recent friends
        :return: list of recent friends
        """

        url = 'https://api.vk.com/method/friends.getRecent'
        params = {'access_token': self.token, 'v': '5.131', 'count': 1}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            logger.debug(data)
            return data['response'][0]

    async def get_user_info(self, user_id: str) -> str:
        """
        Get user info
        :param user_id: user id
        :return: user info
        """

        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token, 'v': '5.131', 'user_ids': user_id}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            return f"{data['response'][0]['first_name']} {data['response'][0]['last_name']}"

    async def set_status(self, text: str) -> None:
        """
        Set status from text
        :param text: text to set
        :return: None
        """

        url = 'https://api.vk.com/method/status.set'
        params = {'access_token': self.token, 'v': '5.131', 'text': text}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            logger.debug(data)


async def main():
    my_vk = MyVk()

    while True:
        online_friends = await my_vk.get_all_online_friends()
        await asyncio.sleep(1)

        recent_friend = await my_vk.get_recent_friend()
        await asyncio.sleep(1)

        user_info = await my_vk.get_user_info(recent_friend)
        await asyncio.sleep(1)

        time_is = time.localtime()
        time_is_str = time.strftime("%d/%m/%Y", time_is)

        text = f"Friends online: {len(online_friends)} \n Last application from: {user_info} \n Today is {time_is_str}"

        await my_vk.set_status(text)

        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
