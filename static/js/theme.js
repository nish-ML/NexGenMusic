// Theme Management
const themeToggle = document.getElementById('themeToggle');
const userBtn = document.getElementById('userBtn');
const userDropdown = document.getElementById('userDropdown');
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
document.body.setAttribute('data-theme', savedTheme);

// Theme toggle
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// User dropdown toggle
if (userBtn && userDropdown) {
    userBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!userDropdown.contains(e.target) && !userBtn.contains(e.target)) {
            userDropdown.classList.remove('active');
        }
    });
}

// Mobile menu toggle
if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// Logout functionality
const logoutBtn = document.querySelector('.dropdown-item.logout');
if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
    });
}

// Auto-login helper
async function autoLogin() {
    const API_BASE = '/api/';
    let userToken = localStorage.getItem('token');
    
    if (!userToken) {
        try {
            const response = await fetch(API_BASE + 'register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    username: 'user_' + Date.now(), 
                    password: 'pass123' 
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                userToken = data.access;
                localStorage.setItem('token', userToken);
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    }
    
    return userToken;
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export for use in other scripts
window.autoLogin = autoLogin;
window.escapeHtml = escapeHtml;
