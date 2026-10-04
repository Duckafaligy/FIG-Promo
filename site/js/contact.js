// One field takes an email or a Canadian mobile number. Returns {email} or {phone: "+1XXXXXXXXXX"}, or null.
function parseContact(value) {
  const v = String(value || "").trim();
  if (v.includes("@")) return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) && v.length <= 254 ? { email: v.toLowerCase() } : null;
  const d = v.replace(/\D/g, "");
  if (d.length === 10 && /^[2-9]/.test(d)) return { phone: "+1" + d };
  if (d.length === 11 && /^1[2-9]/.test(d)) return { phone: "+" + d };
  return null;
}
if (typeof module !== "undefined") module.exports = { parseContact };
