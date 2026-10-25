// The Supabase project, as the app uses it. Both values are public by design (the publishable key: what it can do is
// limited by the database's own rules). The contact form and Home's diner waitlist use it.
window.FIG_CONFIG = {
  supabaseUrl: "https://frpoykqldlsysitiqnhz.supabase.co",
  supabaseKey: "sb_publishable_3YFOf3yQj010ppmatdj5-w_-H45r2se",
  // The business address on the contact page and the Help page (hello@figpromo.ca). Hidden until it has been tested end to end:
  // set this to true (and nothing else) to show it. Emails FIG sends always carry the address in their footer; this is only the website.
  showEmail: false,
};
