import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class SearchEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', csv_path='products.csv'):
        self.model = SentenceTransformer(model_name)
        self.csv_path = csv_path
        self.products_df = None
        self.index = None
        self.load_data()

    def load_data(self):
        try:
            if not os.path.exists(self.csv_path):
                raise FileNotFoundError(f"CSV file not found at {self.csv_path}")
            
            self.products_df = pd.read_csv(self.csv_path)
            
            # Filter: Only keep products with valid image URLs
            self.products_df = self.products_df[self.products_df['image_url'].notna() & (self.products_df['image_url'] != "")]
            
            # Enhanced combined text for better semantic matching
            self.products_df['combined_text'] = self.products_df.apply(
                lambda x: f"Product: {x['name']}. Category: {x['category']}. Brand: {x['brand']}. Description: {x['description']}. Price: ${x['price']}", axis=1
            )
            
            index_path = 'vector_index.faiss'
            rebuild_needed = True
            
            if os.path.exists(index_path) and os.path.getmtime(index_path) > os.path.getmtime(self.csv_path):
                print("Loading existing FAISS index...")
                temp_index = faiss.read_index(index_path)
                
                # Check if dimension matches current model
                sample_embedding = self.model.encode(["test"])
                if temp_index.d == sample_embedding.shape[1]:
                    self.index = temp_index
                    rebuild_needed = False
                    print(f"Loaded existing index (dim: {self.index.d})")
                else:
                    print(f"Dimension mismatch found (Index: {temp_index.d}, Model: {sample_embedding.shape[1]}). Rebuilding...")

            if rebuild_needed:
                # Generate embeddings
                print(f"Generating new embeddings for {len(self.products_df)} products...")
                embeddings = self.model.encode(self.products_df['combined_text'].tolist(), show_progress_bar=True)
                embeddings = np.array(embeddings).astype('float32')
                
                # Initialize FAISS index
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(embeddings)
                
                # Save index
                faiss.write_index(self.index, index_path)
                print(f"New index generated and saved to {index_path} (dim: {dimension}).")
                
            print(f"Index ready with {self.index.ntotal} vectors.")
        except Exception as e:
            print(f"Error loading data or generating embeddings: {e}")
            raise

    async def search(self, query, top_k=5):
        if not query or not query.strip():
            return []

        # 1. Web Search (Primary for real-time data)
        web_results = []
        try:
            print(f"Searching web for: {query}")
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                # User specifically asked for "products with pic", so we prioritize image search results
                # because they contain Title, URL, and Image URL.
                web_results = []
                
                # 1. Try Image Search (Best for "Visual" shopping)
                try:
                    # 'safesearch' off to ensure we get results, but use with caution
                    image_hits = list(ddgs.images(query + " product price", region='us-en', safesearch='off', max_results=top_k))
                    for hit in image_hits:
                        web_results.append({
                            "name": hit['title'],
                            "brand": "Web Search", 
                            "category": "Web Result",
                            "description": "Click link for details.", # Images don't give descriptions usually
                            "price": "Check Link",
                            "image_url": hit['image'],
                            "source": "web",
                            "link": hit['url'],
                            "stock": "in_stock", # Web results are assumed available or at least we want to show them
                            "final_score": 0
                        })
                except Exception as img_e:
                    print(f"Image search failed: {img_e}")

                # 2. If Image search yielded few results, try Text Search 'lite'
                if len(web_results) < 2:
                    try:
                        text_hits = list(ddgs.text(query + " buy", region='us-en', safesearch='off', backend='lite', max_results=top_k))
                        for hit in text_hits:
                            web_results.append({
                                "name": hit['title'],
                                "brand": "Web Search",
                                "category": "Web Result",
                                "description": hit['body'],
                                "price": "Check Link",
                                "image_url": "https://via.placeholder.com/150?text=No+Image",
                                "source": "web",
                                "link": hit['href'],
                                "stock": "in_stock",
                                "final_score": 0
                            })
                    except Exception as txt_e:
                        print(f"Text search failed: {txt_e}")

        except Exception as e:
            print(f"Web search failed: {e}")
                        
        except Exception as e:
            print(f"Web search failed: {e}")

        # 2. Semantic Search (FAISS) - Local Catalog
        local_results = []
        if self.index is not None:
            query_embedding = self.model.encode([query]).astype('float32')
            distances, indices = self.index.search(query_embedding, top_k)
            
            for i in range(len(indices[0])):
                idx = indices[0][i]
                if idx != -1:
                    product = self.products_df.iloc[idx].to_dict()
                    product['semantic_score'] = float(distances[0][i])
                    product['source'] = 'local'
                    local_results.append(product)

            # Hybrid Boost for local
            query_lower = query.lower()
            for res in local_results:
                boost = 0
                if query_lower in res['name'].lower(): boost += 20
                if query_lower in res['brand'].lower(): boost += 30
                if query_lower in res['category'].lower(): boost += 15
                res['final_score'] = res['semantic_score'] - boost
                res['price'] = f"${res['price']}" # Format local price

        # Combine results: Web results first, then local
        all_results = web_results + local_results
        return all_results[:top_k*2]

if __name__ == "__main__":
    # Test the search engine
    se = SearchEngine()
    test_query = "noise cancelling headphones"
    results = se.search(test_query)
    for res in results:
        print(f"Name: {res['name']}, Price: {res['price']}, Score: {res['score']}")
