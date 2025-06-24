<h1 align="center">Troyonix: Legal-Compliant Financial AI</h1>



<h2 align="center">
Enterprise-grade, open-source AI for wealth management and financial analysis.
</h2>


## 🚀 What We're Open-Sourcing

This repository contains the foundational layers of the Troyonix AI platform. We are open-sourcing our core data processing and model training pipeline to promote transparency and build a community around legally-sound financial AI.

### Key Features:
-   **Legal-Compliant Data Pipeline**: A production-ready data collection system that uses only public-domain sources like SEC EDGAR and Federal Reserve (FRED) data, eliminating legal risks associated with other financial data sources.
-   **Wealth Management Specialization**: Advanced preprocessing tailored for wealth management use cases and a fine-tuned FinBERT model that understands the nuances of financial sentiment.
-   **Full Transparency Framework**: Complete documentation on data lineage, processing steps, and legal considerations, ensuring every step is auditable and trustworthy.

## 🏗️ Architecture

The diagram below illustrates the flow of data from collection to training.

```mermaid
graph LR;
    A[Sources] --> B[Collection];
    B --> C[Prep];
    C --> D[Train Data];
    D --> E[Model];
    E --> F[Deploy];
```

## 🛡️ The Troyonix Legal-First Approach

In an industry where data privacy and compliance are paramount, Troyonix is built on a "legal-first" principle. Our pipeline uses only:
-   ✅ **SEC EDGAR Filings**: Public domain data for corporate financial reporting.
-   ✅ **Federal Reserve Economic Data (FRED)**: Authoritative U.S. government economic indicators.
-   ✅ **Policy Uncertainty Indices**: Respected academic sources for market sentiment.

This approach ensures our models are built on a foundation of data that is ethical, transparent, and free from commercial licensing restrictions.

## 🚀 Quick Start

Get the entire pipeline running in just a few commands.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/troyonix-legal-financial-ai.git
cd troyonix-legal-financial-ai

# 2. Set up your environment (requires Python 3.8+)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure your API keys (optional, for FRED data)
# Copy config.example.json to config.json and add your FRED API key.

# 4. Run the data collection and processing pipeline
python src/data_collection/collect_all_data.py
python src/preprocessing/prepare_training_data.py

# 5. Run the model training
python src/training/train_finbert.py

# 6. Evaluate model performance
python src/analysis/evaluate_model.py

# 7. Run inference examples
python src/analysis/run_inference_examples.py
```

## 📊 Performance

To ensure transparency and provide a clear measure of the model's capabilities, we evaluate it against a labeled dataset of financial texts.

**Evaluation Dataset:** A custom-labeled dataset of sentences from SEC filings.
*NOTE: For a truly robust benchmark, we plan to evaluate against standardized datasets like the Financial PhraseBank in the future.*

| Metric    | Score   |
| :-------- | :------ |
| Accuracy  | TBD     |
| Precision | TBD     |
| Recall    | TBD     |
| F1-Score  | TBD     |

*The "TBD" scores will be updated after running the full evaluation on a comprehensive test set. You can run the evaluation yourself using the `evaluate_model.py` script.*

## 🌟 Why Contribute to Troyonix?

- **Shape the Future of Finance:**  Help build the first truly transparent, legally-compliant AI platform for wealth management—setting new industry standards.
- **Learn & Grow:**  Collaborate with experts in AI, finance, and compliance. Gain experience with real-world NLP, data engineering, and responsible AI.
- **Make an Impact:**  Your contributions will be used by financial professionals, researchers, and innovators worldwide.
- **Get Recognized:**  Top contributors will be featured in our documentation, blog, and (eventually) have early access to commercial features and opportunities.
- **Join a Mission-Driven Community:**  We believe in open, ethical, and impactful technology. If you do too, you'll fit right in.

Ready to get started? Check out our CONTRIBUTING.md and join the discussion!

## Future Work

**Transparency is our priority. Here's what Troyonix can and can't do today:**

- **Current Limitations:**
  - The evaluation dataset is small and focused on U.S. SEC filings; broader coverage is coming.
  - The model is optimized for sentiment and basic event detection; more advanced tasks are in development.
  - Only public-domain data is used—no proprietary or alternative data sources (yet).
  - Not intended as financial advice or a replacement for human expertise.
- **Future Work:**
  - Expand labeled datasets (with community and partner contributions)
  - Add support for global filings, news, and alternative data
  - Develop more advanced models for risk, compliance, and portfolio analytics
  - Enhance explainability, audit trails, and human-in-the-loop features

We're committed to continuous improvement and welcome your feedback and contributions!

## 📊 Use Cases

This foundational pipeline can be used by:

-   **Wealth Management Firms** to build tools for client communication, portfolio analysis, and risk assessment with full legal and compliance backing.
-   **Financial Analysts** to automate the analysis of SEC filings and economic reports for market research and compliance.
-   **Fintech Startups** as a legally-sound starting point for building their own financial AI products.

## 🎯 My Story

I'm a 19-year-old founder building the AI tools I believe the wealth management industry needs. Recognizing that many AI solutions rely on questionable data, I committed to building Troyonix on a foundation of 100% legal and transparent sources. I'm leveraging AI to help me write the code, allowing me to focus on the architectural vision, product strategy, and legal compliance.

I'm open-sourcing this foundation because I believe in transparency and community collaboration. Let's build the future of financial AI, the right way.

## 🤝 Contributing

We welcome contributions of all kinds, from code and documentation to bug reports and feature ideas. Please see our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software in accordance with the terms of the license.

---

**Built by a founder who believes in transparency, legal compliance, and the power of community.**

# Open Source Release Structure

To prepare this project for open source release, use the following structure:

**Include in your GitHub repo:**
- `src/` (all code: data collection, preprocessing, training, analysis, utils, and tests)
- `config/config.example.json` (example config only)
- `config/model_config.yaml` (model config)
- `docs/` (all documentation)
- `README.md`, `CONTRIBUTING.md`, `LICENSE`
- `requirements.txt`
- `.gitignore`

**Do NOT include (add to .gitignore if not already):**
- `config/config.json` (real secrets/configs)
- Any files in `data/` (raw, processed, or model data)
- `venv/` or any virtual environment folders

This structure keeps your open-source release clean, safe, and easy for others to use.

<!-- Trigger new CI run --> 
