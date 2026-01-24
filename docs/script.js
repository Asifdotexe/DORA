// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
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

function switchGallery(tabId) {
    // Update active state
    // Buttons
    document.querySelectorAll('.gallery-tab').forEach(tab => {
        tab.classList.remove('active');
        // Find the button that called this function or matches the tabId
        if (tab.onclick.toString().includes(tabId)) {
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

    // Reset timer on manual interaction (if event exists)
    if (window.event && window.event.isTrusted) {
        resetAutoRotate();
    }
}

function autoRotate() {
    currentTabIndex = (currentTabIndex + 1) % tabs.length;
    switchGallery(tabs[currentTabIndex]);
}

function resetAutoRotate() {
    clearInterval(autoRotateInterval);
    autoRotateInterval = setInterval(autoRotate, 5000);
}

// Start auto-rotation
autoRotateInterval = setInterval(autoRotate, 5000);
