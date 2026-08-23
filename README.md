# Policy Hub 

**Policy Hub** (formerly MyPolicy) is a modern, high-performance web-based intelligence platform designed to centralize, analyze, and simplify access to **76 flagship government schemes** in India (across both Central Sector/Sponsored and State-level programs).

The platform addresses a major civic pain point: the highly fragmented and dense nature of public policy guidelines. It simplifies eligibility verification, enables programmatic comparisons, and visualizes policy outlays against actual beneficiary reach.

---

## Key Features

1. **Interactive Analytics Dashboard**
   * Visualizes scheme distributions across 9 policy domains (Agriculture, Livelihood, Health, Education, Social Security, etc.).
   * Dynamic horizontal bar charts comparing the top 10 schemes by **annual budget outlays (₹ Crore)** and **beneficiary reach (Crore)** based on the latest 2025-2026 data.
   * Responsive summary cards tracking Central vs. State coverage stats.
2. **Instant Eligibility Checker**
   * Programmatic matching engine checks personal details (age, income, region, gender, caste, profession, and BPL status).
   * Calculates a match score percentage and displays matched schemes instantly.
3. **Side-by-Side Scheme Comparison**
   * Directly pits two schemes together to compare ministries, budgets, reach, and document requirements.
   * Structured eligibility breakdown side-by-side.
4. **State-Level Regional Dashboard**
   * Map filters to view and browse localized schemes (e.g., Maharashtra's Shetkari Karjmukti, West Bengal's Kanyashree, Karnataka's Yuva Nidhi, etc.).
5. **Verified Civic Datasets**
   * Clean, client-side database (`data.js`) normalized using vectors.
   * No placeholders: strictly verified, source-linked metrics from official press releases, NITI Aayog, and Ministry dashboards.

---

## Tech Stack & Architecture

* **Frontend:** Single Page Application (SPA) using Vanilla JavaScript, HTML5, and CSS3. 
* **Styling:** Custom CSS layout using CSS Grid and Flexbox (fully responsive on tablet and mobile viewports).
* **Charts:** Chart.js (version 4.4.0) for dynamic canvas rendering.
* **Icons:** Lucide Icons SVG vectors.
* **Server:** Lightweight client-side rendering—serves via any static HTTP server.

---

##  How to Run Locally

### 1. Clone the repository
Create a repository on your GitHub and clone it locally, or initialize it directly:
```bash
git clone <your-repository-url>
cd policy-finder
```

### 2. Spin up a local static server
Using Python (built-in on macOS):
```bash
python3 -m http.server 3456
```

### 3. Open in Browser
Visit **[http://localhost:3456](http://localhost:3456)**.
