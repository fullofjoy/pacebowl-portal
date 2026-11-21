# 7-Day Dog Food Transition Calculator — Algorithm

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
