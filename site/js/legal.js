// The legal pages (user 2026-10-13: the title, the document tabs and "On this page" stay put, only the text scrolls).
// Scrollspy: the section you're reading is marked in the list. A click on a section scrolls to its heading clear of the
// navbar and the sticky bar (smoothly, unless the visitor asked for less motion). Under 1024 px the list is a menu
// ("On this page") that opens under the bar: Esc or a tap outside closes it.
(() => {
  const side = document.querySelector('.lg-side');
  if (!side) return;
  const btn = side.querySelector('.lg-toc-btn');
  const now = btn && btn.querySelector('.lg-toc-now');
  const links = [...side.querySelectorAll('.lg-rail a')];
  const secs = links.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
  const wide = () => innerWidth >= 1024;
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  // where a heading should land: under the navbar (desktop) or under the sticky bar (phone and tablet)
  const offset = () => (wide() ? 112 : Math.max(96, side.getBoundingClientRect().bottom + 12));

  const close = () => { side.classList.remove('open'); if (btn) btn.setAttribute('aria-expanded', 'false'); const r = side.querySelector('.lg-rail'); if (r) r.style.maxHeight = ''; };
  if (btn) btn.addEventListener('click', () => {
    const open = side.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    // the menu fits in what's left of the screen under the bar
    const rail = side.querySelector('.lg-rail');
    if (open && rail) rail.style.maxHeight = `${Math.max(160, Math.min(520, window.innerHeight - side.getBoundingClientRect().bottom - 16))}px`;
    if (open) (links.find((a) => a.classList.contains('on')) || links[0])?.focus();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && side.classList.contains('open')) { close(); btn?.focus(); } });
  document.addEventListener('click', (e) => { if (side.classList.contains('open') && !side.contains(e.target)) close(); });

  links.forEach((a) => a.addEventListener('click', (e) => {
    const target = document.getElementById(a.hash.slice(1));
    if (!target) return;
    e.preventDefault();
    close();
    window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset(), behavior: reduce() ? 'auto' : 'smooth' });
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
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) cur = secs[secs.length - 1];
    links.forEach((a) => {
      const on = !!cur && a.hash === '#' + cur.id;
      a.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      if (on && now) now.textContent = a.textContent;
      // keep the marked one in view inside a long list
      if (on && wide()) { const r = a.getBoundingClientRect(), box = side.getBoundingClientRect(); if (r.top < box.top || r.bottom > box.bottom) a.scrollIntoView({ block: 'nearest' }); }
    });
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(mark); } }, { passive: true });
  addEventListener('resize', () => { close(); mark(); });
  mark();
})();
