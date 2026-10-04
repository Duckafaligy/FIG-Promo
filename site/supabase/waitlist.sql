-- FIG website waitlist. Run once in the Supabase SQL editor (or `supabase db query`) of the FIG project.
-- The site can only ADD rows: nobody can read the list through the public key, only the total count.
create table if not exists public.waitlist (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  role        text not null check (role in ('diner', 'restaurant')),
  email       text check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' and length(email) <= 254),
  phone       text check (phone ~ '^\+1[2-9][0-9]{9}$'),
  restaurant  text check (length(restaurant) <= 120),
  area        text check (length(area) <= 60),
  consent     boolean not null check (consent),   -- CASL: express consent to email/text
  source      text check (length(source) <= 60),  -- ?src=ig, owners, site
  check (email is not null or phone is not null)
);
create unique index if not exists waitlist_email on public.waitlist (lower(email)) where email is not null;
create unique index if not exists waitlist_phone on public.waitlist (phone) where phone is not null;

alter table public.waitlist enable row level security;
drop policy if exists "anyone can join" on public.waitlist;
create policy "anyone can join" on public.waitlist for insert to anon, authenticated with check (true);
revoke all on public.waitlist from anon, authenticated;
grant insert on public.waitlist to anon, authenticated;

create or replace function public.waitlist_count() returns integer
  language sql stable security definer set search_path = public
  as $$ select count(*)::int from public.waitlist where role = 'diner' $$;
revoke all on function public.waitlist_count() from public;
grant execute on function public.waitlist_count() to anon, authenticated;
