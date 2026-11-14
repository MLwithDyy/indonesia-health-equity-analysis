# Analysis plan (locked before the analysis)

Locked on: 14 November 2026

Topic: life expectancy and socio-economic factors across Indonesian provinces, 2024.

## Disclosure

I originally planned to study access to health services (facilities and health workers) against health outcomes. The recent province tables for facilities and health workers were not available to me (the facilities table I could download stops at 2015 and the health-worker table would not load), so I changed the topic to socio-economic factors. See `data_sources.md`.

Before this plan was locked, a data-quality check I ran also printed quick Spearman correlations with life expectancy. These were seen before the analysis choices below were fixed:

| Factor | Spearman rho with life expectancy |
|---|---|
| Poverty rate | -0.65 |
| Decent sanitation | +0.66 |
| School participation 7-12 | +0.59 |
| log GRDP per capita | +0.33 |
| School participation 16-18 | +0.21 |

The choices in the model section were made with this knowledge, so the model selection is exploratory, not confirmatory. Nothing else about the analysis was looked at.

## Variables (fixed)

- **Outcome:** life expectancy = mean of male and female life expectancy (BPS 2024). This is my own average, not the official BPS total figure. Male and female values are analysed separately only for question 5.
- **Poverty:** mean of the March and September 2024 poverty rates (total, urban + rural).
- **Economy:** log of GRDP per capita at current prices (2010 series). Used descriptively and as a sensitivity check, because mining-heavy provinces inflate GRDP without reflecting residents' living standards.
- **Education:** school participation rate (APS) for ages 16-18 is the main indicator, because ages 7-12 are close to the ceiling in most provinces and separate provinces less. All four age groups are reported in an appendix.
- **Sanitation:** share of households with decent sanitation, 2024.

## Questions

1. How large is the gap in life expectancy between provinces, and which provinces are highest and lowest? (Range, interquartile range, standard deviation, ranking; males and females shown separately.)
2. Which factors correlate most strongly with life expectancy across provinces? (Spearman correlation per factor, with bootstrap 95% intervals.)
3. When the factors are considered together, which ones still relate to life expectancy?
4. Which provinces have life expectancy far above or below what the model predicts? (Residuals.)
5. Does the female-minus-male difference in life expectancy vary across provinces or regions? (Descriptive; correlations with the factors are exploratory.)

## Methods (fixed)

- **Unit and sample:** 38 provinces, one year (2024). National rows are excluded from all analyses.
- **Main model (question 3):** ordinary least squares, life expectancy ~ poverty + sanitation + APS 16-18. Predictors are standardised so coefficients are comparable. Three predictors is the limit for 38 observations.
- **Uncertainty:** bootstrap over provinces (2,000 resamples), 95% percentile intervals, for correlations and model coefficients. Report variance inflation factors for the model.
- **Sensitivity checks (all reported, whatever they show):**
  1. Repeat the correlations and the main model without the six Papua provinces (n = 32).
  2. Four-predictor model that adds log GRDP per capita.
  3. Correlations for males and females separately.
  4. Correlations for all four APS age groups.
- **Residuals (question 4):** report the five largest positive and the five largest negative residuals, with the caution that with n = 38 individual residuals are noisy.
- **Rule for reporting:** every analysis above is reported, including ones that show weak or unexpected results. No analyses are added because a chart looks interesting; anything added later is labelled exploratory and listed in the deviation log.

## Required limitations in the README

- Province-level correlations, not cause and effect. A province average does not describe the people in it (ecological fallacy).
- n = 38 and one year. Intervals are wide.
- The six Papua provinces sit at the extreme of most variables and can dominate correlations.
- GRDP per capita is distorted by mining.
- Life expectancy here is the mean of male and female values.
- Poverty combines two survey rounds by simple averaging.
- Facility and health-worker data are not included.

## Deviation log

Record any change made after locking this plan, with the date and the reason.

| Date | Change | Reason |
|---|---|---|
| | | |