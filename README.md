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
|
+-- ir_project/
|   +-- settings.py
|   +-- urls.py
|   +-- ...
|
+-- ir_system/
|   +-- data_structures/
|   +-- document_preprocessing/
|   +-- processing_classes/
|   +-- query_preprocessing/
|   +-- utils/
|   +-- docs/
|   +-- ir_system.py
|
+-- ir_web/
|   +-- templates/
|   |   +-- search.html
|   +-- views.py
|   +-- ...
|
+-- manage.py
+-- requirements.txt
+-- .gitignore
+-- README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aylin-nxt/information-retrieval-system.git

cd information-retrieval-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

On Linux or macOS:

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

### 5. Configure the Django secret key

Set the environment variable before running the application.

On Windows PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = (python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

On Linux or macOS:

```bash
export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")Get-Content README.md | Select-String -Pattern 'DJANGO_SECRET_KEY|ir_project/|ir_system/|ir_web/'
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

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