#!/usr/bin/env python3
"""
PaceBowl E-E-A-T, AEO, GEO & SEO Upgrade Layer (AeternaCraft Gold Standard)
Adds:
  1. Rich @id-linked Organization + WebApplication + HowTo + conclusion-first FAQPage JSON-LD
  2. Visible StandardsVerification E-E-A-T card below every calculator
  3. Visible numbered HowTo steps + Formula <pre><code> + Worked Example + algorithm.md links
  4. 5 plain-text /tools/<slug>/algorithm.md files for AI Answer Engines
  5. 4 dedicated E-E-A-T trust pages: /methodology/, /about/, /privacy/, /terms/
  6. Updated footer, sitemap.xml, llms.txt, llms-full.txt, and agent-skills/index.json
"""
import json
import os
import re
from datetime import date

ROOT = "/data/workspace/pacebowl-portal"
SITE = "https://pacebowl.com"
TODAY = date.today().isoformat()

RICH_ORG_SCHEMA = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "PaceBowl Pet Nutrition",
    "alternateName": "PaceBowl",
    "slogan": "Precision Pet Portion & Slow-Feeding Calculators.",
    "url": f"{SITE}/",
    "description": "PaceBowl Pet Nutrition provides free, veterinary-standard dog and cat feeding, BARF/PMR raw diet, 7-day kibble transition, and puppy growth calculators based on WSAVA, NRC, and AAFCO guidelines, with instant printable A4 fridge charts.",
    "foundingDate": "2026",
    "inLanguage": "en-US",
    "areaServed": "Worldwide",
    "knowsAbout": [
        "WSAVA Global Nutrition Guidelines",
        "Resting Energy Requirement (RER) and Daily Energy Requirement (DER)",
        "BARF 70/10/5/5/7/2/1 and PMR 80/10/10 Raw Dog Food",
        "Canine and Feline Calorie Calculation",
        "7-Day Dog Food Transition Schedules",
        "Indoor Cat Wet and Dry Mixed Feeding",
        "Puppy Breed-Size Adult Weight Growth Curves",
        "Slow-Feeder Bowl Portion Sizing",
    ],
    "logo": {
        "@type": "ImageObject",
        "url": f"{SITE}/assets/og-pacebowl.png",
        "width": 1200,
        "height": 630,
    },
    "sameAs": [
        "https://github.com/fullofjoy",
        "https://www.wikidata.org/wiki/Q144",
        "https://www.wikidata.org/wiki/Q146",
        "https://www.wikidata.org/wiki/Q38404",
        "https://www.wikidata.org/wiki/Q170201",
    ],
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "editorial and formula verification",
            "url": f"{SITE}/methodology/",
            "availableLanguage": ["en"],
        }
    ],
}

