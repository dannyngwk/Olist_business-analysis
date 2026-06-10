# Key Findings — Olist E-Commerce Analysis

*Period: Sept 2016 – Oct 2018 · ~100K orders · figures from the dbt `analytics` marts.*

## Headline metrics
| Metric | Value |
|---|---|
| Total GMV (items + freight) | **R$ 15.8M** |
| Items revenue | R$ 13.6M |
| Orders | 99,441 |
| Unique customers | 96,096 |
| Average order value | **R$ 159** |
| Average review score | **4.09 / 5** |
| On-time delivery | 91.9% (8.1% late) |
| Avg delivery time | 12.5 days |
| Repeat-customer rate | **3.1%** |

## 1. Growth — strong and accelerating
Monthly GMV grew ~8x, from ~R$120K (Jan 2017) to ~R$1.0M (mid-2018), with a
pronounced Black Friday spike in Nov 2017 (R$1.01M). The business has proven
demand and acquisition momentum.

## 2. Delivery reliability is the #1 satisfaction driver
- On-time orders average **4.29 ★**; late orders average **2.57 ★** — a **1.72-point** gap.
- 8.1% of delivered orders arrive after the estimated date.
- This is the single largest *controllable* driver of review scores, and reviews
  correlate with repeat behavior and word-of-mouth.

## 3. Revenue concentration — category and geography
- **Top categories:** health & beauty (R$1.26M), watches & gifts (R$1.21M),
  bed/bath/table (R$1.04M), sports & leisure, computer accessories.
- **Geography:** São Paulo state ≈ **38% of GMV** (R$5.2M), followed by RJ and MG.
  Top 3 states ≈ ~55% of revenue — concentration risk + expansion headroom.

## 4. Retention is the biggest untapped lever
Only **3.1%** of customers place a second order. Acquisition works; the lifetime
value of acquired customers is largely unrealized.

## 5. Payments
Credit card dominates (73.9% of payments), followed by boleto (19.0%).
Installment usage is high — relevant to cash-flow and risk modeling.

---

## Recommendations (data-driven)
1. **Delivery SLA program** targeting late-prone lanes/sellers. Modeled impact:
   moving the 8.1% late orders to on-time could lift average review toward ~4.2+,
   improving retention and organic acquisition.
2. **Retention engine** — post-purchase nudges, category-based reorder reminders,
   and a loyalty mechanic. Lifting repeat rate from 3% → 6% roughly doubles
   repeat-driven GMV with no extra acquisition cost.
3. **Regional fulfillment** to expand beyond SP and reduce delivery times in
   under-served states.
4. **Category strategy** — protect margin in top categories while watching
   per-category review scores for early churn signals.
