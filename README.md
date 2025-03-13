# AEP_DCVS_BatchBlaster

## Overview
**AEP_DCVS_BatchBlaster** is a Python script designed to tackle ingestion errors in Adobe Experience Platform (AEP) head-on. If you're managing data pipelines and constantly battling failed batches due to Data Collection Validation Service (DCVS) errors, this tool is your new best friend. It automates the process of identifying, analyzing, and reporting on failed batches, saving you hours of manual troubleshooting.

### The Business Problem
In AEP, data ingestion failures can disrupt your analytics workflows, delay insights, and frustrate stakeholders. These failures often stem from DCVS validation errors (e.g., malformed data, missing fields like eVar245), but pinpointing the exact cause across hundreds or thousands of batch records is a nightmare. Manually sifting through logs or API responses is time-consuming and error-prone, leaving teams scrambling to fix issues before they escalate. The result? Downtime, data gaps, and unhappy users.

### The Solution
AEP_DCVS_BatchBlaster solves this by:
1. **Retrieving Failed Batches**: Queries the AEP API for all failed batches in the last 24 hours.
2. **Downloading Details**: Pulls detailed failure data (NDJSON files) for each batch.
3. **Extracting Key Insights**: Parses errors, including DCVS error codes, messages, and custom dimensions like eVar245.
4. **Generating Reports**: Outputs organized CSV files with error counts and details, making it easy to spot patterns and fix root causes.

With dated outputs and a clean slate on each run, it’s built for daily use and scales with your AEP workload.

## Prerequisites
- **Environment**: 
  - Designed to run in an **AEP Platform Jupyter Notebook** without using the platform’s internal authentication mechanism.
  - Should work in a standalone **Jupyter Notebook** (untested) or as a regular Python script if Python is installed locally (3.7+).
- **Dependencies**: 
  - `requests` and `pandas` are required. These are pre-installed in AEP’s Jupyter environment. For standalone use, install them with:
    ```bash
    pip install requests pandas
