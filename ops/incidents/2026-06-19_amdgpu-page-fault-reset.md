# INCIDENT: AMD GPU Page Fault → MES Hang → MODE2 Reset (Recovered)

**Date**: 2026-06-19 ~23:10 PDT
**Severity**: MEDIUM (GPU reset, session restart, no hard reboot required)
**Device**: AMD Radeon (PCI c4:00.0, Device 1114 rev d2, Lenovo subsystem 512f)
**Kernel**: 6.17.0-1025-oem (Ubuntu 24.04 OEM)
**Trigger**: Chrome GPU process (pid 5635, thread chrome:cs0 pid 5663) triggered gfxhub page fault

---

## Timeline

| Time (PDT) | Event |
|---|---|
| 23:10:39 | **gfxhub page fault** — Chrome shader compiler (SQC data client) accessed unmapped address 0x49253a430000, PERMISSION_FAULTS=0x3 |
| 23:10:39 | 7 prior page fault callbacks suppressed (fault was already escalating) |
| 23:10:49 | **Ring timeout** — gfx_0.0.0 ring stalled (signaled seq=38604088, emitted=38604090, 2 commands lost) |
| 23:10:49 | GPU IP state dumped, coredump created at /sys/class/drm/card1/device/devcoredump/data |
| 23:10:49 | Ring reset attempted |
| 23:10:51 | **MES failed to respond to msg=RESET** — scheduler unresponsive |
| 23:10:51 | Pipe reset attempted — "CPFW hasn't support pipe reset yet" |
| 23:10:51 | Ring gfx_0.0.0 reset FAILED → full GPU reset initiated |
| 23:10:53 | amdgpu_cs_ioctl parser error -125 (ECANCELED — in-flight commands rejected) |
| 23:10:54 | **MES failed to respond to msg=REMOVE_QUEUE** — still unresponsive during teardown |
| 23:10:54 | Failed to halt CP GFX |
| 23:10:54 | **MODE2 reset** executed |
| 23:10:54 | GPU reset succeeded, SMU resumed |
| 23:10:55 | All rings re-initialized, GPU operational |
| 23:10:55 | "device wedged, but recovered through reset" |
| 23:11:00 | USB disconnect (dock billboard device — display re-enumeration side effect) |
| 23:11:05 | GDM/GNOME session restarted (GNOME Power service failed, display re-initialized) |
| 23:11:19 | System stable, user session active |

## Root Cause

**Chrome's GPU process triggered a page fault in the shader queue compiler (SQC).** The fault was a permission violation (PERMISSION_FAULTS=0x3, RW=0x0 = read attempt) at a mapped-but-protected address. This wedged the gfx ring, and MES (still on unified scheduler, `uni_mes` default) could not recover gracefully — forcing a full MODE2 hardware reset.

Key differences from 2026-05-28 incident:
- **This time**: Page fault from userspace process (Chrome) → ring timeout → MES unresponsive → MODE2 reset → **recovered**
- **May 28**: No triggering process, MES hung spontaneously → ring buffer filled → **hard freeze, no recovery**
- **Improvement**: Kernel 6.17.0-1025-oem (was -1023) successfully executed MODE2 reset path. The system survived.

## Boot Parameters

```
quiet splash amdgpu.sg_display=0
```

**Note**: `amdgpu.uni_mes=0` was recommended on 2026-05-28 but **never applied**. The unified MES scheduler is still active.

## Impact

- **Lost work**: GNOME session restarted — any unsaved GUI state lost. Terminal sessions survived (tmux/screen).
- **Data risk**: None — filesystem untouched, GPU reset is display-controller only.
- **System state**: Fully recovered, no reboot needed.

## Actions

### Immediate
- [x] System recovered via MODE2 reset
- [x] Incident logged

### Recommended
- [ ] **Apply `amdgpu.uni_mes=0`** — this was recommended on May 28 and is still pending. Tonight's crash confirms the unified MES cannot handle fault recovery. Command:
  ```bash
  sudo sed -i 's/amdgpu.sg_display=0/amdgpu.sg_display=0 amdgpu.uni_mes=0/' /etc/default/grub
  sudo update-grub
  ```
  Takes effect on next reboot. 🔄 TWO-WAY DOOR (reversible kernel param).
- [ ] Check if Chrome hardware acceleration can be limited to reduce GPU fault surface (`chrome://flags/#enable-vulkan` → disabled, or `--disable-gpu-compositing`)

## Frequency (updated)

| Date | Cause | Outcome | Kernel |
|---|---|---|---|
| 2026-04-23 | MES ring buffer overflow (multi-monitor drag) | Hard reboot | 6.17.0-1017-oem |
| 2026-05-28 | MES hang (spontaneous) | Hard freeze → hard reboot | 6.17.0-1023-oem |
| **2026-06-19** | **Chrome page fault → MES hang** | **MODE2 reset → recovered** | **6.17.0-1025-oem** |

**Trend**: Same underlying MES firmware bug. Newer kernel handles recovery better (MODE2 reset works now), but the root cause (unified MES scheduler fragility on gfx11) remains. `amdgpu.uni_mes=0` is overdue.

---

*Logged by kiro.design — 2026-06-19T23:17 PDT*
