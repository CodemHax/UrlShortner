document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('urlInput');
    const shortenBtn = document.getElementById('shortenBtn');
    const result = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrlInput');
    const copyBtn = document.getElementById('copyBtn');
    const uuidInput = document.getElementById('uuidInput');
    const newUrlInput = document.getElementById('newUrlInput');
    const updateBtn = document.getElementById('updateBtn');
    const deleteInput = document.getElementById('deleteInput');
    const deleteBtn = document.getElementById('deleteBtn');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');

            const tabName = button.getAttribute('data-tab');
            if (tabName === 'update') {
                document.getElementById('updateTab').classList.add('active');
            } else if (tabName === 'delete') {
                document.getElementById('deleteTab').classList.add('active');
            }
        });
    });

    function showMessage(element, message, type) {
        const existingMessage = element.querySelector('.message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        element.appendChild(messageElement);

        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }

    async function shortenUrl() {
        const url = urlInput.value.trim();

        if (!url) {
            showMessage(document.querySelector('.form-group'), 'Please enter a URL', 'error');
            return;
        }

        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (response.ok) {
                result.classList.remove('hidden');
                shortUrlInput.value = data.url;
            } else {
                showMessage(document.querySelector('.form-group'), data.error || 'Error shortening URL', 'error');
            }
        } catch (error) {
            showMessage(document.querySelector('.form-group'), 'Network error, please try again', 'error');
        }
    }

    async function updateUrl() {
        const uuid = uuidInput.value.trim();
        const newUrl = newUrlInput.value.trim();

        if (!uuid || !newUrl) {
            showMessage(document.getElementById('updateTab'), 'Please fill in all fields', 'error');
            return;
        }

        try {
            const response = await fetch('/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ uuid, url: newUrl })
            });

            if (response.ok) {
                showMessage(document.getElementById('updateTab'), 'URL updated successfully', 'success');
                uuidInput.value = '';
                newUrlInput.value = '';
            } else {
                const data = await response.json();
                showMessage(document.getElementById('updateTab'), data.detail || 'Error updating URL', 'error');
            }
        } catch (error) {
            showMessage(document.getElementById('updateTab'), 'Network error, please try again', 'error');
        }
    }

    async function deleteUrl() {
        const urlToDelete = deleteInput.value.trim();

        if (!urlToDelete) {
            showMessage(document.getElementById('deleteTab'), 'Please enter a URL ID to delete', 'error');
            return;
        }

        try {
            const response = await fetch(`/delete/${urlToDelete}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                showMessage(document.getElementById('deleteTab'), 'URL deleted successfully', 'success');
                deleteInput.value = '';
            } else {
                const data = await response.json();
                showMessage(document.getElementById('deleteTab'), data.detail || 'Error deleting URL', 'error');
            }
        } catch (error) {
            showMessage(document.getElementById('deleteTab'), 'Network error, please try again', 'error');
        }
    }

    function copyToClipboard() {
        shortUrlInput.select();
        document.execCommand('copy');
        showMessage(document.querySelector('.result-container'), 'Copied to clipboard!', 'success');
    }

    shortenBtn.addEventListener('click', shortenUrl);
    copyBtn.addEventListener('click', copyToClipboard);
    updateBtn.addEventListener('click', updateUrl);
    deleteBtn.addEventListener('click', deleteUrl);

    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            shortenUrl();
        }
    });
});
