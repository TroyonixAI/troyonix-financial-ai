# Troyonix Data Strategy & Tracking

## Guiding Principles
- **Legal Integrity:** All data for production models must be 100% free and commercially usable (Public Domain).
- **Domain Specificity:** The AI must become an expert in analyzing documents relevant to the wealth management industry.
- **Technical Excellence:** Data pipelines must be robust, reproducible, and well-documented.

---

## Data Collection Roadmap

### Phase 1: SEC Filings (Foundation) ✅ COMPLETED
- **Goal:** Create a rich, structured dataset of corporate disclosures.
- **Source:** SEC EDGAR Database.
- **Filings:** 10-K (Annual), 10-Q (Quarterly), 8-K (Current Events).
- **Parsing:** Extract key sections (Item 1A: Risk Factors, Item 7: MD&A).
- **Status:** ✅ Initial collection completed (208 documents from 10 major companies).
- **Status:** ✅ Intelligent Parser Development completed (MCP server with section extraction).
- **Model Performance:** 87.5% accuracy on validation set.

### Phase 2: U.S. Economic Data (Macro Context) ✅ COMPLETED
- **Goal:** Correlate company performance with macroeconomic trends.
- **Sources:**
  - Federal Reserve Economic Data (FRED) ✅ IMPLEMENTED
  - U.S. Treasury Public Data (Planned for future).
- **Data Points:** Interest Rates, Inflation (CPI), GDP, Unemployment, Yield Curves, Consumer Sentiment.
- **Status:** ✅ FRED API integration completed.
- **Status:** ✅ Economic data transformation to text completed (15 descriptions generated).
- **Status:** ✅ Enhanced training pipeline created (combines SEC + economic context).

### Phase 3: Qualitative Public Domain Data (Expert Context) 🔄 PLANNED
- **Goal:** Enhance the model's understanding of expert financial discourse.
- **Sources:**
  - Federal Reserve Governor Speeches (Transcripts).
  - Congressional Testimony (Transcripts).
- **Status:** [ ] Data connector development.

### Phase 4: Real-time Corporate News 🔄 PLANNED
- **Goal:** Add real-time corporate press releases and announcements.
- **Sources:**
  - Corporate Investor Relations pages.
  - Press release aggregators.
- **Status:** [ ] Data connector development.

---

## Current Data Pipeline Status

### Data Sources Active:
1. **SEC Filings:** 208 documents from major companies (Apple, Amazon, Google, Microsoft, Tesla, JPMorgan, Bank of America, Goldman Sachs, BlackRock, Berkshire Hathaway)
2. **FRED Economic Data:** 5 key indicators (GDP, CPI, Unemployment, Federal Funds Rate, Consumer Sentiment)

### Processing Pipeline:
1. **Data Collection:** ✅ `download_sec_filings.py` and `download_fred_data.py`
2. **Data Processing:** ✅ `mcp_server.py` (SEC filings) and `combine_training_data.py` (enhanced dataset)
3. **Model Training:** ✅ `finetune_model.py` with evaluation metrics

### Next Steps:
1. **Retrain Model:** Use enhanced dataset (SEC + economic context) for improved performance
2. **Build First Agent:** Risk Monitoring Agent using the enriched model
3. **Phase 3 Implementation:** Add Federal Reserve speech data

---

## Storage & Legal
- **Current Raw Data Size:** ~65 MB (SEC filings) + ~1 MB (FRED data)
- **Estimated Final Data Size:** ~500 MB (all phases)
- **Legal Status:** All implemented data sources are U.S. Public Domain.
- **Storage Plan:** Local storage on MacBook Air is sufficient for all planned phases.
- **API Keys:** FRED API key securely stored in `config/config.json`

---

## Model Performance Tracking

### Current Model (SEC Filings Only):
- **Accuracy:** 87.5%
- **F1-Score:** 86.9%
- **Precision:** 87.2%
- **Recall:** 87.5%

### Target for Enhanced Model (SEC + Economic Context):
- **Goal:** Improve contextual understanding and reduce false positives/negatives
- **Expected Improvement:** 2-5% across all metrics
- **Key Benefit:** Better understanding of company performance within economic context
