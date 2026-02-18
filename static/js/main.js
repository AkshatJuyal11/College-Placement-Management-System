// ========================================
// CPMS - JavaScript Utilities
// ========================================

// API Base URL
const API_BASE = '/api';

// Token management
const TokenManager = {
    set(token) {
        localStorage.setItem('token', token);
    },
    
    get() {
        return localStorage.getItem('token');
    },
    
    remove() {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        localStorage.removeItem('user_id');
    },
    
    setRole(role) {
        localStorage.setItem('role', role);
    },
    
    getRole() {
        return localStorage.getItem('role');
    },
    
    setUserId(userId) {
        localStorage.setItem('user_id', userId);
    },
    
    getUserId() {
        return localStorage.getItem('user_id');
    }
};

// API Client
const API = {
    async request(endpoint, options = {}) {
        const token = TokenManager.get();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                ...options,
                headers
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async get(endpoint) {
        return this.request(endpoint);
    },
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async uploadFile(endpoint, formData) {
        const token = TokenManager.get();
        const headers = {};
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        return data;
    }
};

// Utilities
const Utils = {
    showToast(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
        toast.style.zIndex = '9999';
        toast.style.minWidth = '300px';
        toast.innerHTML = message;
        
        document.body.appendChild(toast);
        
        // Fade in
        setTimeout(() => toast.style.opacity = '1', 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    logout() {
        TokenManager.remove();
        window.location.href = '/login';
    },
    
    checkAuth() {
        const token = TokenManager.get();
        if (!token) {
            window.location.href = '/login';
            return false;
        }
        return true;
    },
    
    showLoading(element) {
        element.innerHTML = '<div class="spinner mx-auto"></div>';
    },
    
    hideLoading(element, content) {
        element.innerHTML = content;
    }
};

// Form validation
const FormValidator = {
    email(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    password(password) {
        return password.length >= 6;
    },
    
    cgpa(cgpa) {
        const num = parseFloat(cgpa);
        return !isNaN(num) && num >= 0 && num <= 10;
    },
    
    required(value) {
        return value && value.trim().length > 0;
    }
};

// Export for use in other files
window.TokenManager = TokenManager;
window.API = API;
window.Utils = Utils;
window.FormValidator = FormValidator;