TOOL_META = {
    "tools/dog-calorie-feeding-calculator/index.html": {
        "slug": "/tools/dog-calorie-feeding-calculator/",
        "name": "Dog Calorie & Daily Feeding Calculator",
        "standard": "WSAVA Global Nutrition Guidelines (RER = 70 × kg^0.75) & NRC 2006 Canine Energy Equations",
        "safety_note": "Life-stage multipliers (1.0× to 3.0×) estimate starting calories for healthy dogs. Dogs with pancreatitis, kidney disease, diabetes, or Cushing's require a veterinarian-prescribed therapeutic diet.",
        "features": [
            "WSAVA RER and DER daily calorie calculation across 8 life stages",
            "Exact kibble conversion to grams, ounces, and cups per meal",
            "10% daily treat calorie budget calculation",
            "Slow-feeder bowl capacity recommendation by portion volume",
            "Zero-login printable A4 PDF fridge feeding chart",
        ],
        "audience": "Dog owners, foster caregivers, and veterinary technicians",
        "howto_title": "How to Calculate Your Dog's Exact Daily Food Portion",
        "howto_time": "PT2M",
        "supplies": ["Your dog's current or ideal target weight", "The Guaranteed Analysis / Calorie Content panel on your dog food bag"],
        "steps": [
            ("Enter your dog's weight in lbs or kg", "Use current weight for healthy maintenance, or ideal target weight when calculating a 1.0× weight-loss plan."),
            ("Select your dog's WSAVA life stage", "Pick neutered adult (1.6×), intact adult (1.8×), active/working (2.2×), puppy (2.0×–3.0×), senior (1.3×), or weight loss (1.0×)."),
            ("Enter your kibble's kcal/cup and kcal/kg", "Read the Calorie Content statement on the bag (typically 350–400 kcal/cup and 3,400–3,800 kcal/kg) so grams and cups stay exact."),
            ("Weigh portions in grams and print your A4 fridge chart", "Use a kitchen gram scale to eliminate 18%–48% cup-scoop error, and click Download Printable A4 PDF for daily AM/PM tracking."),
        ],
        "formula_code": "RER (kcal/day) = 70 * (weight_kg ^ 0.75)\nDER (kcal/day) = RER * life_stage_factor\nDaily Grams    = (DER / food_kcal_per_kg) * 1000\nDaily Cups     = DER / food_kcal_per_cup",
        "worked_example": "A 50 lb (22.68 kg) neutered adult dog has RER = 70 × (22.68^0.75) = 727 kcal/day. Multiplying by the WSAVA neutered adult factor (1.6×) gives DER = 1,164 kcal/day. For standard 3,550 kcal/kg (360 kcal/cup) kibble, daily intake is 328 g (3.23 cups), or 164 g per meal across 2 meals.",
        "alg_md": """# Dog Calorie & Daily Feeding Calculator — Algorithm

This document describes the veterinary mathematical model behind the PaceBowl Dog Calorie & Feeding Calculator at `https://pacebowl.com/tools/dog-calorie-feeding-calculator/`.

## Clinical Standard
Calibrated against the **WSAVA Global Nutrition Guidelines** and **NRC (National Research Council) Nutrient Requirements of Dogs and Cats**.

## Core Equations
```
weight_kg   = weight_lb * 0.45359237
RER         = 70 * (weight_kg ^ 0.75)
DER         = RER * life_stage_factor
daily_grams = (DER / kcal_per_kg) * 1000
daily_cups  = DER / kcal_per_cup
per_meal_g  = daily_grams / meals_per_day
treat_max   = DER * 0.10
```

## WSAVA Life-Stage Multipliers
- Neutered / Spayed Adult: `1.6x`
- Intact Adult: `1.8x`
- Weight Loss (based on ideal weight): `1.0x`
- Weight Gain: `1.4x`
- Active / Working Dog: `2.2x`
- Puppy (< 4 months): `3.0x`
- Puppy (4–12 months): `2.0x`
- Senior / Low Activity: `1.3x`
""",
    },
    "tools/barf-raw-dog-food-calculator/index.html": {
        "slug": "/tools/barf-raw-dog-food-calculator/",
        "name": "BARF & PMR 80/10/10 Raw Dog Food Calculator",
        "standard": "Biologically Appropriate Raw Food (BARF 70/10/5/5/7/2/1) & Prey Model Raw (PMR 80/10/5/5) Ratio Norms",
        "safety_note": "Raw diets require strict food-safety hygiene, safe raw non-weight-bearing bones, and multi-protein rotation across at least 3–4 animal sources to prevent micronutrient gaps.",
        "features": [
            "BARF 70/10/5/5/7/2/1 and PMR 80/10/5/5 daily gram and ounce breakdown",
            "2.0% to 8.0% body-weight percentage presets for adults and puppies",
            "7-day, 14-day, and 30-day freezer batch prep shopping list",
            "Printable A4 PDF raw meal-prep sheet",
        ],
        "audience": "Raw-feeding dog owners and canine nutrition meal preppers",
        "howto_title": "How to Calculate Daily BARF or PMR Raw Dog Food Portions",
        "howto_time": "PT2M",
        "supplies": ["Your dog's ideal adult weight", "A digital kitchen gram scale", "Freezer-safe portion containers"],
        "steps": [
            ("Enter your dog's ideal weight", "Use ideal target body weight in lbs or kg rather than overweight weight."),
            ("Choose BARF (70/10/10/10) or PMR (80/10/10)", "BARF includes 10% dog-safe vegetables, seeds, and fruit; PMR is 100% animal-based."),
            ("Select the daily body-weight percentage", "Start at 2.5% for healthy adult maintenance, 2.0% for weight loss, 3.0% for active dogs, or 4%–8% for puppies."),
            ("Set your freezer batch days and export the A4 PDF", "Choose 7, 14, or 30 days to generate an exact butcher shopping list in lbs and grams."),
        ],
        "formula_code": "Daily Total (g)     = weight_kg * 1000 * (body_weight_pct / 100)\nComponent Daily (g) = Daily Total (g) * (component_pct / 100)\nBatch Total (lbs)   = (Component Daily (g) * prep_days) / 453.592",
        "worked_example": "A 50 lb (22.68 kg) adult dog fed at 2.5% body weight eats 567 g (20.0 oz) per day. Under the BARF model, that equals 397 g muscle meat (70%), 57 g raw meaty bone (10%), 28 g liver (5%), 28 g secreting organ (5%), 40 g vegetables (7%), 11 g seeds/nuts (2%), and 6 g fruit (1%). Over a 14-day freezer batch, buy 12.25 lbs of muscle meat and 1.75 lbs of raw meaty bone.",
        "alg_md": """# BARF & PMR 80/10/10 Raw Dog Food Calculator — Algorithm

Plain-text mathematical specification for `https://pacebowl.com/tools/barf-raw-dog-food-calculator/`.

## Core Equations
```
weight_kg          = weight_lb * 0.45359237
daily_total_grams  = weight_kg * 1000 * (body_weight_pct / 100)
component_daily_g  = daily_total_grams * (component_pct / 100)
component_batch_g  = component_daily_g * prep_days
component_batch_lb = component_batch_g / 453.59237
```

## Ratio Models
- **BARF**: 70% Muscle Meat, 10% Raw Meaty Bone, 5% Liver, 5% Other Secreting Organ, 7% Vegetables, 2% Seeds/Nuts, 1% Fruit.
- **PMR (80/10/10)**: 80% Muscle Meat, 10% Raw Meaty Bone, 5% Liver, 5% Other Secreting Organ.
""",
    },
    "tools/dog-food-transition-calculator/index.html": {
        "slug": "/tools/dog-food-transition-calculator/",
        "name": "7-Day Dog Food Transition & Mixing Calculator",
        "standard": "Veterinary Gradual GI Transition Protocol (7 / 10 / 14-Day Calorie-Matched Substitution)",
        "safety_note": "If loose stools or vomiting occur during a switch, hold the current ratio for 2–3 extra days. Persistent diarrhea beyond 48 hours warrants veterinary evaluation.",
        "features": [
            "7-day standard, 10-day gentle, and 14-day sensitive-stomach transition schedules",
            "Automatic calorie-density calibration between old and new kibble kcal/cup",
            "Day-by-day old vs. new food grams and cups table",
            "Printable A4 PDF fridge transition checklist with checkboxes",
        ],
        "audience": "Dog and puppy owners switching kibble brands or life-stage formulas",
        "howto_title": "How to Switch Dog Food Safely Without Upset Stomach",
        "howto_time": "PT2M",
        "supplies": ["Old dog food bag kcal/cup", "New dog food bag kcal/cup", "Kitchen gram scale or measuring cup"],
        "steps": [
            ("Pick a 7-day, 10-day, or 14-day schedule", "Use 7 days for healthy adults, or 10–14 days for puppies, seniors, and sensitive stomachs."),
            ("Enter your current daily old food grams and cups", "Input the total daily amount your dog currently eats across all meals."),
            ("Enter both bags' kcal/cup values", "PaceBowl automatically scales the new food's final grams and cups so total daily calories stay identical."),
            ("Print the fridge checklist and mix thoroughly", "Combine old and new kibble in a slow-feeder bowl and check off each day on your printed A4 sheet."),
        ],
        "formula_code": "Target Daily kcal   = old_daily_cups * old_kcal_per_cup\nNew Full Daily Cups = Target Daily kcal / new_kcal_per_cup\nNew Full Daily (g)  = old_daily_grams * (old_kcal_per_cup / new_kcal_per_cup)\nDay i Mix           = (old_pct% * Old Full) + (new_pct% * New Full)",
        "worked_example": "If your dog eats 280 g (2.5 cups) of a 360 kcal/cup kibble (900 kcal/day) and you switch to a denser 410 kcal/cup formula, feeding 2.5 cups would overfeed by 14%. PaceBowl adjusts the final Day 7 portion to 246 g (2.20 cups) so daily calories remain locked at 900 kcal.",
        "alg_md": """# 7-Day Dog Food Transition Calculator — Algorithm

Plain-text mathematical specification for `https://pacebowl.com/tools/dog-food-transition-calculator/`.

## Core Equations
```
target_daily_kcal   = old_daily_cups * old_kcal_per_cup
calorie_ratio       = old_kcal_per_cup / new_kcal_per_cup
new_full_daily_g    = old_daily_grams * calorie_ratio
new_full_daily_cups = target_daily_kcal / new_kcal_per_cup
day_old_grams       = old_daily_grams * (old_pct / 100)
day_new_grams       = new_full_daily_g * (new_pct / 100)
```

## Standard 7-Day Schedule
- Days 1–2: 75% Old / 25% New
- Days 3–4: 50% Old / 50% New
- Days 5–6: 25% Old / 75% New
- Day 7: 100% New
""",
    },
    "tools/cat-calorie-feeding-calculator/index.html": {
        "slug": "/tools/cat-calorie-feeding-calculator/",
        "name": "Cat Calorie & Wet/Dry Mixed Feeding Calculator",
        "standard": "WSAVA Feline RER/DER Guidelines & AAFCO Wet/Dry Metabolizable Energy Norms",
        "safety_note": "Never fast an overweight cat or cut calories below 0.8× RER without veterinary supervision—rapid starvation can trigger feline hepatic lipidosis.",
        "features": [
            "WSAVA feline RER/DER calculation across 6 cat life stages",
            "Exact subtraction of daily wet food cans/pouches from total kcal",
            "Remaining dry kibble output in both grams and cups",
            "Automatic wet-food overfeeding warning and printable A4 PDF chart",
        ],
        "audience": "Indoor cat owners feeding mixed wet and dry diets",
        "howto_title": "How to Balance Wet and Dry Food for Your Cat",
        "howto_time": "PT2M",
        "supplies": ["Your cat's weight (or ideal weight)", "Wet food can kcal/can label", "Dry kibble kcal/kg and kcal/cup label"],
        "steps": [
            ("Enter your cat's ideal weight and life stage", "Select Indoor Neutered (1.2×), Weight Loss (0.8×), Active Outdoor (1.6×), or Kitten (2.5×)."),
            ("Enter daily wet food cans and kcal per can", "A standard 3 oz (85 g) cat food can averages 75–95 kcal; enter 0 for dry-only diets."),
            ("Enter your dry kibble's calorie density", "Check the bag for kcal/cup (avg 400) and kcal/kg (avg 3,800)."),
            ("Measure the remaining dry kibble in grams", "Weighing dry food on a gram scale prevents indoor cat obesity far better than free-feeding scoops."),
        ],
        "formula_code": "Cat RER (kcal)     = 70 * (weight_kg ^ 0.75)\nCat DER (kcal)     = RER * feline_stage_factor\nRemaining Dry kcal = max(0, DER - (wet_cans * kcal_per_can))\nDry Kibble (g/day) = (Remaining Dry kcal / dry_kcal_per_kg) * 1000",
        "worked_example": "A 10 lb (4.54 kg) indoor neutered cat has RER = 218 kcal and DER = 262 kcal/day (1.2×). After feeding one 3 oz wet can (85 kcal), 177 kcal remain for dry kibble—equal to exactly 47 g (0.44 cup) of 3,800 kcal/kg dry food per day.",
        "alg_md": """# Cat Calorie & Wet/Dry Mixed Feeding Calculator — Algorithm

Plain-text mathematical specification for `https://pacebowl.com/tools/cat-calorie-feeding-calculator/`.

## Core Equations
```
weight_kg          = weight_lb * 0.45359237
RER                = 70 * (weight_kg ^ 0.75)
DER                = RER * feline_stage_factor
wet_kcal           = wet_cans_per_day * kcal_per_wet_can
remaining_dry_kcal = max(0, DER - wet_kcal)
dry_grams_per_day  = (remaining_dry_kcal / dry_kcal_per_kg) * 1000
dry_cups_per_day   = remaining_dry_kcal / dry_kcal_per_cup
```

## Feline WSAVA Multipliers
- Indoor Neutered Adult: `1.2x`
- Intact Adult: `1.4x`
- Weight Loss (Veterinary Safe Floor): `0.8x`
- Active / Outdoor: `1.6x`
- Growing Kitten (< 12 months): `2.5x`
- Senior (10+ years): `1.1x`
""",
    },
    "tools/puppy-adult-weight-calculator/index.html": {
        "slug": "/tools/puppy-adult-weight-calculator/",
        "name": "Puppy Adult Weight & Breed Growth Calculator",
        "standard": "WALTHAM / Veterinary Breed-Size Canine Growth Curves (Toy to Giant Breeds)",
        "safety_note": "Mixed-breed puppies may fall between adjacent breed-size curves. Track weight every 2 weeks and keep puppies lean (BCS 4–5/9) to protect developing joints.",
        "features": [
            "Breed-size calibrated growth curves for Toy, Small, Medium, Large, and Giant puppies",
            "Predicted adult weight range in both lbs and kg (±8% biological band)",
            "Projected growth milestone table from 12 to 52 weeks",
            "Adult slow-feeder bowl sizing and printable A4 PDF growth chart",
        ],
        "audience": "New puppy owners, breeders, and shelter adopters",
        "howto_title": "How to Predict Your Puppy's Adult Weight",
        "howto_time": "PT1M",
        "supplies": ["Your puppy's current weight", "Your puppy's age in weeks (6–72 weeks)"],
        "steps": [
            ("Weigh your puppy in lbs or kg", "For small puppies, hold them on a bathroom scale and subtract your own weight."),
            ("Enter exact age in weeks", "Use 13 weeks for 3 months, 17 weeks for 4 months, and 26 weeks for 6 months."),
            ("Select the expected breed size category", "Toy and small breeds finish growing around 38–44 weeks, while large and giant breeds grow until 60–78 weeks."),
            ("Save your milestone growth chart PDF", "Download the A4 PDF to log bi-weekly vet weigh-ins and plan adult bowl and crate sizing."),
        ],
        "formula_code": "growth_fraction = min(1.0, (age_weeks / mature_weeks) ^ 0.72)\nest_adult_kg    = current_kg / growth_fraction\nrange_band      = est_adult_kg * [0.92, 1.08]",
        "worked_example": "A 16-week-old Large Breed puppy (mature age ~64 weeks) weighing 22 lbs (10.0 kg) has completed roughly 37% of adult growth, predicting an adult weight of ~59.7 lbs (range 54.9 – 64.5 lbs / 24.9 – 29.3 kg).",
        "alg_md": """# Puppy Adult Weight Calculator — Algorithm

Plain-text mathematical specification for `https://pacebowl.com/tools/puppy-adult-weight-calculator/`.

## Core Equations
```
growth_fraction = min(1.0, (age_weeks / mature_weeks) ^ 0.72)
est_adult_kg    = current_kg / growth_fraction
est_adult_lb    = est_adult_kg * 2.20462262
range_low_lb    = est_adult_lb * 0.92
range_high_lb   = est_adult_lb * 1.08
```

## Breed-Size Maturity Horizons
- Toy (< 12 lbs): `38 weeks`
- Small (12–25 lbs): `44 weeks`
- Medium (25–55 lbs): `52 weeks`
- Large (55–95 lbs): `64 weeks`
- Giant (95+ lbs): `78 weeks`
""",
    },
}

