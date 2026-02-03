document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const productList = document.getElementById('product-list');
    const clearChatBtn = document.getElementById('clear-chat');
    const cartModal = document.getElementById('cart-modal');
    const cartItemsDiv = document.getElementById('cart-items');
    const cartTotalSpan = document.getElementById('cart-total');
    const cartCountBadge = document.getElementById('cart-count');
    const cartNav = document.getElementById('cart-nav');
    const clearCartBtn = document.getElementById('clear-cart-btn');
    const productModal = document.getElementById('product-modal');
    const modalBody = document.getElementById('modal-body');
    const API_URL = 'http://localhost:8000';

    // Persistent Session ID (Try to get from localStorage)
    let sessionId = localStorage.getItem('shopai_session_id') || 'session_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('shopai_session_id', sessionId);

    fetchProducts();
    refreshCart();

    // Unified Tab Management
    const navItems = document.querySelectorAll('.nav-item');
    const productSidebar = document.getElementById('product-sidebar');
    const chatArea = document.querySelector('.chat-area');

    function setActiveTab(index) {
        navItems.forEach((item, i) => {
            if (i === index) item.classList.add('active');
            else item.classList.remove('active');
        });
    }

    // Assistant / Chat Tab
    navItems[0].addEventListener('click', (e) => {
        e.preventDefault();
        setActiveTab(0);
        // Ensure chat area is visible if it was hidden
        chatArea.style.display = 'flex';
    });

    // Discover / Catalog Tab (Toggle Sidebar on Mobile/Desktop)
    navItems[1].addEventListener('click', (e) => {
        e.preventDefault();
        setActiveTab(1);
        productSidebar.classList.toggle('visible');
        // Scroll to product list for mobile users
        productList.scrollIntoView({ behavior: 'smooth' });
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        // UI State: Disable input
        userInput.disabled = true;
        const sendBtn = chatForm.querySelector('button');
        sendBtn.disabled = true;

        addMessage(query, 'user');
        userInput.value = '';

        const typingId = addTypingIndicator();

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, session_id: sessionId })
            });

            if (!response.ok) throw new Error('Failed to fetch response');

            removeTypingIndicator(typingId);

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let messageDiv = null;
            let contentDiv = null;

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith('DATA:PRODUCTS:')) {
                        const jsonStr = line.replace('DATA:PRODUCTS:', '');
                        try {
                            const products = JSON.parse(jsonStr);
                            if (!messageDiv) {
                                ({ messageDiv, contentDiv } = createMessageContainer('bot'));
                            }
                            displayProductsInMessage(messageDiv, products);
                        } catch (e) { console.error("JSON Parse Error", e); }
                    } else if (line.startsWith('DATA:TEXT:')) {
                        const text = line.replace('DATA:TEXT:', '');
                        if (!messageDiv) {
                            ({ messageDiv, contentDiv } = createMessageContainer('bot'));
                        }
                        // Append text safely with basic markdown support
                        contentDiv.innerHTML += text
                            .replace(/\n/g, '<br>')
                            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                            .replace(/\*(.*?)\*/g, '<i>$1</i>');

                    }
                }
            }
            // Final scroll for the complete message
            chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator(typingId);
            addMessage("I apologize, but I encountered a slight hiccup in our connection. Should we try that again? ✨", 'bot');
        } finally {
            // UI State: Re-enable input
            userInput.disabled = false;
            sendBtn.disabled = false;
            removeTypingIndicator(typingId); // Double check
            userInput.focus();
        }
    });

    clearChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        addMessage("Chat history cleared. I'm ready for fresh shopping adventures! 🛍️", 'bot');
        sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('shopai_session_id', sessionId);
        refreshCart();
    });

    cartNav.addEventListener('click', (e) => {
        e.preventDefault();
        if (cartModal) {
            cartModal.style.display = 'flex';
            refreshCart();
        }
    });

    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', async () => {
            const originalText = checkoutBtn.innerText;
            checkoutBtn.disabled = true;
            checkoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

            // Simulate processing
            await new Promise(r => setTimeout(r, 1500));

            await fetch(`${API_URL}/cart/${sessionId}`, { method: 'DELETE' });
            refreshCart();

            checkoutBtn.innerHTML = '<i class="fas fa-check"></i> Order Placed!';
            checkoutBtn.style.background = 'var(--accent-green)';

            setTimeout(() => {
                cartModal.style.display = 'none';
                checkoutBtn.innerText = originalText;
                checkoutBtn.disabled = false;
                checkoutBtn.style.background = 'var(--primary)';
                addMessage("🎉 Your order has been placed successfully! Thank you for shopping with ShopAI.", 'bot');
            }, 1000);
        });
    }

    // History Toggle
    const historyNav = navItems[2];
    historyNav.addEventListener('click', async (e) => {
        e.preventDefault();
        setActiveTab(2);
        const response = await fetch(`${API_URL}/sessions`);
        const sessions = await response.json();

        chatMessages.innerHTML = '<div class="history-view"><h2>Conversation History</h2><p style="margin-bottom: 24px; color: var(--text-secondary);">Select a previous session to resume.</p></div>';
        const historyContainer = chatMessages.querySelector('.history-view');

        sessions.forEach(s => {
            const sDiv = document.createElement('div');
            sDiv.classList.add('history-item');
            sDiv.style.cssText = 'padding: 20px; background: var(--glass); border: 1px solid var(--glass-border); border-radius: var(--radius-md); margin-bottom: 12px; cursor: pointer; transition: all 0.2s;';
            sDiv.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 4px; display: flex; justify-content: space-between;">
                    <span>Session: ${s.session_id.substring(0, 12)}...</span>
                    <i class="fas fa-arrow-right" style="opacity: 0.5;"></i>
                </div>
                <div style="font-size: 12px; color: var(--text-secondary);">Last active: ${new Date(s.last_activity).toLocaleString()}</div>
            `;
            sDiv.onclick = () => loadSession(s.session_id);
            historyContainer.appendChild(sDiv);
        });
    });

    async function loadSession(id) {
        sessionId = id;
        localStorage.setItem('shopai_session_id', id);
        chatMessages.innerHTML = '';
        setActiveTab(0); // Return to assistant view
        const response = await fetch(`${API_URL}/sessions/${id}`);
        const history = await response.json();

        history.forEach(msg => {
            addMessage(msg.content, msg.role);
        });
        refreshCart();
    }

    clearCartBtn.addEventListener('click', async () => {
        const confirmClear = confirm("Are you sure you want to empty your cart?");
        if (!confirmClear) return;
        await fetch(`${API_URL}/cart/${sessionId}`, { method: 'DELETE' });
        refreshCart();
    });

    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.onclick = () => {
            if (typeof productModal !== 'undefined') productModal.style.display = 'none';
            if (typeof cartModal !== 'undefined') cartModal.style.display = 'none';
        }
    });

    window.onclick = (event) => {
        if (event.target == productModal || event.target == cartModal) {
            if (typeof productModal !== 'undefined') productModal.style.display = 'none';
            if (typeof cartModal !== 'undefined') cartModal.style.display = 'none';
        }
    };

    function addMessage(text, sender, products = []) {
        const { messageDiv, contentDiv } = createMessageContainer(sender);

        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/\n/g, '<br>');

        contentDiv.innerHTML = formattedText;

        if (products && products.length > 0) {
            displayProductsInMessage(messageDiv, products);
        }

        chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    }

    function createMessageContainer(sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        return { messageDiv, contentDiv };
    }

    function displayProductsInMessage(messageDiv, products) {
        const productsDiv = document.createElement('div');
        productsDiv.classList.add('product-results');

        products.forEach(product => {
            const pCard = document.createElement('div');
            pCard.classList.add('product-card-mini');
            // Determine button based on source
            const isWeb = product.source === 'web';
            const actionBtnHtml = isWeb
                ? `<button class="visit-btn-tiny" title="Visit Website"><i class="fas fa-external-link-alt"></i></button>`
                : `<button class="add-btn-tiny" title="Add to Cart"><i class="fas fa-plus"></i></button>`;

            const priceDisplay = typeof product.price === 'number' ? '$' + product.price : product.price;

            pCard.innerHTML = `
                <div class="product-img-container" style="height: 120px; background: var(--glass); border-radius: var(--radius-sm); margin-bottom: 12px; overflow: hidden;">
                    <img src="${product.image_url}" alt="${product.name}" 
                         onerror="this.src='https://via.placeholder.com/200?text=No+Image'"
                         style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <h4>${product.name}</h4>
                <div class="brand">${product.brand}</div>
                <div class="rating" style="font-size: 12px; color: #facc15; margin-bottom: 4px;">
                    ${'★'.repeat(Math.floor(product.rating || 5))}${product.rating % 1 >= 0.5 ? '½' : ''}
                </div>
                <div class="price-row" style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="price" style="font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${priceDisplay}</div>
                    ${actionBtnHtml}
                </div>
            `;
            pCard.onclick = () => showProductDetails(product);

            // Interaction: Direct Action
            if (isWeb) {
                const visitBtn = pCard.querySelector('.visit-btn-tiny');
                visitBtn.onclick = (e) => {
                    e.stopPropagation();
                    window.open(product.link, '_blank');
                };
            } else {
                const addBtn = pCard.querySelector('.add-btn-tiny');
                addBtn.onclick = (e) => {
                    e.stopPropagation();
                    addToCart(product);
                };
            }

            productsDiv.appendChild(pCard);
        });
        messageDiv.appendChild(productsDiv);
    }

    function showProductDetails(product) {
        // Determine action button based on source
        let actionButton = '';
        if (product.source === 'web') {
            actionButton = `<button onclick="window.open('${product.link}', '_blank')" style="flex: 1; background: var(--text-primary); color: var(--bg-primary); border: none; padding: 16px; border-radius: var(--radius-md); font-weight: 600; cursor: pointer;"><i class="fas fa-external-link-alt"></i> Check Website</button>`;
        } else {
            actionButton = `<button id="add-to-cart-btn" style="flex: 1; background: var(--primary); color: white; border: none; padding: 16px; border-radius: var(--radius-md); font-weight: 600; cursor: pointer;">Add to Cart</button>`;
        }

        // Determine Stock Status Display
        let stockDisplay = '';
        if (product.source === 'web' && product.stock === 'in_stock') {
            stockDisplay = `<span style="color: var(--accent-green);"><i class="fas fa-check-circle" style="margin-right: 8px;"></i> Available Online</span>`;
        } else {
            stockDisplay = product.stock > 0 ?
                `<span style="color: var(--accent-green);"><i class="fas fa-circle" style="font-size: 8px; margin-right: 8px;"></i> In Stock (${product.stock} units)</span>` :
                `<span style="color: var(--accent-red);">Out of Stock</span>`;
        }

        modalBody.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 40px;">
                <div class="product-gallery">
                    <img src="${product.image_url}" alt="${product.name}" 
                        onerror="this.src='https://via.placeholder.com/400x400?text=No+Image'"
                        style="width: 100%; border-radius: var(--radius-md); box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                </div>
                <div class="product-info">
                    <div style="text-transform: uppercase; color: var(--primary); font-weight: 700; letter-spacing: 2px; font-size: 12px; margin-bottom: 12px;">${product.brand}</div>
                    <h2 style="font-size: 32px; margin-bottom: 16px;">${product.name}</h2>
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                        <span style="color: #facc15; font-size: 18px;">${'★'.repeat(Math.floor(product.rating || 5))}${'☆'.repeat(5 - Math.floor(product.rating || 5))}</span>
                        <span style="color: var(--text-secondary); font-size: 14px;">(${product.rating || 'N/A'})</span>
                    </div>
                    <div style="font-size: 24px; font-weight: 700; color: var(--text-primary); margin-bottom: 24px;">${typeof product.price === 'number' ? '$' + product.price : product.price}</div>
                    <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 32px; font-size: 16px;">${product.description}</p>
                    <div style="display: flex; gap: 16px;">
                        ${actionButton}
                        <button style="background: var(--glass); color: var(--text-primary); border: 1px solid var(--glass-border); padding: 16px; border-radius: var(--radius-md); cursor: pointer;"><i class="far fa-heart"></i></button>
                    </div>
                    <div style="margin-top: 24px; font-size: 13px;">
                        ${stockDisplay}
                    </div>
                </div>
            </div>
        `;
        productModal.style.display = 'flex';

        if (product.source !== 'web') {
            document.getElementById('add-to-cart-btn').onclick = () => addToCart(product);
        }
    }

    async function addToCart(product) {
        try {
            await fetch(`${API_URL}/cart/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, product: product })
            });
            refreshCart();
            // Optional: Close product modal or show a snackbar
        } catch (err) {
            console.error('Cart Error:', err);
        }
    }

    async function refreshCart() {
        try {
            const response = await fetch(`${API_URL}/cart/${sessionId}`);
            const items = await response.json();

            cartItemsDiv.innerHTML = '';
            let total = 0;
            let count = 0;

            if (items.length === 0) {
                cartItemsDiv.innerHTML = '<p style="text-align: center; color: var(--text-secondary); margin: 40px 0;">Your cart is empty.</p>';
            }

            items.forEach(item => {
                total += item.price * item.quantity;
                count += item.quantity;
                const itemDiv = document.createElement('div');
                itemDiv.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding: 12px; background: var(--glass); border-radius: var(--radius-sm);';
                itemDiv.innerHTML = `
                    <div>
                        <div style="font-weight: 600;">${item.name}</div>
                        <div style="font-size: 13px; color: var(--text-secondary);">$${item.price} × ${item.quantity}</div>
                    </div>
                    <div style="font-weight: 700;">$${(item.price * item.quantity).toFixed(2)}</div>
                `;
                cartItemsDiv.appendChild(itemDiv);
            });

            cartTotalSpan.innerText = `$${total.toFixed(2)}`;
            cartCountBadge.innerText = count;
            cartCountBadge.style.display = count > 0 ? 'flex' : 'none';
        } catch (err) {
            console.error('Refresh Cart Error:', err);
        }
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.classList.add('message', 'bot-message');
        typingDiv.innerHTML = '<div class="typing-dots" style="display: flex; gap: 4px; padding: 8px 0;"><span class="dot" style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; opacity: 0.4; animation: blink 1.4s infinite both;"></span><span class="dot" style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; opacity: 0.4; animation: blink 1.4s infinite both 0.2s;"></span><span class="dot" style="width: 8px; height: 8px; background: var(--text-secondary); border-radius: 50%; opacity: 0.4; animation: blink 1.4s infinite both 0.4s;"></span></div>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    async function fetchProducts() {
        try {
            const response = await fetch(`${API_URL}/products`);
            if (!response.ok) return;
            const products = await response.json();

            productList.innerHTML = '';
            products.forEach(product => {
                const card = document.createElement('div');
                card.classList.add('catalog-card');
                card.innerHTML = `
                    <div class="catalog-img-container" style="height: 140px; border-radius: var(--radius-sm); margin-bottom: 12px; overflow: hidden; background: var(--glass);">
                        <img src="${product.image_url}" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <h3>${product.name}</h3>
                    <p>${product.description.substring(0, 60)}...</p>
                    <div class="meta">
                        <span class="price">$${product.price}</span>
                        <button class="add-btn-catalog" title="Add to Cart"><i class="fas fa-cart-plus"></i> Add</button>
                    </div>
                `;
                card.onclick = () => showProductDetails(product);

                // Interaction: Direct Add to Cart
                const addBtn = card.querySelector('.add-btn-catalog');
                addBtn.onclick = (e) => {
                    e.stopPropagation();
                    addToCart(product);
                };

                productList.appendChild(card);
            });
        } catch (err) {
            console.error('Error fetching products:', err);
        }
    }
});

// Animation for typing indicator
const style = document.createElement('style');
style.textContent = `
    @keyframes blink {
        0% { opacity: 0.2; }
        20% { opacity: 1; }
        100% { opacity: 0.2; }
    }
`;
document.head.appendChild(style);
