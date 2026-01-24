// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const href = this.getAttribute('href');
        if (!href || href === '#') return;

        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Copy code to clipboard
function copyCode(elementId) {
    const codeElement = document.getElementById(elementId);
    let codeText = codeElement.innerText;

    // Remove the '$ ' prompt if present for copying
    if (codeText.startsWith('$ ')) {
        codeText = codeText.substring(2);
    }

    navigator.clipboard.writeText(codeText).then(() => {
        // Visual feedback
        const btn = codeElement.parentElement.querySelector('.copy-btn');
        const originalText = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.background = '#2b9388';

        setTimeout(() => {
            btn.innerText = originalText;
            btn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

// Simple fade-in animation on scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add visible class styling
const style = document.createElement('style');
style.textContent = `
    .visible {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);

// Gallery switching
const tabs = ['cli', 'web', 'report'];
let currentTabIndex = 0;
let autoRotateInterval;

function switchGallery(tabId, event) {
    // Update active state
    // Buttons
    document.querySelectorAll('.gallery-tab').forEach(tab => {
        tab.classList.remove('active');
        // Check data attribute
        if (tab.dataset.tab === tabId) {
            tab.classList.add('active');
        }
    });

    // Content
    document.querySelectorAll('.gallery-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById('gallery-' + tabId).classList.add('active');

    // Update current index for auto-rotation
    currentTabIndex = tabs.indexOf(tabId);

    // Reset timer on manual interaction (if event exists and is trusted)
    if (event && event.isTrusted) {
        resetAutoRotate();
    }
}

function autoRotate() {
    currentTabIndex = (currentTabIndex + 1) % tabs.length;
    switchGallery(tabs[currentTabIndex]); // No event passed for auto-rotation
}

function resetAutoRotate() {
    clearInterval(autoRotateInterval);
    autoRotateInterval = setInterval(autoRotate, 5000);
}

// Start auto-rotation
autoRotateInterval = setInterval(autoRotate, 5000);

// Mobile Nav Toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');

        // Change icon
        const icon = navToggle.querySelector('i');
        if (navLinks.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.querySelector('i').classList.add('fa-bars');
            navToggle.querySelector('i').classList.remove('fa-times');
        });
    });
}
