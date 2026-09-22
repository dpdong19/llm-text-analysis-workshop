# Airline Review Classification — Workshop Project

Classify airline customer reviews into service aspects and sentiments,
using an LLM-assisted workflow.

## What's in the box

```
classification-rule/   ← The classification rules (prompt, taxonomy, output schema)
data/                  ← 50 sample airline reviews to classify
output/                ← Will hold results after you run the classifier
compare.py             ← Compare your results against the instructor reference set
```

## Setup

### 1. Python environment

Python 3.10+ required. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. API key

Copy the example env file and add your Anthropic API key:

```bash
cp .env.example .env
```

Use your own key if you have one. If not, your instructor can provide
a shared key during the session.

> ⚠️ **Do not commit or share your `.env` file.**
> Run small batches (`--limit 3`) while developing to conserve API credits.

## The task

You will build `classify.py` — a script that:

1. Reads the classification rules from `classification-rule/`
2. Sends each review to the LLM for classification
3. Validates the output (schema compliance + business rules)
4. Saves valid results and failed records separately to `output/`

**The script does not exist yet. Building it is the exercise.**

Your instructor will walk through the process of designing and
implementing this workflow step by step, working with an AI coding
assistant.

### Model

If you are using an Anthropic API key, use **`claude-haiku-4-5-20251001`**.
It is the cheapest model and keeps costs minimal for everyone.
Tell your AI assistant to hardcode this model in the script.

If you are using a different provider (e.g. DeepSeek), use whatever
model your provider offers — ignore the Haiku requirement above.

## Comparing your results

Once you have `output/results.jsonl`, your instructor will provide
`reference_set_final.csv` — an adjudicated reference for 15 of the 50 reviews.
Drop it into this folder and run:

```bash
python compare.py
```

Differences are discussion starters, not errors.

## Quick reference

- **Prompt**: `classification-rule/classification_prompt.md`
- **Taxonomy**: `classification-rule/taxonomy.yaml`
- **Output schema**: `classification-rule/output_schema.json`
- **Input data**: `data/airline_reviews_sample_50.csv`
