# AST02 — Supply Chain Compromise

The skill itself may be honest, but what it *pulls in* is not: dependencies,
mirrors, tarball URLs, or a "trusted" distribution channel that can serve
malware to everyone downstream.

## Detection cues (static)

- Dependencies from non-registry sources: a git URL, a raw tarball
  (`"pkg": "https://…/x.tgz"`), a private mirror the author controls instead of
  the public registry. Grep `package.json`, `requirements.txt`,
  `pyproject.toml` for `http`, `git+`, `.tgz`, `file:`.
- Typosquat / lookalike names (`left-pad-helper`, `reqeusts`, `chalk`).
- `postinstall` / `preinstall` / build hooks that run arbitrary code on
  `npm install`. Grep `package.json` for `"postinstall"`, `"preinstall"`,
  `"prepare"`.
- Unverified downloads at setup time: `curl … | bash`, `pip install` from a URL.
- No integrity: no lockfile, no hashes/SRI, no signature.

## Severity

`postinstall` running a remote script = **Critical**. Non-registry/mirror
dependency the author controls = **High**. Typosquat = **High**. Missing
lockfile alone = **Low/Medium** depending on what else is present.

## Remediation

Pin to the public registry with a committed lockfile and hashes. Remove
install-time code execution. Vendor or vet any non-registry dependency.
