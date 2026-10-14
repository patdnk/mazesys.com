# mazesys.com

Small static site built with [Astro](https://astro.build), hosted free on GitHub Pages.

| URL | Source |
|---|---|
| `https://mazesys.com/` | `src/pages/index.astro` |
| `https://mazesys.com/zerobite/` | `src/pages/zerobite/index.astro` |
| `https://mazesys.com/zerobite/privacy-policy.html` | `src/pages/zerobite/privacy-policy.astro` (App Store Privacy Policy URL) |
| `https://mazesys.com/zerobite/support.html` | `src/pages/zerobite/support.astro` (App Store Support URL) |

`build.format: 'preserve'` in `astro.config.mjs` keeps those `.html` file names, so the App Store URLs never change.
Apps listed on the home page come from `src/data/apps.ts`; add an app there and give it a folder under `src/pages/<slug>/`.

## SEO

- `Base.astro` writes the canonical URL, Open Graph and Twitter tags for every page; pass `image` (1200 × 630) and `jsonLd` where a page has them.
- The home page's social preview is `public/og.png`, rendered from `design/og.html` by `scripts/render-og.sh` (headless Brave; set `BROWSER` for another Chromium).
- `src/pages/sitemap.xml.ts` lists every page in `src/pages/` except the 404, so new pages appear without editing it. `public/robots.txt` points crawlers at it.

## Logo

`src/assets/mazesys-logo.svg` is traced from `design/mazesys-logo-source.jpg` by `python3 scripts/trace-logo.py`
(Pillow only). The home page inlines it so CSS can draw the maze wall by wall; swap in an original vector
file any time, keeping the `wall` / `wordmark` classes and `pathLength="1"` on the walls.

## Local development

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # static output in dist/
npm run preview   # serve dist/
```

## Going live (one-time)

1. Create a GitHub repo (e.g. `patdnk/mazesys.com`) and push this folder to `main`.
2. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
   `.github/workflows/deploy.yml` builds and deploys on every push to `main`.
3. Still in **Settings → Pages**, set **Custom domain** to `mazesys.com` (the `public/CNAME` file matches).
4. At your domain registrar, add these DNS records and **leave the existing MX records alone** so email keeps working:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | patdnk.github.io |

5. Once GitHub shows the domain as verified (can take up to a day for DNS), tick **Enforce HTTPS**.
6. Make sure `support@mazesys.com` exists as a mailbox or alias with your email provider. It's the public contact on every page.

## Later: Sanity

Pages are plain `.astro` files today. To edit them in Sanity instead, fetch documents in each page's frontmatter at build
time (`@sanity/client`) and trigger a rebuild from a Sanity webhook (a GitHub `repository_dispatch` or the
`workflow_dispatch` above). URLs stay the same.
