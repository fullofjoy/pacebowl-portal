# Dog Calorie & Daily Feeding Calculator — Algorithm

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
