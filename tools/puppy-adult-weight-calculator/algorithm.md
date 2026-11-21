# Puppy Adult Weight Calculator — Algorithm

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
