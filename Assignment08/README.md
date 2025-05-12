# AI Text Summarizer

This project is a web application that uses transformer-based models to generate summaries from long-form text. Built with Streamlit and Hugging Face Transformers, the app allows users to input text, select a model, adjust summarization parameters, and view results with relevant performance metrics and visualizations.

---

## Features

* Choose between two transformer models:

  * BART (`facebook/bart-base`)
  * Pegasus (`google/pegasus-xsum`)
* Customize summary length and beam search quality
* Display of summary text with:

  * Inference time
  * Compression ratio
  * Token counts (input vs. output)
* Bar chart comparing original and summarized token lengths
* Minimal, responsive user interface with custom styling

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-text-summarizer.git
cd ai-text-summarizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Note: Make sure PyTorch is installed according to your system configuration (CPU or GPU). See [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Models

* **facebook/bart-base**: A transformer-based encoder-decoder model for general-purpose summarization
* **google/pegasus-xsum**: A model fine-tuned on the XSum dataset for producing highly abstractive summaries

---

## Tech Stack

* Python
* Streamlit
* PyTorch
* Hugging Face Transformers
* Plotly
* Pandas

---

## File Overview

* `app.py`: Main application file
* `requirements.txt`: Python dependencies
* `README.md`: Project documentation

---
