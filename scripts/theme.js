// Theme switch: sets data-theme on <html>, persists it, and holds it if the host stamps its own value.
(function () {
  var KEY = 'hellocg-theme', VALID = ['a-orange', 'a-blue', 'b'], root = document.documentElement;
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(v) {
    if (VALID.indexOf(v) < 0) v = 'a-orange';
    root.setAttribute('data-theme', v);
    try { localStorage.setItem(KEY, v); } catch (e) {}
    var r = document.getElementById('theme-' + v); if (r) r.checked = true;
  }
  apply(stored() || 'a-orange');
  document.addEventListener('change', function (e) {
    if (e.target && e.target.name === 'theme') apply(e.target.value);
  });
  if (window.MutationObserver) {
    new MutationObserver(function () {
      var v = root.getAttribute('data-theme');
      if (VALID.indexOf(v) < 0) apply(stored() || 'a-orange');
    }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  }
})();
