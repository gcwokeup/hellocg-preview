// Mobile menu, the Services drop-down, and the contact form's demonstrable states.
(function () {
  var toggle = document.querySelector('.menu-toggle'), nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
  var sub = document.querySelector('.sub-toggle'), list = document.getElementById('sub-services');
  if (sub && list) {
    sub.addEventListener('click', function () {
      var open = list.classList.toggle('is-open');
      sub.setAttribute('aria-expanded', String(open));
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (list) { list.classList.remove('is-open'); if (sub) sub.setAttribute('aria-expanded', 'false'); }
      if (nav) { nav.classList.remove('is-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
    }
  });
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = document.getElementById('f-email'), err = document.getElementById('f-email-error'), field = email.closest('.field');
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      if (!ok) { field.classList.add('has-error'); err.hidden = false; email.setAttribute('aria-invalid', 'true'); email.focus(); return; }
      field.classList.remove('has-error'); err.hidden = true; email.removeAttribute('aria-invalid');
      // A real handler goes here.
      form.hidden = true;
      var s = document.getElementById('contact-success'); s.hidden = false; s.setAttribute('tabindex', '-1'); s.focus();
    });
  }
})();
