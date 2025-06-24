<h1 align="center">Troyonix: Legal-Compliant Financial AI</h1>

<p align="center">
  <b>Enterprise-grade, open-source AI for wealth management and financial analysis.</b>
</p>

<p align="center">
  <a href="https://github.com/TroyonixAI/troyonix-open-source/actions/workflows/python-ci.yml">
    <img src="https://github.com/TroyonixAI/troyonix-open-source/actions/workflows/python-ci.yml/badge.svg" alt="Build Status">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contributions Welcome">
</p>

## 🚀 What We're Open-Sourcing

This repository contains the foundational layers of the Troyonix AI platform. We are open-sourcing our core data processing and model training pipeline to promote transparency and build a community around legally-sound financial AI.

### Key Features
- **Legal-Compliant Data Pipeline:** Uses only public-domain sources like SEC EDGAR and Federal Reserve (FRED) data.
- **Wealth Management Specialization:** Advanced preprocessing and a fine-tuned FinBERT model for financial sentiment.
- **Full Transparency Framework:** Complete documentation on data lineage, processing steps, and legal considerations.

## 🏗️ Architecture

```mermaid
graph LR;
    A[Sources] --> B[Collection];
    B --> C[Prep];
    C --> D[Train Data];
    D --> E[Model];
    E --> F[Deploy];
```

## 🛡️ The Troyonix Legal-First Approach

Troyonix is built on a "legal-first" principle. Our pipeline uses only:
- ✅ **SEC EDGAR Filings:** Public domain data for corporate financial reporting.
- ✅ **Federal Reserve Economic Data (FRED):** Authoritative U.S. government economic indicators.
- ✅ **Policy Uncertainty Indices:** Respected academic sources for market sentiment.

## 🚀 Quick Start

Get the entire pipeline running in just a few commands.

```bash
# 1. Clone the repository
git clone https://github.com/TroyonixAI/troyonix-open-source.git
cd troyonix-open-source

# 2. Set up your environment (Python 3.8+)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Optional) Configure your API keys for FRED
cp config/config.example.json config/config.json

# 5. Run the data pipeline
python src/data_collection/collect_all_data.py
python src/preprocessing/prepare_training_data.py

# 6. Train the model
python src/training/train_finbert.py

# 7. Evaluate & run inference
python src/analysis/evaluate_model.py
python src/analysis/run_inference_examples.py
```

## 📊 Performance

*Performance metrics will be updated after running the full evaluation on a comprehensive test set.*

| Metric    | Score   |
| :-------- | :------ |
| Accuracy  | TBD     |
| Precision | TBD     |
| Recall    | TBD     |
| F1-Score  | TBD     |

## 🌟 Why Contribute to Troyonix?

- **Shape the Future:** Build a transparent, compliant AI for finance.
- **Grow Your Skills:** Collaborate with experts in AI, finance, and compliance.
- **Make an Impact:** Your code will be used by professionals worldwide.
- **Get Recognized:** Top contributors featured in docs and blogs.

## 🚧 Future Work & Roadmap

**Short Term:**
- Expand labeled datasets (community input welcome!)
- Add more evaluation metrics and visualizations

**Long Term:**
- Integrate global filings and alternative data sources
- Advance model capabilities (risk, compliance, portfolio analytics)
- Enhance explainability and audit trails

## 📊 Use Cases

- **Wealth Management Firms:** Build legal/compliant portfolio and risk tools.
- **Financial Analysts:** Automate SEC filings and economic report analysis.
- **Fintech Startups:** Use as a foundation for compliant financial AI products.

## 🤝 Community & Contributing

How to contribute:
1. Fork this repo and create a new branch.
2. Make your changes and add tests where appropriate.
3. Submit a pull request with a clear description of your changes.
4. For ideas, see our [open issues](https://github.com/TroyonixAI/troyonix-open-source/issues) or [CONTRIBUTING.md](CONTRIBUTING.md).

Join the community:
- GitHub Discussions
- (Add Slack/Discord link if available)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Built by a founder who believes in transparency, legal compliance, and the power of community.**

<!-- trigger CI -->
