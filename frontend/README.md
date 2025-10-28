
# 🧠 Job Market Scraper — Frontend

The **Job Market Scraper Frontend** is a modern web interface built with  **Next.js 16** ,  **React 18** , and  **TypeScript** , designed to deliver a smooth, responsive, and multilingual user experience.

It enables users to fill out their professional profile — including skills, location, and seniority — and retrieves **ranked job listings** based on skill compatibility from the backend API.

---

## 🚀 Key Features

* ⚡ **Next.js App Router** architecture with full TypeScript support.
* 🌍 **Internationalization (i18n)** with persistent language context (`pt` / `en`).
* 🧠 **Custom React hooks** (`useJobSearch`) using `useReducer` for clean async logic and error handling.
* 🧩 **Reusable UI components** (`ProfileForm`, `JobResultsTable`, `SkillSummary`, `LanguageSelector`).
* 🎨 **Tailwind CSS** for utility-first, responsive styling.
* 🧱 **Clean modular structure** for easy scalability and maintainability.
* ♿ **Accessible design** with tooltips, aria-labels, and keyboard-friendly interactions.
* 🧾 **Fully typed codebase** with strict TypeScript configuration.

---

## 🗂️ Project Structure

<pre class="overflow-visible!" data-start="1460" data-end="2603"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>frontend/
├── app/
│   ├── layout.tsx           </span><span># Root layout: global styles, fonts, metadata</span><span>
│   └── page.tsx             </span><span># Main app page (form + job results)</span><span>
├── src/
│   ├── components/          </span><span># Reusable components (UI and logic)</span><span>
│   │   ├── ProfileForm.tsx
│   │   ├── JobResultsTable.tsx
│   │   ├── SkillSummary.tsx
│   │   ├── TooltipHelpIcon.tsx
│   │   └── LanguageSelector.tsx
│   ├── context/             </span><span># Global context providers (LanguageContext)</span><span>
│   ├── hooks/               </span><span># Custom React hooks (useJobSearch)</span><span>
│   ├── locales/             </span><span># Translations (en / pt)</span><span>
│   ├── styles/              </span><span># Global styles (Tailwind + globals.css)</span><span>
│   ├── types/               </span><span># Type definitions (e.g., Job)</span><span>
│   ├── utils/               </span><span># Utilities and helpers (e.g., pct formatter)</span><span>
│   └── assets/              </span><span># App-specific static assets</span><span>
├── public/                  </span><span># Static files (flags, icons, etc.)</span><span>
├── package.json             </span><span># Dependencies and scripts</span><span>
├── tsconfig.json            </span><span># TypeScript configuration</span><span>
├── next.config.mjs          </span><span># Next.js configuration</span><span>
└── eslint.config.mjs        </span><span># ESLint + formatting rules</span><span>
</span></span></code></div></div></pre>

---

## 🧩 How It Works

1. **Profile Setup**
   Users input their desired tech stack, location, and seniority via the form component.

2. **Job Search Logic**
   The `useJobSearch` hook builds a structured query, calls the `/api/search` endpoint, and updates state through a reducer pattern.

3. **Results Display**
    Results are rendered through the `JobResultsTable` and `SkillSummary` components, showing compatibility percentages and matched/missing skills.

4. **Language Context**
   The `LanguageContext` manages global language state with persistence in `localStorage`, ensuring i18n across components.

5. **UX and Accessibility**
   Tooltips, keyboard navigation, and visual focus states enhance usability and compliance with accessibility standards.

---

## 🌍 Internationalization
This frontend supports Portuguese (pt) and English (en), with all UI texts centralized in:
```bash
src/locales/translations.ts
```
Language preference is stored locally and managed globally through the ``LanguageContext``.

---

## 🧰 Tech Stack
- Next.js 16 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Heroicons
- Framer Motion (optional animation support)

---

## 🧱 Design Principles

-- **Separation of concerns:** business logic, UI, and translation layers are isolated.
-- **Declarative components:** minimal state management inside UI components.
-- **Type safety:** every layer (API, UI, utils) uses strict TypeScript interfaces.
-- **Scalability:** designed for feature extension and easy backend integration.