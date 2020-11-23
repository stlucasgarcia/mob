import aiohttp


async def request(url: str, params: dict):  # TODO: REMOVE REQUEST FROM INIT
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            return await response.content.read()
