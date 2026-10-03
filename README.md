# PaceBowl Studio Portal (Mothership)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Cloudflare Pages](https://img.shields.io/badge/Deployed%20with-Cloudflare%20Pages-f38020.svg)](https://pages.cloudflare.com)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](https://pacebowl.com)

The central portal and mothership showcase for the **PaceBowl Studio Matrix** — a suite of zero-friction, 100% client-side micro-utilities engineered for AI artists, prompters, and modern software developers.

Live Portal: [https://pacebowl.com](https://pacebowl.com)

---

## 🧭 The PaceBowl Tool Matrix

| Tool | Subdomain | Description | Open Source Repo |
| :--- | :--- | :--- | :--- |
| **DeepSeek Studio** | [deepseek.pacebowl.com](https://deepseek.pacebowl.com) | Zero-latency prompt engineering studio for DeepSeek-R1 & V3 with 277+ agency personas | [`fullofjoy/deepseek-prompt-generator`](https://github.com/fullofjoy/deepseek-prompt-generator) |
| **Cursor Rules Generator** | [cursor.pacebowl.com](https://cursor.pacebowl.com) | Modular `.cursor/rules/*.mdc` generator with Claude Code & Windsurf support | [`fullofjoy/cursor-rules-generator`](https://github.com/fullofjoy/cursor-rules-generator) |
| **ComfyUI Prompt Studio** | [comfy.pacebowl.com](https://comfy.pacebowl.com) | Aspect ratio latent calculator, Danbooru weighting studio & SDXL/Flux presets | [`fullofjoy/comfyui-prompt-studio`](https://github.com/fullofjoy/comfyui-prompt-studio) |
| **Reddit Growth Studio** | [reddit.pacebowl.com](https://reddit.pacebowl.com) | 15-word viral one-liner engine, AutoMod risk radar & karma growth matrix | [`fullofjoy/reddit-growth-studio`](https://github.com/fullofjoy/reddit-growth-studio) |
| **AI Radar & Hotlist** | [hot.pacebowl.com](https://hot.pacebowl.com) | Real-time AI industry signals, model releases, and trending GitHub papers | Built-in Feed |

---

## ✨ Features

- **Centralized Micro-Tool Showcase**: Responsive catalog with filterable tool cards, live preview links, and feature badges.
- **Unified Cross-Subdomain Theme Engine**: Seamless dark/light theme switching automatically synchronized across all `*.pacebowl.com` subdomains using shared first-party cookies.
- **AEO / GEO / SEO Optimized**:
  - Full Schema.org JSON-LD graph (`Organization`, `WebSite`, `WebApplication` entities).
  - Search engine crawler discovery via `sitemap.xml`, `robots.txt`, and generative AI discovery via `llms.txt`.
- **Zero-Friction Privacy First**:
  - 100% Client-Side execution.
  - No server queues, no user prompt storage, zero telemetry bloat.
  - Integrated privacy-friendly analytics ([Umami](https://umami.is)).
- **Zero Running Costs ($0/mo)**: Pure static frontend deployable anywhere with zero server maintenance.

---

## 🚀 Instant Deployment (Cloudflare Pages)

### Deploy via Git (Continuous Deployment)
1. Fork or clone this repository to your GitHub account:
   ```bash
   git clone https://github.com/fullofjoy/pacebowl-portal.git
   ```
2. Open the [Cloudflare Dashboard](https://dash.cloudflare.com/) and navigate to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
3. Select this repository.
4. Set build settings:
   - **Framework preset**: `None`
   - **Build command**: *(leave empty)*
   - **Build output directory**: `.`
5. Click **Save and Deploy**. Your portal is globally served over Cloudflare CDN edge nodes.

---

## 📁 Repository Structure

```text
pacebowl-portal/
├── index.html        # Main portal landing page and responsive layout
├── favicon.svg       # Vector icon branding
├── favicon.ico       # Fallback icon
├── apple-touch-icon.png
├── robots.txt        # Search engine indexing directives
├── sitemap.xml       # Portal and tool index sitemap
├── llms.txt          # LLM & AI agent discovery spec
├── _redirects        # Cloudflare Pages edge routing and affiliate gateways
└── LICENSE           # MIT License
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/fullofjoy/pacebowl-portal/issues).

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
