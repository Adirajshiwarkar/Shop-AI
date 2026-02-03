import aiosqlite
import json

class CartManager:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    product_id TEXT,
                    product_name TEXT,
                    price REAL,
                    quantity INTEGER DEFAULT 1,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await conn.commit()

    async def add_to_cart(self, session_id, product):
        async with aiosqlite.connect(self.db_path) as conn:
            # Check if item exists
            cursor = await conn.execute(
                "SELECT id, quantity FROM cart WHERE session_id = ? AND product_name = ?",
                (session_id, product['name'])
            )
            row = await cursor.fetchone()
            
            if row:
                await conn.execute(
                    "UPDATE cart SET quantity = quantity + 1 WHERE id = ?",
                    (row[0],)
                )
            else:
                await conn.execute(
                    "INSERT INTO cart (session_id, product_name, price) VALUES (?, ?, ?)",
                    (session_id, product['name'], product['price'])
                )
            await conn.commit()

    async def get_cart(self, session_id):
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                "SELECT product_name as name, price, quantity FROM cart WHERE session_id = ?",
                (session_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def clear_cart(self, session_id):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("DELETE FROM cart WHERE session_id = ?", (session_id,))
            await conn.commit()
