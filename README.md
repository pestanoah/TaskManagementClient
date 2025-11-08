# Task Management Client

A Python client that receives task messages from AWS SQS and prints them using ESCPOS thermal printers.

## Features

- Polls AWS SQS queue for task messages
- Converts task data to formatted receipts
- Prints tasks using ESCPOS thermal printers
- Supports task attributes: title, body, priority, created date, due date

## Requirements

- Python 3.14+
- ESCPOS-compatible thermal printer
- AWS credentials configured

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install boto3 python-escpos python-dotenv pillow
```

3. Configure AWS credentials and create `.env` file with required settings

## Usage

```bash
python main.py
```

## Libraries

- [python-escpos](https://github.com/python-escpos/python-escpos) - ESCPOS printer library
