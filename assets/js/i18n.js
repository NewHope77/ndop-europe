/* ==========================================================================
   Lightweight i18n layer.

   The site ships in English and English lives in the markup, so the pages are
   fully readable and indexable with JavaScript disabled. Every translatable
   node carries a `data-i18n="key"` attribute; `assets/i18n/en.json` is the
   reference dictionary of those keys.

   To add a language: drop `assets/i18n/<code>.json` next to en.json, add the
   code to SUPPORTED below, and expose a language switcher that calls
   `NDOP.i18n.setLocale('<code>')`. Missing keys fall back to the English
   already present in the HTML.
   ========================================================================== */
window.NDOP = window.NDOP || {};
window.NDOP.i18n = (function () {
  'use strict';

  var DEFAULT = 'en';
  var SUPPORTED = ['en'];          // add locale codes here as translations land
  var STORAGE_KEY = 'ndop.locale';

  function apply(dict) {
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var value = dict[el.getAttribute('data-i18n')];
      if (typeof value === 'string') el.innerHTML = value;
    });
    document.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
      // format: data-i18n-attr="placeholder:search.placeholder, title:nav.home"
      el.getAttribute('data-i18n-attr').split(',').forEach(function (pair) {
        var parts = pair.split(':');
        var attr = (parts[0] || '').trim();
        var value = dict[(parts[1] || '').trim()];
        if (attr && typeof value === 'string') el.setAttribute(attr, value);
      });
    });
  }

  function setLocale(code) {
    if (SUPPORTED.indexOf(code) === -1) code = DEFAULT;
    document.documentElement.lang = code;
    try { localStorage.setItem(STORAGE_KEY, code); } catch (e) { /* private mode */ }

    if (code === DEFAULT) return Promise.resolve();   // English is already in the DOM

    return fetch('assets/i18n/' + code + '.json')
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(apply)
      .catch(function () { /* keep the English fallback */ });
  }

  function current() {
    var stored;
    try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) { stored = null; }
    return SUPPORTED.indexOf(stored) !== -1 ? stored : DEFAULT;
  }

  setLocale(current());

  return { setLocale: setLocale, current: current, supported: SUPPORTED.slice() };
})();
