# Savills Commercial Office Analysis (TAMI Focus)

> End-to-end analytics on U.S. office leasing trends with an emphasis on **TAMI** (Technology, Advertising, Media, Information) markets—covering data cleaning, feature engineering, clustering, KPI tracking, and presentation-ready visuals.

![status](https://img.shields.io/badge/status-completed-lightgray) ![python](https://img.shields.io/badge/python-3.12.3-blue)

---

## Table of Contents

* [Overview](#overview)
* [Key Findings](#key-findings-presentation-summary)
* [Methods](#methods)
* [Figures & Deliverables](#figures--deliverables)
* [Data Access & Confidentiality](#data-access--confidentiality)
* [Assumptions & Limitations](#assumptions--limitations)
* [Roadmap](#roadmap)

---

## Overview

This project analyzes office leasing patterns across major U.S. markets, with a focus on the TAMI sector. It combines leasing transactions and market-level fundamentals to quantify availability, rent levels, and leasing momentum, and applies unsupervised learning to segment markets into **strategic clusters** for expansion or optimization decisions.

**Tech stack:** Python (pandas, numpy, pyarrow), Jupyter, matplotlib/plotly, scikit-learn, DuckDB (optional).

**Scope:** 2018–2024 leasing period; metro and submarket time series; city deep dives on **San Francisco, New York, Austin, and Atlanta**.

---

## Key Findings (Presentation Summary)

**K-means clustering of TAMI markets** (features include rent levels and average leased square footage) yields four strategic market types:

1. **Cost-efficient satellite** (e.g., *Atlanta, Houston*): affordable rents, modest leasing activity → attractive for budget-conscious expansion.
2. **Global Tier-1 hubs** (e.g., *San Francisco, Manhattan*): high rents, critical for brand presence and elite talent access.
3. **Cost-sensitive core** (e.g., *Austin, Boston, Los Angeles*): balance of visibility and affordability → flexibility without sacrificing location quality.
4. **High-growth** (e.g., *Seattle, Nashville*): larger lease sizes with moderate rents → strong momentum.

**Availability proportion trends (2020–2024):**

* *San Francisco* and *Austin* rose notably in availability (higher vacancy/slower absorption).
* *New York* stayed elevated but stable.
* *Atlanta* climbed gradually.
* **All four dipped in Q4-2024**, suggesting a possible turning point toward renewed absorption.

**Rent levels:**

* *San Francisco* and *New York* consistently highest despite softer demand in recent years.
* *Austin* and *Atlanta* remained more affordable → compelling options for cost-sensitive TAMI firms.

**Interpretation:**

* Beginning in **2023**, TAMI firms started expanding footprints again after a sharp 2019–2022 contraction.
* A key driver is the **AI build-out** (product teams + ethics/testing + infra footprints like GPUs/data centers), which raises near-term space needs.
* Employer policy shifts toward **return-to-office (RTO) in early 2025** are likely to further support leasing demand beyond the traditional hubs.
* Growth momentum is increasingly concentrated in **Austin, Atlanta, and Houston**, with SF/NY retaining symbolic and strategic importance.


---

## Methods

* **Data prep & harmonization:** time indexing to quarter; unit standardization (psf), categorical normalization (sector, class), outlier and missing-value handling.
* **Feature engineering:** availability proportion, effective rent proxies (where feasible), rolling growth, average leased SF by sector/market, lease count density.
* **Unsupervised learning:** standardization → K-means (k=4), elbow/silhouette diagnostics; cluster profiling by rent, size, and momentum metrics.
* **Time-series analysis:** availability and rent trend decomposition; pre-/post-COVID regime comparison; Q4-2024 inflection checks.
* **Visualization:** city dashboards and cluster comparison charts for executive communication.

---


## Figures & Deliverables

**Analysis overview (TAMI markets):**

![TAMI overview – availability, rent, leases vs avg SF, and K-means clustering](main/tami_slide2.png)

- **Availability (2018–2024):** SF & Austin rose notably; NYC elevated but stable; Atlanta gradual until a **Q4-2024 dip** across all four—possible inflection toward renewed absorption.
- **Rent trends:** SF/NY lead on pricing despite softer demand; Austin/Atlanta remain meaningfully more affordable.
- **Leasing structure (mirrored bar):** yearly **number of leases** vs **avg leased SF** highlights cycle severity and recovery staging for TAMI.
- **K-means clustering (2D view):** four strategic groups by rent level and average leased SF—*Global Tier-1 hubs* (SF/Manhattan), *Cost-sensitive core* (Austin/Boston/LA), *High-growth* (Seattle/Nashville), and *Cost-efficient satellites* (Atlanta/Houston).

---

## Data Access & Confidentiality

**The dataset is not included in this repository and cannot be shared here due to company confidentiality.** 

---

## Assumptions & Limitations

* Leasing data can be **lagged** and **incomplete**; market/submarket boundaries may change over time.
* Availability and rent aggregates are market-level proxies; effective rents require concessions data not always available.
* Cluster labels are **interpretive** and depend on feature selection and scaling choices.

---

## Roadmap

* Add hedonic controls (size, age/class, location) for rent and pricing normalization.
* Extend cluster features (growth/volatility metrics, sector mix, RTO policy signals).
* Publish a lightweight dashboard (Plotly/Dash) for market toggling.
* Robusticity: bootstrap clustering stability and sensitivity analyses.

---

