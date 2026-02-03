import asyncio
from duckduckgo_search import DDGS

async def test():
    print("Testing DDGS Images...")
    from duckduckgo_search import DDGS
    try:
        # Try images
        results = list(DDGS().images("iphone 16", max_results=2))
        print(f"Image Results: {results}")
    except Exception as e:
        print(f"Image Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