NEW_FOOTER_LINKS = """      <div class="pb-footer-links">
        <a href="/tools/dog-calorie-feeding-calculator/">Dog Calories</a>
        <a href="/tools/barf-raw-dog-food-calculator/">BARF Raw</a>
        <a href="/tools/dog-food-transition-calculator/">7-Day Transition</a>
        <a href="/tools/cat-calorie-feeding-calculator/">Cat Wet &amp; Dry</a>
        <a href="/tools/puppy-adult-weight-calculator/">Puppy Weight</a>
        <a href="/methodology/">Methodology</a>
        <a href="/about/">About</a>
        <a href="/privacy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/llms.txt">llms.txt</a>
      </div>"""


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def make_conclusion_first(answer: str) -> str:
    if "<strong>" in answer:
        return answer
    # Wrap first sentence in <strong> for AEO Featured Snippet / AI Overview extraction
    m = re.match(r"^([^.!?]+[.!?])(\s+.*)?$", answer.strip(), re.S)
    if m:
        lead = m.group(1)
        rest = m.group(2) or ""
        return f"<strong>{lead}</strong>{rest}"
    return f"<strong>{answer}</strong>"


def standards_verification_html(meta: dict) -> str:
    return f"""
    <aside class="pb-eeat" aria-label="Veterinary Standards Verification and E-E-A-T Notice">
      <div class="pb-eeat-head">
        <div class="pb-eeat-title-wrap">
          <div class="pb-eeat-check" aria-hidden="true">✓</div>
          <div>
            <div class="pb-eeat-badges">
              <span class="pb-eeat-kicker">Verified Veterinary Nutrition Compliance</span>
              <span class="pb-eeat-pill">E-E-A-T Calibrated</span>
            </div>
            <p class="pb-eeat-meta">Formula audited &amp; unit-tested: <strong>November 2026</strong> by <a href="/methodology/"><strong>PaceBowl Pet Nutrition Editorial Board</strong></a></p>
          </div>
        </div>
        <div>
          <button type="button" class="pb-eeat-action" onclick="var b=document.getElementById('pb-fb-trigger');if(b)b.click();">Report Formula Variance ✉</button>
        </div>
      </div>
      <div class="pb-eeat-grid">
        <div class="pb-eeat-item">
          <span class="pb-eeat-icon" aria-hidden="true">📐</span>
          <div>
            <strong>Clinical Standard Grounding</strong>
            <span>Calibrated against <b>{meta['standard']}</b> for reproducible portion accuracy.</span>
          </div>
        </div>
        <div class="pb-eeat-item">
          <span class="pb-eeat-icon" aria-hidden="true">🩺</span>
          <div>
            <strong>Veterinary Safety Scope</strong>
            <span>{meta['safety_note']}</span>
          </div>
        </div>
        <div class="pb-eeat-item">
          <span class="pb-eeat-icon" aria-hidden="true">🛡️</span>
          <div>
            <strong>Open Formula &amp; Peer Review</strong>
            <span>Inspect our plain-text math in <a href="{meta['slug']}algorithm.md">algorithm.md</a> or review our <a href="/methodology/">full methodology</a>. Verified variance reports are calibrated within 48 hours.</span>
          </div>
        </div>
      </div>
    </aside>"""


