/* ============================================================
   EDUCDIM - Complete JavaScript (FIXED)
   All dropdowns, menus, animations working
   ============================================================ */

(function() {
    "use strict";

    // Main initialization function
    function initEducDim() {
        console.log('EducDim: Initializing...');

        // ============================================
        // 1. MOBILE MENU TOGGLE (FIXED)
        // ============================================
        var menuToggle = document.getElementById('menuToggle');
        var mainNav = document.getElementById('mainNav');

        if (menuToggle && mainNav) {
            // Supprime les anciens écouteurs en clonant
            var newMenuToggle = menuToggle.cloneNode(true);
            menuToggle.parentNode.replaceChild(newMenuToggle, menuToggle);
            menuToggle = newMenuToggle;

            menuToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                var isOpen = mainNav.classList.toggle('active');
                var icon = this.querySelector('i');
                
                if (icon) {
                    icon.className = isOpen ? 'fas fa-times' : 'fas fa-bars';
                }
                
                this.setAttribute('aria-expanded', String(isOpen));
                this.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
            });

            // Ferme le menu au clic extérieur
            document.addEventListener('click', function(e) {
                var target = e.target;
                if (!(target instanceof Element)) return;
                
                if (!target.closest('.main-header') && !target.closest('#mainNav')) {
                    mainNav.classList.remove('active');
                    if (menuToggle) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        var icon = menuToggle.querySelector('i');
                        if (icon) {
                            icon.className = 'fas fa-bars';
                        }
                    }
                }
            });
        }

        // ============================================
        // 2. DROPDOWNS UNIFIÉS (USER + CHAT)
        // Utilise la délégation d'événements sur document
        // ============================================
        
        // Supprime d'abord tous les anciens écouteurs en clonant
        var userDropdownBtn = document.getElementById('userDropdownBtn');
        var chatDropdownBtn = document.getElementById('chatDropdownBtn');
        
        // On n'utilise PAS de clonage ici pour éviter les conflits
        // On utilise la délégation d'événements sur document
        
        // Fonction pour fermer tous les dropdowns
        function closeAllDropdowns(exceptDropdown) {
            var allDropdowns = document.querySelectorAll('.user-dropdown, .nav-dropdown');
            allDropdowns.forEach(function(dropdown) {
                if (dropdown !== exceptDropdown) {
                    dropdown.classList.remove('open');
                    var btn = dropdown.querySelector('.dropbtn, .nav-dropdown-btn');
                    if (btn) btn.setAttribute('aria-expanded', 'false');
                }
            });
        }

        // Gestionnaire de clic global pour les dropdowns
        document.addEventListener('click', function(e) {
            var target = e.target;
            if (!(target instanceof Element)) return;

            // Vérifie si on a cliqué sur un bouton dropdown
            var dropdownBtn = target.closest('.dropbtn, .nav-dropdown-btn');
            
            if (dropdownBtn) {
                e.preventDefault();
                e.stopPropagation();
                
                var dropdown = dropdownBtn.closest('.user-dropdown, .nav-dropdown');
                if (!dropdown) return;
                
                // Ferme tous les autres dropdowns
                closeAllDropdowns(dropdown);
                
                // Toggle le dropdown courant
                var isOpen = dropdown.classList.toggle('open');
                dropdownBtn.setAttribute('aria-expanded', String(isOpen));
                
                console.log('Dropdown toggled:', isOpen);
            } else {
                // Clic en dehors des dropdowns - ferme tout
                if (!target.closest('.user-dropdown, .nav-dropdown')) {
                    closeAllDropdowns(null);
                }
            }
        });

        // ============================================
        // 3. CLOSE DROPDOWNS ON ESCAPE KEY
        // ============================================
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                // Ferme tous les dropdowns
                closeAllDropdowns(null);
                
                // Ferme le menu mobile
                if (mainNav && mainNav.classList.contains('active')) {
                    mainNav.classList.remove('active');
                    if (menuToggle) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        var icon = menuToggle.querySelector('i');
                        if (icon) {
                            icon.className = 'fas fa-bars';
                        }
                    }
                }
            }
        });

        // ============================================
        // 4. ALERT DISMISS (FIXED)
        // ============================================
        var closeButtons = document.querySelectorAll('.close-alert');
        closeButtons.forEach(function(btn) {
            var newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);
            
            newBtn.addEventListener('click', function() {
                var alert = this.closest('.alert');
                if (alert) {
                    alert.style.transition = 'all 0.3s ease';
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(20px)';
                    setTimeout(function() {
                        if (alert.parentNode) alert.remove();
                    }, 300);
                }
            });
        });

        // Auto-dismiss alerts after 5 seconds
        document.querySelectorAll('.alert:not(.alert-persistent)').forEach(function(alert) {
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
        // 5. SMOOTH SCROLL FOR ANCHOR LINKS
        // ============================================
        document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function(link) {
            link.addEventListener('click', function(event) {
                var href = this.getAttribute('href');
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
                
                // Ferme menu mobile
                if (mainNav) {
                    mainNav.classList.remove('active');
                    if (menuToggle) {
                        menuToggle.setAttribute('aria-expanded', 'false');
                        var icon = menuToggle.querySelector('i');
                        if (icon) {
                            icon.className = 'fas fa-bars';
                        }
                    }
                }
            });
        });

        // ============================================
        // 6. SCROLL REVEAL ANIMATIONS (VISIBLE BY DEFAULT)
        // ============================================
        var revealItems = document.querySelectorAll('.reveal, .reveal-two, .reveal-three, .animate-on-scroll');
        
        // Ajoute directement la classe visible pour que tout soit visible
        revealItems.forEach(function(item) {
            item.classList.add('visible');
        });

        // ============================================
        // 7. STATS COUNTER ANIMATION
        // ============================================
        var statNumbers = document.querySelectorAll('.stat-number');
        
        if (statNumbers.length) {
            var statTargets = [];

            statNumbers.forEach(function(stat) {
                var target = parseInt(stat.getAttribute('data-target'));
                if (!target) {
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

            // Anime immédiatement sans attendre IntersectionObserver
            statTargets.forEach(function(data) {
                setTimeout(function() {
                    animateCounter(data);
                }, 300);
            });
        }

        // ============================================
        // 8. FEATURE CARD INTERACTIVE EFFECTS
        // ============================================
        var featureCards = document.querySelectorAll('.feature-card');

        featureCards.forEach(function(card) {
            card.addEventListener('mouseenter', function() {
                var icon = this.querySelector('.feature-icon, .feature-icon-wrapper');
                if (icon) {
                    icon.style.transition = 'transform 0.3s ease';
                    icon.style.transform = 'scale(1.1) rotate(5deg)';
                }
            });

            card.addEventListener('mouseleave', function() {
                var icon = this.querySelector('.feature-icon, .feature-icon-wrapper');
                if (icon) {
                    icon.style.transform = 'scale(1) rotate(0deg)';
                }
            });
        });

        // ============================================
        // 9. TESTIMONIAL CARD HOVER
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
        // 10. PROOF AVATARS PULSE
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
        // 11. PARALLAX EFFECT ON HERO
        // ============================================
        var heroOrbits = document.querySelectorAll('.hero-orbit');
        var heroPhoto = document.querySelector('.hero-photo-frame');

        if (heroOrbits.length) {
            window.addEventListener('scroll', function() {
                var scrolled = window.pageYOffset;

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
        // 12. ORBIT PARALLAX ON MOUSE MOVE
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
        // 13. HEADER SCROLL EFFECT
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
        // 14. SWIPER CAROUSEL (if available)
        // ============================================
        if (typeof Swiper !== 'undefined') {
            var swiperEl = document.querySelector('.banner-swiper, .swiper-container');
            if (swiperEl) {
                new Swiper(swiperEl, {
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
        // 15. LOADING OVERLAY
        // ============================================
        var loadingOverlay = document.getElementById('loadingOverlay');

        if (loadingOverlay) {
            loadingOverlay.classList.add('active');

            setTimeout(function() {
                loadingOverlay.classList.remove('active');
                loadingOverlay.style.opacity = '0';
                setTimeout(function() {
                    loadingOverlay.style.display = 'none';
                }, 400);
            }, 800);
        }

        // ============================================
        // 16. LAZY LOAD IMAGES
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
        // 17. FIX: CLOSE DROPDOWNS ON WINDOW RESIZE
        // ============================================
        var resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                if (window.innerWidth < 768) {
                    document.querySelectorAll('.user-dropdown.open, .nav-dropdown.open').forEach(function(item) {
                        item.classList.remove('open');
                    });
                    var allBtns = document.querySelectorAll('#userDropdownBtn, #chatDropdownBtn');
                    allBtns.forEach(function(btn) {
                        btn.setAttribute('aria-expanded', 'false');
                    });
                }
            }, 250);
        });

        console.log('EducDim: Initialization complete!');
    }

    // ============================================
    // INITIALIZATION
    // ============================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEducDim);
    } else {
        initEducDim();
    }

    // Réinitialise sur navigation dynamique
    if (typeof Turbolinks !== 'undefined') {
        document.addEventListener('turbolinks:load', function() {
            setTimeout(initEducDim, 100);
        });
    }

    if (typeof htmx !== 'undefined') {
        document.addEventListener('htmx:afterSwap', function() {
            setTimeout(initEducDim, 100);
        });
    }

    // Expose pour ré-init manuel
    window.EducDim = {
        init: initEducDim,
        version: '3.0.0'
    };

})();

/* ============================================
   AURORA GLASS — playful interactive polish
   Pointer-tracked 3D tilt + light spotlight on
   glass surfaces. Desktop only, respects
   prefers-reduced-motion. Pure vanilla JS.
   ============================================ */
(function() {
    "use strict";

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
    if (reduceMotion || isTouch) return;

    var TILT_SELECTOR = '.course-card, .feature-card, .testimonial-card, .room-card, .badge-card, .plan-card, .quiz-card, .hero-visual .hero-card, .rank-card';

    function bindTilt() {
        var cards = document.querySelectorAll(TILT_SELECTOR);

        cards.forEach(function(card) {
            if (card.dataset.tiltBound === '1') return;
            card.dataset.tiltBound = '1';

            card.style.transformStyle = 'preserve-3d';
            card.style.willChange = 'transform';

            card.addEventListener('mousemove', function(e) {
                var rect = card.getBoundingClientRect();
                var px = (e.clientX - rect.left) / rect.width;
                var py = (e.clientY - rect.top) / rect.height;
                var rotY = (px - 0.5) * 9;
                var rotX = (0.5 - py) * 9;

                card.style.transition = 'transform 0.08s ease-out';
                card.style.transform = 'perspective(900px) rotateX(' + rotX.toFixed(2) + 'deg) rotateY(' + rotY.toFixed(2) + 'deg) translateY(-6px)';

                card.style.setProperty('--mx', (px * 100).toFixed(1) + '%');
                card.style.setProperty('--my', (py * 100).toFixed(1) + '%');
                if (!card.dataset.spotlight) {
                    card.dataset.spotlight = '1';
                    card.style.backgroundImage = 'radial-gradient(220px circle at var(--mx) var(--my), rgba(255,255,255,0.28), transparent 60%)';
                }
            });

            card.addEventListener('mouseleave', function() {
                card.style.transition = 'transform 0.5s cubic-bezier(0.34,1.56,0.64,1)';
                card.style.transform = '';
                card.style.backgroundImage = '';
                delete card.dataset.spotlight;
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindTilt);
    } else {
        bindTilt();
    }

    if (typeof htmx !== 'undefined') {
        document.addEventListener('htmx:afterSwap', function() { setTimeout(bindTilt, 120); });
    }
    if (typeof Turbolinks !== 'undefined') {
        document.addEventListener('turbolinks:load', function() { setTimeout(bindTilt, 120); });
    }
})();