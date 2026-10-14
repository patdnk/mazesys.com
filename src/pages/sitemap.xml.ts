// sitemap.xml, built from the pages folder so new pages are listed without editing this file.
// With `build.format: 'preserve'`, index pages map to their folder and every other page keeps its `.html` name.
import type { APIRoute } from 'astro';

const pages = Object.keys(import.meta.glob('./**/*.astro'))
  .filter((file) => !file.endsWith('/404.astro'))
  .map((file) => file.slice(1).replace(/index\.astro$/, '').replace(/\.astro$/, '.html'))
  .sort();

export const GET: APIRoute = ({ site }) => {
  const urls = pages.map((path) => `  <url><loc>${new URL(path, site)}</loc></url>`).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
