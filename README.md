# Information Retrieval System

A Django-based Information Retrieval System implementing classical Information Retrieval techniques, data structures, and query-processing methods through a web interface.

## Overview

This project demonstrates the implementation of a basic Information Retrieval pipeline, from document preprocessing and index construction to query processing and ranked retrieval.

It provides several retrieval methods and indexing structures to explore how different Information Retrieval techniques work together.

## Features

### Indexing and Data Structures
- **Inverted Index:** Maps terms to the documents containing them.
- **Positional Index:** Stores term positions to support phrase and proximity queries.
- **Trie:** Supports efficient prefix-based term lookup.
- **Permuterm Index:** Enables wildcard query processing.

### Query Processing and Retrieval
- Boolean retrieval using `AND`, `OR`, and `NOT` operators.
- Phrase search.
- Proximity search.
- Wildcard search.
- Spelling correction.
- TF-IDF-based document ranking.

### Document Processing
- Text preprocessing and normalization.
- Tokenization and lemmatization.
- Processing a collection of text documents.

## Technologies

- Python
- Django
- spaCy
- NLTK
- HTML / CSS

## Project Structure

```text
information-retrieval-system/
│
├── ir_project/                     # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── ir_system/                      # Core Information Retrieval implementation
│   ├── data_structures/             # Indexing data structures
│   │   ├── Trie.py
│   │   ├── inverted_index.py
│   │   └── positional_index.py
│   │
│   ├── document_preprocessing/      # Document preprocessing
│   │   └── document_preprocessing.py
│   │
│   ├── processing_classes/          # Retrieval algorithms
│   │   ├── boolean.py
│   │   ├── permuterm.py
│   │   ├── phrase.py
│   │   ├── proximity.py
│   │   └── ranking.py
│   │
│   ├── query_preprocessing/         # Query processing
│   │   ├── boolean_query_preprocessing.py
│   │   ├── proximity_query_preprocessing.py
│   │   ├── query_preprocessing.py
│   │   └── spell_correction.py
│   │
│   ├── utils/
│   ├── docs/                        # Document collection
│   └── ir_system.py                # Core system integration
│
├── ir_web/                          # Django web interface
│   ├── templates/
│   │   └── search.html
│   ├── views.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/aylin-nxt/information-retrieval-system.git
cd information-retrieval-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### 5. Set the Django secret key

The application reads its secret key from the `DJANGO_SECRET_KEY` environment variable.

**Windows (PowerShell)**

```powershell
$secret = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_SECRET_KEY = $secret
```

**Linux / macOS**

```bash
export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## Dataset

The project includes a collection of text documents stored in:

```text
ir_system/docs/
```

These documents serve as the input corpus for document preprocessing and index construction.

## Implementation Notes

The project separates document preprocessing, indexing structures, query preprocessing, retrieval algorithms, and the Django web interface into dedicated modules.

This modular structure makes individual Information Retrieval components easier to understand, test, and extend.

## Future Improvements

- Improve query-processing robustness and edge-case handling.
- Add automated unit and integration tests.
- Improve search result presentation.
- Expand the document collection.
- Optimize indexing and retrieval performance.

## Author

**Aylin Nakhostin**

Computer Engineering Graduate | AI & Machine Learning Developer

[GitHub](https://github.com/aylin-nxt)
