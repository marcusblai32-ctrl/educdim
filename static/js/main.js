/* ============================================
   EDUCDIM - Complete JavaScript
   Merged: Vanilla JS + Enhanced Features
   ============================================ */

(function() {
    "use strict";

    // Main initialization function
    function initEducDim() {

        // ============================================
        // 1. MOBILE MENU TOGGLE
        // ============================================
        var menuToggle = document.getElementById('menuToggle');
        var mainNav = document.getElementById('mainNav');

        if (menuToggle && mainNav) {
            menuToggle.addEventListener('click', function(e) {
                e.stopPropagation();
                var isOpen = mainNav.classList.toggle('active');
                var icon = this.querySelector('i');
                
                if (icon) {
                    if (isOpen) {
                        icon.classList.remove('fa-bars');
                        icon.classList.add('fa-times');
                    } else {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
                
                // Update accessibility attributes
                menuToggle.setAttribute('aria-expanded', String(isOpen));
                menuToggle.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
            });

            // Close menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.main-header')) {
                    mainNav.classList.remove('active');
                    var icon = menuToggle.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                    menuToggle.setAttribute('aria-expanded', 'false');
                }
            });
        }

        // ============================================
        // 2. DROPDOWN TOGGLE (Unified function)
        // ============================================
        function setupDropdown(buttonId, containerSelector, otherSelector) {
            var button = document.getElementById(buttonId);
            if (!button) return;

            button.addEventListener('click', function(e) {
                e.stopPropagation();
                var parent = this.closest(containerSelector);
                if (!parent) return;

                // Close other dropdowns
                document.querySelectorAll(otherSelector).forEach(function(item) {
                    if (item !== parent) item.classList.remove('open');
                });

                var isOpen = parent.classList.toggle('open');
                button.setAttribute('aria-expanded', String(isOpen));
            });
        }

        // Setup User Dropdown
        setupDropdown('userDropdownBtn', '.user-dropdown', '.user-dropdown, .nav-dropdown');

        // Setup Chat Dropdown
        setupDropdown('chatDropdownBtn', '.nav-dropdown', '.user-dropdown, .nav-dropdown');

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            var target = e.target;
            if (!(target instanceof Element)) return;

            // Close user dropdown
            if (!target.closest('.user-dropdown')) {
                document.querySelectorAll('.user-dropdown').forEach(function(item) {
                    item.classList.remove('open');
                });
            }

            // Close chat dropdown
            if (!target.closest('.nav-dropdown')) {
                document.querySelectorAll('.nav-dropdown').forEach(function(item) {
                    item.classList.remove('open');
                });
            }
        });

        // ============================================
        // 3. ALERT DISMISS
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

        // Auto-dismiss alerts after 5 seconds
        document.querySelectorAll('.alert').forEach(function(alert) {
            setTimeout(function() {
                if (alert && alert.parentNode) {
                    alert.style.transition = 'all 0.3s ease';
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(20px)';
                    setTimeout(function() {
                        if (alert.parentNode) alert.remove();
                    }, 300);
                }
            }, 5000);
        });

        // ============================================
        // 4. SMOOTH SCROLL FOR ANCHOR LINKS
        // ============================================
        document.querySelectorAll('a[href^="#"]').forEach(function(link) {
            link.addEventListener('click', function(event) {
                var href = link.getAttribute('href');
                if (!href || href === '#') return;
                
                var target = document.querySelector(href);
                if (!target) return;
                
                event.preventDefault();
                
                var headerOffset = 80;
                var elementPosition = target.getBoundingClientRect().top;
                var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (mainNav) {
                    mainNav.classList.remove('active');
                    if (menuToggle) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        var icon = menuToggle.querySelector('i');
                        if (icon) {
                            icon.classList.remove('fa-times');
                            icon.classList.add('fa-bars');
                        }
                    }
                }
                
                // Update URL without reload
                if (history.pushState) {
                    history.pushState(null, null, href);
                }
            });
        });

        // ============================================
        // 5. SCROLL REVEAL ANIMATIONS
        // ============================================
        var revealItems = document.querySelectorAll('.reveal, .reveal-two, .reveal-three, .animate-on-scroll');

        if ('IntersectionObserver' in window) {
            var revealObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.12,
                rootMargin: '0px 0px -30px 0px'
            });

            revealItems.forEach(function(item) {
                revealObserver.observe(item);
            });
        } else {
            // Fallback for older browsers
            revealItems.forEach(function(item) {
                item.classList.add('visible');
            });
        }

        // ============================================
        // 6. STATS COUNTER ANIMATION
        // ============================================
        var statNumbers = document.querySelectorAll('.stat-number');
        var statTargets = [];

        // Store targets from data-target or from content
        statNumbers.forEach(function(stat) {
            var target = parseInt(stat.getAttribute('data-target'));
            if (!target) {
                // Extract number from text content
                var textContent = stat.textContent.replace(/[^0-9]/g, '');
                target = parseInt(textContent);
                if (isNaN(target) || target === 0) return;
                stat.setAttribute('data-target', target);
            }
            statTargets.push({
                element: stat,
                target: target,
                current: 0,
                suffix: stat.textContent.replace(/[0-9]/g, ''),
                animated: false
            });
        });

        function animateCounter(data) {
            if (data.animated) return;
            data.animated = true;

            var duration = 2000;
            var startTime = null;
            var target = data.target;
            var element = data.element;
            var suffix = data.suffix;

            function updateCounter(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                
                // Ease out cubic
                var eased = 1 - Math.pow(1 - progress, 3);
                var current = Math.floor(eased * target);
                
                element.textContent = current + suffix;
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    element.textContent = target + suffix;
                }
            }

            requestAnimationFrame(updateCounter);
        }

        if ('IntersectionObserver' in window) {
            var statsObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        var index = statTargets.findIndex(function(item) {
                            return item.element === entry.target;
                        });
                        if (index !== -1 && !statTargets[index].animated) {
                            animateCounter(statTargets[index]);
                        }
                        statsObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            statNumbers.forEach(function(stat) {
                statsObserver.observe(stat);
            });
        } else {
            // Fallback: animate all stats immediately
            statTargets.forEach(function(data) {
                animateCounter(data);
            });
        }

        // ============================================
        // 7. FEATURE CARD INTERACTIVE EFFECTS
        // ============================================
        var featureCards = document.querySelectorAll('.feature-card');

        featureCards.forEach(function(card) {
            card.addEventListener('mouseenter', function() {
                var icon = this.querySelector('.feature-icon');
                if (icon) {
                    icon.style.transition = 'transform 0.3s ease';
                    icon.style.transform = 'scale(1.1) rotate(5deg)';
                }
                this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            });

            card.addEventListener('mouseleave', function() {
                var icon = this.querySelector('.feature-icon');
                if (icon) {
                    icon.style.transform = 'scale(1) rotate(0deg)';
                }
            });
        });

        // ============================================
        // 8. TESTIMONIAL CARD HOVER
        // ============================================
        var testimonialCards = document.querySelectorAll('.testimonial-card');

        testimonialCards.forEach(function(card) {
            card.addEventListener('mouseenter', function() {
                this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
                this.style.transform = 'translateY(-6px)';
                this.style.boxShadow = '0 20px 35px rgba(19, 43, 53, 0.12)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        });

        // ============================================
        // 9. PROOF AVATARS PULSE
        // ============================================
        var proofDots = document.querySelectorAll('.proof-dot');

        proofDots.forEach(function(dot, index) {
            dot.style.transition = 'transform 0.3s ease';
            var delay = index * 200;
            
            setInterval(function() {
                dot.style.transform = 'scale(1.2)';
                setTimeout(function() {
                    dot.style.transform = 'scale(1)';
                }, 300);
            }, 3000 + delay);
        });

        // ============================================
        // 10. PARALLAX EFFECT ON HERO
        // ============================================
        var heroSection = document.querySelector('.hero-section');
        var heroOrbits = document.querySelectorAll('.hero-orbit');
        var heroPhoto = document.querySelector('.hero-photo-frame');

        if (heroSection && heroOrbits.length) {
            window.addEventListener('scroll', function() {
                var scrolled = window.pageYOffset;
                var rate = Math.min(scrolled / 500, 1);

                heroOrbits.forEach(function(orbit, index) {
                    var speed = (index === 0) ? 0.15 : 0.25;
                    var translateY = scrolled * speed * 0.05;
                    var translateX = scrolled * speed * 0.02;
                    orbit.style.transform = 'translate(' + translateX + 'px, ' + translateY + 'px)';
                });

                if (heroPhoto) {
                    var scale = 1 + (scrolled * 0.0001);
                    var opacity = 1 - (scrolled * 0.0003);
                    heroPhoto.style.transform = 'scale(' + Math.min(scale, 1.03) + ')';
                    heroPhoto.style.opacity = Math.max(opacity, 0.7);
                }
            }, { passive: true });
        }

        // ============================================
        // 11. ORBIT PARALLAX ON MOUSE MOVE
        // ============================================
        if (heroOrbits.length) {
            document.addEventListener('mousemove', function(e) {
                var x = (e.clientX / window.innerWidth - 0.5) * 20;
                var y = (e.clientY / window.innerHeight - 0.5) * 20;

                heroOrbits.forEach(function(orbit, index) {
                    var speed = (index === 0) ? 0.3 : 0.5;
                    orbit.style.transition = 'transform 0.1s ease-out';
                    orbit.style.transform = 'translate(' + (x * speed) + 'px, ' + (y * speed) + 'px)';
                });
            });
        }

        // ============================================
        // 12. SWIPER CAROUSEL (if available)
        // ============================================
        if (typeof Swiper !== 'undefined') {
            var swiperEl = document.querySelector('.banner-swiper, .swiper-container');
            if (swiperEl) {
                var swiper = new Swiper(swiperEl, {
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
                    effect: 'slide',
                    speed: 600,
                });
            }
        }

        // ============================================
        // 13. LOADING OVERLAY
        // ============================================
        var loadingOverlay = document.getElementById('loadingOverlay');

        if (loadingOverlay) {
            // Add active class to show loading
            loadingOverlay.classList.add('active');

            setTimeout(function() {
                loadingOverlay.classList.remove('active');
                loadingOverlay.classList.add('hidden');
                setTimeout(function() {
                    loadingOverlay.style.display = 'none';
                }, 400);
            }, 800);
        }

        // ============================================
        // 14. LAZY LOAD IMAGES
        // ============================================
        if ('IntersectionObserver' in window) {
            var lazyImages = document.querySelectorAll('.hero-photo-frame img, .about-photo-wrap img, .testimonial-person img');

            var imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        var img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            }, { rootMargin: '50px' });

            lazyImages.forEach(function(img) {
                imageObserver.observe(img);
            });
        }

        // ============================================
        // 15. HEADER SCROLL EFFECT
        // ============================================
        var header = document.querySelector('.main-header');

        if (header) {
            window.addEventListener('scroll', function() {
                if (window.scrollY > 50) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            }, { passive: true });
        }

        // ============================================
        // 16. KEYBOARD ACCESSIBILITY
        // ============================================
        // Close dropdowns on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.user-dropdown.open, .nav-dropdown.open').forEach(function(item) {
                    item.classList.remove('open');
                });
                if (mainNav && mainNav.classList.contains('active')) {
                    mainNav.classList.remove('active');
                    if (menuToggle) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        var icon = menuToggle.querySelector('i');
                        if (icon) {
                            icon.classList.remove('fa-times');
                            icon.classList.add('fa-bars');
                        }
                    }
                }
            }
        });

        // ============================================
        // 17. CONSOLE LOG (for debugging)
        // ============================================
        console.log('EducDim JavaScript initialized successfully!');

        // ============================================
        // 18. EXPOSE FOR REINIT
        // ============================================
        window.EducDim = {
            init: initEducDim,
            version: '2.0.0'
        };
    }

    // ============================================
    // INITIALIZATION
    // ============================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEducDim);
    } else {
        initEducDim();
    }

    // Re-initialize on Turbolinks/HTMX navigation
    if (typeof Turbolinks !== 'undefined') {
        document.addEventListener('turbolinks:load', initEducDim);
    }

    if (typeof htmx !== 'undefined') {
        document.addEventListener('htmx:afterSwap', function() {
            setTimeout(initEducDim, 100);
        });
    }

})();
