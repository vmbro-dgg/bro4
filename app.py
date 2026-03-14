import asyncio
import random
import os
from camoufox import AsyncCamoufox
# from dotenv import load_dotenv
# load_dotenv()

URL_BROWSER = os.getenv("URL_BROWSER")
URL = random.choice(os.getenv("URL"))
MINUTOS = int(os.getenv("MINUTOS"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES"))  # None = infinito


async def run_browser():
    async with AsyncCamoufox(
        headless=True,
        # screen=Screen(max_width=1920, max_height=1080),
        humanize=0.2,  # humanize=True,
        # geoip=True,
    ) as browser:
        page = await browser.new_page()
        await page.goto(URL_BROWSER, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#url")
        await page.fill("#url", URL)
        await page.wait_for_timeout(2000)
        await page.click("text=Launch Workspace")
        minutos = MINUTOS
        # await asyncio.sleep(minutos * 60)
        await page.wait_for_timeout(minutos * 60 * 1000)
        await page.screenshot(path="screen.png", full_page=True)


async def main():
    attempts = 0
    while True:
        try:
            print("🚀 Iniciando navegador...")
            await run_browser()
            print("✅ Finalizado com sucesso")
            break
        except Exception as e:
            attempts += 1
            print(f"❌ Erro (tentativa {attempts}): {e}")
            if MAX_RETRIES and attempts >= MAX_RETRIES:
                print("🛑 Limite de tentativas atingido")
                break
            print("♻️ Reiniciando em 5 segundos...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
