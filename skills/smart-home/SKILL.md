---
name: smart-home
description: "Smart home device control. Covers Philips Hue lights and scenes (openhue), Eight Sleep pod temperature and alarms (eightctl), BluOS/NAD audio players (blucli), and Sonos speaker control (sonoscli)."
---

# Smart Home

Consolidated skill for controlling smart home devices: lights, sleep pods, and multi-room audio.

---

## openhue — Philips Hue Lights

Control Philips Hue lights and scenes via the OpenHue CLI.

**Requires:** `openhue`
**Install:** `brew install openhue/cli/openhue-cli`
**Homepage:** https://www.openhue.io/cli

### When to use
✅ Turn on/off lights, dim rooms, set scenes, adjust brightness/color/temperature on Hue devices.
❌ Not for non-Hue brands, HomeKit, TVs, thermostats, or non-Hue smart plugs.

### List resources

```bash
openhue get light       # List all lights
openhue get room        # List all rooms
openhue get scene       # List all scenes
```

### Control lights

```bash
# On/off
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# Brightness (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# Color temperature (warm to cool: 153-500 mirek)
openhue set light "Bedroom Lamp" --on --temperature 300

# Color (by name or hex)
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### Control rooms

```bash
openhue set room "Bedroom" --off
openhue set room "Bedroom" --on --brightness 30
```

### Scenes

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

### Quick presets

```bash
# Bedtime (dim warm)
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode (bright cool)
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode (dim)
openhue set room "Living Room" --on --brightness 10
```

### Notes
- Bridge must be on local network.
- First run requires button press on Hue bridge to pair.
- Colors only work on color-capable bulbs (not white-only).

---

## eightctl — Eight Sleep Pod Control

Use `eightctl` for Eight Sleep pod control (status, temperature, alarms, schedules).

**Requires:** `eightctl`
**Install:** `go install github.com/steipete/eightctl/cmd/eightctl@latest`
**Homepage:** https://eightctl.sh

### Auth

- Config: `~/.config/eightctl/config.yaml`
- Env: `EIGHTCTL_EMAIL`, `EIGHTCTL_PASSWORD`

### Quick start

```bash
eightctl status
eightctl on
eightctl off
eightctl temp 20
```

### Common tasks

```bash
# Alarms
eightctl alarm list
eightctl alarm create
eightctl alarm dismiss

# Schedules
eightctl schedule list
eightctl schedule create
eightctl schedule update

# Audio
eightctl audio state
eightctl audio play
eightctl audio pause

# Base
eightctl base info
eightctl base angle
```

### Notes
- API is unofficial and rate-limited; avoid repeated logins.
- Confirm before changing temperature or alarms.

---

## blucli — BluOS / NAD Audio Players

Use `blu` to control Bluesound/NAD players.

**Requires:** `blu`
**Install:** `go install github.com/steipete/blucli/cmd/blu@latest`
**Homepage:** https://blucli.sh

### Quick start

```bash
blu devices                        # Discover devices (pick target)
blu --device <id> status           # Check status
blu play                           # Start playback
blu pause
blu stop
blu volume set 15
```

### Target selection (priority order)
1. `--device <id|name|alias>`
2. `BLU_DEVICE` env var
3. Config default (if set)

### Common tasks

```bash
# Grouping
blu group status
blu group add
blu group remove

# TuneIn
blu tunein search "query"
blu tunein play "query"
```

### Notes
- Prefer `--json` for scripts.
- Confirm the target device before changing playback.

---

## sonoscli — Sonos Speakers

Control Sonos speakers on the local network.

**Requires:** `sonos`
**Install:** `go install github.com/steipete/sonoscli/cmd/sonos@latest`
**Homepage:** https://sonoscli.sh

### Quick start

```bash
sonos discover
sonos status --name "Kitchen"
sonos play --name "Kitchen"
sonos pause --name "Kitchen"
sonos stop --name "Kitchen"
sonos volume set 15 --name "Kitchen"
```

### Common tasks

```bash
# Grouping
sonos group status
sonos group join
sonos group unjoin
sonos group party
sonos group solo

# Favorites
sonos favorites list
sonos favorites open

# Queue
sonos queue list
sonos queue play
sonos queue clear

# Spotify SMAPI search
sonos smapi search --service "Spotify" --category tracks "query"
```

### Notes
- If SSDP fails, specify `--ip <speaker-ip>`.
- Spotify Web API search is optional and requires `SPOTIFY_CLIENT_ID/SECRET`.

### Troubleshooting

**`sonos discover` → `no route to host`:**
On macOS in direct (no Docker) mode, go to Settings → Privacy & Security → Local Network and enable it for the parent process hosting the Gateway (`node` if via launchd, `Terminal` if direct, `Visual Studio Code` if via VS Code terminal). Alternative: use `sandbox` mode with network access allowed.

**`sonos discover` → `bind: operation not permitted`:**
You may be running in a Codex or other sandbox that does not permit network access. Approve the escalation request or switch to a non-sandboxed exec mode.
