---
name: media-video
description: "Video capture, frame extraction, and macOS UI automation. Covers ffmpeg-based frame/clip extraction from video files (video-frames), RTSP/ONVIF camera snapshots and clips (camsnap), and full macOS UI automation including screenshots and live capture (peekaboo)."
---

# Media & Video

Consolidated skill covering video frame extraction, IP camera capture, and macOS UI/screen capture automation.

---

## video-frames — Extract Frames from Video Files (ffmpeg)

Extract a single frame from a video, or create quick thumbnails for inspection.

**Requires:** `ffmpeg` on PATH
**Install:** `brew install ffmpeg`

### Quick start

First frame:
```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --out /tmp/frame.jpg
```

At a timestamp:
```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
```

### Notes
- Prefer `--time` for "what is happening around here?".
- Use `.jpg` for quick share; use `.png` for crisp UI frames.

---

## camsnap — Capture from RTSP/ONVIF Cameras

Use `camsnap` to grab snapshots, clips, or motion events from configured cameras.

**Requires:** `camsnap` + `ffmpeg` on PATH
**Install:** `brew install steipete/tap/camsnap`
**Homepage:** https://camsnap.ai

### Setup

- Config file: `~/.config/camsnap/config.yaml`
- Add camera: `camsnap add --name kitchen --host 192.168.0.10 --user user --pass pass`

### Common commands

```bash
camsnap discover --info                                # Discover cameras
camsnap snap kitchen --out shot.jpg                    # Snapshot
camsnap clip kitchen --dur 5s --out clip.mp4           # Short clip
camsnap watch kitchen --threshold 0.2 --action '...'  # Motion watch
camsnap doctor --probe                                  # Diagnose connectivity
```

### Notes
- Requires `ffmpeg` on PATH.
- Prefer a short test capture before longer clips.

---

## peekaboo — macOS UI Automation & Screen Capture

Full macOS UI automation CLI: capture/inspect screens, target UI elements, drive input, and manage apps/windows/menus.

**Requires:** `peekaboo` (macOS only), Screen Recording + Accessibility permissions
**Install:** `brew install steipete/tap/peekaboo`
**Homepage:** https://peekaboo.boo

### Quickstart

```bash
peekaboo permissions
peekaboo list apps --json
peekaboo see --annotate --path /tmp/peekaboo-see.png
peekaboo click --on B1
peekaboo type "Hello" --return
```

### See → click → type (most reliable flow)

```bash
peekaboo see --app Safari --window-title "Login" --annotate --path /tmp/see.png
peekaboo click --on B3 --app Safari
peekaboo type "user@example.com" --app Safari
peekaboo press tab --count 1 --app Safari
peekaboo type "supersecret" --app Safari --return
```

### Capture screenshots + analyze

```bash
peekaboo image --mode screen --screen-index 0 --retina --path /tmp/screen.png
peekaboo image --app Safari --window-title "Dashboard" --analyze "Summarize KPIs"
peekaboo see --mode screen --screen-index 0 --analyze "Summarize the dashboard"
```

### Live capture (motion-aware)

```bash
peekaboo capture live --mode region --region 100,100,800,600 --duration 30 \
  --active-fps 8 --idle-fps 2 --highlight-changes --path /tmp/capture
```

### App + window management

```bash
peekaboo app launch "Safari" --open https://example.com
peekaboo window focus --app Safari --window-title "Example"
peekaboo window set-bounds --app Safari --x 50 --y 50 --width 1200 --height 800
peekaboo app quit --app Safari
```

### Menus, menubar, dock

```bash
peekaboo menu click --app Safari --item "New Window"
peekaboo menu click --app TextEdit --path "Format > Font > Show Fonts"
peekaboo menu click-extra --title "WiFi"
peekaboo dock launch Safari
peekaboo menubar list --json
```

### Mouse + gesture input

```bash
peekaboo move 500,300 --smooth
peekaboo drag --from B1 --to T2
peekaboo swipe --from-coords 100,500 --to-coords 100,200 --duration 800
peekaboo scroll --direction down --amount 6 --smooth
```

### Keyboard input

```bash
peekaboo hotkey --keys "cmd,shift,t"
peekaboo press escape
peekaboo type "Line 1\nLine 2" --delay 10
```

### Common targeting parameters

- App/window: `--app`, `--pid`, `--window-title`, `--window-id`, `--window-index`
- Element/coords: `--on`/`--id` (element ID), `--coords x,y`
- Snapshot targeting: `--snapshot` (ID from `see`; defaults to latest)
- Focus control: `--no-auto-focus`, `--space-switch`, `--bring-to-current-space`

### Notes
- Requires Screen Recording + Accessibility permissions.
- Use `peekaboo see --annotate` to identify targets before clicking.
- Tip: run via `polter peekaboo` to ensure fresh builds.
- Use `--json`/`-j` for scripting; `--verbose`/`-v` for debug output.
