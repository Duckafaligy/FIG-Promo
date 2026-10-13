// /preview/: the "Preview" ribbon and a Desktop / Phone (390) toggle on every mock page. Nothing is sent anywhere.
(() => {
  const inFrame = new URLSearchParams(location.search).has("frame");
  if (inFrame) { document.documentElement.classList.add("pv-in-frame"); return; }
  const bar = document.createElement("div");
  bar.className = "pv-bar";
  bar.innerHTML = '<a href="/preview/" class="pv-home">← All directions</a><span class="pv-tag">Preview · not live</span>' +
    '<span class="pv-seg"><button data-v="desk">Desktop</button><button data-v="phone">Phone 390</button></span>';
  document.body.appendChild(bar);
  const set = (v) => {
    document.querySelectorAll(".pv-seg button").forEach((b) => b.classList.toggle("on", b.dataset.v === v));
    let f = document.getElementById("pv-phone");
    if (v === "phone") {
      if (!f) { f = document.createElement("div"); f.id = "pv-phone"; f.innerHTML = `<iframe title="Phone view" src="${location.pathname}?frame=1"></iframe>`; document.body.appendChild(f); }
      document.documentElement.classList.add("pv-phone-on");
    } else document.documentElement.classList.remove("pv-phone-on");
    try { sessionStorage.setItem("pv-view", v); } catch (e) {}
  };
  bar.addEventListener("click", (e) => { const b = e.target.closest("button[data-v]"); if (b) set(b.dataset.v); });
  // Direction C: flip the top navbar into a sidebar (the user said "maybe" on the navbar)
  if (document.body.dataset.flip) {
    const seg = document.createElement("span"); seg.className = "pv-seg pv-nav";
    seg.innerHTML = '<button data-n="top">Navbar</button><button data-n="side">Sidebar</button>';
    bar.insertBefore(seg, bar.querySelector(".pv-seg"));
    const nav = (n) => { document.documentElement.classList.toggle("side-nav", n === "side"); seg.querySelectorAll("button").forEach((b) => b.classList.toggle("on", b.dataset.n === n)); try { sessionStorage.setItem("pv-nav", n); } catch (e) {} const f = document.querySelector("#pv-phone iframe"); if (f) f.src = f.src; };
    seg.addEventListener("click", (e) => { const b = e.target.closest("button[data-n]"); if (b) nav(b.dataset.n); });
    let n = "top"; try { n = sessionStorage.getItem("pv-nav") || "top"; } catch (e) {}
    nav(n);
  }
  let start = "desk"; try { start = sessionStorage.getItem("pv-view") || "desk"; } catch (e) {}
  set(start);
})();
