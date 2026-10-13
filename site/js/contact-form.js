// The contact page's form: goes to FIG's support inbox (contact_fig), the same one as Message us in the app.
(() => {
  const form = document.querySelector("form.contact");
  if (!form) return;
  const cfg = window.FIG_CONFIG || {}, msg = form.querySelector(".form-msg"), btn = form.querySelector("button");
  const say = (t, kind) => { msg.textContent = t; msg.className = "form-msg " + (kind || ""); };
  const bad = (el, t) => { el.setAttribute("aria-invalid", "true"); el.focus(); say(t, "err"); };
  form.addEventListener("input", (e) => e.target.removeAttribute("aria-invalid"));
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    if (form.elements.website.value) return; // bots fill the hidden field
    const { email, topic, body } = form.elements;
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value.trim())) return bad(email, "Enter your email, so we can reply.");
    if (body.value.trim().length < 5) return bad(body, "Write a few words about what you need.");
    if (!cfg.supabaseUrl || !cfg.supabaseKey) return say("Messages open in the next few days. Check back soon!", "err");
    btn.disabled = true; say(""); btn.textContent = "Sending…";
    try {
      const r = await fetch(`${cfg.supabaseUrl}/rest/v1/rpc/contact_fig`, { method: "POST",
        headers: { apikey: cfg.supabaseKey, "Content-Type": "application/json" },
        body: JSON.stringify({ p_topic: topic.value, p_body: body.value.trim(), p_email: email.value.trim() }) });
      if (!r.ok) throw new Error((await r.text()).includes("slow-down") ? "slow" : r.status);
      // the card turns into a "sent" note (pages.css .ct-done), with a way to write another
      const done = document.createElement("div");
      done.className = "ct-done"; done.setAttribute("role", "status");
      done.innerHTML = '<span class="ct-done-tick" aria-hidden="true"></span><b>Message sent</b><p></p><button class="btn btn-soft" type="button">Send another</button>';
      done.querySelector("p").textContent = "We'll reply to " + email.value.trim() + ", usually within 24 hours.";
      done.querySelector("button").addEventListener("click", () => { body.value = ""; form.classList.remove("sent"); done.remove(); btn.disabled = false; btn.textContent = "Send message"; body.focus(); });
      form.append(done); form.classList.add("sent");
    } catch (e) {
      btn.disabled = false; btn.textContent = "Send message";
      say(e.message === "slow" ? "That's a lot of messages at once. Try again in an hour." : "Something went wrong. Try again in a moment.", "err");
    }
  });
})();
