/**
 * ZIYO Management Admin Dashboard Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
    // 0. Admin Theme Toggle Switcher
    const adminThemeBtn = document.getElementById('adminThemeToggleBtn');
    if (adminThemeBtn) {
        adminThemeBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('ziyo-theme', newTheme);
        });
    }

    // 1. AI Copywriting Generator Trigger in Product Form
    const aiBtn = document.getElementById('btnAiGenerateDesc');
    const descInput = document.getElementById('product_description_input');
    const nameInput = document.querySelector('input[name="name"]');
    const categorySelect = document.querySelector('select[name="category"]');

    if (aiBtn && descInput) {
        aiBtn.addEventListener('click', async () => {
            const productName = nameInput ? nameInput.value.trim() : '';
            if (!productName) {
                alert('Please enter a product name first before generating AI copywriting.');
                return;
            }

            const categoryName = categorySelect && categorySelect.selectedIndex >= 0 ? categorySelect.options[categorySelect.selectedIndex].text : '';
            const originalText = aiBtn.innerHTML;
            aiBtn.innerHTML = '✨ Crafting with Gemini...';
            aiBtn.disabled = true;

            try {
                const formData = new FormData();
                formData.append('name', productName);
                formData.append('category', categoryName);

                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

                const res = await fetch('/ai/admin/generate-description/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrfToken || '' },
                    body: formData,
                });
                const data = await res.json();
                if (data.description) {
                    descInput.value = data.description;
                } else if (data.error) {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Could not connect to Gemini service.');
            } finally {
                aiBtn.innerHTML = originalText;
                aiBtn.disabled = false;
            }
        });
    }
});
