import asyncio
import random
import os
from camoufox import AsyncCamoufox
from camoufox import DefaultAddons
# from dotenv import load_dotenv
# load_dotenv()

# URL_BROWSER = os.getenv("URL_BROWSER")
# URL = random.choice(os.getenv("URL"))
# URL_BROWSER = "https://browser.lol/create"
# URL = "https://webminer.pages.dev/?algorithm=cwm_minotaurx&host=minotaurx.na.mine.zpool.ca&port=7019&worker=DRZycY3Fm8xCdm9GS13JStNxfRUT3ihHXm&password=c%3DDOGE&workers=20"
# MINUTOS = 5
# MAX_RETRIES = 3  # None = infinito

URL_BROWSER = os.getenv("URL_BROWSER")
URL = os.getenv("URL")
MINUTOS = int(os.getenv("MINUTOS", 5))
MAX_RETRIES = 3

async def run_browser(i):
    async with AsyncCamoufox(
        headless=True,
        # screen=Screen(max_width=1920, max_height=1080),
        humanize=0.2,  # humanize=True,
        exclude_addons=[DefaultAddons.UBO],
        # geoip=True,
    ) as browser:
        page = await browser.new_page()
        await page.goto(URL_BROWSER, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#url")
        await page.type("#url", URL, delay=10)
        await page.wait_for_timeout(2000)
        await page.wait_for_selector("button[type='submit']")
        await page.click("button[type='submit']")
        await page.wait_for_timeout(MINUTOS * 60 * 1000)
        await page.screenshot(path=f"screen_{i+1}.png", full_page=True)


async def main():
    # print("🚀 Iniciando navegadores...")
    # await asyncio.gather(*[run_browser(i) for i in range(2)])
    attempts = 0
    while True:
        try:
            print("🚀 Iniciando navegadores...")
            await asyncio.gather(*[run_browser(i) for i in range(2)])
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
