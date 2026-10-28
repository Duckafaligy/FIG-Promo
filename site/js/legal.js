// The legal pages (user 2026-10-13/14): a band pinned at the top (the big title, the date, the documents) and only the
// document scrolls; nothing moves by a pixel. On a computer the contents column is pinned right under the band: its height
// is measured into --lg-band, so the column rests and sticks on the same line. Scrollspy marks the section you're reading.
// A click on a section lands its heading just under the band (smooth unless the visitor asked for less motion). Under
// 1024 px the contents are a menu in the band ("On this page"): Esc or a tap outside closes it.
(() => {
  const band = document.querySelector('.lg-band');
  if (!band) return;
  const root = document.documentElement;
  const btn = band.querySelector('.lg-toc-btn');
  const now = btn && btn.querySelector('.lg-toc-now');
  const menu = band.querySelector('.lg-menu');
  const col = document.querySelector('.lg-col');
  const links = [...document.querySelectorAll('.lg-rail a')];
  const ids = [...new Set(links.map((a) => a.hash.slice(1)))];
  const secs = ids.map((id) => document.getElementById(id)).filter(Boolean);

  // the band's height, for the column's pinned line (and again whenever it changes: fonts, a resize, tabs wrapping)
  const measure = () => root.style.setProperty('--lg-band', `${band.offsetHeight}px`);
  measure();
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(band);
  if (document.fonts) document.fonts.ready.then(measure);

  const offset = () => band.getBoundingClientRect().bottom + 16;
  const close = () => { band.classList.remove('open'); if (btn) btn.setAttribute('aria-expanded', 'false'); if (menu) menu.style.maxHeight = ''; };
  if (btn) btn.addEventListener('click', () => {
    const open = band.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    // the menu fits in what's left of the screen under the band
    if (open && menu) menu.style.maxHeight = `${Math.max(160, Math.min(520, window.innerHeight - band.getBoundingClientRect().bottom - 16))}px`;
    if (open && menu) ([...menu.querySelectorAll('a')].find((a) => a.classList.contains('on')) || menu.querySelector('a'))?.focus();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && band.classList.contains('open')) { close(); btn?.focus(); } });
  document.addEventListener('click', (e) => { if (band.classList.contains('open') && !band.contains(e.target)) close(); });

  links.forEach((a) => a.addEventListener('click', (e) => {
    const target = document.getElementById(a.hash.slice(1));
    if (!target) return;
    e.preventDefault();
    close();
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset(), behavior: 'smooth' });
    history.replaceState(null, '', a.hash);
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  }));

  let ticking = false;
  const mark = () => {
    ticking = false;
    const line = offset() + 8;
    let cur = secs[0];
    for (const s of secs) if (s.getBoundingClientRect().top <= line) cur = s;
    // at the very bottom, the last section counts even if its heading can't reach the line
    if (window.innerHeight + window.scrollY >= root.scrollHeight - 4) cur = secs[secs.length - 1];
    links.forEach((a) => {
      const on = !!cur && a.hash === '#' + cur.id;
      a.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      if (on && now) now.textContent = a.textContent;
      // keep the marked one in view inside a long column
      if (on && col && col.contains(a)) { const r = a.getBoundingClientRect(), box = col.getBoundingClientRect(); if (r.top < box.top || r.bottom > box.bottom) a.scrollIntoView({ block: 'nearest' }); }
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(mark); } }, { passive: true });
  addEventListener('resize', () => { close(); mark(); });
  mark();
})();
