// Restaurant balance on the website (/business): an owner or manager signs in with their FIG business account, sees the
// balance, tops it up through Stripe Checkout (the same business-billing function the app uses) and sets automatic top-up.
// The FIG app shows the new balance within seconds. Everything is checked by the database with the person's own sign-in;
// the key below is Supabase's public key (safe in a web page).
(function () {
  "use strict";
  const URL_ = "https://frpoykqldlsysitiqnhz.supabase.co";
  const KEY = "sb_publishable_3YFOf3yQj010ppmatdj5-w_-H45r2se";
  const PRICE = 1.5, MIN = 10, MAX = 500;
  const $ = (s) => document.querySelector(s);
  const money = (n) => (n < 0 ? "−" : "") + "$" + Math.abs(n).toFixed(2);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many || one + "s");
  const day = (iso) => new Date(iso).toLocaleDateString("en-CA", { month: "short", day: "numeric", year: "numeric" });
  const when = (iso) => new Date(iso).toLocaleString("en-CA", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  const db = window.supabase.createClient(URL_, KEY, { auth: { persistSession: true, detectSessionInUrl: true } });
  let me = null; // { owner, business, isOwner, billing, restIds }
  let pick = 50;

  const show = (id) => ["#bal-out", "#bal-in", "#bal-none"].forEach((s) => ($(s).hidden = s !== id));
  const say = (el, text, bad) => { el.textContent = text; el.className = "form-msg" + (bad ? " err" : " ok"); el.hidden = !text; };

  async function load() {
    const { data: { session } } = await db.auth.getSession();
    if (!session) return show("#bal-out");
    const [b] = (await db.rpc("my_billing")).data ?? [];
    if (!b) { show("#bal-none"); return; }
    const billing = (await db.from("billing_accounts").select("*").eq("owner_id", b.owner_id).single()).data;
    const rests = (await db.from("restaurants").select("id,name").eq("owner_id", b.owner_id)).data ?? [];
    me = { owner: b.owner_id, business: b.business, isOwner: b.is_owner, billing, restIds: rests.map((r) => r.id), names: rests.map((r) => r.name) };
    show("#bal-in");
    render();
    activity();
  }

  function render() {
    const b = me.billing;
    const bal = Number(b.balance);
    const free = b.comped || (b.free_until && Date.parse(b.free_until) > Date.now());
    const open = free || b.free_scans > 0 || bal >= PRICE;
    $("#b-name").textContent = me.names.join(" · ") || me.business;
    $("#b-amount").textContent = money(bal);
    const [pill, cls, line] = b.comped ? ["Free", "volt", "Scans are free for the FIG team"]
      : free ? ["Founding", "volt", "Scans are free until " + day(b.free_until)]
      : b.free_scans > 0 ? ["Free scans", "volt", plural(b.free_scans, "free scan") + " left, then $1.50 each"]
      : !open ? ["Paused", "red", "Top up so diners can claim your deals again"]
      : bal < 10 ? ["Low", "amber", "About " + plural(Math.floor(bal / PRICE), "scan") + " left"]
      : ["Active", "volt", "About " + plural(Math.floor(bal / PRICE), "scan") + " left"];
    $("#b-pill").textContent = pill;
    $("#b-pill").className = "bal-pill " + cls;
    $("#b-line").textContent = line;
    $("#b-card").textContent = b.card ? b.card.brand.toUpperCase() + " •• " + b.card.last4 : "";
    $("#b-paused").hidden = open;
    const a = b.auto || { on: false, below: 5, amount: 20, monthlyLimit: 200 };
    $("#a-on").checked = !!a.on;
    $("#a-below").value = String(a.below);
    $("#a-amount").value = String(a.amount);
    $("#a-limit").value = String(a.monthlyLimit);
    $("#a-fields").hidden = !a.on;
    $("#a-card").textContent = b.card ? "Charged to " + b.card.brand.toUpperCase() + " •• " + b.card.last4 + ". You get a notice in FIG each time." : "Top up once first: Stripe keeps the card for automatic top-ups.";
    amount();
  }

  async function activity() {
    const ledger = (await db.from("ledger").select("id,kind,amount,at").order("at", { ascending: false }).limit(20)).data ?? [];
    const scans = me.restIds.length ? (await db.from("redemptions").select("id,title,fee,at").in("restaurant_id", me.restIds).gt("fee", 0).order("at", { ascending: false }).limit(20)).data ?? [] : [];
    const rows = [
      ...ledger.map((x) => ({ at: x.at, title: x.kind === "auto" ? "Automatic top-up" : x.kind === "refund" ? "Refund" : "Top-up", amount: Number(x.amount) })),
      ...scans.map((x) => ({ at: x.at, title: "Scan · " + x.title, amount: -Number(x.fee) })),
    ].sort((p, q) => Date.parse(q.at) - Date.parse(p.at)).slice(0, 15);
    $("#b-activity").innerHTML = rows.length
      ? rows.map((r) => `<li><span><b>${esc(r.title)}</b><small>${esc(when(r.at))}</small></span><em class="${r.amount > 0 ? "plus" : ""}">${r.amount > 0 ? "+" : ""}${money(r.amount)}</em></li>`).join("")
      : '<li class="empty">Nothing yet. Top-ups and paid scans show up here.</li>';
  }

  // the amount picked: $20 / $50 / $100, or any amount
  function amount() {
    const custom = pick === "custom";
    $("#t-custom").hidden = !custom;
    const n = custom ? Number(String($("#t-custom input").value).replace(/[^0-9.]/g, "")) : pick;
    const ok = Number.isFinite(n) && n >= MIN && n <= MAX;
    $("#t-go").disabled = !ok;
    $("#t-go").textContent = ok ? "Top up " + money(n) : "Top up";
    $("#t-scans").textContent = ok ? "About " + plural(Math.floor(n / PRICE), "scan") : `Between $${MIN} and $${MAX}`;
    document.querySelectorAll("[data-amt]").forEach((b) => b.classList.toggle("on", String(pick) === b.dataset.amt));
    return ok ? n : 0;
  }

  async function topUp() {
    const n = amount();
    if (!n) return;
    const btn = $("#t-go");
    btn.disabled = true; btn.textContent = "Opening Stripe…";
    try { sessionStorage.setItem("fig-bal-before", String(me.billing.balance)); } catch (e) { /* private mode */ }
    const back = location.origin + "/business";
    const { data, error } = await db.functions.invoke("business-billing", { body: { action: "topup", amount: n, returnUrl: back } });
    if (error || !data?.url) {
      say($("#t-msg"), data?.error === "not-allowed" ? "Only the owner or a manager can top up." : "Couldn’t open Stripe. Try again in a moment.", true);
      amount();
      return;
    }
    location.assign(data.url);
  }

  async function saveAuto() {
    if ($("#a-on").checked && !me.billing.card) {
      $("#a-on").checked = false;
      return say($("#a-msg"), "Top up once first, so Stripe keeps your card for automatic top-ups.", true);
    }
    const auto = { on: $("#a-on").checked, below: Number($("#a-below").value), amount: Number($("#a-amount").value), monthlyLimit: Number($("#a-limit").value) };
    if (auto.monthlyLimit < auto.amount) auto.monthlyLimit = auto.amount * 2;
    const { error } = await db.from("billing_accounts").update({ auto }).eq("owner_id", me.owner);
    if (error) return say($("#a-msg"), "Couldn’t save. Try again.", true);
    me.billing.auto = auto;
    render();
    say($("#a-msg"), auto.on ? "Saved. FIG tops you up when you run low." : "Automatic top-up is off.");
  }

  // back from Stripe: wait for the payment to land (stripe-webhook adds it within seconds)
  async function returning() {
    if (!new URLSearchParams(location.search).has("topup")) return;
    history.replaceState(null, "", "/business");
    let before = NaN;
    try { before = Number(sessionStorage.getItem("fig-bal-before")); } catch (e) { /* private mode */ }
    const note = $("#b-note");
    note.hidden = false;
    note.className = "bal-note wait";
    note.textContent = "Confirming your payment with Stripe…";
    for (let i = 0; i < 30; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      if (!me) continue;
      me.billing = (await db.from("billing_accounts").select("*").eq("owner_id", me.owner).single()).data;
      if (!Number.isFinite(before) || Number(me.billing.balance) > before) {
        render(); activity();
        note.className = "bal-note done";
        note.textContent = "Topped up. Your balance is " + money(Number(me.billing.balance)) + ", and the FIG app shows it too.";
        return;
      }
    }
    note.textContent = "Still waiting on Stripe. Refresh in a minute, or check your email receipt.";
  }

  async function signIn(e) {
    e.preventDefault();
    const msg = $("#s-msg");
    say(msg, "");
    const { error } = await db.auth.signInWithPassword({ email: $("#s-email").value.trim().toLowerCase(), password: $("#s-pass").value });
    if (error) return say(msg, /invalid/i.test(error.message) ? "That email and password don’t match a FIG account." : "Couldn’t sign in. Try again.", true);
    await load();
  }

  document.addEventListener("DOMContentLoaded", async () => {
    $("#s-form").addEventListener("submit", signIn);
    $("#s-google").addEventListener("click", () => db.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/business" } }));
    document.querySelectorAll("[data-out]").forEach((b) => b.addEventListener("click", async () => { await db.auth.signOut(); me = null; show("#bal-out"); }));
    document.querySelectorAll("[data-amt]").forEach((b) => b.addEventListener("click", () => { pick = b.dataset.amt === "custom" ? "custom" : Number(b.dataset.amt); amount(); if (pick === "custom") $("#t-custom input").focus(); }));
    $("#t-custom input").addEventListener("input", amount);
    $("#t-go").addEventListener("click", topUp);
    $("#a-on").addEventListener("change", () => { $("#a-fields").hidden = !$("#a-on").checked; saveAuto(); });
    ["#a-below", "#a-amount", "#a-limit"].forEach((s) => $(s).addEventListener("change", saveAuto));
    await load();
    returning();
  });
})();
