/**
 * PaceBowl — Veterinary-Standard Pet Feeding & Diet Portion Math Engine
 * Based on WSAVA (World Small Animal Veterinary Association) & NRC guidelines:
 *   RER (Resting Energy Requirement) = 70 * (weight_kg ^ 0.75)
 *   DER (Daily Energy Requirement)   = RER * life_stage_factor
 */
(function (root) {
  'use strict';

  const LB_TO_KG = 0.45359237;
  const OZ_TO_G = 28.349523125;

  function toKg(weight, unit) {
    const w = Number(weight);
    if (!Number.isFinite(w) || w <= 0) return 0;
    return unit === 'lb' ? w * LB_TO_KG : w;
  }

  function toLb(kg) {
    return kg / LB_TO_KG;
  }

  function round1(n) {
    return Math.round(n * 10) / 10;
  }

  function round2(n) {
    return Math.round(n * 100) / 100;
  }

  /** WSAVA Resting Energy Requirement (kcal/day) */
  function calcRER(weightKg) {
    if (!Number.isFinite(weightKg) || weightKg <= 0) return 0;
    return 70 * Math.pow(weightKg, 0.75);
  }

  /** 1. Dog Calorie & Daily Feeding Calculator */
  const DOG_FACTORS = {
    neutered_adult: { factor: 1.6, label: 'Neutered / Spayed Adult' },
    intact_adult: { factor: 1.8, label: 'Intact Adult' },
    weight_loss: { factor: 1.0, label: 'Weight Loss (Overweight)' },
    weight_gain: { factor: 1.4, label: 'Weight Gain / Underweight' },
    active_working: { factor: 2.2, label: 'Active / Working Dog' },
    puppy_young: { factor: 3.0, label: 'Puppy (Under 4 Months)' },
    puppy_older: { factor: 2.0, label: 'Puppy (4 to 12 Months)' },
    senior: { factor: 1.3, label: 'Senior / Low Activity (7+ yrs)' },
  };

  function calcDogFeeding(opts) {
    const weightKg = toKg(opts.weight, opts.unit || 'lb');
    const stage = DOG_FACTORS[opts.stage] || DOG_FACTORS.neutered_adult;
    const kcalPerCup = Math.max(150, Math.min(800, Number(opts.kcalPerCup) || 360));
    const kcalPerKg = Math.max(2000, Math.min(6000, Number(opts.kcalPerKg) || 3550));
    const meals = Math.max(1, Math.min(4, parseInt(opts.meals, 10) || 2));

    const rer = calcRER(weightKg);
    const der = rer * stage.factor;
    const cupsPerDay = der / kcalPerCup;
    const gramsPerDay = (der / kcalPerKg) * 1000;
    const ozPerDay = gramsPerDay / OZ_TO_G;

    let bowlRec = 'Small Slow-Feeder Bowl (1–1.5 cup capacity)';
    if (cupsPerDay / meals > 2.0) bowlRec = 'Large / XL Slow-Feeder Bowl (3–4 cup capacity)';
    else if (cupsPerDay / meals > 0.85) bowlRec = 'Medium Slow-Feeder Bowl (2 cup capacity)';

    return {
      weightKg: round2(weightKg),
      weightLb: round1(toLb(weightKg)),
      stageLabel: stage.label,
      factor: stage.factor,
      rer: Math.round(rer),
      der: Math.round(der),
      cupsPerDay: round2(cupsPerDay),
      cupsPerMeal: round2(cupsPerDay / meals),
      gramsPerDay: Math.round(gramsPerDay),
      gramsPerMeal: Math.round(gramsPerDay / meals),
      ozPerDay: round1(ozPerDay),
      ozPerMeal: round1(ozPerDay / meals),
      meals,
      bowlRec,
    };
  }

  /** 2. BARF / PMR Raw Dog Food Calculator */
  const RAW_MODELS = {
    barf: {
      label: 'BARF (70/10/5/5/7/2/1)',
      ratios: [
        { key: 'muscle', label: 'Muscle Meat', pct: 70 },
        { key: 'bone', label: 'Raw Meaty Bone (RMB)', pct: 10 },
        { key: 'liver', label: 'Liver (Secreting Organ)', pct: 5 },
        { key: 'organ', label: 'Other Secreting Organ (Kidney/Spleen)', pct: 5 },
        { key: 'veggies', label: 'Leafy & Low-Glycemic Veggies', pct: 7 },
        { key: 'seeds', label: 'Seeds, Nuts & Omega Oils', pct: 2 },
        { key: 'fruit', label: 'Low-Sugar Berries / Fruit', pct: 1 },
      ],
    },
    pmr: {
      label: 'PMR — Prey Model Raw (80/10/5/5)',
      ratios: [
        { key: 'muscle', label: 'Muscle Meat', pct: 80 },
        { key: 'bone', label: 'Raw Meaty Bone (RMB)', pct: 10 },
        { key: 'liver', label: 'Liver', pct: 5 },
        { key: 'organ', label: 'Other Secreting Organ', pct: 5 },
      ],
    },
  };

  function calcRawDogFood(opts) {
    const weightKg = toKg(opts.weight, opts.unit || 'lb');
    const bodyPct = Math.max(1.5, Math.min(10.0, Number(opts.bodyPct) || 2.5));
    const prepDays = Math.max(1, Math.min(60, parseInt(opts.prepDays, 10) || 14));
    const model = RAW_MODELS[opts.model] || RAW_MODELS.barf;

    const dailyGrams = weightKg * 1000 * (bodyPct / 100);
    const dailyOz = dailyGrams / OZ_TO_G;
    const batchGrams = dailyGrams * prepDays;
    const batchLbs = (batchGrams / 1000) / LB_TO_KG;

    const breakdown = model.ratios.map((r) => {
      const gDay = dailyGrams * (r.pct / 100);
      const gBatch = batchGrams * (r.pct / 100);
      return {
        key: r.key,
        label: r.label,
        pct: r.pct,
        dailyGrams: Math.round(gDay),
        dailyOz: round1(gDay / OZ_TO_G),
        batchGrams: Math.round(gBatch),
        batchLbs: round2((gBatch / 1000) / LB_TO_KG),
      };
    });

    return {
      weightKg: round2(weightKg),
      weightLb: round1(toLb(weightKg)),
      modelLabel: model.label,
      bodyPct,
      prepDays,
      dailyGrams: Math.round(dailyGrams),
      dailyOz: round1(dailyOz),
      batchKg: round2(batchGrams / 1000),
      batchLbs: round2(batchLbs),
      breakdown,
    };
  }

  /** 3. Dog Food Transition Calculator (7 / 10 / 14 Day Schedule with Calorie Matching) */
  function calcFoodTransition(opts) {
    const oldDailyGrams = Math.max(20, Number(opts.oldDailyGrams) || 240);
    const oldKcalPerCup = Math.max(150, Number(opts.oldKcalPerCup) || 360);
    const newKcalPerCup = Math.max(150, Number(opts.newKcalPerCup) || 380);
    const oldDailyCups = Number(opts.oldDailyCups) > 0 ? Number(opts.oldDailyCups) : oldDailyGrams / 105;
    const days = [7, 10, 14].includes(Number(opts.days)) ? Number(opts.days) : 7;

    // Preserve exact daily calories when switching between different calorie-density kibbles
    const targetDailyKcal = oldDailyCups * oldKcalPerCup;
    const newFullDailyCups = targetDailyKcal / newKcalPerCup;
    const newFullDailyGrams = oldDailyGrams * (oldKcalPerCup / newKcalPerCup);

    const schedules = {
      7: [25, 25, 50, 50, 75, 75, 100],
      10: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
      14: [10, 10, 25, 25, 40, 40, 50, 50, 75, 75, 90, 90, 100, 100],
    };

    const steps = schedules[days].map((newPct, idx) => {
      const oldPct = 100 - newPct;
      return {
        day: idx + 1,
        oldPct,
        newPct,
        oldGrams: Math.round(oldDailyGrams * (oldPct / 100)),
        newGrams: Math.round(newFullDailyGrams * (newPct / 100)),
        oldCups: round2(oldDailyCups * (oldPct / 100)),
        newCups: round2(newFullDailyCups * (newPct / 100)),
      };
    });

    return {
      days,
      targetDailyKcal: Math.round(targetDailyKcal),
      oldDailyGrams: Math.round(oldDailyGrams),
      newFullDailyGrams: Math.round(newFullDailyGrams),
      oldDailyCups: round2(oldDailyCups),
      newFullDailyCups: round2(newFullDailyCups),
      steps,
    };
  }

  /** 4. Cat Calorie & Mixed Wet/Dry Feeding Calculator */
  const CAT_FACTORS = {
    indoor_neutered: { factor: 1.2, label: 'Indoor Neutered / Spayed Adult' },
    intact_adult: { factor: 1.4, label: 'Intact Adult Cat' },
    weight_loss: { factor: 0.8, label: 'Weight Loss (Overweight Cat)' },
    active_outdoor: { factor: 1.6, label: 'Active / Outdoor Cat' },
    kitten: { factor: 2.5, label: 'Growing Kitten (Under 12 Months)' },
    senior: { factor: 1.1, label: 'Senior Cat (10+ Years)' },
  };

  function calcCatFeeding(opts) {
    const weightKg = toKg(opts.weight, opts.unit || 'lb');
    const stage = CAT_FACTORS[opts.stage] || CAT_FACTORS.indoor_neutered;
    const wetCansPerDay = Math.max(0, Math.min(6, Number(opts.wetCansPerDay) || 0));
    const kcalPerWetCan = Math.max(30, Math.min(300, Number(opts.kcalPerWetCan) || 85));
    const dryKcalPerCup = Math.max(200, Math.min(700, Number(opts.dryKcalPerCup) || 400));
    const dryKcalPerKg = Math.max(2500, Math.min(5500, Number(opts.dryKcalPerKg) || 3800));

    const rer = calcRER(weightKg);
    const der = rer * stage.factor;
    const wetKcal = wetCansPerDay * kcalPerWetCan;
    const remainingDryKcal = Math.max(0, der - wetKcal);
    const dryCupsPerDay = remainingDryKcal / dryKcalPerCup;
    const dryGramsPerDay = (remainingDryKcal / dryKcalPerKg) * 1000;
    const overfedWarning = wetKcal > der * 1.05;

    return {
      weightKg: round2(weightKg),
      weightLb: round1(toLb(weightKg)),
      stageLabel: stage.label,
      factor: stage.factor,
      rer: Math.round(rer),
      der: Math.round(der),
      wetCansPerDay,
      wetKcal: Math.round(wetKcal),
      remainingDryKcal: Math.round(remainingDryKcal),
      dryCupsPerDay: round2(dryCupsPerDay),
      dryGramsPerDay: Math.round(dryGramsPerDay),
      overfedWarning,
    };
  }

  /** 5. Puppy Adult Weight Predictor (Breed-Size Growth Curves) */
  const BREED_MATURITY_WEEKS = {
    toy: { label: 'Toy Breed (< 12 lbs)', matureWeeks: 36, peakMultiplierAt16w: 1.65 },
    small: { label: 'Small Breed (12–25 lbs)', matureWeeks: 42, peakMultiplierAt16w: 1.85 },
    medium: { label: 'Medium Breed (25–55 lbs)', matureWeeks: 52, peakMultiplierAt16w: 2.0 },
    large: { label: 'Large Breed (55–95 lbs)', matureWeeks: 68, peakMultiplierAt16w: 2.35 },
    giant: { label: 'Giant Breed (95+ lbs)', matureWeeks: 84, peakMultiplierAt16w: 2.65 },
  };

  function calcPuppyAdultWeight(opts) {
    const currentKg = toKg(opts.weight, opts.unit || 'lb');
    const ageWeeks = Math.max(6, Math.min(72, Number(opts.ageWeeks) || 16));
    const sizeInfo = BREED_MATURITY_WEEKS[opts.breedSize] || BREED_MATURITY_WEEKS.medium;

    // Smooth logistic/power growth fraction by breed maturity window
    const progressRatio = Math.min(0.98, Math.pow(ageWeeks / sizeInfo.matureWeeks, 0.72));
    const estAdultKg = currentKg / Math.max(0.15, progressRatio);
    const estAdultLb = toLb(estAdultKg);
    const lowLb = Math.max(toLb(currentKg), estAdultLb * 0.92);
    const highLb = estAdultLb * 1.08;

    const milestones = [12, 16, 24, 36, 52].map((w) => {
      const frac = Math.min(1.0, Math.pow(w / sizeInfo.matureWeeks, 0.72));
      const kg = estAdultKg * frac;
      return {
        weeks: w,
        pctAdult: Math.round(frac * 100),
        weightLb: round1(toLb(kg)),
        weightKg: round1(kg),
      };
    });

    let adultBowl = 'Medium Slow-Feeder Bowl (2 cups)';
    if (estAdultLb < 20) adultBowl = 'Small Slow-Feeder Bowl (1 cup)';
    else if (estAdultLb > 55) adultBowl = 'Large / XL Slow-Feeder Bowl (3–4 cups)';

    return {
      currentLb: round1(toLb(currentKg)),
      currentKg: round2(currentKg),
      ageWeeks,
      breedLabel: sizeInfo.label,
      pctGrown: Math.round(progressRatio * 100),
      estAdultLb: round1(estAdultLb),
      estAdultKg: round1(estAdultKg),
      rangeLb: `${round1(lowLb)} – ${round1(highLb)} lbs`,
      rangeKg: `${round1(lowLb * LB_TO_KG)} – ${round1(highLb * LB_TO_KG)} kg`,
      adultBowl,
      milestones,
    };
  }

  const api = {
    calcRER,
    calcDogFeeding,
    calcRawDogFood,
    calcFoodTransition,
    calcCatFeeding,
    calcPuppyAdultWeight,
    DOG_FACTORS,
    RAW_MODELS,
    CAT_FACTORS,
    BREED_MATURITY_WEEKS,
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else {
    root.PaceBowlMath = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
