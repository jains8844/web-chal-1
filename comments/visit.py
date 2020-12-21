import asyncio
from pyppeteer import launch
from redis import Redis
from rq import Queue
import requests
import json

async def main(url, environ):
    environ = json.loads(environ)
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-gpu'])
    try:
        page = await browser.newPage()
        cookies = [
            {
                'name' : 'session',
                'value' : environ.get('ADMIN_COOKIE'),
                'domain' : environ.get('DOMAIN_NAME'),
                'httpOnly' : True,
                'session' : True
            },
            {
                'name' : 'cids',
                'value' : environ.get('ADMIN_CIDS'),
                'domain' : environ.get('DOMAIN_NAME'),
                'session' : True
            }
        ]
        await page.setCookie(*cookies)
        await page.goto(url, timeout=5000)
    except Exception as e:
        raise e
    finally:
        await browser.close()


def visit_url(url, environ):
    asyncio.get_event_loop().run_until_complete(main(url, environ))

q = Queue(connection=Redis('127.0.0.1'))
