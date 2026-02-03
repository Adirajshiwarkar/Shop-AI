import asyncio
from search_engine import SearchEngine

async def test():
    print("Initializing Search Engine...")
    se = SearchEngine()
    
    query = "latest iphone 16"
    print(f"\nSearching for: {query}")
    results = await se.search(query)
    
    print(f"\nFound {len(results)} results:")
    for res in results:
        print(f"[{res.get('source', 'unknown').upper()}] {res['name']}")
        print(f"   Image: {res.get('image_url')}")
        print(f"   Link: {res.get('link')}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test())