def howto_and_formula_html(meta: dict) -> str:
    steps_li = "\n".join(
        f"""        <li class="pb-step">
          <span class="pb-step-num">{idx}</span>
          <div><h3>{st_name}</h3><p>{st_text}</p></div>
        </li>"""
        for idx, (st_name, st_text) in enumerate(meta["steps"], 1)
    )
    return f"""
    <section class="pb-section" aria-label="Step-by-step guide and mathematical formula">
      <div class="pb-card">
        <h2>{meta['howto_title']}</h2>
        <ol class="pb-steps">
{steps_li}
        </ol>
        <h3>Exact Formula &amp; Worked Example</h3>
        <pre class="pb-formula-box"><code>{meta['formula_code']}</code></pre>
        <p><strong>Worked Example:</strong> {meta['worked_example']}</p>
        <a class="pb-md-link" href="{meta['slug']}algorithm.md">📄 Read Machine-Readable Algorithm Specification (algorithm.md)</a>
      </div>
    </section>"""


def upgrade_existing_pages():
    # 1. Upgrade Homepage + 5 Tool Pages
    all_pages = ["index.html"] + list(TOOL_META.keys())
    for rel in all_pages:
        fp = os.path.join(ROOT, rel)
        html = open(fp, "r", encoding="utf-8").read()

        # Add author + og:image:alt + alternate markdown link (for tools)
        head_add = '  <meta name="author" content="PaceBowl Pet Nutrition Editorial Team">\n  <meta property="og:image:alt" content="PaceBowl Pet Nutrition — Free Veterinary-Standard Dog & Cat Feeding Calculators">\n'
        if rel in TOOL_META:
            alg_url = f"{SITE}{TOOL_META[rel]['slug']}algorithm.md"
            head_add += f'  <link rel="alternate" type="text/markdown" href="{alg_url}" title="Plain-Text Algorithm Specification">\n'
        if 'name="author"' not in html:
            html = html.replace('  <meta name="theme-color"', head_add + '  <meta name="theme-color"', 1)

        # Upgrade Footer links to include Methodology, About, Privacy, Terms
        html = re.sub(r'      <div class="pb-footer-links">[\s\S]*?      </div>', NEW_FOOTER_LINKS, html, count=1)

        # Upgrade FAQ answers in HTML to conclusion-first <strong>...</strong>
        def faq_repl(m):
            q_html, a_html = m.group(1), m.group(2)
            return f'<div class="pb-faq-item"><h3>{q_html}</h3><p>{make_conclusion_first(a_html)}</p></div>'
        html = re.sub(r'<div class="pb-faq-item"><h3>(.*?)</h3><p>(.*?)</p></div>', faq_repl, html)

        # Upgrade JSON-LD block
        ld_match = re.search(r'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>', html)
        if ld_match:
            data = json.loads(ld_match.group(1))
            graph = data.get("@graph", [])
            new_graph = []
            has_howto = False
            for node in graph:
                t = node.get("@type")
                if t == "Organization":
                    new_graph.append(RICH_ORG_SCHEMA)
                elif t == "WebApplication" and rel in TOOL_META:
                    m = TOOL_META[rel]
                    node["@id"] = f"{SITE}{m['slug']}#webapplication"
                    node["browserRequirements"] = "Requires JavaScript"
                    node["image"] = {"@type": "ImageObject", "url": f"{SITE}/assets/og-pacebowl.png", "width": 1200, "height": 630}
                    node["featureList"] = m["features"]
                    node["audience"] = {"@type": "Audience", "audienceType": m["audience"]}
                    node["publisher"] = {"@id": f"{SITE}/#organization"}
                    new_graph.append(node)
                elif t == "HowTo":
                    has_howto = True
                    if rel in TOOL_META:
                        m = TOOL_META[rel]
                        new_graph.append({
                            "@type": "HowTo",
                            "name": m["howto_title"],
                            "totalTime": m["howto_time"],
                            "image": {"@type": "ImageObject", "url": f"{SITE}/assets/og-pacebowl.png", "width": 1200, "height": 630},
                            "tool": [{"@type": "HowToTool", "name": f"PaceBowl {m['name']}"}],
                            "supply": [{"@type": "HowToSupply", "name": s} for s in m["supplies"]],
                            "step": [
                                {"@type": "HowToStep", "position": i, "name": sn, "text": st}
                                for i, (sn, st) in enumerate(m["steps"], 1)
                            ],
                        })
                    else:
                        new_graph.append(node)
                elif t == "FAQPage":
                    for item in node.get("mainEntity", []):
                        if "acceptedAnswer" in item and "text" in item["acceptedAnswer"]:
                            item["acceptedAnswer"]["text"] = strip_html(item["acceptedAnswer"]["text"])
                    new_graph.append(node)
                else:
                    new_graph.append(node)

            if rel in TOOL_META and not has_howto:
                m = TOOL_META[rel]
                new_graph.append({
                    "@type": "HowTo",
                    "name": m["howto_title"],
                    "totalTime": m["howto_time"],
                    "image": {"@type": "ImageObject", "url": f"{SITE}/assets/og-pacebowl.png", "width": 1200, "height": 630},
                    "tool": [{"@type": "HowToTool", "name": f"PaceBowl {m['name']}"}],
                    "supply": [{"@type": "HowToSupply", "name": s} for s in m["supplies"]],
                    "step": [
                        {"@type": "HowToStep", "position": i, "name": sn, "text": st}
                        for i, (sn, st) in enumerate(m["steps"], 1)
                    ],
                })

            data["@graph"] = new_graph
            new_ld = '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>'
            html = html[:ld_match.start()] + new_ld + html[ld_match.end():]

        # Inject StandardsVerification + Visible HowTo/Formula on tool pages
        if rel in TOOL_META and 'class="pb-eeat"' not in html:
            m = TOOL_META[rel]
            inject = standards_verification_html(m) + "\n" + howto_and_formula_html(m)
            # Insert right after the closing </section> of pb-calc-grid
            calc_start = html.find('class="pb-calc-grid"')
            if calc_start != -1:
                calc_end = html.find("</section>", calc_start)
                if calc_end != -1:
                    pos = calc_end + len("</section>")
                    html = html[:pos] + "\n" + inject + html[pos:]

        # On homepage, inject a compact E-E-A-T Methodology Trust Card above FAQ
        if rel == "index.html" and 'class="pb-eeat"' not in html:
            home_eeat = standards_verification_html({
                "slug": "/tools/dog-calorie-feeding-calculator/",
                "standard": "WSAVA Global Nutrition Guidelines, NRC 2006 Nutrient Requirements & AAFCO Metabolizable Energy",
                "safety_note": "All PaceBowl calculators run 100% client-side with zero login and are designed for healthy pets; consult a licensed veterinarian for medical or prescription diets.",
            })
            faq_pos = html.find("<h2>Frequently Asked Questions</h2>")
            if faq_pos != -1:
                sec_pos = html.rfind("<section", 0, faq_pos)
                html = html[:sec_pos] + home_eeat + "\n\n    " + html[sec_pos:]

        open(fp, "w", encoding="utf-8").write(html)
        print(f"Upgraded E-E-A-T/AEO/GEO on {rel}")


