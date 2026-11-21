# Cat Calorie & Wet/Dry Mixed Feeding Calculator — Algorithm

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
