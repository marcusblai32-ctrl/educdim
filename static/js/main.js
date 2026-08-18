document.addEventListener('DOMContentLoaded', function() {

    // ============================================
    // 1. MENU MOBILE
    // ============================================
    var menuToggle = document.getElementById('menuToggle');
    var mainNav = document.getElementById('mainNav');

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            mainNav.classList.toggle('active');
            var icon = this.querySelector('i');
            if (mainNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.main-header')) {
                mainNav.classList.remove('active');
                var icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }

    // ============================================
    // 2. USER DROPDOWN
    // ============================================
    var userDropdownBtn = document.getElementById('userDropdownBtn');

    if (userDropdownBtn) {
        userDropdownBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var parent = this.closest('.user-dropdown');
            if (parent) {
                parent.classList.toggle('open');
            }
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.user-dropdown')) {
                var dropdown = document.querySelector('.user-dropdown');
                if (dropdown) {
                    dropdown.classList.remove('open');
                }
            }
        });
    }

    // ============================================
    // 3. CHAT DROPDOWN
    // ============================================
    var chatDropdownBtn = document.getElementById('chatDropdownBtn');

    if (chatDropdownBtn) {
        chatDropdownBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var parent = this.closest('.nav-dropdown');
            if (parent) {
                parent.classList.toggle('open');
            }
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.nav-dropdown')) {
                var dropdowns = document.querySelectorAll('.nav-dropdown');
                dropdowns.forEach(function(dropdown) {
                    dropdown.classList.remove('open');
                });
            }
        });
    }

    // ============================================
    // 4. ALERT DISMISS
    // ============================================
    var closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var alert = this.closest('.alert');
            if (alert) {
                alert.style.transition = 'all 0.3s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(20px)';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        });
    });

    // ============================================
    // 5. ANIMASYON ON SCROLL
    // ============================================
    var animateElements = document.querySelectorAll('.animate-on-scroll');
    
    function checkVisibility() {
        animateElements.forEach(function(el) {
            var rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 100) {
                el.classList.add('visible');
            }
        });
    }

    checkVisibility();
    window.addEventListener('scroll', checkVisibility);

    // ============================================
    // 6. STATS COUNTER ANIMATION
    // ============================================
    var statNumbers = document.querySelectorAll('.stat-number');
    
    function animateStats() {
        statNumbers.forEach(function(stat) {
            var target = parseInt(stat.getAttribute('data-target'));
            if (!target) return;
            
            var current = parseInt(stat.textContent);
            if (current >= target) return;
            
            var increment = Math.ceil(target / 40);
            var interval = setInterval(function() {
                var currentVal = parseInt(stat.textContent);
                if (currentVal + increment >= target) {
                    stat.textContent = target;
                    clearInterval(interval);
                } else {
                    stat.textContent = currentVal + increment;
                }
            }, 50);
        });
    }

    var statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateStats();
                statsObserver.unobserve(entry.target);
            }
        });
    });

    statNumbers.forEach(function(stat) {
        statsObserver.observe(stat);
    });

    // ============================================
    // 7. SWIPER CAROUSEL (si w itilize l)
    // ============================================
    if (typeof Swiper !== 'undefined') {
        var swiper = new Swiper('.banner-swiper', {
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }

    // ============================================
    // 8. LOADING OVERLAY
    // ============================================
    var loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        setTimeout(function() {
            loadingOverlay.classList.add('hidden');
            setTimeout(function() {
                loadingOverlay.style.display = 'none';
            }, 400);
        }, 800);
    }

    console.log('JavaScript loaded successfully!');
});