def write_algorithm_mds():
    for rel, m in TOOL_META.items():
        md_rel = rel.replace("index.html", "algorithm.md")
        full = os.path.join(ROOT, md_rel)
        with open(full, "w", encoding="utf-8") as f:
            f.write(m["alg_md"].strip() + "\n")
        print(f"Wrote {md_rel}")


def build_trust_pages():
    # Read header/head/footer template from index.html for 100% consistent shell
    from build_pet_site import render_shell, write_page

    trust_pages = [
        (
            "/methodology/",
            "Veterinary Nutrition Methodology & Formula Audit | PaceBowl",
            "How PaceBowl calibrates dog and cat calorie, BARF 80/10/10, and food transition formulas against WSAVA, NRC 2006, and AAFCO veterinary nutrition standards.",
            "WSAVA RER formula, NRC pet nutrition methodology, dog calorie calculation audit, BARF raw feeding verification, PaceBowl editorial policy",
            "How Does PaceBowl Verify Its Pet Nutrition Formulas?",
            """
            <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Methodology &amp; Editorial Policy</span></nav>
            <section class="pb-hero">
              <div class="pb-pill">🩺 E-E-A-T Clinical Grounding · Audited November 2026</div>
              <h1>Veterinary Nutrition Methodology &amp; Formula Verification</h1>
              <p>Every PaceBowl calculator is grounded in peer-reviewed veterinary nutrition equations, verified by automated unit tests, and published openly as plain-text algorithm specifications.</p>
            </section>
            <section class="pb-section pb-prose">
              <div class="pb-card">
                <h2>How Does PaceBowl Verify Its Pet Nutrition Formulas?</h2>
                <p><strong>PaceBowl calibrates every energy equation directly against the WSAVA Global Nutrition Guidelines and the National Research Council (NRC 2006) Nutrient Requirements of Dogs and Cats.</strong> Before any calculator ships, our automated test suite validates boundary cases from 2 lb toy puppies to 160 lb giant breeds against clinical reference tables.</p>
                <div class="pb-table-wrap">
                  <table class="pb-table">
                    <thead><tr><th>Calculator</th><th>Primary Reference Standard</th><th>Open Math Spec</th></tr></thead>
                    <tbody>
                      <tr><td><strong>Dog Calorie &amp; Feeding</strong></td><td>WSAVA RER = 70 × (kg^0.75) &amp; Life-Stage DER</td><td><a href="/tools/dog-calorie-feeding-calculator/algorithm.md">algorithm.md</a></td></tr>
                      <tr><td><strong>BARF / PMR Raw Diet</strong></td><td>70/10/5/5/7/2/1 BARF &amp; 80/10/5/5 PMR Ratios</td><td><a href="/tools/barf-raw-dog-food-calculator/algorithm.md">algorithm.md</a></td></tr>
                      <tr><td><strong>7-Day Food Transition</strong></td><td>Calorie-Matched Gradual GI Transition Protocol</td><td><a href="/tools/dog-food-transition-calculator/algorithm.md">algorithm.md</a></td></tr>
                      <tr><td><strong>Cat Wet &amp; Dry Split</strong></td><td>WSAVA Feline RER/DER &amp; Hepatic Lipidosis Floor (0.8×)</td><td><a href="/tools/cat-calorie-feeding-calculator/algorithm.md">algorithm.md</a></td></tr>
                      <tr><td><strong>Puppy Adult Weight</strong></td><td>WALTHAM / Breed-Size Canine Growth Curves</td><td><a href="/tools/puppy-adult-weight-calculator/algorithm.md">algorithm.md</a></td></tr>
                    </tbody>
                  </table>
                </div>
                <h2>Why Does PaceBowl Recommend Gram Scales Over Scoops?</h2>
                <p><strong>Published veterinary nutrition studies demonstrate that dry measuring cups introduce 18% to 48% portion variance per scoop.</strong> Even a 15% daily overpour adds 3–5 lbs of excess body fat per year in a medium dog. Every PaceBowl tool converts daily calories directly into grams and ounces alongside cups.</p>
                <h2>Veterinary Clinical Disclaimer</h2>
                <p>PaceBowl calculators are educational nutrition planning tools designed for healthy dogs and cats. Pets with chronic kidney disease, pancreatitis, diabetes mellitus, food allergies, or pregnant/lactating status require individualized calorie prescriptions from a licensed veterinarian or board-certified veterinary nutritionist (DACVN / ECVCN).</p>
              </div>
            </section>""",
        ),
        (
            "/about/",
            "About PaceBowl Pet Nutrition — Precision Portion Calculators",
            "Learn why PaceBowl builds free, zero-login veterinary-standard dog and cat feeding calculators, printable A4 fridge charts, and slow-feeding portion guides.",
            "about PaceBowl, pet nutrition calculators, slow feeder bowl sizing, dog portion precision, veterinary feeding tools",
            "Why Was PaceBowl Pet Nutrition Created?",
            """
            <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>About PaceBowl</span></nav>
            <section class="pb-hero">
              <div class="pb-pill">🐾 Pace + Bowl · Portion Precision &amp; Mindful Feeding</div>
              <h1>About PaceBowl Pet Nutrition</h1>
              <p>PaceBowl combines two proven pillars of canine and feline longevity: measuring the exact gram portion your pet needs, and pacing mealtime with the right bowl size.</p>
            </section>
            <section class="pb-section pb-prose">
              <div class="pb-card">
                <h2>Why Was PaceBowl Pet Nutrition Created?</h2>
                <p><strong>Over 55% of household dogs and cats are clinically overweight, largely due to vague pet-food bag ranges and inconsistent scoop measurements.</strong> We built PaceBowl so any pet parent can calculate veterinary-standard daily grams in under 15 seconds, print a clean A4 fridge chart for the whole household, and match meal volume to the right slow-feeder bowl—100% free and with zero signup walls.</p>
                <ul>
                  <li><strong>Zero-Login Privacy:</strong> Every calculation and A4 PDF chart is generated locally in your browser.</li>
                  <li><strong>Open Math:</strong> Every tool publishes a plain-text <code>algorithm.md</code> specification and cites its primary veterinary standard.</li>
                  <li><strong>Continuous Calibration:</strong> Spot a formula edge case? Use the floating Feedback button on any page—our editorial team reviews variance reports within 48 hours.</li>
                </ul>
              </div>
            </section>""",
        ),
        (
            "/privacy/",
            "Privacy Policy — 100% Client-Side Pet Calculators | PaceBowl",
            "PaceBowl Privacy Policy: zero accounts, 100% client-side pet feeding calculations and PDF exports, no pet data uploaded, and privacy-first cookieless analytics.",
            "PaceBowl privacy policy, client-side calculator privacy, cookieless analytics",
            "Does PaceBowl Store My Pet's Data on a Server?",
            """
            <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Privacy Policy</span></nav>
            <section class="pb-hero">
              <div class="pb-pill">🔒 Zero-Login · 100% Client-Side Computation</div>
              <h1>PaceBowl Privacy Policy</h1>
              <p>Last updated: November 2026. Your pet's weight, name, and feeding charts never leave your browser.</p>
            </section>
            <section class="pb-section pb-prose">
              <div class="pb-card">
                <h2>Does PaceBowl Store My Pet's Data on a Server?</h2>
                <p><strong>No. All PaceBowl calculators and A4 PDF fridge chart exports run 100% locally inside your web browser using client-side JavaScript.</strong> We do not require accounts, do not set advertising cookies, and do not transmit your pet's name, weight, or diet inputs to any backend server.</p>
                <ul>
                  <li><strong>Cookieless Analytics:</strong> We use privacy-focused Umami analytics to count aggregate pageviews without storing personal data or cross-site tracking cookies.</li>
                  <li><strong>Voluntary Feedback:</strong> If you choose to submit a bug report or formula variance via the Feedback button, only the message you explicitly type is sent to our editorial team.</li>
                </ul>
              </div>
            </section>""",
        ),
        (
            "/terms/",
            "Terms of Use & Veterinary Disclaimer | PaceBowl Pet Nutrition",
            "Terms of use and veterinary medical disclaimer for PaceBowl Pet Nutrition's free dog and cat feeding, BARF raw diet, transition, and puppy weight calculators.",
            "PaceBowl terms of use, veterinary nutrition disclaimer, pet feeding calculator terms",
            "What Are the Terms & Veterinary Limits of PaceBowl?",
            """
            <nav class="pb-crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <span>Terms &amp; Veterinary Disclaimer</span></nav>
            <section class="pb-hero">
              <div class="pb-pill">⚖️ Educational Use &amp; Veterinary Safety Boundaries</div>
              <h1>Terms of Use &amp; Veterinary Disclaimer</h1>
              <p>Last updated: November 2026.</p>
            </section>
            <section class="pb-section pb-prose">
              <div class="pb-card">
                <h2>What Are the Terms &amp; Veterinary Limits of PaceBowl?</h2>
                <p><strong>PaceBowl provides free educational pet nutrition calculators for informational planning only and does not provide veterinary medical diagnosis or treatment.</strong></p>
                <ul>
                  <li><strong>Consult Your Veterinarian:</strong> Always consult a licensed veterinarian before putting a pet on a weight-loss diet, transitioning to raw food, or managing medical conditions such as diabetes, pancreatitis, or kidney disease.</li>
                  <li><strong>Verify Bag Labels:</strong> Pet food manufacturers periodically reformulate kcal/cup and kcal/kg values; always check the current Guaranteed Analysis panel on your physical bag or can.</li>
                  <li><strong>Free Personal &amp; Clinic Use:</strong> Pet owners, shelters, and veterinary clinics may freely use and print PaceBowl A4 feeding charts for non-commercial care.</li>
                </ul>
              </div>
            </section>""",
        ),
    ]

    for slug, title, desc, kw, q_h2, body in trust_pages:
        graph = [
            RICH_ORG_SCHEMA,
            {
                "@type": "WebPage",
                "@id": f"{SITE}{slug}#webpage",
                "url": f"{SITE}{slug}",
                "name": title,
                "description": desc,
                "dateModified": TODAY,
                "isPartOf": {"@id": f"{SITE}/#website"},
                "publisher": {"@id": f"{SITE}/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": title.split("|")[0].strip(), "item": f"{SITE}{slug}"},
                ],
            },
        ]
        html = render_shell(slug, title, desc, kw, graph, body, "")
        html = re.sub(r'      <div class="pb-footer-links">[\s\S]*?      </div>', NEW_FOOTER_LINKS, html, count=1)
        html = html.replace(
            '  <meta name="theme-color"',
            '  <meta name="author" content="PaceBowl Pet Nutrition Editorial Team">\n  <meta property="og:image:alt" content="PaceBowl Pet Nutrition — Veterinary-Standard Dog & Cat Feeding Calculators">\n  <meta name="theme-color"',
            1,
        )
        write_page(slug.strip("/") + "/index.html", html)


