# AEP_DCVS_BatchBlaster

## Overview
**AEP_DCVS_BatchBlaster** is a Python script designed to obliterate Data Collection Validation Service (DCVS) errors in Adobe Experience Platform (AEP). If you’re battling failed ingestion batches and cryptic DCVS error codes inside AEP, this tool is your ultimate fix. It automates fetching failed batches, downloading error details, extracting insights (like eVar245 issues), and generating actionable reports—all in about 10 minutes. Paste it into an AEP Jupyter Notebook, update your credentials, and watch it work—no local setup needed.

### The Business Problem
Data ingestion powers AEP’s analytics, personalization, and insights, but DCVS validation errors can grind it to a halt. These errors, triggered during ingestion validation, include:
- **`DCVS-1104-400`**: Data type mismatches (e.g., String where a Number’s expected).
- **`DCVS-1111-400`**: Missing required fields (e.g., eVar245 nowhere to be found).
- **`DCVS-1106-400`**: Enum violations (e.g., invalid option in a list).
- **`DCVS-1105-400`**: Format errors (e.g., a timestamp gone rogue).

Unlike ingestion errors (e.g., `INGEST-1002-400` for upload issues), DCVS errors are validation-specific and barely documented by Adobe. This forces AEP admins and engineers to manually dig through logs or APIs—a process that can take hours or days with hundreds or thousands of records. The result? Delayed insights, annoyed stakeholders, and data gaps. For more on DCVS woes, see [Barry Mann’s Medium article](https://barrymann2.medium.com/adobe-aep-solving-dcvs-ingestion-errors-fdfa93285a78).

### The Solution
AEP_DCVS_BatchBlaster tackles DCVS errors with a four-step blast:
1. **Batch Retrieval**: Queries the AEP API for all batches failed in the last 24 hours.
2. **Detail Download**: Grabs NDJSON files with failure specifics for each batch.
3. **Insight Extraction**: Parses DCVS errors (`DCVS-1104-400`, `DCVS-1111-400`, `DCVS-1106-400`, `DCVS-1105-400`), messages, and fields like eVar245.
4. **Report Generation**: Outputs dated CSV files with error counts and details, so you can fix root causes (e.g., schema tweaks or data cleanup).

It’s scoped to DCVS errors—ingestion issues like `INGEST-1002-400` are out of scope. Built for daily use within AEP, it clears old outputs each run for fresh results.

## Prerequisites
- **Environment**: Runs inside **AEP Platform Jupyter Notebook** (Data Science Workspace). No local Python or dependency installs needed—everything’s preloaded.
- **AEP API Access**: You’ll need:
  - Client ID
  - Client Secret
  - Organization ID
  - Get these via a two-part OAuth token from [Adobe Developer Console](https://developer.adobe.com/console/43621/home) (see "Setup" below).

## Setup
1. **Open AEP Jupyter Notebook**:
   - Log into AEP, go to Data Science Workspace, and start a Jupyter Notebook.
2. **Paste the Script**:
   - Copy all of `AEP_DCVS_BatchBlaster.py`, paste it into a new notebook cell.
3. **Update Credentials**:
   - Replace the placeholder API credentials with yours from [Adobe Developer Console](https://developer.adobe.com/console/43621/home):
     ```python
     CLIENT_ID = "2c8dcae8d9ff466c9f******"
     CLIENT_SECRET = "p8e-RkRfvr30n93******"
     ORG_ID = "988D095F54BD18520A******@AdobeOrg"


     Running the Script
Execute:
In your AEP Jupyter Notebook, hit Shift+Enter on the cell with the script.
Runtime: Takes ~10 minutes, depending on batch volume. CPU will hit 100%—normal for the heavy lifting.
Output:
A folder like output_DD_MMMM_YYYY (e.g., output_23_March_2025) appears in your notebook’s working directory.
Inside:
failed_batches_last24hrs_prod_DD_MMMM_YYYY.csv: Failed batch metadata.
failed_batches_ndjson/: NDJSON files with error details.
evar245_dcvserrors_with_message_count_DD_MMMM_YYYY.csv: DCVS error summary by code, message, and eVar245.
Logging: Check the notebook output for logs—progress, errors, and completion.
Usage Tips
Daily Run: Kick it off each morning to catch yesterday’s failures. It wipes the same-day output folder for a clean slate.
Results: Open CSVs in Excel or similar. High-count errors (e.g., DCVS-1111-400) signal where to fix—schema or data issues.
Troubleshooting
Won’t Start?: Check your Client ID, Secret, and Org ID—typos are the enemy.
No Output?: Logs showing no failures means a clean AEP (yay!). Otherwise, scan logs for clues.
More Help: Dive into DCVS details with Barry Mann’s article.
Future Enhancements
Filter by specific DCVS codes.
Add email/Slack alerts for failures.
Expand beyond 24 hours.
Ideas? Open an issue or PR!
Notes
Scope: Targets DCVS errors (DCVS-1104-400, DCVS-1111-400, DCVS-1106-400, DCVS-1105-400). Ingestion errors (INGEST-1002-400) are out of scope—use AEP’s UI for those.
Performance: CPU-heavy due to NDJSON processing—expected behavior.
Contributing
Bugs or upgrades? Open an issue or pull request—let’s make it blastier!

License
Licensed under the BatchBlaster Attribution & Commercial Use License:

Free for non-commercial use with attribution to [Your Name].
Commercial use requires permission from [Your Name], acknowledgment, and a negotiated fee.
See LICENSE for details. Commercial inquiries: [Your Email].
Acknowledgments
Fueled by caffeine, DCVS frustration, and data pipeline love. Thanks to xAI’s Grok for the assist!
