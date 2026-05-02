import time

last= 0
min_delay= 12  

def rate_limit():
    global last
    now = time.time()
    elapsed = now - last

    if elapsed < min_delay:
        time.sleep(min_delay - elapsed)

    last = time.time()