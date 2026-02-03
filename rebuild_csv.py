import pandas as pd

products = [
    {
        "id": 1, "name": "Wireless Noise Cancelling Headphones", "category": "Electronics",
        "description": "High-fidelity audio with active noise cancellation and 30-hour battery life.",
        "price": 199.99, "brand": "SoundPro", 
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=800",
        "rating": 4.8, "stock": 25
    },
    {
        "id": 2, "name": "Smart LED Desk Lamp", "category": "Home Office",
        "description": "Adjustable brightness and color temperature with built-in USB charging port.",
        "price": 45.00, "brand": "LiteBright",
        "image_url": "https://images.unsplash.com/photo-1534073828943-f801091bb18c?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 12
    },
    {
        "id": 3, "name": "Organic Cotton T-Shirt", "category": "Apparel",
        "description": "Soft breathable organic cotton t-shirt in various colors.",
        "price": 25.00, "brand": "EcoStyle",
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=800",
        "rating": 4.2, "stock": 50
    },
    {
        "id": 4, "name": "Stainless Steel Water Bottle", "category": "Kitchen",
        "description": "Vacuum insulated bottle that keeps drinks cold for 24 hours.",
        "price": 18.50, "brand": "HydroPeak",
        "image_url": "https://images.unsplash.com/photo-1602143399827-bd959683a342?auto=format&fit=crop&q=80&w=800",
        "rating": 4.7, "stock": 30
    },
    {
        "id": 5, "name": "Portable Power Bank 20000mAh", "category": "Electronics",
        "description": "Fast-charging power bank with multiple ports for all your devices.",
        "price": 39.99, "brand": "VoltCharge",
        "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&q=80&w=800",
        "rating": 4.4, "stock": 18
    },
    {
        "id": 6, "name": "Mechanical Gaming Keyboard", "category": "Electronics",
        "description": "RGB backlit keyboard with blue switches for a tactile gaming experience.",
        "price": 89.00, "brand": "GameMaster",
        "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?auto=format&fit=crop&q=80&w=800",
        "rating": 4.9, "stock": 15
    },
    {
        "id": 7, "name": "Yoga Mat - Non-Slip", "category": "Sports",
        "description": "Extra thick cushioning for joint support with a textured non-slip surface.",
        "price": 29.99, "brand": "ZenFit",
        "image_url": "https://images.unsplash.com/photo-1592432676556-269e382bc88a?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 22
    },
    {
        "id": 8, "name": "Ceramic Coffee Mug - 12oz", "category": "Kitchen",
        "description": "Handcrafted ceramic mug with a matte finish and ergonomic handle.",
        "price": 12.00, "brand": "MugLife",
        "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fbed20?auto=format&fit=crop&q=80&w=800",
        "rating": 4.3, "stock": 40
    },
    {
        "id": 9, "name": "Compact Foldable Umbrella", "category": "Accessories",
        "description": "Windproof and travel-friendly umbrella with automatic open/close.",
        "price": 22.00, "brand": "RainGuard",
        "image_url": "https://images.unsplash.com/photo-1511285227091-c24766324905?auto=format&fit=crop&q=80&w=800",
        "rating": 4.1, "stock": 35
    },
    {
        "id": 10, "name": "Streaming Webcam 1080p", "category": "Electronics",
        "description": "Full HD webcam with built-in microphone for clear video calls and streaming.",
        "price": 55.00, "brand": "VisionTech",
        "image_url": "https://images.unsplash.com/photo-1585338107529-13afc5f0141f?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 20
    },
    {
        "id": 11, "name": "Leather Men's Wallet", "category": "Accessories",
        "description": "Genuine leather trifold wallet with RFID blocking technology.",
        "price": 35.00, "brand": "LegacyLeather",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 15
    },
    {
        "id": 12, "name": "Air Quality Monitor", "category": "Smart Home",
        "description": "Real-time monitoring of CO2, temperature, and humidity levels.",
        "price": 79.99, "brand": "PureAir",
        "image_url": "https://images.unsplash.com/photo-1585338107529-13afc5f0141f?auto=format&fit=crop&q=80&w=800",
        "rating": 4.4, "stock": 10
    },
    {
        "id": 13, "name": "Electric Gooseneck Kettle", "category": "Kitchen",
        "description": "Precision pour electric kettle with temperature control for coffee and tea.",
        "price": 65.00, "brand": "BrewCore",
        "image_url": "https://images.unsplash.com/photo-1516335193237-640a233364f9?auto=format&fit=crop&q=80&w=800",
        "rating": 4.8, "stock": 12
    },
    {
        "id": 14, "name": "Men's Performance Running Shoes", "category": "Sports",
        "description": "Lightweight and responsive running shoes for maximum comfort and speed.",
        "price": 110.00, "brand": "SwiftDash",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=800",
        "rating": 4.7, "stock": 20
    },
    {
        "id": 15, "name": "Noise-Cancelling Sleep Earbuds", "category": "Electronics",
        "description": "Comfortable earbuds designed specifically for side sleepers with white noise masking.",
        "price": 149.00, "brand": "DreamSound",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 8
    },
    {
        "id": 16, "name": "Silicone Face Scrub Brush", "category": "Skincare",
        "description": "Soft silicone sonic face brush for a deep and gentle facial cleanse.",
        "price": 25.00, "brand": "GlowKit",
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&q=80&w=800",
        "rating": 4.3, "stock": 30
    },
    {
        "id": 17, "name": "Bamboo Cotton Towel Set", "category": "Home",
        "description": "Ultra-soft and absorbent bamboo cotton towel set (2 bath, 2 hand, 2 face).",
        "price": 49.99, "brand": "EcoSprout",
        "image_url": "https://images.unsplash.com/photo-1560343090-f0409e92791a?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 18
    },
    {
        "id": 18, "name": "Modern Office Chair", "category": "Home Office",
        "description": "Ergonomic mesh office chair with lumbar support and adjustable armrests.",
        "price": 180.00, "brand": "ComfySit",
        "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&q=80&w=800",
        "rating": 4.8, "stock": 5
    },
    {
        "id": 19, "name": "Handheld Vacuum Cleaner", "category": "Home",
        "description": "Cordless handheld vacuum with powerful suction for quick cleanups.",
        "price": 59.00, "brand": "DustBuster",
        "image_url": "https://images.unsplash.com/photo-1527515545081-5db817172677?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 14
    },
    {
        "id": 20, "name": "Reusable Mesh Produce Bags", "category": "Kitchen",
        "description": "Eco-friendly washable mesh bags for groceries and storage.",
        "price": 15.00, "brand": "EcoLoop",
        "image_url": "https://images.unsplash.com/photo-1544256718-3bcf237f3974?auto=format&fit=crop&q=80&w=800",
        "rating": 4.2, "stock": 40
    },
    {
        "id": 21, "name": "Adjustable Dumbbell Set", "category": "Sports",
        "description": "Compact adjustable dumbbells, replaces multiple weights in one set.",
        "price": 199.00, "brand": "IronGrip",
        "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&q=80&w=800",
        "rating": 4.9, "stock": 8
    },
    {
        "id": 22, "name": "Smart Plant Monitor", "category": "Pet Supplies",
        "description": "Bluetooth sensor to monitor soil moisture, light, and nutrients for your plants.",
        "price": 29.00, "brand": "BloomTrack",
        "image_url": "https://images.unsplash.com/photo-1416870234185-d6c5df550ce3?auto=format&fit=crop&q=80&w=800",
        "rating": 4.3, "stock": 25
    },
    {
        "id": 23, "name": "Pet Water Fountain", "category": "Pet Supplies",
        "description": "Continuous flow water fountain for cats and small dogs.",
        "price": 34.99, "brand": "HappyPaws",
        "image_url": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&q=80&w=800",
        "rating": 4.7, "stock": 20
    },
    {
        "id": 24, "name": "Lavender Soy Candle", "category": "Home",
        "description": "Relaxing lavender-scented soy candle in a decorative glass jar.",
        "price": 18.00, "brand": "ZenFlow",
        "image_url": "https://images.unsplash.com/photo-1603006899172-642948f90d97?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 35
    },
    {
        "id": 25, "name": "Polarized Classic Sunglasses", "category": "Accessories",
        "description": "Timeless classic frames with polarized lenses and UV protection.",
        "price": 45.00, "brand": "ClearVue",
        "image_url": "https://images.unsplash.com/photo-1511499767390-a8a19759918a?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 22
    },
    {
        "id": 26, "name": "Wireless Charging Stand", "category": "Electronics",
        "description": "15W fast wireless charging stand for compatible smartphones.",
        "price": 24.00, "brand": "QiPower",
        "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&q=80&w=800",
        "rating": 4.4, "stock": 28
    },
    {
        "id": 27, "name": "Natural Wood Cutting Board", "category": "Kitchen",
        "description": "Large solid walnut wood cutting board with deep juice grooves.",
        "price": 60.00, "brand": "KitchenCraft",
        "image_url": "https://images.unsplash.com/photo-1544650039-22886fbb4323?auto=format&fit=crop&q=80&w=800",
        "rating": 4.8, "stock": 12
    },
    {
        "id": 28, "name": "Mini Portable Projector", "category": "Electronics",
        "description": "Pocket-sized smart projector for movies and gaming anywhere.",
        "price": 129.00, "brand": "PocketCinema",
        "image_url": "https://images.unsplash.com/photo-1535016120720-40c646be896a?auto=format&fit=crop&q=80&w=800",
        "rating": 4.3, "stock": 10
    },
    {
        "id": 29, "name": "Ceramide Barrier Cream", "category": "Skincare",
        "description": "Intensive hydrating cream with ceramides and hyaluronic acid.",
        "price": 28.00, "brand": "DewFace",
        "image_url": "https://images.unsplash.com/photo-1556229162-da50294156b6?auto=format&fit=crop&q=80&w=800",
        "rating": 4.7, "stock": 20
    },
    {
        "id": 30, "name": "Wool Blend Winter Coat", "category": "Apparel",
        "description": "Classic wool blend overcoat with a modern slim fit.",
        "price": 150.00, "brand": "UrbanEdge",
        "image_url": "https://images.unsplash.com/photo-1539533377285-a764dca63972?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 8
    },
    {
        "id": 31, "name": "Camping Lantern - Rechargeable", "category": "Outdoor Gear",
        "description": "High-lumen LED camping lantern with multiple brightness modes.",
        "price": 35.00, "brand": "TrailBlaze",
        "image_url": "https://images.unsplash.com/photo-1540324155974-7523202daa3f?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 18
    },
    {
        "id": 32, "name": "Matte Lip Stain Set", "category": "Skincare",
        "description": "Long-lasting matte lip stain set in 4 versatile shades.",
        "price": 30.00, "brand": "BoldLook",
        "image_url": "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=800",
        "rating": 4.4, "stock": 25
    },
    {
        "id": 33, "name": "Graphite Tennis Racket", "category": "Sports",
        "description": "Professional grade graphite tennis racket for power and control.",
        "price": 140.00, "brand": "EliteAce",
        "image_url": "https://images.unsplash.com/photo-1617083273204-c8273678eb17?auto=format&fit=crop&q=80&w=800",
        "rating": 4.8, "stock": 10
    },
    {
        "id": 34, "name": "Automatic Pet Feeder", "category": "Pet Supplies",
        "description": "Programmable automatic pet feeder with portion control and voice record.",
        "price": 89.00, "brand": "SmartPet",
        "image_url": "https://images.unsplash.com/photo-1516733725897-1aa73b87c8e8?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 12
    },
    {
        "id": 35, "name": "Lightweight Trail Backpack", "category": "Outdoor Gear",
        "description": "Durable 30L trail backpack for day hikes and travel.",
        "price": 55.00, "brand": "PeakTrail",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 15
    },
    {
        "id": 36, "name": "Glass Food Storage Set", "category": "Kitchen",
        "description": "10-piece set of BPA-free glass containers with airtight lids.",
        "price": 40.00, "brand": "KitchenCare",
        "image_url": "https://images.unsplash.com/photo-1581447100595-3a74ad9900a8?auto=format&fit=crop&q=80&w=800",
        "rating": 4.7, "stock": 20
    },
    {
        "id": 37, "name": "Mini Succulent Trio", "category": "Home",
        "description": "A set of three living succulents in minimalist white ceramic pots.",
        "price": 24.00, "brand": "GreenVibe",
        "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&q=80&w=800",
        "rating": 4.4, "stock": 15
    },
    {
        "id": 38, "name": "Smart Home Security Hub", "category": "Smart Home",
        "description": "Unified control hub for all your smart home sensors and cameras.",
        "price": 120.00, "brand": "SafeNest",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df8d7?auto=format&fit=crop&q=80&w=800",
        "rating": 4.5, "stock": 10
    },
    {
        "id": 39, "name": "Portable Solar Charger", "category": "Outdoor Gear",
        "description": "Foldable solar panel for charging electronics off-grid.",
        "price": 65.00, "brand": "SunDrive",
        "image_url": "https://images.unsplash.com/photo-1511275215011-f10f13501740?auto=format&fit=crop&q=80&w=800",
        "rating": 4.3, "stock": 12
    },
    {
        "id": 40, "name": "Scented Bath Bomb Set", "category": "Home",
        "description": "Luxurious set of 6 bath bombs with organic essential oils.",
        "price": 22.00, "brand": "PureSpa",
        "image_url": "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?auto=format&fit=crop&q=80&w=800",
        "rating": 4.6, "stock": 30
    }
]

df = pd.DataFrame(products)
df.to_csv("products.csv", index=False)
print("Safe products.csv generated successfully.")
