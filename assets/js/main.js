/* ==========================================================================
   The National Days of Prayer Movement in Europe — site behaviour
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Current year ---------- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- Active navigation item ---------- */
  var page = document.body.getAttribute('data-page');
  if (page) {
    var current = document.querySelector('.nav a[data-nav="' + page + '"]');
    if (current) current.setAttribute('aria-current', 'page');
  }

  /* ---------- Light / dark theme ----------
     The inline script in <head> has already applied the stored choice, so all
     that is left here is the switch itself. Light is the default. */
  var themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    var meta = document.getElementById('themeColor');
    var GROUND = { light: '#0C335B', dark: '#0D1822' };

    var render = function (theme) {
      document.documentElement.setAttribute('data-theme', theme);
      themeToggle.setAttribute('aria-pressed', String(theme === 'dark'));
      themeToggle.setAttribute('aria-label',
        theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      if (meta) meta.setAttribute('content', GROUND[theme]);
    };

    render(document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

    themeToggle.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      render(next);
      try { localStorage.setItem('ndop.theme', next); } catch (e) { /* private mode */ }
    });
  }

  /* ---------- Mobile navigation ---------- */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('primaryNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---------- Sticky header shadow ---------- */
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Reveal on scroll ---------- */
  var revealables = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq__q').forEach(function (btn) {
    var item = btn.closest('.faq__item');
    var panel = item.querySelector('.faq__a');
    btn.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');

      // Close siblings for a single-open accordion.
      item.parentElement.querySelectorAll('.faq__item.is-open').forEach(function (other) {
        if (other === item) return;
        other.classList.remove('is-open');
        other.querySelector('.faq__q').setAttribute('aria-expanded', 'false');
        other.querySelector('.faq__a').style.height = '0px';
      });

      if (isOpen) {
        panel.style.height = panel.scrollHeight + 'px';
        requestAnimationFrame(function () { panel.style.height = '0px'; });
        item.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
        panel.style.height = panel.scrollHeight + 'px';
        panel.addEventListener('transitionend', function once() {
          if (item.classList.contains('is-open')) panel.style.height = 'auto';
          panel.removeEventListener('transitionend', once);
        });
      }
    });
  });

  /* ---------- Lightbox ---------- */
  var lightbox = document.getElementById('lightbox');
  if (lightbox) {
    var lbImg = document.getElementById('lightboxImg');
    var lbCap = document.getElementById('lightboxCap');
    var lastFocused = null;

    var open = function (src, alt, caption) {
      lastFocused = document.activeElement;
      lbImg.src = src;
      lbImg.alt = alt || '';
      lbImg.hidden = false;
      lbCap.textContent = caption || '';
      lightbox.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      document.getElementById('lightboxClose').focus();
    };
    var close = function () {
      lightbox.classList.remove('is-open');
      document.body.style.overflow = '';
      if (lastFocused) lastFocused.focus();
    };

    document.querySelectorAll('[data-lightbox]').forEach(function (el) {
      var img = el.tagName === 'IMG' ? el : el.querySelector('img');
      if (!img) return;
      el.style.cursor = 'zoom-in';
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      el.setAttribute('aria-label', 'Enlarge image');
      var fire = function () { open(img.src, img.alt, el.getAttribute('data-caption') || img.alt); };
      el.addEventListener('click', fire);
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fire(); }
      });
    });

    document.getElementById('lightboxClose').addEventListener('click', close);
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target.tagName === 'FIGURE') close();
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lightbox.classList.contains('is-open')) close();
    });
  }

  /* ---------- Contact form (no backend — opens the visitor's mail client) ---------- */
  var form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.getElementById('formStatus');

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var data = new FormData(form);
      var body = [
        'Name: ' + (data.get('name') || ''),
        'Email: ' + (data.get('email') || ''),
        'Country: ' + (data.get('country') || ''),
        'Writing as: ' + (data.get('role') || ''),
        '',
        data.get('message') || ''
      ].join('\n');

      var href = 'mailto:info@ndop-europe.org'
        + '?subject=' + encodeURIComponent('National Days of Prayer Movement — enquiry from ' + (data.get('name') || 'the website'))
        + '&body=' + encodeURIComponent(body);

      window.location.href = href;
      status.textContent = 'Opening your email client… If nothing happens, write directly to info@ndop-europe.org.';
      status.classList.add('is-visible');
    });
  }
})();
