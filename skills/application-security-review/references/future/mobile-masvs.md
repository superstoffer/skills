# Mobile — MASVS / MASTG  (v1.1, not yet implemented)

**Detection is wired** in `../framework-selection.md`; the review checklist is
**not implemented yet** (planned: v1.1). If a project triggers this module, say
the mobile module is not yet available rather than improvising a mobile review.

- Standard: **OWASP MASVS** (Mobile Application Security Verification Standard) —
  requirements; **MASWE** — weaknesses; **MASTG** — testing. Applies to native,
  cross-platform, and hybrid apps.
- Activation cues: `android/`, `ios/`, `*.xcodeproj`, `build.gradle`,
  `AndroidManifest.xml`, React Native, Flutter, Expo, Capacitor.
- Planned scope: secure local storage, credential handling, platform IPC,
  network/TLS pinning, code/binary protection, privacy.
