/*
 * EducDim — main.js
 * Complete JavaScript for navigation, dropdowns, animations
 * Version 4.0 - Final
 */
(function () {
  "use strict";

  function initEducDim() {
    var menuToggle = document.getElementById("menuToggle");
    var mainNav = document.getElementById("mainNav");
    var loadingOverlay = document.getElementById("loadingOverlay");

    var dropdownButtons = document.querySelectorAll(
      "#chatDropdownBtn, #userDropdownBtn, .nav-dropdown-btn, .dropbtn"
    );
    var dropdowns = document.querySelectorAll(".nav-dropdown, .user-dropdown");
    var closeAlerts = document.querySelectorAll(".close-alert");
    var revealItems = document.querySelectorAll(".animate-on-scroll, .reveal, .reveal-two, .reveal-three");
    var statNumbers = document.querySelectorAll(".stat-number");

    function isMobile() {
      return window.matchMedia("(max-width: 768px)").matches;
    }

    function setExpanded(button, expanded) {
      if (button) button.setAttribute("aria-expanded", String(expanded));
    }

    function setMenuIcon(open) {
      if (!menuToggle) return;
      var icon = menuToggle.querySelector("i, svg");
      if (icon) {
        if (icon.classList.contains("fa-bars") || icon.classList.contains("fa-times")) {
          icon.className = open ? "fas fa-times" : "fas fa-bars";
        }
      }
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    }

    function closeDropdown(dropdown) {
      dropdown.classList.remove("open");
      setExpanded(dropdown.querySelector(".nav-dropdown-btn, .dropbtn"), false);
    }

    function closeAllDropdowns(except) {
      dropdowns.forEach(function (dropdown) {
        if (dropdown !== except) closeDropdown(dropdown);
      });
    }

    function closeMenu() {
      if (!mainNav) return;
      mainNav.classList.remove("active");
      setMenuIcon(false);
      closeAllDropdowns();
    }

    function toggleMenu(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      if (!mainNav || !isMobile()) return;
      var open = !mainNav.classList.contains("active");
      if (open) {
        closeAllDropdowns();
        mainNav.classList.add("active");
        setMenuIcon(true);
      } else {
        closeMenu();
      }
    }

    // ============================================
    // MOBILE MENU TOGGLE
    // ============================================
    if (menuToggle && mainNav) {
      menuToggle.addEventListener("click", toggleMenu);
      setMenuIcon(mainNav.classList.contains("active"));
    }

    // ============================================
    // DROPDOWNS - Délégation d'événements
    // ============================================
    dropdownButtons.forEach(function (button) {
      button.setAttribute("aria-expanded", "false");
      button.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        var dropdown = button.closest(".nav-dropdown, .user-dropdown");
        if (!dropdown) return;

        var open = !dropdown.classList.contains("open");
        closeAllDropdowns(dropdown);
        dropdown.classList.toggle("open", open);
        setExpanded(button, open);
      });
    });

    // ============================================
    // CLOSE ON OUTSIDE CLICK
    // ============================================
    document.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof Element)) return;

      if (!target.closest(".nav-dropdown, .user-dropdown")) {
        closeAllDropdowns();
      }

      if (
        isMobile() &&
        !target.closest("#mainNav") &&
        !target.closest("#menuToggle")
      ) {
        closeMenu();
      }
    });

    // ============================================
    // CLOSE ON ESCAPE KEY
    // ============================================
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeAllDropdowns();
        closeMenu();
      }
    });

    // ============================================
    // CLOSE ALERTS
    // ============================================
    closeAlerts.forEach(function (button) {
      button.addEventListener("click", function () {
        var alert = button.closest(".alert");
        if (alert) {
          alert.style.transition = "all 0.3s ease";
          alert.style.opacity = "0";
          alert.style.transform = "translateX(20px)";
          setTimeout(function () {
            if (alert.parentNode) alert.remove();
          }, 300);
        }
      });
    });

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll(".alert:not(.alert-persistent)").forEach(function (alert) {
      setTimeout(function () {
        if (alert && alert.parentNode) {
          alert.style.transition = "all 0.3s ease";
          alert.style.opacity = "0";
          alert.style.transform = "translateX(20px)";
          setTimeout(function () {
            if (alert.parentNode) alert.remove();
          }, 300);
        }
      }, 5000);
    });

    // ============================================
    // CLOSE MENU ON NAV LINK CLICK (MOBILE)
    // ============================================
    document.querySelectorAll("#mainNav a, .footer-container nav a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (isMobile()) closeMenu();
      });
    });

    // ============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function (event) {
        var href = link.getAttribute("href");
        if (!href || href === "#" || href.length < 2) return;
        var target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        var headerOffset = 80;
        var elementPosition = target.getBoundingClientRect().top;
        var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth"
        });
        if (isMobile()) closeMenu();
      });
    });

    // ============================================
    // SCROLL REVEAL ANIMATIONS
    // ============================================
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
      revealItems.forEach(function (item) { observer.observe(item); });
    } else {
      revealItems.forEach(function (item) { item.classList.add("visible"); });
    }

    // ============================================
    // STATS COUNTER ANIMATION
    // ============================================
    if (statNumbers.length) {
      var statTargets = [];

      statNumbers.forEach(function (stat) {
        var target = parseInt(stat.getAttribute("data-target"));
        if (!target) {
          var textContent = stat.textContent.replace(/[^0-9]/g, "");
          target = parseInt(textContent);
          if (isNaN(target) || target === 0) return;
          stat.setAttribute("data-target", target);
        }

        statTargets.push({
          element: stat,
          target: target,
          suffix: stat.textContent.replace(/[0-9]/g, ""),
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

      if ("IntersectionObserver" in window) {
        var statsObserver = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var index = statTargets.findIndex(function (item) {
                return item.element === entry.target;
              });
              if (index !== -1 && !statTargets[index].animated) {
                animateCounter(statTargets[index]);
              }
              statsObserver.unobserve(entry.target);
            }
          });
        }, { threshold: 0.5 });

        statNumbers.forEach(function (stat) {
          statsObserver.observe(stat);
        });
      } else {
        statTargets.forEach(function (data) {
          animateCounter(data);
        });
      }
    }

    // ============================================
    // FEATURE CARD HOVER EFFECTS
    // ============================================
    var featureCards = document.querySelectorAll(".feature-card");
    featureCards.forEach(function (card) {
      card.addEventListener("mouseenter", function () {
        var icon = this.querySelector(".feature-icon, .feature-icon-wrapper");
        if (icon) {
          icon.style.transition = "transform 0.3s ease";
          icon.style.transform = "scale(1.1) rotate(5deg)";
        }
      });
      card.addEventListener("mouseleave", function () {
        var icon = this.querySelector(".feature-icon, .feature-icon-wrapper");
        if (icon) {
          icon.style.transform = "scale(1) rotate(0deg)";
        }
      });
    });

    // ============================================
    // TESTIMONIAL CARD HOVER
    // ============================================
    var testimonialCards = document.querySelectorAll(".testimonial-card");
    testimonialCards.forEach(function (card) {
      card.addEventListener("mouseenter", function () {
        this.style.transition = "transform 0.3s ease, box-shadow 0.3s ease";
        this.style.transform = "translateY(-6px)";
      });
      card.addEventListener("mouseleave", function () {
        this.style.transform = "translateY(0)";
      });
    });

    // ============================================
    // HEADER SCROLL EFFECT
    // ============================================
    var header = document.querySelector(".main-header");
    if (header) {
      window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
          header.classList.add("scrolled");
        } else {
          header.classList.remove("scrolled");
        }
      }, { passive: true });
    }

    // ============================================
    // LOADING OVERLAY
    // ============================================
    if (loadingOverlay) {
      loadingOverlay.classList.add("active");
      window.setTimeout(function () {
        loadingOverlay.classList.remove("active");
        loadingOverlay.style.opacity = "0";
        setTimeout(function () {
          loadingOverlay.style.display = "none";
        }, 400);
      }, 350);
    }

    // ============================================
    // SWIPER CAROUSEL (if available)
    // ============================================
    if (typeof Swiper !== "undefined") {
      var swiperEl = document.querySelector(".banner-swiper, .swiper-container");
      if (swiperEl) {
        new Swiper(swiperEl, {
          loop: true,
          autoplay: {
            delay: 5000,
            disableOnInteraction: false
          },
          pagination: {
            el: ".swiper-pagination",
            clickable: true
          },
          navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev"
          },
          effect: "slide",
          speed: 600
        });
      }
    }

    // ============================================
    // LAZY LOAD IMAGES
    // ============================================
    if ("IntersectionObserver" in window) {
      var lazyImages = document.querySelectorAll(".hero-photo-frame img, .about-photo-wrap img, .testimonial-person img");
      var imageObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var img = entry.target;
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.removeAttribute("data-src");
            }
            img.classList.add("loaded");
            imageObserver.unobserve(img);
          }
        });
      }, { rootMargin: "50px" });

      lazyImages.forEach(function (img) {
        imageObserver.observe(img);
      });
    }

    // ============================================
    // PARALLAX EFFECT ON HERO
    // ============================================
    var heroOrbits = document.querySelectorAll(".hero-orbit");
    if (heroOrbits.length) {
      window.addEventListener("scroll", function () {
        var scrolled = window.pageYOffset;
        heroOrbits.forEach(function (orbit, index) {
          var speed = index === 0 ? 0.15 : 0.25;
          var translateY = scrolled * speed * 0.05;
          var translateX = scrolled * speed * 0.02;
          orbit.style.transform = "translate(" + translateX + "px, " + translateY + "px)";
        });
      }, { passive: true });
    }

    // ============================================
    // RESIZE HANDLER
    // ============================================
    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (!isMobile()) {
          closeMenu();
        } else {
          closeAllDropdowns();
        }
      }, 250);
    });

    console.log("EducDim initialized successfully");
  }

  // ============================================
  // INITIALIZATION
  // ============================================
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEducDim);
  } else {
    initEducDim();
  }

  // Re-initialize on dynamic navigation
  if (typeof Turbolinks !== "undefined") {
    document.addEventListener("turbolinks:load", function () {
      setTimeout(initEducDim, 100);
    });
  }

  if (typeof htmx !== "undefined") {
    document.addEventListener("htmx:afterSwap", function () {
      setTimeout(initEducDim, 100);
    });
  }

  // Expose for manual re-init
  window.EducDim = {
    init: initEducDim,
    version: "4.0.0"
  };
})();