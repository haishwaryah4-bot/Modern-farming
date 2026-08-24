import asyncio
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from api.index import app

async def test_asgi_call(path, method="GET", payload=None):
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "headers": []
    }
    
    body_sent = []
    status_sent = []
    
    async def receive():
        if payload is not None:
            return {"body": json.dumps(payload).encode("utf-8"), "more_body": False}
        return {"body": b"", "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            status_sent.append(msg["status"])
        elif msg["type"] == "http.response.body":
            body_sent.append(msg.get("body", b""))

    await app(scope, receive, send)
    
    raw_body = b"".join(body_sent).decode("utf-8", errors="ignore")
    status = status_sent[0] if status_sent else 500
    return status, raw_body

async def main():
    print("=" * 70)
    print("TESTING VERCEL ASGI ENTRYPOINT (api/index.py)")
    print("=" * 70)
    
    # 1. GET /api/health
    status, body = await test_asgi_call("/api/health", "GET")
    print(f"1. GET /api/health -> Status: {status}")
    print(f"   Response: {body[:150]}")
    assert status == 200, "GET /api/health failed"

    # 2. POST /api/chat
    status, body = await test_asgi_call("/api/chat", "POST", {"message": "What is precision agriculture?"})
    print(f"\n2. POST /api/chat -> Status: {status}")
    print(f"   Response Excerpt: {body[:250]}...")
    assert status == 200, "POST /api/chat failed"
    data = json.loads(body)
    assert "answer" in data, "No answer in chat response"
    assert len(data.get("citations", [])) > 0, "No citations in chat response"

    # 3. POST /api
    status, body = await test_asgi_call("/api", "POST", {"message": "What is fertigation?"})
    print(f"\n3. POST /api -> Status: {status}")
    print(f"   Response Excerpt: {body[:250]}...")
    assert status == 200, "POST /api failed"

    # 4. GET /
    status, body = await test_asgi_call("/", "GET")
    print(f"\n4. GET / -> Status: {status}")
    print(f"   Response Excerpt: {body[:150]}...")
    assert status == 200, "GET / failed"

    print("\n" + "=" * 70)
    print("🎉 ALL VERCEL SERVERLESS ASGI ENTRYPOINT TESTS PASSED (100%)!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
