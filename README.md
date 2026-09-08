# nginx-tools (nxtool)

A small CLI wrapper around common nginx site-management tasks - enable/disable a
site, validate the config, reload - packaged as a `.deb` and built via GitLab CI.

## Why

Debian ships `a2ensite` / `a2dissite` for Apache, but nginx has no built-in
equivalent - enabling a site usually means manually symlinking into
`sites-enabled` and hoping the config is valid. `nxtool` fills that gap and adds
a safety net Apache's tools don't have either: it runs `nginx -t` before every
reload and automatically rolls back the change if the config is broken, instead
of leaving nginx in a bad state.

## Features

- `nxtool ensite <config>` - symlinks a config from `sites-available` into
  `sites-enabled`, validates it, and reloads nginx. If validation fails, the
  symlink is removed again automatically.
- `nxtool dissite <config>` - removes a config from `sites-enabled`, validates,
  reloads. If validation fails, the site is left enabled and nginx is not
  reloaded.
- `nxtool reload` - `systemctl reload nginx`.
- Bash tab-completion (via `argcomplete`) - suggests available sites for
  `ensite` and currently enabled sites for `dissite`.
- Packaged as a `.deb`, built and versioned automatically per pipeline run.

## Installation

**Via CI artifact:** download the `.deb` built by the latest pipeline (see
[CI/CD](#cicd) below) and install it:

```bash
sudo dpkg -i nxtool_*.deb
```

**From source:**

```bash
git clone <repo-url>
cd nginx-tools
./build_deb.sh
sudo dpkg -i nxtool_*.deb
```

### Requirements

- Debian/Ubuntu-based system with `nginx` installed
- `python3`, `python3-argcomplete`
- sudo privileges (`ensite`/`dissite`/`reload` internally run
  `sudo nginx -t` / `sudo systemctl reload nginx`)

## Usage

```bash
nxtool ensite example.com.conf   # enable + validate + reload
nxtool dissite example.com.conf  # disable + validate + reload
nxtool reload                    # reload nginx
nxtool help                      # print version
```

Config paths are fixed to the standard Debian/nginx layout:

- `sites-available`: `/etc/nginx/sites-available`
- `sites-enabled`: `/etc/nginx/sites-enabled`

## CI/CD

`.gitlab-ci.yml` builds a versioned `.deb` on every push:

1. Installs build dependencies (`binutils`, `python3`, `python3-pip`,
   `python3-argcomplete`) on `ubuntu:latest`.
2. Assembles the package layout - `usr/bin/nxtool`, `usr/lib/nxtool/*`, and a
   generated bash-completion script.
3. Versions the build as `<base-version>-<CI_PIPELINE_IID>`, so every pipeline
   run produces a distinct, traceable package.
4. Publishes the resulting `*.deb` as a pipeline artifact (1 week expiry).

## Status

Early alpha - built for managing my own nginx setup, not hardened or tested
for production fleets.
