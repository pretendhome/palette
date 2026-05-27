# INCIDENT: APFS Kernel Module Crash — Hard Reboot

**Date**: 2026-05-27 ~10:16 PDT
**Severity**: HIGH (unplanned hard reboot, lost in-flight work)
**Device**: Fantom Drives external HDD (USB 3.0 SuperSpeed, /dev/sda)
**Filesystem**: APFS (partition sda2, UUID 6c8a38ab-0b83-4b39-b38e-158a5fdd4f76)

---

## Timeline

| Time (PDT) | Event |
|---|---|
| 09:13 | First APFS mount attempt: `mount -t apfs /dev/sda2 /mnt/fantom` — "requested volume does not exist" |
| 09:16 | Tried vol=0, vol=1 — same error. Ran `apfsck -n`, `apfsck -c` |
| 09:17 | Mount with `-o vol=1` — succeeded (or partially) |
| 09:55 | APFS error recurs: "requested volume does not exist" (72g) |
| 09:56 | **UBSAN: array-index-out-of-bounds in xattr.c:47:21** — index 20 out of range for type 'u8 [*]' |
| 09:56 | Kernel stack trace through `apfs_xattr_from_query`, `apfs_get_link` |
| 10:16:37 | Attempted `umount /mnt/fantom` |
| 10:16:37 | Attempted `mount -t apfs -o vol=1,rw /dev/sda2 /mnt/fantom` |
| 10:16:42 | `umount -l /mnt/fantom` (lazy unmount) |
| 10:16:43 | Re-mount attempt with `-o vol=1,rw` |
| 10:16:47 | `fuser -km /mnt/fantom` — killed all processes using mount |
| 10:16:48 | **Mass SIGKILL**: dbus, bluetooth, upower, power-profiles-daemon, polkit, udevd, resolved, timesyncd, gnome-remote-desktop, accounts-daemon, switcheroo-control — all killed simultaneously |
| 10:17:19 | `usb 4-1: reset SuperSpeed USB device number 2 using xhci_hcd` |
| 10:17:21 | Final APFS error: "requested volume does not exist (4fg)" — note corrupted generation number |
| 10:17:xx | System rebooted, GDM restarted |

## Root Cause

The **out-of-tree APFS kernel module** (unsigned, taints kernel) has a buffer overrun bug in its xattr handling (`xattr.c:47`, index 20 out of bounds). This corrupted kernel state. The subsequent mount/unmount/fuser cycle while the kernel was already in a bad state triggered a hard crash.

Key evidence:
- `apfs: loading out-of-tree module taints kernel`
- `apfs: module verification failed: signature and/or required key missing`
- UBSAN triggered at 09:56 but system continued running in degraded state
- The `fuser -km` at 10:16:47 was the final trigger — killed processes while kernel memory was corrupted
- Generation numbers in APFS errors went from `71g` → `72g` → `4fg` (corrupted)

## Impact

- **Lost work**: In-flight Adaptive Intent Framework crew discussion (bus messages survived, no code lost)
- **Data risk**: None — the Fantom drive was never successfully written to
- **System state**: Clean after reboot, no filesystem corruption on boot drive

## Lessons / Actions

1. **Do NOT use `-o rw` with the Linux APFS module** — write support is experimental and triggers the xattr bug
2. **Mount read-only only**: `sudo mount -t apfs -o vol=0,ro /dev/sda2 /mnt/fantom`
3. **If read-write access needed**: Reformat to exFAT (cross-platform) or ext4 (Linux-only)
4. **The UBSAN warning at 09:56 was the early signal** — should have unmounted immediately and not re-attempted
5. **Never run `fuser -km` on a mount backed by a tainted kernel module in error state**

## Drive Info

```
NAME   FSTYPE FSVER LABEL UUID                                 MOUNTPOINTS
sda
├─sda1 vfat   FAT32 EFI   67E3-17ED
└─sda2 apfs               6c8a38ab-0b83-4b39-b38e-158a5fdd4f76
```

## Status

- **Resolved**: System stable after reboot
- **Fantom drive**: NOT mounted, data accessible only via macOS or read-only Linux mount
- **Recommendation**: If you need this drive on Linux regularly, reformat to exFAT

---

*Logged by kiro.design — 2026-05-27T10:32 PDT*
