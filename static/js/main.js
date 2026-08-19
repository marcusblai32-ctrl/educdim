/* EducDim vanilla JavaScript
 * Works with the existing IDs/classes from base.html and home.html.
 */
(function () {
  "use strict";

  function initEducDim() {
    var menuToggle = document.getElementById("menuToggle");
    var mainNav = document.getElementById("mainNav");
    var userDropdownBtn = document.getElementById("userDropdownBtn");
    var chatDropdownBtn = document.getElementById("chatDropdownBtn");
    var loadingOverlay = document.getElementById("loadingOverlay");

    if (menuToggle && mainNav) {
      menuToggle.addEventListener("click", function () {
        var open = mainNav.classList.toggle("active");
        menuToggle.setAttribute("aria-expanded", String(open));
        menuToggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      });
    }

    function toggleDropdown(button, selector, otherSelector) {
      if (!button) return;
      button.addEventListener("click", function (event) {
        event.stopPropagation();
        var parent = button.closest(selector);
        if (!parent) return;
        document.querySelectorAll(otherSelector).forEach(function (item) {
          if (item !== parent) item.classList.remove("open");
        });
        var open = parent.classList.toggle("open");
        button.setAttribute("aria-expanded", String(open));
      });
    }

    toggleDropdown(userDropdownBtn, ".user-dropdown", ".user-dropdown, .nav-dropdown");
    toggleDropdown(chatDropdownBtn, ".nav-dropdown", ".user-dropdown, .nav-dropdown");

    document.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof Element)) return;
      if (!target.closest(".user-dropdown")) {
        document.querySelectorAll(".user-dropdown").forEach(function (item) { item.classList.remove("open"); });
      }
      if (!target.closest(".nav-dropdown")) {
        document.querySelectorAll(".nav-dropdown").forEach(function (item) { item.classList.remove("open"); });
      }
    });

    document.querySelectorAll(".close-alert").forEach(function (button) {
      button.addEventListener("click", function () {
        var alert = button.closest(".alert");
        if (alert) alert.remove();
      });
    });

    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function (event) {
        var href = link.getAttribute("href");
        if (!href || href === "#") return;
        var target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        if (mainNav) mainNav.classList.remove("active");
        if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
      });
    });

    var revealItems = document.querySelectorAll(".reveal, .animate-on-scroll");
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      revealItems.forEach(function (item) { observer.observe(item); });
    } else {
      revealItems.forEach(function (item) { item.classList.add("visible"); });
    }

    if (loadingOverlay) {
      window.setTimeout(function () { loadingOverlay.classList.remove("active"); }, 350);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEducDim);
  } else {
    initEducDim();
  }
})();
