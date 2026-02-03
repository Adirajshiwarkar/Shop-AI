from duckduckgo_search import DDGS
import json

def test_ddg():
    print("Testing DDG connection...")
    try:
        with DDGS() as ddgs:
            print("1. Testing 'api' backend...")
            try:
                r = list(ddgs.text("test", backend="api", max_results=2))
                print(f"   Success: {len(r)} results")
            except Exception as e:
                print(f"   Failed: {e}")

            print("2. Testing 'html' backend...")
            try:
                r = list(ddgs.text("test", backend="html", max_results=2))
                print(f"   Success: {len(r)} results")
            except Exception as e:
                print(f"   Failed: {e}")
                
            print("3. Testing 'lite' backend...")
            try:
                r = list(ddgs.text("test", backend="lite", max_results=2))
                print(f"   Success: {len(r)} results")
            except Exception as e:
                print(f"   Failed: {e}")

    except Exception as e:
        print(f"Fatal init error: {e}")

if __name__ == "__main__":
    test_ddg()
