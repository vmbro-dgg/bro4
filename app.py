# import asyncio
# import random
# import os
# from camoufox import AsyncCamoufox
# from camoufox import DefaultAddons

# URL_BROWSER = os.getenv("URL_BROWSER")
# URL = os.getenv("URL")
# EMAIL = os.getenv("EMAIL")
# SENHA = os.getenv("SENHA")
# MINUTOS = int(os.getenv("MINUTOS", 5))
# NUM_BROWSERS = int(os.getenv("NUM_BROWSERS", 1))
# MAX_RETRIES = 3
# DELAY = 50


# async def run_browser(i, email):
#     async with AsyncCamoufox(
#         headless=True,
#         # screen=Screen(max_width=1920, max_height=1080),
#         humanize=0.2,  # humanize=True,
#         exclude_addons=[DefaultAddons.UBO],
#         # geoip=True,
#     ) as browser:
#         page = await browser.new_page()
#         login = random.choice([True, False])
#         if login and email:
#             await page.goto(f"{URL_BROWSER}/auth", wait_until="domcontentloaded")
#             await page.wait_for_selector("#email")
#             await page.type("#email", email, delay=10)
#             await page.type("#password", SENHA, delay=10)
#             await page.click("button[type='submit']")
#             await page.wait_for_timeout(10000)
#         await page.goto(f"{URL_BROWSER}/create", wait_until="domcontentloaded")
#         await page.wait_for_timeout(5000)
#         await page.wait_for_selector("#url")
#         await page.type("#url", URL, delay=10)
#         await page.wait_for_timeout(2000)
#         await page.wait_for_selector("button[type='submit']")
#         await page.click("button[type='submit']")
#         await page.wait_for_timeout(MINUTOS * 60 * 1000)
#         await page.screenshot(path=f"screen_{i+1}.png", full_page=True)

# # 🔥 NOVA FUNÇÃO COM DELAY


# async def run_with_delay(i):
#     # await asyncio.sleep(i * DELAY)
#     await asyncio.sleep(DELAY)
#     emails = [e.strip() for e in EMAIL.splitlines() if e.strip()]
#     email = random.choice(emails)
#     print(f"🚀 Iniciando navegador {i+1} com email: {email}")
#     await run_browser(i, email)


# async def main():
#     attempts = 0
#     while True:
#         try:
#             print("🚀 Iniciando navegadores...")
#             await asyncio.gather(*[run_with_delay(i) for i in range(NUM_BROWSERS)])
#             print("✅ Finalizado com sucesso")
#             break
#         except Exception as e:
#             attempts += 1
#             print(f"❌ Erro (tentativa {attempts}): {e}")
#             if MAX_RETRIES and attempts >= MAX_RETRIES:
#                 print("🛑 Limite de tentativas atingido")
#                 break
#             print("♻️ Reiniciando em 5 segundos...")
#             await asyncio.sleep(5)

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import random
import os
from playwright.async_api import async_playwright

URL_BROWSER = os.getenv("URL_BROWSER")
URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")
MINUTOS = int(os.getenv("MINUTOS", 5))
NUM_BROWSERS = int(os.getenv("NUM_BROWSERS", 1))
MAX_RETRIES = 3
DELAY = 50


async def run_browser(i, email):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        page = await browser.new_page()
        login = random.choice([True, False])
        if login and email:
            await page.goto(f"{URL_BROWSER}/auth", wait_until="domcontentloaded")
            await page.wait_for_selector("#email")
            await page.type("#email", email, delay=10)
            await page.type("#password", SENHA, delay=10)
            await page.click("button[type='submit']")
            await page.wait_for_timeout(10000)
        await page.goto(f"{URL_BROWSER}/create", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#url")
        await page.type("#url", URL, delay=10)
        await page.wait_for_timeout(2000)
        await page.wait_for_selector("button[type='submit']")
        await page.click("button[type='submit']")
        await page.wait_for_timeout(MINUTOS * 60 * 1000)
        await page.screenshot(path=f"screen_{i+1}.png", full_page=True)

# 🔥 NOVA FUNÇÃO COM DELAY


async def run_with_delay(i):
    # await asyncio.sleep(i * DELAY)
    await asyncio.sleep(DELAY)
    emails = [e.strip() for e in EMAIL.splitlines() if e.strip()]
    email = random.choice(emails)
    print(f"🚀 Iniciando navegador {i+1} com email: {email}")
    await run_browser(i, email)


async def main():
    attempts = 0
    while True:
        try:
            print("🚀 Iniciando navegadores...")
            await asyncio.gather(*[run_with_delay(i) for i in range(NUM_BROWSERS)])
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

