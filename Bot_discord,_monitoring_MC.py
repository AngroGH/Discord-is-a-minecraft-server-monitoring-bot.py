import discord
from mcstatus import JavaServer
import asyncio

TOKEN = 'Токен дискорд бота'
MINECRAFT_SERVER_ADDRESS = 'Айпи сервера что вы хотите отслеживать'
CHECK_INTERVAL = 60  # Время в секундах между проверками

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_server_status():
    await client.wait_until_ready()
    while not client.is_closed():
        server = JavaServer.lookup(MINECRAFT_SERVER_ADDRESS)
        try:
            status = server.status()
            await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{status.players.online} игроков в сети"))
        except Exception as e:
            print(f"Ошибка при проверке статуса сервера: {e}")
            await client.change_presence(status=discord.Status.offline)
        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f'Вошел в систему как {client.user}')

@client.event
async def on_disconnect():
    await client.change_presence(status=discord.Status.offline)

@client.event
async def on_connect():
    await client.change_presence(status=discord.Status.idle)

async def main():
    async with client:
        client.loop.create_task(check_server_status())
        await client.start(TOKEN)

# Для отладки выведем токен. При надобности можете удалить сроку ниже.
print(f"Используется токен бота: {TOKEN}")
print("Бот сделан командой BastionTeam")

asyncio.run(main())