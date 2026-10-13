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
  let start = "desk"; try { start = sessionStorage.getItem("pv-view") || "desk"; } catch (e) {}
  set(start);
})();
