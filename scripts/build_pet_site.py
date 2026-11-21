#!/usr/bin/env python3
"""
PaceBowl Pet Nutrition Hub — Static Site & SEO/GEO/AEO Generator
Generates:
  - /index.html (Hub Homepage)
  - /tools/dog-calorie-feeding-calculator/index.html
  - /tools/barf-raw-dog-food-calculator/index.html
  - /tools/dog-food-transition-calculator/index.html
  - /tools/cat-calorie-feeding-calculator/index.html
  - /tools/puppy-adult-weight-calculator/index.html
  - /assets/og-pacebowl.png (1200x630 Open Graph card)
  - /robots.txt, /sitemap.xml, /llms.txt, /llms-full.txt
  - /.well-known/agent-skills/index.json, /_redirects
"""
import json
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont

ROOT = "/data/workspace/pacebowl-portal"
SITE = "https://pacebowl.com"
TODAY = date.today().isoformat()

UMAMI_SNIPPET = """  <script>
  (function () {
    try {
      var p = new URLSearchParams(window.location.search).get('umami_ignore');
      if (p === '1') localStorage.setItem('umami.disabled', '1');
      else if (p === '0') localStorage.removeItem('umami.disabled');
    } catch (e) {}
    window.__matrixUmamiBeforeSend = function (type, payload) {
      try {
        if (localStorage.getItem('umami.disabled') === '1') return false;
        if (navigator.webdriver) return false;
        if (/HeadlessChrome|Playwright|Puppeteer/i.test(navigator.userAgent || '')) return false;
        var h = window.location.hostname || '';
        if (h === 'localhost' || h === '127.0.0.1' || /\\.(pages\\.dev|workers\\.dev|instabox\\.tech)$/i.test(h)) return false;
      } catch (e) {}
      return payload;
    };
  })();
  </script>
  <script defer src="https://umami-ruby-alpha-96.vercel.app/script.js" data-website-id="260de255-2ac2-4a9b-a17d-e4aec78f9ab1" data-domains="pacebowl.com,www.pacebowl.com" data-before-send="__matrixUmamiBeforeSend"></script>"""

NAV_ITEMS = [
    ("Dog Calories", "/tools/dog-calorie-feeding-calculator/"),
    ("BARF Raw Diet", "/tools/barf-raw-dog-food-calculator/"),
    ("7-Day Transition", "/tools/dog-food-transition-calculator/"),
    ("Cat Wet & Dry", "/tools/cat-calorie-feeding-calculator/"),
    ("Puppy Weight", "/tools/puppy-adult-weight-calculator/"),
]

def generate_og_image():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    img = Image.new("RGB", (1200, 630), (27, 67, 50))
    draw = ImageDraw.Draw(img)
    # Warm amber accent bar
    draw.rectangle([0, 0, 1200, 14], fill=(217, 119, 6))
    draw.rectangle([60, 74, 1140, 556], fill=(250, 248, 245), outline=(217, 119, 6), width=3)
    try:
        font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font_lg = font_md = font_sm = ImageFont.load_default()
    draw.text((110, 130), "PaceBowl Pet Nutrition", fill=(27, 67, 50), font=font_lg)
    draw.text((110, 220), "Vet-Standard Dog & Cat Feeding Calculators", fill=(28, 25, 23), font=font_md)
    draw.text((110, 285), "* Dog RER / DER Calorie & Daily Grams Calculator", fill=(87, 83, 78), font=font_sm)
    draw.text((110, 328), "* BARF 70/10/10 & PMR 80/10/10 Raw Diet Portion Planner", fill=(87, 83, 78), font=font_sm)
    draw.text((110, 371), "* 7-Day Food Transition Mixing Chart & Cat Wet/Dry Split", fill=(87, 83, 78), font=font_sm)
    draw.text((110, 414), "* Free Printable A4 Fridge Feeding Charts (WSAVA / NRC)", fill=(217, 119, 6), font=font_sm)
    draw.text((110, 490), "https://pacebowl.com  |  100% Free Client-Side Tools", fill=(27, 67, 50), font=font_sm)
    out = os.path.join(ROOT, "assets", "og-pacebowl.png")
    img.save(out, "PNG", optimize=True)
    print(f"Generated OG image: {out} (1200x630)")

def render_shell(path_slug, title, desc, keywords, json_ld_graph, body_html, inline_js=""):
    assert 48 <= len(title) <= 64, f"Title length out of SEO range ({len(title)}): {title}"
    assert 120 <= len(desc) <= 162, f"Desc length out of SEO range ({len(desc)}): {desc}"
    canonical = f"{SITE}{path_slug}"
    nav_links = "\n        ".join(
        f'<a href="{href}" class="{"active" if href == path_slug else ""}">{label}</a>'
        for label, href in NAV_ITEMS
    )
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": json_ld_graph}, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="application/json" href="{SITE}/.well-known/agent-skills/index.json" title="Agent Skills Index">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#1B4332">
  <meta name="google-site-verification" content="p_5pqOozjilh_Db2M0Owy5AQCZHdlvAVFpxQ-Asdxcs">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="PaceBowl Pet Nutrition">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/og-pacebowl.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/assets/og-pacebowl.png">

  <link rel="stylesheet" href="/assets/css/pacebowl.css">
  <script type="application/ld+json">
{schema_json}
  </script>
{UMAMI_SNIPPET}
  <script defer src="/assets/js/pacebowl-math.js"></script>
  <script defer src="/assets/js/pacebowl-pdf.js"></script>
  <script defer src="/assets/js/pacebowl-feedback.js"></script>
</head>
<body>
  <header class="pb-header">
    <div class="pb-container pb-nav-inner">
      <a href="/" class="pb-logo">
        <span>🐾 PaceBowl</span>
        <span class="pb-logo-badge">Pet Nutrition</span>
      </a>
      <nav class="pb-nav-links" aria-label="Primary Pet Calculators">
        {nav_links}
      </nav>
    </div>
  </header>

  <main class="pb-container">
{body_html}
  </main>

  <footer class="pb-footer">
    <div class="pb-container pb-footer-inner">
      <div>
        <strong>PaceBowl Pet Nutrition Studio</strong> · Based on WSAVA &amp; NRC veterinary nutrition formulas. For educational use; consult your veterinarian for medical diets.
      </div>
      <div class="pb-footer-links">
        <a href="/tools/dog-calorie-feeding-calculator/">Dog Calories</a>
        <a href="/tools/barf-raw-dog-food-calculator/">BARF Raw</a>
        <a href="/tools/dog-food-transition-calculator/">7-Day Transition</a>
        <a href="/tools/cat-calorie-feeding-calculator/">Cat Wet &amp; Dry</a>
        <a href="/tools/puppy-adult-weight-calculator/">Puppy Weight</a>
        <a href="/llms.txt">llms.txt</a>
      </div>
    </div>
  </footer>
  {f'<script>{inline_js}</script>' if inline_js else ''}
