# BARF & PMR 80/10/10 Raw Dog Food Calculator — Algorithm

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
