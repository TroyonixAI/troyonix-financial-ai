# Troyonix Open Source Strategy

This document outlines the strategy for open-sourcing parts of the Troyonix project. The goal is to build community, establish technical credibility, and provide value to the public, while protecting the core intellectual property of the commercial product.

## Guiding Principles
- **Give Value:** Open-source components should be genuinely useful and well-maintained.
- **Build Trust:** Be transparent about what is open source and what is not.
- **Protect the Core:** The proprietary, commercial value of the Troyonix platform must be preserved.

---

## Component Strategy

### 1. Data Pipeline (The "ETL" Layer)

- **To Be Open Sourced:**
  - **`sec-data-pipeline`:** A standalone repository containing the Python scripts for downloading, parsing, and structuring SEC filings (10-K, 10-Q, 8-K).
  - **Features:** This tool will extract key sections (MD&A, Risk Factors, etc.) and save them in a clean JSON format.
  - **Benefit:** This provides a huge value to the financial analysis and NLP communities and establishes Troyonix as an expert in handling financial documents.

- **To Be Kept Proprietary:**
  - The internal scripts that **correlate** the parsed SEC data with proprietary signals and other data sources (like the economic data from FRED).

### 2. Machine Learning Models

- **To Be Open Sourced:**
  - **`Troyonix-FinBERT-SEC-Base`:** The FinBERT model that has been fine-tuned *only* on the public SEC filing data.
  - **Distribution:** This model can be hosted on the Hugging Face Model Hub under the Troyonix organization.
  - **Benefit:** This becomes a go-to model for anyone doing analysis on SEC filings and directly points back to Troyonix.

- **To Be Kept Proprietary:**
  - The more advanced models that are fine-tuned on the combined, correlated dataset.
  - All models that are trained for specific, complex wealth management tasks (e.g., portfolio health analysis, risk forecasting).

### 3. Application & API

- **To Be Open Sourced:**
  - None.

- **To Be Kept Proprietary:**
  - The entire user-facing application, including the UI, backend APIs, client management, and analytics dashboards. This is the core commercial product.

---

## Execution Plan
1. **Develop `sec-data-pipeline`:** Create the robust data collection and parsing scripts within this project.
2. **Launch Open Source Repo:** Once mature, move the data pipeline scripts to a new, public GitHub repository under the Troyonix name.
3. **Train and Release Base Model:** After collecting sufficient data, train `Troyonix-FinBERT-SEC-Base` and publish it to Hugging Face. 