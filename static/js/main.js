/**
 * ZIYO E-Commerce Storefront Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
    // 0. Theme Toggle Switcher
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('ziyo-theme', newTheme);
            window.dispatchEvent(new CustomEvent('themechanged', { detail: { theme: newTheme } }));
        });
    }

    // Sync with OS color scheme changes if user hasn't chosen a persistent preference
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('ziyo-theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', newTheme);
            }
        });
    }

    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    // 2. Product gallery thumbnail switcher
    const mainGalleryImg = document.getElementById('mainProductImage');
    const galleryThumbs = document.querySelectorAll('.gallery-thumb');
    if (mainGalleryImg && galleryThumbs.length > 0) {
        galleryThumbs.forEach(thumb => {
            thumb.addEventListener('click', (e) => {
                e.preventDefault();
                const targetSrc = thumb.getAttribute('data-full-img');
                if (targetSrc) {
                    mainGalleryImg.src = targetSrc;
                    galleryThumbs.forEach(t => t.classList.remove('active'));
                    thumb.classList.add('active');
                }
            });
        });
    }

    // 3. Variant selection updates price
    const variantSelect = document.getElementById('variantSelector');
    const displayPrice = document.getElementById('productDisplayPrice');
    if (variantSelect && displayPrice) {
        variantSelect.addEventListener('change', () => {
            const selectedOption = variantSelect.options[variantSelect.selectedIndex];
            const variantPrice = selectedOption.getAttribute('data-price');
            if (variantPrice) {
                displayPrice.textContent = '₹' + variantPrice;
            }
        });
    }

    // 4. Quantity Steppers
    document.querySelectorAll('.qty-decrement').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.qty-stepper').querySelector('input[type="number"]');
            if (input && parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    document.querySelectorAll('.qty-increment').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.qty-stepper').querySelector('input[type="number"]');
            if (input) {
                input.value = parseInt(input.value) + 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // 5. AI Concierge Floating Support Chat
    const chatToggle = document.getElementById('aiChatToggle');
    const chatModal = document.getElementById('aiChatModal');
    const chatClose = document.getElementById('aiChatClose');
    const chatForm = document.getElementById('aiChatForm');
    const chatInput = document.getElementById('aiChatInput');
    const chatMessages = document.getElementById('aiChatMessages');

    if (chatToggle && chatModal) {
        chatToggle.addEventListener('click', () => {
            chatModal.classList.toggle('open');
            if (chatModal.classList.contains('open') && chatInput) {
                chatInput.focus();
            }
        });

        if (chatClose) {
            chatClose.addEventListener('click', () => chatModal.classList.remove('open'));
        }

        if (chatForm) {
            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const msg = chatInput.value.trim();
                if (!msg) return;

                // Append user message
                appendChatMessage(msg, 'user');
                chatInput.value = '';

                // Typing indicator
                const typingNode = appendChatMessage('Ziyo Concierge is typing...', 'ai', true);

                try {
                    const formData = new FormData();
                    formData.append('message', msg);
                    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

                    const response = await fetch('/ai/chat/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken || '',
                        },
                        body: formData,
                    });
                    const data = await response.json();
                    typingNode.remove();
                    appendChatMessage(data.reply, 'ai');
                } catch (err) {
                    typingNode.remove();
                    appendChatMessage('I am currently experiencing a brief pause. Please feel free to browse or email support@ziyo.store.', 'ai');
                }
            });
        }
    }

    function appendChatMessage(text, sender, isTyping = false) {
        if (!chatMessages) return null;
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-bubble chat-bubble-${sender} ${isTyping ? 'typing-indicator' : ''}`;
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msgDiv;
    }
});
