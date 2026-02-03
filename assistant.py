import os
import json
import aiosqlite
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class ConversationalAssistant:
    def __init__(self, db_path='chat_history.db'):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("Warning: Valid OPENAI_API_KEY not found in environment. Please set it in .env")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await conn.commit()

    async def get_history(self, session_id, limit=12):
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
                (session_id, limit)
            )
            rows = await cursor.fetchall()
            history = [{"role": row[0], "content": row[1]} for row in rows]
            return history[::-1]

    async def save_message(self, session_id, role, content):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            await conn.commit()

    async def generate_streaming_response(self, user_query, search_results, session_id="default"):
        history = await self.get_history(session_id)
        
        context = "Relevant products found in our catalog:\n"
        if not search_results:
            context = "No matches found.\n"
        else:
            for res in search_results:
                source = res.get('source', 'unknown')
                link_info = f" [Link: {res.get('link', 'N/A')}]" if source == 'web' else ""
                context += f"- [{source.upper()}] {res['name']} ({res.get('category', 'N/A')}): {res.get('description', '')[:200]}... Price: {res.get('price', 'N/A')}{link_info}\n"
        
        system_prompt = f"""
        You are ShopAI, a sophisticated and friendly premium shopping assistant.
        
        {context}
        
        Voice and Personality:
        - Communicate naturally, like a knowledgeable and helpful person.
        - You can engage in small talk and normal conversation (greetings, how are you, etc.), but subtly steer back to shopping if appropriate.
        - Be witty, polite, and enthusiastically helpful.
        - Use emojis naturally ✨.
        - If the user isn't asking about products, respond like a friendly human companion would.
        - Don't just list products; tell a story about why they fit the user's life.
        - If the user is indecisive, be the confident shopping expert who helps them choose.
        
        Instructions:
        1. When relevant products are available, explain *why* they are great choices for the user's specific needs.
        2. Maintain context from the current session history to feel like a continuous conversation.
        3. If no products are found for a search, help the user refine their request or suggest similar categories.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append(msg)
        messages.append({"role": "user", "content": user_query})
        
        full_response = ""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=True
            )
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    full_response += content
                    yield content
            
            # Save the complete exchange once finished
            await self.save_message(session_id, "user", user_query)
            await self.save_message(session_id, "assistant", full_response)
            
        except Exception as e:
            print(f"OpenAI Streaming Error: {e}")
            yield f"Error: {str(e)}"

    async def get_all_sessions(self):
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(
                "SELECT session_id, MAX(timestamp) as last_activity FROM messages GROUP BY session_id ORDER BY last_activity DESC"
            )
            rows = await cursor.fetchall()
            return [{"session_id": row[0], "last_activity": row[1]} for row in rows]
            
    async def get_session_history(self, session_id):
        return await self.get_history(session_id, limit=50)

if __name__ == "__main__":
    # Simple test
    assistant = ConversationalAssistant()
    sample_results = [
        {"name": "Wireless Headphones", "brand": "SoundPro", "category": "Electronics", "description": "Noise cancelling headphones", "price": 199.99}
    ]
    print(assistant.generate_response("I need some quiet headphones", sample_results))
