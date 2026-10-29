# MagicNet UI · S-UI 1.6.6

A GPL-3.0 fork of [alireza0/s-ui](https://github.com/alireza0/s-ui), with a
[separate Vue frontend fork](https://github.com/bunajianke/s-ui-frontend/tree/magicnet/mobile).
Existing users, credentials, quotas, inbound listeners and subscription endpoints
remain managed by S-UI. This customization does not replace the proxy core.

## What changed

- Home: real service state, account traffic, resource usage and a shortcut to add users.
- Clients: mobile cards, search, accessible enable switches and edit/subscription actions.
- Mobile: two-tab navigation, full-screen client and subscription dialogs, safe-area
  spacing, sticky action footers, wrapped long identifiers and 44px touch targets.
- Subscription QR: explicit Shadowrocket, Clash/Mihomo and Surge formats when the
  existing MagicNet subscription adapter is configured. Generic installations retain
  the upstream subscription formats.
- Advanced monitoring and desktop client tables remain available.
- Simultaneous equivalent reads share one pending result instead of cancelling
  each other. Mutating requests remain independent, and explicit cancellation
  does not create a misleading failure toast. Network/authentication failures
  are still reported normally.

Account traffic is S-UI's existing upload + download counters, with each account's
own reset cycle. It is **not** the provider's billable monthly usage.

## Build and deploy

Use the frontend commit pinned by this repository, rather than an arbitrary `main`.
The deployed backend is the official release binary, not a rebuilt Go binary.

```sh
git submodule update --init --recursive
cd frontend
npm ci
npm run lint
npm run test
npm run build
```

Copy `frontend/dist` and the scripts in this directory to the server. As root:

```sh
python3 install-ui.py --dist /root/frontend-dist --release FRONTEND_COMMIT
```

Defaults match an existing S-UI deployment behind Nginx: SQLite in
`/var/lib/s-ui/s-ui.db`, Nginx site `/etc/nginx/sites-available/default`.
The installer reads the private `webPath` and web port from SQLite, replaces only
that path's existing Nginx proxy location, and keeps API requests on S-UI.
It verifies the Nginx configuration before reloading and restores the previous
files on failure. It does not edit SQLite, systemd, accounts or subscriptions.

Static UI files live under `/opt/magicnet-sui/ui/releases/`, with an atomic `current`
symlink. The generated Nginx include lives in `/etc/cloudcone-panel/`. Authentication
for application HTML is delegated to the existing S-UI session; API authentication
and same-origin checks remain enforced by S-UI. Only login HTML and static assets
are public. The runtime base path is substituted on the server and never committed.

After deployment verify unauthenticated redirects, authenticated deep routes, login,
all client CRUD fields, subscription formats, proxy TCP/UDP and any local integrations.
Keep the previous backend binary and a consistent SQLite backup before an upgrade.
Do not run the upstream installer over a customized service unit.

## Roll back the UI

Use the snapshot path printed by the installer:

```sh
python3 rollback-ui.py /opt/magicnet-sui/ui/backups/SNAPSHOT
```

This restores Nginx and the previous UI symlink without restarting S-UI. Backend
rollback is separate: restore the previous binary and restart the existing unit.
Never restore an old database casually: it discards accounts and traffic recorded
since that backup. Check schema compatibility first.

## Future S-UI releases

Replacing the official S-UI binary does not overwrite this UI directory. Replacing
the Nginx site or running another installer can remove the routing include, however.
Back up the site, include, active UI release and symlink together.

For a new upstream release, branch from this fork, merge the upstream backend tag,
merge the corresponding pinned upstream frontend into `magicnet/mobile`, resolve
conflicts and pin the resulting frontend commit in this repository. Build and test
against a database clone on loopback-only ports before deploying. Binary updates
are not automatic; changed upstream APIs may require frontend changes even though
the UI files survive. Keep GPL-3.0 notices and source available when redistributing.

Runtime databases, passwords, subscription tokens, certificates and backup archives
must stay outside these public source repositories.
