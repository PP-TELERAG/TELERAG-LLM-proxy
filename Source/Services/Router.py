import httpx


async def notify_service(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                return False
            try:
                return response.json()
            except ValueError:
                return True
        except Exception as e:
            print(f"Exception occurred: {e}")  # TODO: log exception
            return False
