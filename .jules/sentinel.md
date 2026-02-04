## 2025-05-02 - SSRF in Web Loading Tool
**Vulnerability:** The `load_web_page` tool was vulnerable to Server-Side Request Forgery (SSRF). While it disabled redirects, it did not validate the initial URL, allowing access to internal services like `localhost` or private IP ranges.
**Learning:** Disabling redirects is insufficient for SSRF protection. Attackers can directly target internal IPs. URL validation must happen *before* the request and include hostname resolution checks (though DNS rebinding remains a race condition risk, pre-check helps).
**Prevention:** Always validate URLs against a strict allowlist of schemes (http/https) and blocklist of private IP ranges (using `ipaddress` library) before making outbound requests. Set explicit timeouts to prevent DoS.