</body>
</html>
"""

ORG_SCHEMA = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "PaceBowl Pet Nutrition",
    "url": f"{SITE}/",
    "logo": f"{SITE}/apple-touch-icon.png",
    "description": "Free veterinary-standard dog and cat feeding, BARF raw diet, food transition, and puppy growth calculators with printable A4 fridge charts.",
    "sameAs": [
        "https://www.wikidata.org/wiki/Q144",
        "https://www.wikidata.org/wiki/Q146",
        "https://www.wikidata.org/wiki/Q38404",
        "https://www.wikidata.org/wiki/Q170201",
    ],
}

def related_tools_html(current_slug):
    cards = [
        ("🐕", "Dog Calorie & Feeding Calculator", "/tools/dog-calorie-feeding-calculator/", "Calculate exact daily kcal, grams, and cups using WSAVA RER/DER formulas."),
        ("🥩", "BARF Raw Dog Food Calculator", "/tools/barf-raw-dog-food-calculator/", "Split 70/10/5/5/7/2/1 BARF or 80/10/10 PMR raw meals into daily grams & batch lbs."),
        ("🔄", "7-Day Dog Food Transition Chart", "/tools/dog-food-transition-calculator/", "Calorie-matched day-by-day old vs. new kibble mixing schedule to prevent upset stomach."),
        ("🐈", "Cat Wet & Dry Feeding Calculator", "/tools/cat-calorie-feeding-calculator/", "Balance daily wet cans with exact remaining dry kibble grams for indoor cats."),
        ("🐶", "Puppy Adult Weight Predictor", "/tools/puppy-adult-weight-calculator/", "Estimate your puppy's full adult weight range and milestone growth chart by breed size."),
    ]
    items = []
    for icon, name, href, desc in cards:
        if href == current_slug:
            continue
        items.append(f"""
        <a href="{href}" class="pb-tool-card">
          <div>
            <div style="font-size:24px;">{icon}</div>
            <h3>{name}</h3>
            <p>{desc}</p>
          </div>
          <span class="pb-tool-cta">Open Calculator &rarr;</span>
        </a>""")
    return f"""
    <section class="pb-section" aria-label="More Pet Feeding Calculators">
      <h2>Explore More PaceBowl Pet Nutrition Calculators</h2>
      <div class="pb-tools-grid">{''.join(items)}
      </div>
    </section>"""

def write_page(rel_path, html):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {rel_path} ({len(html)} bytes)")

# =====================================================================
# 1. HOMEPAGE (/)
# =====================================================================
def build_homepage():
    title = "PaceBowl — Free Dog & Cat Feeding & Diet Calculators"
    desc = "Free veterinary-standard dog calorie, BARF 80/10/10 raw diet, 7-day food transition, cat wet/dry, and puppy weight calculators with printable A4 fridge charts."
    faqs = [
        ("How accurate are PaceBowl pet feeding calculators?", "PaceBowl uses the official WSAVA and NRC Resting Energy Requirement formula RER = 70 x (weight in kg)^0.75 multiplied by veterinary life-stage factors (1.0x to 3.0x), matching clinical nutrition guidelines."),
        ("Why should I weigh pet food in grams instead of scoops?", "Veterinary studies show measuring cups can vary by 18% to 48% per scoop, which causes gradual pet obesity. Weighing kibble or raw portions in grams on a digital scale keeps daily calories accurate within 2%."),
        ("Are the printable A4 fridge feeding charts free?", "Yes. Every PaceBowl calculator exports a clean, instant A4 PDF fridge chart with AM/PM meal checkboxes directly in your browser with zero signup required."),
    ]
    graph = [
        ORG_SCHEMA,
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "url": f"{SITE}/",
            "name": "PaceBowl Pet Nutrition",
            "dateModified": TODAY,
            "publisher": {"@id": f"{SITE}/#organization"},
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        },
    ]
    body = f"""
    <section class="pb-hero">
      <div class="pb-pill">🐾 WSAVA &amp; NRC Vet Formulas · 100% Free Client-Side · Printable A4 Fridge Charts</div>
      <h1>Precision Dog &amp; Cat Feeding, Raw Diet &amp; Portion Calculators</h1>
      <p>Stop guessing with inconsistent measuring scoops. Calculate exact daily calories (kcal), gram weights, BARF 80/10/10 raw meal prep, and 7-day kibble transition schedules in seconds—then print a clean A4 fridge chart.</p>
    </section>

    <section class="pb-section" style="margin-top:8px;">
      <div class="pb-tools-grid">
        <a href="/tools/dog-calorie-feeding-calculator/" class="pb-tool-card">
          <div>
            <div style="font-size:28px;">🐕</div>
            <h3>Dog Calorie &amp; Feeding Calculator</h3>
            <p>Compute exact WSAVA RER/DER calories, daily grams, oz, and cups per meal across 8 life stages—from 3.0x puppies to 1.0x weight-loss adults.</p>
          </div>
          <span class="pb-tool-cta">Calculate Dog Portions &rarr;</span>
        </a>
        <a href="/tools/barf-raw-dog-food-calculator/" class="pb-tool-card">
          <div>
            <div style="font-size:28px;">🥩</div>
            <h3>BARF &amp; PMR 80/10/10 Raw Calculator</h3>
            <p>Generate exact daily grams and 7–30 day freezer prep shopping lists for Muscle Meat (70–80%), Raw Meaty Bone (10%), Liver (5%), and Organs (5%).</p>
          </div>
          <span class="pb-tool-cta">Plan Raw Dog Meals &rarr;</span>
        </a>
        <a href="/tools/dog-food-transition-calculator/" class="pb-tool-card">
          <div>
            <div style="font-size:28px;">🔄</div>
            <h3>7-Day Dog Food Transition Chart</h3>
            <p>Calorie-matched 7-day, 10-day, or 14-day mixing schedule (75/25 to 100%) that prevents diarrhea and adjusts for different kibble kcal/cup densities.</p>
          </div>
          <span class="pb-tool-cta">Build Mixing Chart &rarr;</span>
        </a>
        <a href="/tools/cat-calorie-feeding-calculator/" class="pb-tool-card">
          <div>
            <div style="font-size:28px;">🐈</div>
            <h3>Cat Wet &amp; Dry Feeding Calculator</h3>
            <p>Prevent indoor cat obesity by subtracting daily wet cans (e.g. 85 kcal per 3 oz can) from daily DER to find exact remaining dry kibble grams.</p>
          </div>
          <span class="pb-tool-cta">Calculate Cat Portions &rarr;</span>
        </a>
        <a href="/tools/puppy-adult-weight-calculator/" class="pb-tool-card">
          <div>
            <div style="font-size:28px;">🐶</div>
            <h3>Puppy Adult Weight Predictor</h3>
            <p>Predict adult weight range (lbs &amp; kg) from 6 to 52 weeks across Toy, Small, Medium, Large, and Giant breed maturity curves with milestone tables.</p>
          </div>
          <span class="pb-tool-cta">Predict Adult Weight &rarr;</span>
        </a>
      </div>
    </section>

    <section class="pb-section">
      <div class="pb-card">
        <h2>How Does PaceBowl Calculate Daily Pet Calories?</h2>
        <p>Every PaceBowl feeding calculator follows the peer-reviewed <strong>WSAVA (World Small Animal Veterinary Association)</strong> and <strong>NRC</strong> energy equations:</p>
        <ul>
          <li><strong>Step 1 — Resting Energy Requirement (RER):</strong> <code>RER = 70 × (Body Weight in kg)^0.75</code>. For example, a 20 kg (44 lb) dog has an RER of 662 kcal/day.</li>
          <li><strong>Step 2 — Daily Energy Requirement (DER):</strong> Multiply RER by the pet's life-stage factor (e.g., <strong>1.6×</strong> for a neutered adult dog = 1,059 kcal/day; <strong>1.2×</strong> for an indoor neutered cat = 262 kcal/day at 10 lbs).</li>
          <li><strong>Step 3 — Gram &amp; Cup Conversion:</strong> Divide DER by your food bag's exact <code>kcal/kg</code> or <code>kcal/cup</code> label (typically 320–420 kcal/cup) and split evenly across 2 or 3 slow-feeder meals.</li>
        </ul>
        <div class="pb-table-wrap">
          <table class="pb-table">
            <thead>
              <tr><th>Pet Weight</th><th>Neutered Adult Dog (1.6x)</th><th>Active Dog (2.2x)</th><th>Weight-Loss Dog (1.0x)</th><th>Approx. Kibble (360 kcal/cup)</th></tr>
            </thead>
            <tbody>
              <tr><td><strong>10 lbs (4.5 kg)</strong></td><td>349 kcal/day</td><td>479 kcal/day</td><td>218 kcal/day</td><td>0.97 cups (98 g)</td></tr>
              <tr><td><strong>25 lbs (11.3 kg)</strong></td><td>693 kcal/day</td><td>953 kcal/day</td><td>433 kcal/day</td><td>1.93 cups (195 g)</td></tr>
              <tr><td><strong>50 lbs (22.7 kg)</strong></td><td>1,164 kcal/day</td><td>1,600 kcal/day</td><td>727 kcal/day</td><td>3.23 cups (328 g)</td></tr>
              <tr><td><strong>75 lbs (34.0 kg)</strong></td><td>1,578 kcal/day</td><td>2,170 kcal/day</td><td>986 kcal/day</td><td>4.38 cups (445 g)</td></tr>
              <tr><td><strong>100 lbs (45.4 kg)</strong></td><td>1,958 kcal/day</td><td>2,692 kcal/day</td><td>1,224 kcal/day</td><td>5.44 cups (552 g)</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">
        {''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}
      </div>
    </section>"""
    write_page("index.html", render_shell("/", title, desc, "dog calorie calculator, pet feeding calculator, BARF raw dog food calculator, cat calorie calculator, dog food transition chart, pacebowl", graph, body))

# =====================================================================
# 2. DOG CALORIE & FEEDING CALCULATOR
# =====================================================================
def build_dog_calorie_page():
    slug = "/tools/dog-calorie-feeding-calculator/"
    title = "Dog Calorie & Feeding Calculator — Daily Grams & Cups"
    desc = "Free vet-standard dog calorie & feeding calculator. Find exact daily kcal (RER/DER), grams, oz, and cups per meal for puppies, adults, and weight loss."
    faqs = [
        ("How many calories does a 50 lb dog need per day?", "A healthy 50 lb (22.7 kg) neutered adult dog has a Resting Energy Requirement (RER) of 727 kcal and needs approximately 1,164 kcal/day (1.6x RER), or about 3.23 cups (328 g) of standard 360 kcal/cup kibble split into two meals."),
        ("How do I calculate grams of kibble per day from calories?", "Check the Guaranteed Analysis panel on your dog food bag for kcal/kg (usually 3,200 to 4,200 kcal/kg). Divide your dog's daily kcal requirement by kcal/kg and multiply by 1,000 to get exact grams per day."),
        ("How much should I reduce calories for dog weight loss?", "Veterinary weight-loss plans typically target 1.0x RER based on your dog's ideal target weight—not current overweight weight—aiming for safe weight loss of 1% to 2% of body weight per week."),
    ]
    graph = [
        ORG_SCHEMA,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Dog Calorie & Feeding Calculator", "item": f"{SITE}{slug}"},
        ]},
        {
            "@type": "WebApplication",
            "name": "PaceBowl Dog Calorie & Daily Feeding Calculator",
            "url": f"{SITE}{slug}",
            "applicationCategory": "HealthApplication",
            "operatingSystem": "All",
            "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        },
        {
            "@type": "HowTo",
            "name": "How to Calculate Exact Daily Dog Food Portions",
            "totalTime": "PT2M",
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Enter your dog's weight", "text": "Enter current weight (or ideal target weight for weight loss) in lbs or kg."},
                {"@type": "HowToStep", "position": 2, "name": "Select life stage & activity", "text": "Choose neutered adult (1.6x), intact (1.8x), active (2.2x), puppy (2.0x-3.0x), or weight loss (1.0x)."},
                {"@type": "HowToStep", "position": 3, "name": "Enter food calorie density", "text": "Read kcal/cup and kcal/kg from your dog food bag label to compute exact grams and cups per meal."},
            ],
        },
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    body = f"""
    <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Dog Calorie &amp; Feeding Calculator</span></nav>
    <section class="pb-hero">
      <div class="pb-pill">🐕 WSAVA Formula: RER = 70 × (kg)^0.75</div>
      <h1>Dog Calorie &amp; Feeding Calculator (Daily Grams &amp; Cups)</h1>
      <p>Calculate your dog's exact Resting Energy Requirement (RER), Daily Energy Requirement (DER), and exact grams, ounces, and cups per meal—plus a free printable A4 fridge chart.</p>
    </section>

    <section class="pb-calc-grid" aria-label="Dog Calorie Calculator">
      <div class="pb-card">
        <div class="pb-field">
          <label for="dog-name">Dog's Name (for Printable Fridge Chart)</label>
          <input id="dog-name" type="text" value="Bella" placeholder="e.g. Bella, Max">
        </div>
        <div class="pb-field">
          <label for="dog-weight">Dog's Weight (Use Ideal Weight for Weight Loss)</label>
          <div class="pb-input-row">
            <input id="dog-weight" type="number" min="1" max="250" step="0.5" value="45">
            <select id="dog-unit" style="max-width:100px;">
              <option value="lb" selected>lbs</option>
              <option value="kg">kg</option>
            </select>
          </div>
        </div>
        <div class="pb-field">
          <label for="dog-stage">Life Stage &amp; Activity Level (WSAVA Factor)</label>
          <select id="dog-stage">
            <option value="neutered_adult" selected>Neutered / Spayed Adult (1.6× RER)</option>
            <option value="intact_adult">Intact Adult (1.8× RER)</option>
            <option value="weight_loss">Weight Loss / Overweight (1.0× RER)</option>
            <option value="weight_gain">Weight Gain / Underweight (1.4× RER)</option>
            <option value="active_working">Active / Working Dog (2.2× RER)</option>
            <option value="puppy_young">Puppy Under 4 Months (3.0× RER)</option>
            <option value="puppy_older">Puppy 4 to 12 Months (2.0× RER)</option>
            <option value="senior">Senior / Low Activity 7+ yrs (1.3× RER)</option>
          </select>
        </div>
        <div class="pb-field">
          <label for="dog-kcal-cup">Food Calorie Density (kcal per cup / kcal per kg)</label>
          <div class="pb-input-row">
            <input id="dog-kcal-cup" type="number" min="150" max="800" value="360" aria-label="kcal per cup">
            <input id="dog-kcal-kg" type="number" min="2000" max="6000" value="3550" aria-label="kcal per kg">
          </div>
          <div class="pb-hint">Left: kcal/cup (avg 350–400). Right: kcal/kg (avg 3,400–3,800 on bag label).</div>
        </div>
        <div class="pb-field">
          <label for="dog-meals">Meals Per Day</label>
          <select id="dog-meals">
            <option value="2" selected>2 Meals / Day (Morning &amp; Evening)</option>
            <option value="3">3 Meals / Day (Recommended for Puppies)</option>
            <option value="1">1 Meal / Day</option>
          </select>
        </div>
      </div>

      <div class="pb-card pb-card-accent">
        <div class="pb-kpi-grid">
          <div class="pb-kpi">
            <div class="pb-kpi-label">Daily Calories (DER)</div>
            <div class="pb-kpi-val" id="out-der">1,076 kcal</div>
            <div class="pb-kpi-sub" id="out-rer">Base RER: 672 kcal/day</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Grams Per Meal</div>
            <div class="pb-kpi-val" id="out-g-meal">152 g</div>
            <div class="pb-kpi-sub" id="out-g-day">303 g/day (10.7 oz/day)</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Cups Per Meal</div>
            <div class="pb-kpi-val" id="out-c-meal">1.49 cups</div>
            <div class="pb-kpi-sub" id="out-c-day">2.99 cups/day total</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Treat Budget (10% Max)</div>
            <div class="pb-kpi-val" id="out-treats">108 kcal</div>
            <div class="pb-kpi-sub">Keep treats under 10% of DER</div>
          </div>
        </div>
        <div class="pb-notice" id="out-bowl"><strong>Recommended Slow-Feeder Bowl:</strong> Medium Slow-Feeder Bowl (2 cup capacity)</div>
        <div style="margin-top:16px; display:flex; flex-direction:column; gap:10px;">
          <button type="button" id="btn-dog-pdf" class="pb-btn pb-btn-primary">📄 Download Printable A4 Fridge Feeding Chart (PDF)</button>
          <a href="/tools/dog-food-transition-calculator/" class="pb-btn pb-btn-outline">Switching Dog Food? Open 7-Day Transition Chart &rarr;</a>
        </div>
      </div>
    </section>

    <section class="pb-section">
      <div class="pb-card">
        <h2>How Much Should I Feed My Dog by Weight? (Quick Chart)</h2>
        <p>Based on standard 360 kcal/cup (3,550 kcal/kg) adult dry kibble for a neutered adult dog (1.6× RER):</p>
        <div class="pb-table-wrap">
          <table class="pb-table">
            <thead><tr><th>Dog Weight</th><th>RER (kcal)</th><th>Daily DER (1.6×)</th><th>Daily Grams</th><th>Daily Cups</th><th>Per Meal (2×/day)</th></tr></thead>
            <tbody>
              <tr><td><strong>10 lbs (4.5 kg)</strong></td><td>218 kcal</td><td>349 kcal</td><td>98 g</td><td>0.97 cups</td><td>49 g (0.48 cup)</td></tr>
              <tr><td><strong>20 lbs (9.1 kg)</strong></td><td>366 kcal</td><td>586 kcal</td><td>165 g</td><td>1.63 cups</td><td>83 g (0.81 cup)</td></tr>
              <tr><td><strong>35 lbs (15.9 kg)</strong></td><td>558 kcal</td><td>893 kcal</td><td>252 g</td><td>2.48 cups</td><td>126 g (1.24 cups)</td></tr>
              <tr><td><strong>50 lbs (22.7 kg)</strong></td><td>727 kcal</td><td>1,164 kcal</td><td>328 g</td><td>3.23 cups</td><td>164 g (1.62 cups)</td></tr>
              <tr><td><strong>75 lbs (34.0 kg)</strong></td><td>986 kcal</td><td>1,578 kcal</td><td>445 g</td><td>4.38 cups</td><td>222 g (2.19 cups)</td></tr>
              <tr><td><strong>100 lbs (45.4 kg)</strong></td><td>1,224 kcal</td><td>1,958 kcal</td><td>552 g</td><td>5.44 cups</td><td>276 g (2.72 cups)</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">{''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}</div>
    </section>
    {related_tools_html(slug)}"""

    js = """
    (function(){
      function run(){
        if(!window.PaceBowlMath) return;
        const name = (document.getElementById('dog-name').value || 'My Dog').trim();
        const r = window.PaceBowlMath.calcDogFeeding({
          weight: document.getElementById('dog-weight').value,
          unit: document.getElementById('dog-unit').value,
          stage: document.getElementById('dog-stage').value,
          kcalPerCup: document.getElementById('dog-kcal-cup').value,
          kcalPerKg: document.getElementById('dog-kcal-kg').value,
          meals: document.getElementById('dog-meals').value,
        });
        document.getElementById('out-der').textContent = r.der.toLocaleString() + ' kcal';
        document.getElementById('out-rer').textContent = 'Base RER: ' + r.rer.toLocaleString() + ' kcal/day (' + r.factor + 'x)';
        document.getElementById('out-g-meal').textContent = r.gramsPerMeal + ' g';
        document.getElementById('out-g-day').textContent = r.gramsPerDay + ' g/day (' + r.ozPerDay + ' oz/day)';
        document.getElementById('out-c-meal').textContent = r.cupsPerMeal + ' cups';
        document.getElementById('out-c-day').textContent = r.cupsPerDay + ' cups/day total';
        document.getElementById('out-treats').textContent = Math.round(r.der * 0.1) + ' kcal';
        document.getElementById('out-bowl').innerHTML = '<strong>Recommended Slow-Feeder Bowl:</strong> ' + r.bowlRec;
        window.__lastDog = { name, r };
      }
      ['dog-name','dog-weight','dog-unit','dog-stage','dog-kcal-cup','dog-kcal-kg','dog-meals'].forEach(id=>{
        document.getElementById(id).addEventListener('input', run);
        document.getElementById(id).addEventListener('change', run);
      });
      document.getElementById('btn-dog-pdf').addEventListener('click', function(){
        const d = window.__lastDog;
        if(!d || !window.PaceBowlPdf) return;
        const r = d.r;
        const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
        window.PaceBowlPdf.downloadFeedingChartPdf({
          title: d.name + ' - Daily Dog Feeding Chart (' + r.der + ' kcal/day)',
          filename: 'PaceBowl-Dog-Feeding-Chart-' + d.name.replace(/\\s+/g,'-') + '.pdf',
          summaryRows: [
            ['Pet & Weight:', d.name + ' | ' + r.weightLb + ' lbs (' + r.weightKg + ' kg) | ' + r.stageLabel],
            ['Daily Energy Target:', r.der + ' kcal/day (WSAVA RER ' + r.rer + ' kcal x ' + r.factor + ')'],
            ['Exact Portion Per Meal:', r.gramsPerMeal + ' g (' + r.ozPerMeal + ' oz) / ' + r.cupsPerMeal + ' cups x ' + r.meals + ' meals/day'],
            ['Daily Total & Treats:', r.gramsPerDay + ' g/day (' + r.cupsPerDay + ' cups) | Max Treats: ' + Math.round(r.der*0.1) + ' kcal/day'],
            ['Slow-Feeder Bowl:', r.bowlRec]
          ],
          tableTitle: 'WEEKLY FRIDGE MEAL TRACKER (CHECK OFF AFTER EACH MEAL)',
          tableHeaders: ['Day of Week', 'Grams / Meal', 'Cups / Meal', 'Daily Total', 'Fed Check'],
          tableRows: days.map(day => [day, r.gramsPerMeal + ' g', r.cupsPerMeal + ' cups', r.gramsPerDay + ' g', '']),
          checkboxes: true
        });
      });
      window.addEventListener('DOMContentLoaded', run);
      setTimeout(run, 120);
    })();"""
    write_page("tools/dog-calorie-feeding-calculator/index.html", render_shell(slug, title, desc, "dog calorie calculator, dog feeding calculator, how much to feed my dog, dog food grams per day, RER DER calculator", graph, body, js))

# =====================================================================
# 3. BARF / PMR RAW DOG FOOD CALCULATOR
# =====================================================================
def build_barf_raw_page():
    slug = "/tools/barf-raw-dog-food-calculator/"
    title = "BARF Raw Dog Food Calculator — 80/10/10 Grams & Oz"
    desc = "Free BARF (70/10/5/5/7/2/1) & PMR 80/10/10 raw dog food calculator. Compute exact daily grams, oz, and 14-day freezer batch prep shopping lists in PDF."
    faqs = [
        ("What is the difference between BARF and PMR 80/10/10 raw dog food?", "BARF (Biologically Appropriate Raw Food) uses 70% muscle meat, 10% raw meaty bone, 5% liver, 5% other secreting organ, 7% vegetables, 2% seeds/nuts, and 1% fruit. PMR (Prey Model Raw) omits plant matter and uses 80% muscle meat, 10% bone, 5% liver, and 5% other secreting organ."),
        ("What percentage of body weight should I feed a raw-fed dog?", "Most healthy adult dogs thrive at 2.5% of ideal adult body weight per day. Overweight or low-activity dogs typically drop to 2.0%, highly active dogs need 3.0%, and growing puppies require 4% to 8% depending on age."),
        ("Can I prep 14 days of raw dog food in advance?", "Yes. Use the Batch Prep Days field above (7, 14, or 30 days) to calculate exact total pounds and grams of muscle meat, raw meaty bones, liver, and secreting organs for freezer meal prep."),
    ]
    graph = [
        ORG_SCHEMA,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "BARF Raw Dog Food Calculator", "item": f"{SITE}{slug}"},
        ]},
        {"@type": "WebApplication", "name": "PaceBowl BARF & PMR Raw Dog Food Calculator", "url": f"{SITE}{slug}", "applicationCategory": "HealthApplication", "operatingSystem": "All", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    body = f"""
    <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>BARF Raw Dog Food Calculator</span></nav>
    <section class="pb-hero">
      <div class="pb-pill">🥩 BARF 70/10/5/5/7/2/1 &amp; PMR 80/10/10 Standards</div>
      <h1>BARF &amp; PMR 80/10/10 Raw Dog Food Calculator</h1>
      <p>Calculate exact daily grams, ounces, and multi-week freezer meal-prep shopping lists for raw-fed dogs and puppies—with instant printable A4 prep sheets.</p>
    </section>

    <section class="pb-calc-grid">
      <div class="pb-card">
        <div class="pb-field">
          <label for="raw-weight">Dog's Ideal Weight</label>
          <div class="pb-input-row">
            <input id="raw-weight" type="number" min="2" max="220" step="0.5" value="50">
            <select id="raw-unit" style="max-width:100px;"><option value="lb" selected>lbs</option><option value="kg">kg</option></select>
          </div>
        </div>
        <div class="pb-field">
          <label for="raw-model">Raw Feeding Ratio Model</label>
          <select id="raw-model">
            <option value="barf" selected>BARF Model (70% Meat / 10% Bone / 10% Organ / 10% Veg-Fruit)</option>
            <option value="pmr">PMR Prey Model Raw (80% Meat / 10% Bone / 5% Liver / 5% Organ)</option>
          </select>
        </div>
        <div class="pb-field">
          <label for="raw-pct">Daily Body Weight Percentage (%)</label>
          <select id="raw-pct">
            <option value="2.0">2.0% — Adult Weight Loss / Low Activity</option>
            <option value="2.5" selected>2.5% — Adult Maintenance (Standard)</option>
            <option value="3.0">3.0% — Active / Working Adult</option>
            <option value="4.0">4.0% — Older Puppy (9–12 months)</option>
            <option value="6.0">6.0% — Growing Puppy (5–8 months)</option>
            <option value="8.0">8.0% — Young Puppy (2–4 months)</option>
          </select>
        </div>
        <div class="pb-field">
          <label for="raw-days">Freezer Batch Prep Duration (Days)</label>
          <select id="raw-days">
            <option value="7">7 Days (1 Week Batch)</option>
            <option value="14" selected>14 Days (2 Week Batch)</option>
            <option value="30">30 Days (1 Month Freezer Prep)</option>
          </select>
        </div>
      </div>

      <div class="pb-card pb-card-accent">
        <div class="pb-kpi-grid">
          <div class="pb-kpi">
            <div class="pb-kpi-label">Daily Raw Total</div>
            <div class="pb-kpi-val" id="raw-daily-g">567 g</div>
            <div class="pb-kpi-sub" id="raw-daily-oz">20.0 oz / day</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label" id="raw-batch-lbl">14-Day Batch Total</div>
            <div class="pb-kpi-val" id="raw-batch-lbs">17.5 lbs</div>
            <div class="pb-kpi-sub" id="raw-batch-kg">7.94 kg total</div>
          </div>
        </div>
        <div class="pb-table-wrap">
          <table class="pb-table">
            <thead><tr><th>Component</th><th>%</th><th>Daily (g / oz)</th><th>Batch Shopping</th></tr></thead>
            <tbody id="raw-tbody"></tbody>
          </table>
        </div>
        <button type="button" id="btn-raw-pdf" class="pb-btn pb-btn-primary" style="margin-top:12px;">📄 Download Printable A4 Raw Batch Prep Sheet (PDF)</button>
      </div>
    </section>

    <section class="pb-section">
      <h2>How Much Raw Food Should a Dog Eat Per Day (BARF vs. PMR)?</h2>
      <div class="pb-card pb-table-wrap">
        <table class="pb-table">
          <thead><tr><th>Dog Weight</th><th>2.0% Weight Loss</th><th>2.5% Maintenance</th><th>3.0% Active</th><th>Muscle Meat (70% BARF)</th></tr></thead>
          <tbody>
            <tr><td><strong>20 lb (9.1 kg)</strong></td><td>181 g (6.4 oz)</td><td>227 g (8.0 oz)</td><td>272 g (9.6 oz)</td><td>159 g / day</td></tr>
            <tr><td><strong>40 lb (18.1 kg)</strong></td><td>363 g (12.8 oz)</td><td>454 g (16.0 oz)</td><td>544 g (19.2 oz)</td><td>318 g / day</td></tr>
            <tr><td><strong>60 lb (27.2 kg)</strong></td><td>544 g (19.2 oz)</td><td>680 g (24.0 oz)</td><td>816 g (28.8 oz)</td><td>476 g / day</td></tr>
            <tr><td><strong>80 lb (36.3 kg)</strong></td><td>726 g (25.6 oz)</td><td>907 g (32.0 oz)</td><td>1,089 g (38.4 oz)</td><td>635 g / day</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">{''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}</div>
    </section>
    {related_tools_html(slug)}"""

    js = """
    (function(){
      function run(){
        if(!window.PaceBowlMath) return;
        const r = window.PaceBowlMath.calcRawDogFood({
          weight: document.getElementById('raw-weight').value,
          unit: document.getElementById('raw-unit').value,
          model: document.getElementById('raw-model').value,
          bodyPct: document.getElementById('raw-pct').value,
          prepDays: document.getElementById('raw-days').value,
        });
        document.getElementById('raw-daily-g').textContent = r.dailyGrams + ' g';
        document.getElementById('raw-daily-oz').textContent = r.dailyOz + ' oz / day (' + r.bodyPct + '% BW)';
        document.getElementById('raw-batch-lbl').textContent = r.prepDays + '-Day Batch Total';
        document.getElementById('raw-batch-lbs').textContent = r.batchLbs + ' lbs';
        document.getElementById('raw-batch-kg').textContent = r.batchKg + ' kg total';
        document.getElementById('raw-tbody').innerHTML = r.breakdown.map(b =>
          '<tr><td><strong>' + b.label + '</strong></td><td>' + b.pct + '%</td><td>' + b.dailyGrams + ' g (' + b.dailyOz + ' oz)</td><td>' + b.batchLbs + ' lbs (' + b.batchGrams + ' g)</td></tr>'
        ).join('');
        window.__lastRaw = r;
      }
      ['raw-weight','raw-unit','raw-model','raw-pct','raw-days'].forEach(id=>{
        document.getElementById(id).addEventListener('input', run);
        document.getElementById(id).addEventListener('change', run);
      });
      document.getElementById('btn-raw-pdf').addEventListener('click', function(){
        const r = window.__lastRaw;
        if(!r || !window.PaceBowlPdf) return;
        window.PaceBowlPdf.downloadFeedingChartPdf({
          title: 'Raw Dog Food Batch Prep Sheet (' + r.modelLabel + ')',
          filename: 'PaceBowl-BARF-Raw-Prep-' + r.prepDays + 'days.pdf',
          summaryRows: [
            ['Dog Ideal Weight:', r.weightLb + ' lbs (' + r.weightKg + ' kg) at ' + r.bodyPct + '% Body Weight/Day'],
            ['Raw Ratio Model:', r.modelLabel],
            ['Daily Portion Total:', r.dailyGrams + ' g/day (' + r.dailyOz + ' oz/day)'],
            [r.prepDays + '-Day Freezer Batch:', r.batchLbs + ' lbs (' + r.batchKg + ' kg) total ingredients']
          ],
          tableTitle: 'EXACT COMPONENT BREAKDOWN & BATCH SHOPPING LIST',
          tableHeaders: ['Ingredient Category', 'Ratio', 'Daily Grams', 'Daily Oz', r.prepDays + '-Day Batch'],
          tableRows: r.breakdown.map(b => [b.label, b.pct + '%', b.dailyGrams + ' g', b.dailyOz + ' oz', b.batchLbs + ' lbs (' + b.batchGrams + ' g)']),
          notes: [
            'Never feed cooked bones; only raw, non-weight-bearing meaty bones sized safely for your dog.',
            'Rotate at least 3 to 4 animal proteins (e.g. chicken, beef, turkey, lamb, sardines) over each month.',
            'Thaw frozen raw meals in the refrigerator (38-40F) and sanitize bowls after every meal.'
          ]
        });
      });
      window.addEventListener('DOMContentLoaded', run);
      setTimeout(run, 120);
    })();"""
    write_page("tools/barf-raw-dog-food-calculator/index.html", render_shell(slug, title, desc, "BARF raw dog food calculator, 80 10 10 raw dog food calculator, PMR raw feeding calculator, raw dog food grams per day", graph, body, js))

# =====================================================================
# 4. 7-DAY DOG FOOD TRANSITION CALCULATOR
# =====================================================================
def build_transition_page():
    slug = "/tools/dog-food-transition-calculator/"
    title = "7-Day Dog Food Transition Calculator & Mixing Chart"
    desc = "Free 7-day, 10-day, and 14-day dog food transition calculator. Calorie-matched old vs. new kibble grams and cups per day to switch food safely."
    faqs = [
        ("What is the safest 7-day dog food transition ratio?", "Veterinarians recommend Days 1-2: 75% old food + 25% new food; Days 3-4: 50% old + 50% new; Days 5-6: 25% old + 75% new; Day 7: 100% new food. For sensitive stomachs or puppies, extend to a 10-day or 14-day schedule."),
        ("Why do calorie densities matter when switching dog food?", "If your old kibble has 340 kcal/cup and your new kibble has 440 kcal/cup, feeding the same number of cups increases daily calories by 29%. PaceBowl automatically adjusts new-food grams and cups so total calories stay constant."),
        ("What if my dog gets loose stools during a food transition?", "Pause at the current ratio for 2 to 3 extra days before increasing the new food percentage, and consider adding 1 tablespoon of plain unsweetened pumpkin puree per meal."),
    ]
    graph = [
        ORG_SCHEMA,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "7-Day Dog Food Transition Calculator", "item": f"{SITE}{slug}"},
        ]},
        {"@type": "WebApplication", "name": "PaceBowl 7-Day Dog Food Transition Calculator", "url": f"{SITE}{slug}", "applicationCategory": "HealthApplication", "operatingSystem": "All", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    body = f"""
    <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Dog Food Transition Calculator</span></nav>
    <section class="pb-hero">
      <div class="pb-pill">🔄 Calorie-Matched 7 / 10 / 14-Day Mixing Schedule</div>
      <h1>7-Day Dog Food Transition Calculator &amp; Mixing Chart</h1>
      <p>Switch dog food without upset stomach or accidental overfeeding. Automatically adjusts for calorie differences between your old and new kibble—with a printable fridge checklist.</p>
    </section>

    <section class="pb-calc-grid">
      <div class="pb-card">
        <div class="pb-field">
          <label for="tr-days">Transition Schedule Length</label>
          <select id="tr-days">
            <option value="7" selected>7-Day Standard Vet Schedule (25% / 50% / 75% / 100%)</option>
            <option value="10">10-Day Gentle Schedule (+10% New Food Daily)</option>
            <option value="14">14-Day Sensitive Stomach / Puppy Schedule</option>
          </select>
        </div>
        <div class="pb-field">
          <label for="tr-old-g">Current Old Food Daily Amount (Grams &amp; Cups)</label>
          <div class="pb-input-row">
            <input id="tr-old-g" type="number" min="20" max="1500" value="280" aria-label="Old food daily grams">
            <input id="tr-old-c" type="number" min="0.25" max="12" step="0.25" value="2.5" aria-label="Old food daily cups">
          </div>
          <div class="pb-hint">Left: total grams/day. Right: total cups/day currently fed.</div>
        </div>
        <div class="pb-field">
          <label for="tr-old-kcal">Old Food vs. New Food Calories (kcal / cup)</label>
          <div class="pb-input-row">
            <input id="tr-old-kcal" type="number" min="150" max="700" value="360" aria-label="Old food kcal per cup">
            <input id="tr-new-kcal" type="number" min="150" max="700" value="410" aria-label="New food kcal per cup">
          </div>
          <div class="pb-hint">Left: Old bag kcal/cup. Right: New bag kcal/cup (auto-matches calories!).</div>
        </div>
      </div>

      <div class="pb-card pb-card-accent">
        <div class="pb-kpi-grid">
          <div class="pb-kpi">
            <div class="pb-kpi-label">Target Daily Calories</div>
            <div class="pb-kpi-val" id="tr-kcal">900 kcal</div>
            <div class="pb-kpi-sub">Held constant across switch</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">New Food Final Portion</div>
            <div class="pb-kpi-val" id="tr-new-final">246 g</div>
            <div class="pb-kpi-sub" id="tr-new-cups">2.20 cups/day on final day</div>
          </div>
        </div>
        <div class="pb-table-wrap">
          <table class="pb-table">
            <thead><tr><th>Day</th><th>Mix Ratio</th><th>Old Food</th><th>New Food</th></tr></thead>
            <tbody id="tr-tbody"></tbody>
          </table>
        </div>
        <button type="button" id="btn-tr-pdf" class="pb-btn pb-btn-primary" style="margin-top:12px;">📄 Download Printable A4 Transition Checklist (PDF)</button>
      </div>
    </section>

    <section class="pb-section">
      <h2>How Do You Switch Dog Food Safely Without Upset Stomach?</h2>
      <div class="pb-card pb-table-wrap">
        <table class="pb-table">
          <thead><tr><th>Transition Phase</th><th>7-Day Standard</th><th>10-Day Gentle</th><th>14-Day Sensitive</th></tr></thead>
          <tbody>
            <tr><td><strong>Phase 1 (Intro)</strong></td><td>Days 1–2: 75% Old / 25% New</td><td>Days 1–3: 80% Old / 20% New</td><td>Days 1–4: 80% Old / 20% New</td></tr>
            <tr><td><strong>Phase 2 (Halfway)</strong></td><td>Days 3–4: 50% Old / 50% New</td><td>Days 4–6: 50% Old / 50% New</td><td>Days 5–8: 50% Old / 50% New</td></tr>
            <tr><td><strong>Phase 3 (Majority)</strong></td><td>Days 5–6: 25% Old / 75% New</td><td>Days 7–9: 20% Old / 80% New</td><td>Days 9–12: 20% Old / 80% New</td></tr>
            <tr><td><strong>Phase 4 (Complete)</strong></td><td>Day 7+: 100% New Food</td><td>Day 10+: 100% New Food</td><td>Day 13–14+: 100% New Food</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">{''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}</div>
    </section>
    {related_tools_html(slug)}"""

    js = """
    (function(){
      function run(){
        if(!window.PaceBowlMath) return;
        const r = window.PaceBowlMath.calcFoodTransition({
          days: document.getElementById('tr-days').value,
          oldDailyGrams: document.getElementById('tr-old-g').value,
          oldDailyCups: document.getElementById('tr-old-c').value,
          oldKcalPerCup: document.getElementById('tr-old-kcal').value,
          newKcalPerCup: document.getElementById('tr-new-kcal').value,
        });
        document.getElementById('tr-kcal').textContent = r.targetDailyKcal + ' kcal';
        document.getElementById('tr-new-final').textContent = r.newFullDailyGrams + ' g';
        document.getElementById('tr-new-cups').textContent = r.newFullDailyCups + ' cups/day on Day ' + r.days;
        document.getElementById('tr-tbody').innerHTML = r.steps.map(s =>
          '<tr><td><strong>Day ' + s.day + '</strong></td><td>' + s.oldPct + '% / ' + s.newPct + '%</td><td>' + s.oldGrams + ' g (' + s.oldCups + ' c)</td><td><strong>' + s.newGrams + ' g (' + s.newCups + ' c)</strong></td></tr>'
        ).join('');
        window.__lastTr = r;
      }
      ['tr-days','tr-old-g','tr-old-c','tr-old-kcal','tr-new-kcal'].forEach(id=>{
        document.getElementById(id).addEventListener('input', run);
        document.getElementById(id).addEventListener('change', run);
      });
      document.getElementById('btn-tr-pdf').addEventListener('click', function(){
        const r = window.__lastTr;
        if(!r || !window.PaceBowlPdf) return;
        window.PaceBowlPdf.downloadFeedingChartPdf({
          title: r.days + '-Day Dog Food Transition Mixing Chart',
          filename: 'PaceBowl-' + r.days + 'Day-Food-Transition-Chart.pdf',
          summaryRows: [
            ['Schedule Mode:', r.days + '-Day Gradual Calorie-Matched Transition'],
            ['Target Daily Energy:', r.targetDailyKcal + ' kcal/day (maintained across switch)'],
            ['Starting Old Food:', r.oldDailyGrams + ' g/day (' + r.oldDailyCups + ' cups/day)'],
            ['Ending New Food:', r.newFullDailyGrams + ' g/day (' + r.newFullDailyCups + ' cups/day)']
          ],
          tableTitle: 'DAILY MIXING SCHEDULE (DIVIDE EQUALLY ACROSS AM & PM MEALS)',
          tableHeaders: ['Day', 'Old / New %', 'Old Food (Total)', 'New Food (Total)', 'Done'],
          tableRows: r.steps.map(s => ['Day ' + s.day, s.oldPct + '% / ' + s.newPct + '%', s.oldGrams + ' g (' + s.oldCups + ' c)', s.newGrams + ' g (' + s.newCups + ' c)', '']),
          checkboxes: true,
          notes: [
            'Mix old and new kibble thoroughly in a slow-feeder bowl so picky dogs do not sort out new pieces.',
            'If stools soften, stay at the current day ratio for 2 extra days before advancing.',
            'Provide plenty of fresh water throughout the transition.'
          ]
        });
      });
      window.addEventListener('DOMContentLoaded', run);
      setTimeout(run, 120);
    })();"""
    write_page("tools/dog-food-transition-calculator/index.html", render_shell(slug, title, desc, "7 day dog food transition chart, dog food transition calculator, how to switch dog food calculator, puppy food transition schedule", graph, body, js))

# =====================================================================
# 5. CAT CALORIE & WET/DRY MIXED FEEDING CALCULATOR
# =====================================================================
def build_cat_calorie_page():
    slug = "/tools/cat-calorie-feeding-calculator/"
    title = "Cat Calorie & Wet/Dry Food Calculator — Daily Grams"
    desc = "Free cat calorie & mixed wet/dry feeding calculator. Subtract daily wet cans from WSAVA DER calories to find exact dry kibble grams for indoor cats."
    faqs = [
        ("How many calories does a 10 lb indoor cat need per day?", "A healthy 10 lb (4.5 kg) neutered indoor cat has an RER of 218 kcal and needs about 262 kcal/day (1.2x RER). If fed one 3 oz wet can (85 kcal), they need 177 kcal of dry kibble (~47 g or 0.44 cup) per day."),
        ("How do I mix wet and dry food for my cat without overfeeding?", "First calculate your cat's total daily calorie need (DER), subtract the exact calories from all wet food cans/pouches fed each day, and measure only the remaining calories in dry kibble using a digital gram scale."),
        ("How many calories should an overweight cat eat to lose weight?", "Veterinarians typically start indoor cat weight loss at 0.8x RER based on ideal target weight (usually 170–210 kcal/day for a 10 lb ideal cat). Never fast a cat—rapid starvation risks hepatic lipidosis."),
    ]
    graph = [
        ORG_SCHEMA,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Cat Calorie & Wet/Dry Calculator", "item": f"{SITE}{slug}"},
        ]},
        {"@type": "WebApplication", "name": "PaceBowl Cat Calorie & Wet/Dry Mixed Feeding Calculator", "url": f"{SITE}{slug}", "applicationCategory": "HealthApplication", "operatingSystem": "All", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    body = f"""
    <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Cat Calorie &amp; Wet/Dry Calculator</span></nav>
    <section class="pb-hero">
      <div class="pb-pill">🐈 Indoor Cat Wet + Dry Mixed Feeding Engine</div>
      <h1>Cat Calorie &amp; Wet/Dry Food Calculator (Daily Grams)</h1>
      <p>Avoid indoor cat weight gain. Enter your cat's weight and daily wet food cans to calculate exact remaining dry kibble grams and cups—with a printable fridge chart.</p>
    </section>

    <section class="pb-calc-grid">
      <div class="pb-card">
        <div class="pb-field">
          <label for="cat-weight">Cat's Weight (Ideal Target Weight for Weight Loss)</label>
          <div class="pb-input-row">
            <input id="cat-weight" type="number" min="1" max="35" step="0.5" value="10">
            <select id="cat-unit" style="max-width:100px;"><option value="lb" selected>lbs</option><option value="kg">kg</option></select>
          </div>
        </div>
        <div class="pb-field">
          <label for="cat-stage">Cat Life Stage &amp; Activity</label>
          <select id="cat-stage">
            <option value="indoor_neutered" selected>Indoor Neutered / Spayed Adult (1.2× RER)</option>
            <option value="intact_adult">Intact Adult Cat (1.4× RER)</option>
            <option value="weight_loss">Weight Loss / Overweight (0.8× RER)</option>
            <option value="active_outdoor">Active / Outdoor Cat (1.6× RER)</option>
            <option value="kitten">Growing Kitten Under 12 Months (2.5× RER)</option>
            <option value="senior">Senior Cat 10+ Years (1.1× RER)</option>
          </select>
        </div>
        <div class="pb-field">
          <label for="cat-wet-cans">Wet Food Cans / Pouches Per Day &amp; kcal/Can</label>
          <div class="pb-input-row">
            <input id="cat-wet-cans" type="number" min="0" max="6" step="0.5" value="1" aria-label="Wet cans per day">
            <input id="cat-wet-kcal" type="number" min="30" max="250" value="85" aria-label="kcal per wet can">
          </div>
          <div class="pb-hint">Standard 3 oz (85 g) cat food can averages 75–95 kcal. Set cans to 0 for dry-only.</div>
        </div>
        <div class="pb-field">
          <label for="cat-dry-cup">Dry Kibble Density (kcal/cup &amp; kcal/kg)</label>
          <div class="pb-input-row">
            <input id="cat-dry-cup" type="number" min="200" max="700" value="400" aria-label="Dry kcal per cup">
            <input id="cat-dry-kg" type="number" min="2500" max="5500" value="3800" aria-label="Dry kcal per kg">
          </div>
        </div>
      </div>

      <div class="pb-card pb-card-accent">
        <div class="pb-kpi-grid">
          <div class="pb-kpi">
            <div class="pb-kpi-label">Daily Calorie Need</div>
            <div class="pb-kpi-val" id="cat-der">262 kcal</div>
            <div class="pb-kpi-sub" id="cat-rer">Base RER: 218 kcal/day</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Wet Food Calories</div>
            <div class="pb-kpi-val" id="cat-wet-out">85 kcal</div>
            <div class="pb-kpi-sub" id="cat-rem-out">177 kcal left for dry kibble</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Dry Kibble (Grams/Day)</div>
            <div class="pb-kpi-val" id="cat-dry-g">47 g</div>
            <div class="pb-kpi-sub">Weigh on digital gram scale</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Dry Kibble (Cups/Day)</div>
            <div class="pb-kpi-val" id="cat-dry-c">0.44 cup</div>
            <div class="pb-kpi-sub">Split into 2–3 small meals</div>
          </div>
        </div>
        <div class="pb-notice" id="cat-warn" style="display:none;"></div>
        <button type="button" id="btn-cat-pdf" class="pb-btn pb-btn-primary" style="margin-top:14px;">📄 Download Printable A4 Cat Feeding Chart (PDF)</button>
      </div>
    </section>

    <section class="pb-section">
      <h2>How Many Calories &amp; Grams of Dry Food Does an Indoor Cat Need?</h2>
      <div class="pb-card pb-table-wrap">
        <table class="pb-table">
          <thead><tr><th>Cat Weight</th><th>Base RER</th><th>Indoor Neutered (1.2×)</th><th>Weight Loss (0.8×)</th><th>Dry Grams After 1 Wet Can (85 kcal)</th></tr></thead>
          <tbody>
            <tr><td><strong>8 lb (3.6 kg)</strong></td><td>184 kcal</td><td>221 kcal/day</td><td>147 kcal/day</td><td>36 g dry kibble</td></tr>
            <tr><td><strong>10 lb (4.5 kg)</strong></td><td>218 kcal</td><td>262 kcal/day</td><td>174 kcal/day</td><td>47 g dry kibble</td></tr>
            <tr><td><strong>12 lb (5.4 kg)</strong></td><td>249 kcal</td><td>299 kcal/day</td><td>199 kcal/day</td><td>56 g dry kibble</td></tr>
            <tr><td><strong>15 lb (6.8 kg)</strong></td><td>295 kcal</td><td>354 kcal/day</td><td>236 kcal/day</td><td>71 g dry kibble</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">{''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}</div>
    </section>
    {related_tools_html(slug)}"""

    js = """
    (function(){
      function run(){
        if(!window.PaceBowlMath) return;
        const r = window.PaceBowlMath.calcCatFeeding({
          weight: document.getElementById('cat-weight').value,
          unit: document.getElementById('cat-unit').value,
          stage: document.getElementById('cat-stage').value,
          wetCansPerDay: document.getElementById('cat-wet-cans').value,
          kcalPerWetCan: document.getElementById('cat-wet-kcal').value,
          dryKcalPerCup: document.getElementById('cat-dry-cup').value,
          dryKcalPerKg: document.getElementById('cat-dry-kg').value,
        });
        document.getElementById('cat-der').textContent = r.der + ' kcal';
        document.getElementById('cat-rer').textContent = 'Base RER: ' + r.rer + ' kcal/day (' + r.factor + 'x)';
        document.getElementById('cat-wet-out').textContent = r.wetKcal + ' kcal';
        document.getElementById('cat-rem-out').textContent = r.remainingDryKcal + ' kcal left for dry kibble';
        document.getElementById('cat-dry-g').textContent = r.dryGramsPerDay + ' g';
        document.getElementById('cat-dry-c').textContent = r.dryCupsPerDay + ' cups';
        const w = document.getElementById('cat-warn');
        if(r.overfedWarning){
          w.style.display='block';
          w.innerHTML='<strong>Heads up:</strong> Wet food alone (' + r.wetKcal + ' kcal) already exceeds your cat\\'s daily target (' + r.der + ' kcal). Reduce wet cans or skip dry kibble.';
        } else { w.style.display='none'; }
        window.__lastCat = r;
      }
      ['cat-weight','cat-unit','cat-stage','cat-wet-cans','cat-wet-kcal','cat-dry-cup','cat-dry-kg'].forEach(id=>{
        document.getElementById(id).addEventListener('input', run);
        document.getElementById(id).addEventListener('change', run);
      });
      document.getElementById('btn-cat-pdf').addEventListener('click', function(){
        const r = window.__lastCat;
        if(!r || !window.PaceBowlPdf) return;
        const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
        window.PaceBowlPdf.downloadFeedingChartPdf({
          title: 'Daily Cat Wet & Dry Feeding Chart (' + r.der + ' kcal/day)',
          filename: 'PaceBowl-Cat-Feeding-Chart.pdf',
          summaryRows: [
            ['Cat Weight & Stage:', r.weightLb + ' lbs (' + r.weightKg + ' kg) | ' + r.stageLabel],
            ['Daily Energy Target:', r.der + ' kcal/day (WSAVA RER ' + r.rer + ' x ' + r.factor + ')'],
            ['Daily Wet Food:', r.wetCansPerDay + ' can(s)/day (' + r.wetKcal + ' kcal)'],
            ['Remaining Dry Kibble:', r.dryGramsPerDay + ' g/day (' + r.dryCupsPerDay + ' cups | ' + r.remainingDryKcal + ' kcal)']
          ],
          tableTitle: 'WEEKLY CAT MEAL TRACKER',
          tableHeaders: ['Day', 'Wet Food', 'Dry Kibble (g)', 'Dry Kibble (cups)', 'Fed'],
          tableRows: days.map(d => [d, r.wetCansPerDay + ' can(s)', r.dryGramsPerDay + ' g', r.dryCupsPerDay + ' c', '']),
          checkboxes: true,
          notes: [
            'Never fast an overweight cat; gradual weight loss (0.5%-1% per week) prevents hepatic lipidosis.',
            'Keep treats under 10% of daily calories (' + Math.round(r.der*0.1) + ' kcal/day).',
            'Use a wide, shallow whisker-friendly bowl or slow-feeder puzzle to curb scarf-and-barf.'
          ]
        });
      });
      window.addEventListener('DOMContentLoaded', run);
      setTimeout(run, 120);
    })();"""
    write_page("tools/cat-calorie-feeding-calculator/index.html", render_shell(slug, title, desc, "cat calorie calculator, how much wet and dry food to feed a cat, mixed feeding cat calculator, kitten calorie calculator", graph, body, js))

# =====================================================================
# 6. PUPPY ADULT WEIGHT PREDICTOR
# =====================================================================
def build_puppy_weight_page():
    slug = "/tools/puppy-adult-weight-calculator/"
    title = "Puppy Adult Weight Calculator — Breed Growth Chart"
    desc = "Free puppy adult weight calculator. Estimate your puppy's adult weight in lbs and kg from 6 to 52 weeks across Toy, Small, Medium, Large, and Giant breeds."
    faqs = [
        ("How do I estimate my puppy's adult weight?", "Toy and small breeds reach 50% of adult weight around 14-16 weeks, medium breeds around 16-18 weeks, and large/giant breeds around 20-24 weeks. Our calculator adjusts the growth curve specifically for your breed size category."),
        ("When do large breed puppies stop growing?", "Large breeds (55-95 lbs, such as Golden Retrievers and Labradors) finish most skeletal growth around 14 to 16 months (60-68 weeks), while giant breeds (95+ lbs) continue filling out until 18 to 24 months."),
        ("Should large-breed puppies eat large-breed puppy food?", "Yes. Large-breed puppy formulas control calcium-to-phosphorus ratios and calorie density so joints grow steadily without orthopedic stress."),
    ]
    graph = [
        ORG_SCHEMA,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Puppy Adult Weight Calculator", "item": f"{SITE}{slug}"},
        ]},
        {"@type": "WebApplication", "name": "PaceBowl Puppy Adult Weight Calculator", "url": f"{SITE}{slug}", "applicationCategory": "HealthApplication", "operatingSystem": "All", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    body = f"""
    <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Puppy Adult Weight Calculator</span></nav>
    <section class="pb-hero">
      <div class="pb-pill">🐶 Toy, Small, Medium, Large &amp; Giant Breed Growth Curves</div>
      <h1>Puppy Adult Weight Calculator &amp; Breed Growth Chart</h1>
      <p>Predict how big your puppy will get in pounds and kilograms, track growth milestones from 12 to 52 weeks, and pick the right adult slow-feeder bowl size.</p>
    </section>

    <section class="pb-calc-grid">
      <div class="pb-card">
        <div class="pb-field">
          <label for="pup-weight">Puppy's Current Weight</label>
          <div class="pb-input-row">
            <input id="pup-weight" type="number" min="0.5" max="150" step="0.5" value="22">
            <select id="pup-unit" style="max-width:100px;"><option value="lb" selected>lbs</option><option value="kg">kg</option></select>
          </div>
        </div>
        <div class="pb-field">
          <label for="pup-weeks">Puppy's Current Age (Weeks)</label>
          <input id="pup-weeks" type="number" min="6" max="72" value="16">
          <div class="pb-hint">Tip: 3 months = 13 wks, 4 months = 17 wks, 6 months = 26 wks.</div>
        </div>
        <div class="pb-field">
          <label for="pup-size">Expected Breed Size Category</label>
          <select id="pup-size">
            <option value="toy">Toy Breed (&lt; 12 lbs — Chihuahua, Yorkie)</option>
            <option value="small">Small Breed (12–25 lbs — Corgi, Frenchie, Dachshund)</option>
            <option value="medium">Medium Breed (25–55 lbs — Aussie, Beagle, Cocker)</option>
            <option value="large" selected>Large Breed (55–95 lbs — Golden, Lab, GSD)</option>
            <option value="giant">Giant Breed (95+ lbs — Great Dane, Bernese, Mastiff)</option>
          </select>
        </div>
      </div>

      <div class="pb-card pb-card-accent">
        <div class="pb-kpi-grid">
          <div class="pb-kpi">
            <div class="pb-kpi-label">Predicted Adult Weight</div>
            <div class="pb-kpi-val" id="pup-adult-lb">62.4 lbs</div>
            <div class="pb-kpi-sub" id="pup-range">Range: 57.4 – 67.4 lbs</div>
          </div>
          <div class="pb-kpi">
            <div class="pb-kpi-label">Growth Completed</div>
            <div class="pb-kpi-val" id="pup-pct">35%</div>
            <div class="pb-kpi-sub" id="pup-adult-kg">~28.3 kg adult weight</div>
          </div>
        </div>
        <div class="pb-table-wrap">
          <table class="pb-table">
            <thead><tr><th>Age Milestone</th><th>% of Adult</th><th>Est. Weight (lbs)</th><th>Est. Weight (kg)</th></tr></thead>
            <tbody id="pup-tbody"></tbody>
          </table>
        </div>
        <div class="pb-notice" id="pup-bowl"></div>
        <button type="button" id="btn-pup-pdf" class="pb-btn pb-btn-primary" style="margin-top:12px;">📄 Download Printable A4 Puppy Growth Chart (PDF)</button>
      </div>
    </section>

    <section class="pb-section">
      <h2>How Big Will My Puppy Get by Breed Size Category?</h2>
      <div class="pb-card pb-table-wrap">
        <table class="pb-table">
          <thead><tr><th>Breed Size</th><th>Adult Weight Range</th><th>50% Adult Weight Reached</th><th>Full Maturity Age</th></tr></thead>
          <tbody>
            <tr><td><strong>Toy Breeds</strong></td><td>4 – 12 lbs (1.8 – 5.4 kg)</td><td>12 – 14 weeks</td><td>8 – 10 months</td></tr>
            <tr><td><strong>Small Breeds</strong></td><td>12 – 25 lbs (5.4 – 11.3 kg)</td><td>14 – 16 weeks</td><td>10 – 12 months</td></tr>
            <tr><td><strong>Medium Breeds</strong></td><td>25 – 55 lbs (11.3 – 25 kg)</td><td>16 – 18 weeks</td><td>12 – 14 months</td></tr>
            <tr><td><strong>Large Breeds</strong></td><td>55 – 95 lbs (25 – 43 kg)</td><td>20 – 22 weeks</td><td>14 – 16 months</td></tr>
            <tr><td><strong>Giant Breeds</strong></td><td>95 – 180+ lbs (43 – 82 kg)</td><td>22 – 26 weeks</td><td>18 – 24 months</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="pb-section">
      <h2>Frequently Asked Questions</h2>
      <div class="pb-card">{''.join(f'<div class="pb-faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)}</div>
    </section>
    {related_tools_html(slug)}"""

    js = """
    (function(){
      function run(){
        if(!window.PaceBowlMath) return;
        const r = window.PaceBowlMath.calcPuppyAdultWeight({
          weight: document.getElementById('pup-weight').value,
          unit: document.getElementById('pup-unit').value,
          ageWeeks: document.getElementById('pup-weeks').value,
          breedSize: document.getElementById('pup-size').value,
        });
        document.getElementById('pup-adult-lb').textContent = r.estAdultLb + ' lbs';
        document.getElementById('pup-range').textContent = 'Range: ' + r.rangeLb;
        document.getElementById('pup-pct').textContent = r.pctGrown + '%';
        document.getElementById('pup-adult-kg').textContent = '~' + r.estAdultKg + ' kg (' + r.rangeKg + ')';
        document.getElementById('pup-bowl').innerHTML = '<strong>Adult Bowl Size:</strong> ' + r.adultBowl;
        document.getElementById('pup-tbody').innerHTML = r.milestones.map(m =>
          '<tr><td><strong>' + m.weeks + ' weeks</strong></td><td>' + m.pctAdult + '%</td><td>' + m.weightLb + ' lbs</td><td>' + m.weightKg + ' kg</td></tr>'
        ).join('');
        window.__lastPup = r;
      }
      ['pup-weight','pup-unit','pup-weeks','pup-size'].forEach(id=>{
        document.getElementById(id).addEventListener('input', run);
        document.getElementById(id).addEventListener('change', run);
      });
      document.getElementById('btn-pup-pdf').addEventListener('click', function(){
        const r = window.__lastPup;
        if(!r || !window.PaceBowlPdf) return;
        window.PaceBowlPdf.downloadFeedingChartPdf({
          title: 'Puppy Adult Weight & Growth Milestone Chart',
          filename: 'PaceBowl-Puppy-Growth-Chart.pdf',
          summaryRows: [
            ['Current Measurement:', r.currentLb + ' lbs (' + r.currentKg + ' kg) at ' + r.ageWeeks + ' weeks old'],
            ['Breed Category:', r.breedLabel],
            ['Predicted Adult Weight:', r.estAdultLb + ' lbs (' + r.estAdultKg + ' kg) | Range: ' + r.rangeLb],
            ['Growth Completed:', r.pctGrown + '% of adult weight | ' + r.adultBowl]
          ],
          tableTitle: 'PROJECTED PUPPY WEIGHT MILESTONES',
          tableHeaders: ['Age Milestone', '% of Adult', 'Est. Weight (lbs)', 'Est. Weight (kg)'],
          tableRows: r.milestones.map(m => [m.weeks + ' weeks', m.pctAdult + '%', m.weightLb + ' lbs', m.weightKg + ' kg'])
        });
      });
      window.addEventListener('DOMContentLoaded', run);
      setTimeout(run, 120);
    })();"""
    write_page("tools/puppy-adult-weight-calculator/index.html", render_shell(slug, title, desc, "puppy weight calculator, how big will my puppy get, puppy growth chart by breed size, adult dog weight predictor", graph, body, js))

# =====================================================================
# 7. SEO / GEO / AEO MACHINE-READABLE INFRASTRUCTURE
# =====================================================================
def build_infra():
    # robots.txt
    robots = f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: SemrushBot
Disallow: /

User-agent: AhrefsBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: PetalBot
Disallow: /

Sitemap: {SITE}/sitemap.xml
"""
    write_page("robots.txt", robots)

    # sitemap.xml
    urls = [
        ("/", "1.0", "weekly"),
        ("/tools/dog-calorie-feeding-calculator/", "0.95", "weekly"),
        ("/tools/barf-raw-dog-food-calculator/", "0.95", "weekly"),
        ("/tools/dog-food-transition-calculator/", "0.95", "weekly"),
        ("/tools/cat-calorie-feeding-calculator/", "0.95", "weekly"),
        ("/tools/puppy-adult-weight-calculator/", "0.90", "weekly"),
    ]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pri, freq in urls:
        sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>\n")
    write_page("sitemap.xml", "\n".join(sm))

    # llms.txt & llms-full.txt
    llms = f"""# PaceBowl Pet Nutrition ({SITE})

> PaceBowl provides free, veterinary-standard dog and cat feeding, BARF/PMR raw diet, 7-day kibble transition, and puppy adult weight calculators based on WSAVA and NRC formulas, with instant printable A4 fridge feeding charts.

## Machine-Readable Resources
- [Agent Skills Index]({SITE}/.well-known/agent-skills/index.json): Structured tool schemas for AI search agents
- [Full LLM Documentation]({SITE}/llms-full.txt): Complete veterinary formulas and reference tables
- [XML Sitemap]({SITE}/sitemap.xml): Canonical index of all PaceBowl pet nutrition calculators
- [Crawler Policy]({SITE}/robots.txt): AI crawler allowlist (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot)
- [Web App Manifest]({SITE}/site.webmanifest): Progressive web app metadata for PaceBowl

## Core Tools & Direct Landing Pages
- [Dog Calorie & Feeding Calculator]({SITE}/tools/dog-calorie-feeding-calculator/): WSAVA RER/DER daily kcal, grams, oz, and cups per meal calculator
- [BARF & PMR Raw Dog Food Calculator]({SITE}/tools/barf-raw-dog-food-calculator/): 70/10/5/5/7/2/1 BARF and 80/10/10 PMR daily grams & 7–30 day freezer batch prep planner
- [7-Day Dog Food Transition Calculator]({SITE}/tools/dog-food-transition-calculator/): Calorie-matched 7/10/14-day old vs. new kibble mixing chart
- [Cat Calorie & Wet/Dry Food Calculator]({SITE}/tools/cat-calorie-feeding-calculator/): Indoor cat mixed wet can + dry kibble gram calculator
- [Puppy Adult Weight Calculator]({SITE}/tools/puppy-adult-weight-calculator/): Breed-size growth curve predictor from 6 to 52 weeks

## Key Differentiators & Veterinary Standards
- **WSAVA RER Formula**: `RER = 70 * (weight_kg ^ 0.75)` with life-stage multipliers from 0.8x (feline weight loss) to 3.0x (young puppies).
- **Gram-Scale Accuracy**: Eliminates the 18%–48% scoop error of measuring cups by converting kcal directly to grams and ounces.
- **Zero-Login Printable A4 PDF**: Generates clean fridge feeding charts with AM/PM meal checkboxes entirely client-side.

## Technical Guides & Veterinary References
- [PaceBowl Pet Nutrition Hub]({SITE}/): Overview of formulas, standard dog calorie table (10 lb to 100 lb), and FAQ
- [WSAVA Global Nutrition Guidelines](https://wsava.org/global-guidelines/global-nutrition-guidelines/): Veterinary clinical standard for Resting Energy Requirement (RER) and Daily Energy Requirement (DER)
- [Wikidata Dog Nutrition Entity](https://www.wikidata.org/wiki/Q144): Canonical entity reference for domestic dogs (`Canis familiaris`)
"""
    write_page("llms.txt", llms)
    write_page("llms-full.txt", llms + "\n## Reference Formulas\n- Dog Neutered Adult DER = 1.6 * 70 * (kg^0.75)\n- Cat Indoor Neutered DER = 1.2 * 70 * (kg^0.75)\n- BARF Daily Grams = kg * 1000 * (body_weight_pct / 100)\n")

    # .well-known/agent-skills/index.json
    skills = {
        "schema_version": "1.0",
        "provider": "PaceBowl Pet Nutrition",
        "domain": SITE,
        "skills": [
            {
                "name": "dog_calorie_feeding_calculator",
                "description": "Compute daily dog kcal (WSAVA RER/DER), grams, oz, and cups per meal across 8 life stages with instant A4 PDF fridge chart export (free, <1s).",
                "path": "/tools/dog-calorie-feeding-calculator/",
                "url": f"{SITE}/tools/dog-calorie-feeding-calculator/",
                "algorithm": "RER = 70 * (weight_kg ^ 0.75); DER = RER * life_stage_factor",
                "input_schema": {"weight": "number", "unit": "lb|kg", "stage": "string", "kcalPerCup": "number", "meals": "number"},
                "output": "Daily kcal, grams/meal, cups/meal, slow-feeder bowl size, printable A4 PDF",
                "turnaround_time": "instant (<1s client-side)",
                "pricing": "Free ($0)",
            },
            {
                "name": "barf_raw_dog_food_calculator",
                "description": "Calculate BARF (70/10/5/5/7/2/1) or PMR (80/10/5/5) daily raw dog food grams, oz, and 7-30 day freezer batch shopping lists (free, <1s).",
                "path": "/tools/barf-raw-dog-food-calculator/",
                "url": f"{SITE}/tools/barf-raw-dog-food-calculator/",
                "algorithm": "daily_grams = weight_kg * 1000 * (body_pct / 100)",
                "input_schema": {"weight": "number", "unit": "lb|kg", "model": "barf|pmr", "bodyPct": "number", "prepDays": "number"},
                "output": "Daily & batch grams/lbs per ingredient + printable A4 prep PDF",
                "turnaround_time": "instant (<1s client-side)",
                "pricing": "Free ($0)",
            },
            {
                "name": "dog_food_transition_calculator",
                "description": "Generate calorie-matched 7-day, 10-day, or 14-day dog food transition mixing charts in grams and cups (free, <1s).",
                "path": "/tools/dog-food-transition-calculator/",
                "url": f"{SITE}/tools/dog-food-transition-calculator/",
                "algorithm": "new_daily_grams = old_daily_grams * (old_kcal_per_cup / new_kcal_per_cup)",
                "input_schema": {"days": "7|10|14", "oldDailyGrams": "number", "oldKcalPerCup": "number", "newKcalPerCup": "number"},
                "output": "Day-by-day old/new grams & cups schedule + printable A4 checklist PDF",
                "turnaround_time": "instant (<1s client-side)",
                "pricing": "Free ($0)",
            },
            {
                "name": "cat_calorie_feeding_calculator",
                "description": "Calculate indoor cat WSAVA RER/DER calories and exact remaining dry kibble grams after subtracting wet food cans (free, <1s).",
                "path": "/tools/cat-calorie-feeding-calculator/",
                "url": f"{SITE}/tools/cat-calorie-feeding-calculator/",
                "algorithm": "remaining_dry_kcal = max(0, DER - wet_cans * kcal_per_can)",
                "input_schema": {"weight": "number", "unit": "lb|kg", "stage": "string", "wetCansPerDay": "number", "kcalPerWetCan": "number"},
                "output": "Daily kcal, wet kcal, remaining dry grams/cups, printable A4 PDF",
                "turnaround_time": "instant (<1s client-side)",
                "pricing": "Free ($0)",
            },
            {
                "name": "puppy_adult_weight_calculator",
                "description": "Predict puppy adult weight range (lbs & kg) and 12-52 week growth milestones by breed size category (free, <1s).",
                "path": "/tools/puppy-adult-weight-calculator/",
                "url": f"{SITE}/tools/puppy-adult-weight-calculator/",
                "algorithm": "est_adult_kg = current_kg / ((age_weeks / mature_weeks) ^ 0.72)",
                "input_schema": {"weight": "number", "unit": "lb|kg", "ageWeeks": "number", "breedSize": "toy|small|medium|large|giant"},
                "output": "Adult weight range, % grown, milestone table, printable A4 PDF",
                "turnaround_time": "instant (<1s client-side)",
                "pricing": "Free ($0)",
            },
        ],
    }
    write_page(".well-known/agent-skills/index.json", json.dumps(skills, indent=2) + "\n")

    # _redirects: cleanly 301 old dev tool URLs so Google de-indexes cleanly without 404s
    redirects = """/tools/cursor-rules-generator/* https://cursor.pacebowl.com/ 301
/tools/comfyui-latent-calculator/* https://pacebowl.com/ 301
/tools/moe-vram-estimator/* https://pacebowl.com/ 301
/tools/deepseek-prompt-studio/* https://pacebowl.com/ 301
/tools/open-geo-attribution/* https://pacebowl.com/ 301
/tools/reddit-growth-studio/* https://pacebowl.com/ 301
"""
    write_page("_redirects", redirects)

if __name__ == "__main__":
    generate_og_image()
    build_homepage()
    build_dog_calorie_page()
    build_barf_raw_page()
    build_transition_page()
    build_cat_calorie_page()
    build_puppy_weight_page()
    build_infra()
    import subprocess, sys
    subprocess.check_call([sys.executable, os.path.join(ROOT, "scripts", "build_eeat_layer.py")])
    print("ALL PACEBOWL PET NUTRITION PAGES & SEO/GEO/AEO/E-E-A-T INFRA BUILT SUCCESSFULLY!")
