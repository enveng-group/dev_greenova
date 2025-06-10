// shared/types.ts
// Common TypeScript types and interfaces for Greenova frontend

export interface Notification {
  message: string;
  type: "info" | "success" | "error";
}

export interface Obligation {
  id: string;
  [key: string]: any;
}

export interface LandingPageContent {
  hero_title: string;
  hero_subtitle: string;
  features: any[];
  stats: any[];
  benefits: string[];
  testimonials: any[];
  cta_title: string;
  cta_subtitle: string;
}