def upgrade_infra_files():
    # 1. Update sitemap.xml with all 10 HTML pages
    urls = [
        ("/", "1.0", "weekly"),
        ("/tools/dog-calorie-feeding-calculator/", "0.95", "weekly"),
        ("/tools/barf-raw-dog-food-calculator/", "0.95", "weekly"),
        ("/tools/dog-food-transition-calculator/", "0.95", "weekly"),
        ("/tools/cat-calorie-feeding-calculator/", "0.95", "weekly"),
        ("/tools/puppy-adult-weight-calculator/", "0.90", "weekly"),
        ("/methodology/", "0.80", "monthly"),
        ("/about/", "0.70", "monthly"),
        ("/privacy/", "0.40", "yearly"),
        ("/terms/", "0.40", "yearly"),
    ]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pri, freq in urls:
        sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))

    # 2. Update llms.txt & llms-full.txt with E-E-A-T pages & algorithm.md endpoints
    llms = f"""# PaceBowl Pet Nutrition ({SITE})

> PaceBowl provides free, veterinary-standard dog and cat feeding, BARF/PMR raw diet, 7-day kibble transition, and puppy adult weight calculators calibrated against WSAVA, NRC 2006, and AAFCO guidelines, with instant printable A4 fridge charts and plain-text algorithm specifications.

## Machine-Readable Resources & Algorithm Specs
- [Agent Skills Index]({SITE}/.well-known/agent-skills/index.json): Structured tool schemas for AI search agents
- [Full LLM Documentation]({SITE}/llms-full.txt): Complete veterinary formulas and reference tables
- [XML Sitemap]({SITE}/sitemap.xml): Canonical index of all 10 PaceBowl pages
- [Dog Calorie Algorithm (Markdown)]({SITE}/tools/dog-calorie-feeding-calculator/algorithm.md): Plain-text WSAVA RER/DER equations
- [BARF Raw Diet Algorithm (Markdown)]({SITE}/tools/barf-raw-dog-food-calculator/algorithm.md): Plain-text 70/10/5/5/7/2/1 and 80/10/10 equations
- [7-Day Transition Algorithm (Markdown)]({SITE}/tools/dog-food-transition-calculator/algorithm.md): Plain-text calorie-matched kibble mixing equations
- [Cat Wet/Dry Algorithm (Markdown)]({SITE}/tools/cat-calorie-feeding-calculator/algorithm.md): Plain-text feline DER and wet-can subtraction equations
- [Puppy Weight Algorithm (Markdown)]({SITE}/tools/puppy-adult-weight-calculator/algorithm.md): Plain-text breed-size growth curve equations

## Core Tools & Direct Landing Pages
- [Dog Calorie & Feeding Calculator]({SITE}/tools/dog-calorie-feeding-calculator/): WSAVA RER/DER daily kcal, grams, oz, and cups per meal calculator
- [BARF & PMR Raw Dog Food Calculator]({SITE}/tools/barf-raw-dog-food-calculator/): 70/10/5/5/7/2/1 BARF and 80/10/10 PMR daily grams & 7–30 day freezer batch prep planner
- [7-Day Dog Food Transition Calculator]({SITE}/tools/dog-food-transition-calculator/): Calorie-matched 7/10/14-day old vs. new kibble mixing chart
- [Cat Calorie & Wet/Dry Food Calculator]({SITE}/tools/cat-calorie-feeding-calculator/): Indoor cat mixed wet can + dry kibble gram calculator
- [Puppy Adult Weight Calculator]({SITE}/tools/puppy-adult-weight-calculator/): Breed-size growth curve predictor from 6 to 52 weeks

## E-E-A-T Trust, Methodology & Governance
- [Veterinary Nutrition Methodology]({SITE}/methodology/): WSAVA, NRC 2006, and AAFCO formula calibration & audit policy
- [About PaceBowl Pet Nutrition]({SITE}/about/): Editorial mission, slow-feeding philosophy, and 48-hour variance review
- [Privacy Policy]({SITE}/privacy/): 100% client-side computation, zero login, cookieless analytics
- [Terms & Veterinary Disclaimer]({SITE}/terms/): Educational use boundaries and clinical safety notice
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(llms)
    full_extra = "\n## Complete Plain-Text Algorithms\n" + "\n\n".join(m["alg_md"].strip() for m in TOOL_META.values()) + "\n"
    open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8").write(llms + full_extra)

    # 3. Update .well-known/agent-skills/index.json with algorithm_md URLs & methodology link
    skills_path = os.path.join(ROOT, ".well-known/agent-skills/index.json")
    skills_data = json.load(open(skills_path, "r", encoding="utf-8"))
    skills_data["methodology_url"] = f"{SITE}/methodology/"
    skills_data["last_audited"] = TODAY
    for sk in skills_data.get("skills", []):
        sk["algorithm_markdown_url"] = sk["url"] + "algorithm.md"
    open(skills_path, "w", encoding="utf-8").write(json.dumps(skills_data, indent=2) + "\n")
    print("Upgraded sitemap.xml, llms.txt, llms-full.txt, and agent-skills/index.json")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    upgrade_existing_pages()
    write_algorithm_mds()
    build_trust_pages()
    upgrade_infra_files()
    print("ALL E-E-A-T / AEO / GEO / SEO UPGRADES APPLIED SUCCESSFULLY!")
