import time

import requests
from requests_toolbelt.adapters.socket_options import TCPKeepAliveAdapter

SERVER_URL = 'http://127.0.0.1:8080'

RETRY_TIMEOUT = 5
LONG_POLL_TIMEOUT = 90  # seconds

session = requests.Session()
keep_alive = TCPKeepAliveAdapter(
    idle=3,  # start sending keepalives after N secs of last successful ack
    count=1,  # aggressively close the connection if X are down in a row
    interval=1  # re-send a keepalive every Y seconds.
)
session.mount(SERVER_URL, keep_alive)

while True:
    try:
        res = session.get(
            SERVER_URL,
            timeout=LONG_POLL_TIMEOUT,
            headers={
                'Host': None,
                'User-Agent': None,
                'Accept-Encoding': None,
            }
        )
        print(res.status_code)
    except Exception as e:
        print('Something happened !\n', e)
        time.sleep(RETRY_TIMEOUT)
