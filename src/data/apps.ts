// Apps listed on mazesys.com. Each app gets its own folder under src/pages/<slug>/.
export interface App {
  slug: string;
  name: string;
  tagline: string;
  summary: string;
  icon: string;
}

export const apps: App[] = [
  {
    slug: 'zerobite',
    name: 'Zero Bite',
    tagline: 'Waste less. Cook more.',
    summary: 'Track the food in your fridge, get a nudge before it goes off, and cook what’s about to expire.',
    icon: '/zerobite/mark.svg',
  },
];

export const contactEmail = 'support@mazesys.com';
