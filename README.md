# Troyonix


**AI for the future of finance.**

Troyonix is a fintech company for wealth management and financial analysis, built for transparency, innovation, and community-driven progress. We use only public-domain data (SEC EDGAR, FRED, and academic indices, etc.) so you can build, learn, and deploy with confidence.

## 🚀 What is Troyonix?
Troyonix provides:
- **A robust data pipeline** for collecting and processing financial data from public sources.
- **Custom preprocessing and training pipelines** for financial NLP, featuring a **fine-tuned FinBERT model** and **continually evolving** domain-specific language models tailored through ongoing research.

- **Full transparency**—every step is documented and auditable.

## 🏗️ Architecture Overview
- **Data Collection:** SEC filings, FRED economic data, policy uncertainty indices
- **Preprocessing:** Clean, label, and prepare data for training
- **Model Training:** Fine-tune FinBERT for financial sentiment and event detection
- **Analysis & Inference:** Evaluate and use your models on real financial text

## 🛡️ Why Legal-First?
Most financial AI projects use questionable or proprietary data. Troyonix is different:
- 100% public-domain sources (no licensing headaches)
- Transparent, auditable pipeline
- Built for compliance from day one

## ⚡ Quick Start
```bash
# Clone the repo
git clone https://github.com/TroyonixAI/troyonix-open-source.git
cd troyonix-open-source

# Set up your environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# (Optional) Add your FRED API key to config/config.json
cp config/config.example.json config/config.json

# Run the pipeline
python src/data_collection/collect_all_data.py
python src/preprocessing/prepare_training_data.py
python src/training/train_finbert.py
python src/analysis/evaluate_model.py
python src/analysis/run_inference_examples.py
```

## 🌟 Why Contribute?
- **Shape the future of finance:** Help set new standards for open, transparent AI.
- **Learn & grow:** Work with real-world NLP, data engineering, and compliance.
- **Make an impact:** Your work will be used by professionals, researchers, and innovators.
- **Get recognized:** Top contributors will be featured and have early access to new features.

## 🤝 How to Contribute
1. Fork the repo and create a new branch.
2. Make your changes and add tests if possible.
3. Open a pull request with a clear description.
4. Join the discussion and help us build the future!

## 📄 License
MIT License. Free for personal, academic, and commercial use—just keep it open and legal.

---

**Ready to build the future of financial AI? Star the repo, join the community, and let's make finance better for everyone!**



## Troyonix
AI systems for wealth management.  
🔗 [Visit Site](https://troyonix.com)
<!-- trigger CI for public workflow test -->
