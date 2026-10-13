// The flow changes for the web app (from fig-promo-e9), each with Yes / No. Ticks are kept in this browser only.
const FLOW = [
  ["Claim in a side panel", "On a computer, claiming a deal opens a panel next to the restaurant, not a full-screen sheet."],
  ["Filters beside the results", "Filters sit in a sidebar or as chips next to the list, not in a pop-up."],
  ["Map and list side by side", "Hover a restaurant in the list and its pin lights up on the map."],
  ["One restaurant page", "Deals, menu and info on one page (A) or in tabs (B), not separate screens."],
  ["Saved and Chats in a drawer", "They slide in from the side, so you never lose the page you were on."],
  ["Top bar or sidebar on computers", "Replaces the phone's bottom tabs. Phones in the browser keep the bottom bar."],
  ["Takeout cart stays visible", "On a computer the cart sits beside the menu while you browse."],
  ["Keyboard shortcuts", "\"/\" jumps to search, Esc closes panels, arrow keys move through the list."],
];
(() => {
  const list = document.getElementById("flow-list"), box = document.getElementById("flow");
  if (!list || !FLOW.length) return;
  let saved = {}; try { saved = JSON.parse(localStorage.getItem("fig-preview-flow") || "{}"); } catch (e) {}
  list.innerHTML = FLOW.map(([title, why], i) => `<li><div><b>${title}</b><span>${why}</span></div><div class="yn" data-i="${i}"><button data-a="yes">Yes</button><button data-a="no">No</button></div></li>`).join("");
  list.querySelectorAll(".yn").forEach((g) => {
    const mark = () => g.querySelectorAll("button").forEach((b) => b.classList.toggle("on", saved[g.dataset.i] === b.dataset.a));
    mark();
    g.addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; saved[g.dataset.i] = b.dataset.a; try { localStorage.setItem("fig-preview-flow", JSON.stringify(saved)); } catch (er) {} mark(); });
  });
  box.hidden = false;
})();
