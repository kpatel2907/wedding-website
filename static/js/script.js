// ==========================================
// Wedding Website - JavaScript
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    initNavigation();
    
    // Initialize RSVP form
    initRSVPForm();
    
    // Initialize scroll effects
    initScrollEffects();
});

// ==========================================
// Navigation
// ==========================================

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetPage = this.getAttribute('data-page');
            
            // If no data-page attribute, let the link navigate normally (e.g., RSVP link)
            if (!targetPage) {
                return;
            }
            
            e.preventDefault();
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Update active page
            pages.forEach(page => {
                page.classList.remove('active');
                if (page.id === targetPage || (targetPage === 'welcome' && page.id === 'welcome')) {
                    page.classList.add('active');
                }
            });
            
            // Scroll to top smoothly
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
            // Update URL hash
            history.pushState(null, null, `#${targetPage}`);
        });
    });
    
    // Handle initial hash in URL
    handleInitialHash();
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', handleInitialHash);
}

function handleInitialHash() {
    const hash = window.location.hash.slice(1);
    if (hash) {
        const targetLink = document.querySelector(`.nav-link[data-page="${hash}"]`);
        if (targetLink) {
            targetLink.click();
        }
    }
}

// ==========================================
// RSVP Form
// ==========================================

function initRSVPForm() {
    const form = document.getElementById('rsvpForm');
    const successMessage = document.getElementById('rsvpSuccess');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                guests: formData.get('guests'),
                events: formData.getAll('events'),
                dietary: formData.get('dietary'),
                message: formData.get('message')
            };
            
            // Log the data (in a real app, you would send this to a server)
            console.log('RSVP Submission:', data);
            
            // Show success message
            form.style.display = 'none';
            successMessage.classList.add('show');
            
            // Store in localStorage for demo purposes
            const rsvps = JSON.parse(localStorage.getItem('weddingRSVPs') || '[]');
            rsvps.push({
                ...data,
                submittedAt: new Date().toISOString()
            });
            localStorage.setItem('weddingRSVPs', JSON.stringify(rsvps));
        });
    }
}

// ==========================================
// Scroll Effects
// ==========================================

function initScrollEffects() {
    // Header shadow on scroll
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
        }
    });
    
    // Animate elements on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.timeline-item, .event-card').forEach(el => {
        observer.observe(el);
    });
}

// ==========================================
// Utility Functions
// ==========================================

// Smooth scroll to element
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Format date
function formatDate(dateString) {
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Countdown timer (can be used for homepage)
function createCountdown(targetDate) {
    const target = new Date(targetDate).getTime();
    
    return setInterval(function() {
        const now = new Date().getTime();
        const distance = target - now;
        
        if (distance < 0) {
            return { days: 0, hours: 0, minutes: 0, seconds: 0 };
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        return { days, hours, minutes, seconds };
    }, 1000);
}
