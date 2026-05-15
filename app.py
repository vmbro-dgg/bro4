import asyncio
import random
import os
from playwright.async_api import async_playwright

URL_BROWSER = os.getenv("URL_BROWSER")
URL_EMAIL = os.getenv("URL_EMAIL")
URL = os.getenv("URL", "")
SENHA = os.getenv("SENHA")
MINUTOS = int(os.getenv("MINUTOS", 5))
NUM_BROWSERS = random.randint(3, 5)

sucessos = 0


async def run_browser(i):
    global sucessos
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://smailpro.com/temporary-email", wait_until="domcontentloaded")
            await page.wait_for_selector('div[x-text="selectedEmail.address"]')
            email = await page.inner_text('div[x-text="selectedEmail.address"]')
            # Registrar
            pageTab = await browser.new_page()
            await pageTab.goto(f"{URL_BROWSER}/auth/register", wait_until="domcontentloaded")
            await pageTab.wait_for_timeout(5000)
            await pageTab.wait_for_selector("#firstname")
            await pageTab.type("#firstname", "Rohn")
            await pageTab.type("#lastname", "Eoe")
            await pageTab.type("#email", email)
            await pageTab.type("#password", SENHA)
            await pageTab.type("#repeatPassword", SENHA)
            await pageTab.click("#terms")
            await pageTab.click("button[type='submit']")
            await pageTab.wait_for_timeout(10000)
            await page.bring_to_front()
            await page.wait_for_timeout(2000)
            await page.wait_for_selector("text=Browser.lol", timeout=10000)
            await page.click("text=Browser.lol")
            frame = page.frame_locator("iframe[srcdoc]")
            code = await frame.locator(".verification-code").text_content(timeout=10000)
            await pageTab.bring_to_front()
            await page.close()
            await pageTab.wait_for_selector("#code", timeout=10000)
            await pageTab.type("#code", code, delay=10)
            await pageTab.click("button[type='submit']")
            await pageTab.wait_for_timeout(10000)
            # SUCESSO
            sucessos += 1
            print(email)
            if sucessos >= NUM_BROWSERS:
                print("🎯 3 sucessos atingidos!")
            await pageTab.goto(f"{URL_BROWSER}/create", wait_until="domcontentloaded")
            await pageTab.wait_for_timeout(5000)
            await pageTab.wait_for_selector("#url")
            await pageTab.type("#url", URL, delay=10)
            await pageTab.wait_for_timeout(2000)
            await pageTab.click("button[type='submit']")
            await pageTab.wait_for_timeout(MINUTOS * 60 * 1000)

    except Exception as e:
        print(f"❌ Browser {i+1} erro: {e}")


async def run_delay(i):
    while True:
        await run_browser(i)
        await asyncio.sleep(50)


async def main():
    print("🚀 Iniciando browsers...")
    await asyncio.gather(*[run_delay(i) for i in range(NUM_BROWSERS)])

if __name__ == "__main__":
    asyncio.run(main())
