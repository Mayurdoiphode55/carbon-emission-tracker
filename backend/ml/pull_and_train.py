import os, requests, time

API_BASE = os.getenv("API_BASE", "http://api:8000")

for i in range(5):
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        print("API health:", r.json())
        break
    except Exception as e:
        print("Retrying connection:", e)
        time.sleep(5)
else:
    raise SystemExit("API not reachable")

print("ML worker ready to proceed with training...")
time.sleep(60)
