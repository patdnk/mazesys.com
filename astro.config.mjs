// @ts-check
import { defineConfig } from 'astro/config';

// Static site for GitHub Pages at https://mazesys.com.
// `preserve` keeps file names as written, so src/pages/zerobite/privacy-policy.astro
// is served at /zerobite/privacy-policy.html (the URL App Store Connect points at).
export default defineConfig({
  site: 'https://mazesys.com',
  build: { format: 'preserve' },
});
