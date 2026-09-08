# Desktop — OWASP Desktop App Security Top 10  (v1.2, not yet implemented)

**Detection is wired** in `../framework-selection.md`; the review checklist is
**not implemented yet** (planned: v1.2). If a project triggers this module, say
the desktop module is not yet available rather than improvising.

- Standard: **OWASP Desktop App Security Top 10** (2021 — note the age; it must
  not dominate a modern review).
- Activation cues: Electron, Tauri, .NET / WPF / WinUI, Qt, Swift/macOS, native
  Rust/C++ desktop. **Electron and Tauri get both web and desktop checks.**
- Planned scope: sensitive data in memory/config, local authentication,
  filesystem access, insecure IPC, unsafe system calls, update integrity.
