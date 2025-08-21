// client/login.js

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');

    messageDiv.style.display = 'none';

    try {
        // L'URL punta ora al path relativo gestito da Nginx
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();

        messageDiv.style.display = 'block';
        if (response.ok) {
            //messageDiv.textContent = 'Login riuscito! Token: ' + data.token;
            //messageDiv.className = 'success';
            localStorage.setItem('jwt_token', data.token);
            window.location.href = '/dashboard.html';
        } else {
            messageDiv.textContent = 'Errore: ' + (data.error || 'Credenziali non valide');
            messageDiv.className = 'error';
        }

    } catch (error) {
        messageDiv.style.display = 'block';
        messageDiv.textContent = 'Errore di rete. Riprova più tardi.';
        messageDiv.className = 'error';
        console.error('Fetch error:', error);
    }
});