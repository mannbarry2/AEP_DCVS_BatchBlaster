# AEP_DCVS_BatchBlaster

## Overview
**AEP_DCVS_BatchBlaster** is a Python script designed to resolve Data Collection Validation Service (DCVS) errors in Adobe Experience Platform (AEP). If you’re dealing with failed ingestion batches and unclear DCVS error codes, this tool automates the process of fetching failed batches, downloading error details, extracting insights, and generating actionable reports in about 10 minutes. Simply paste it into an AEP Jupyter Notebook, update your credentials, and let it run—no local setup required.

## The Business Problem
Data ingestion powers AEP’s analytics, personalization, and insights, but DCVS validation errors can disrupt workflows. These errors occur during ingestion validation and include:
- **`DCVS-1104-400`**: Data type mismatches (e.g., string where a number is expected).
- **`DCVS-1111-400`**: Missing required fields (e.g., a required eVar is absent).
- **`DCVS-1106-400`**: Enum violations (e.g., an invalid option in a list).
- **`DCVS-1105-400`**: Format errors (e.g., incorrect timestamp format).

Unlike ingestion errors (e.g., `INGEST-1002-400` for upload failures), DCVS errors are validation-specific and often undocumented. This leads to time-consuming manual investigations. Delays in fixing these errors impact data quality and insights.

## The Solution
**AEP_DCVS_BatchBlaster** automates DCVS error handling in four steps:
1. **Batch Retrieval**: Queries the AEP API for batches that failed in the last 24 hours.
2. **Detail Download**: Extracts NDJSON files containing error specifics.
3. **Insight Extraction**: Parses DCVS errors, messages, and key fields like eVars.
4. **Report Generation**: Creates CSV files summarizing errors to guide data fixes.

This tool focuses on DCVS errors—general ingestion failures (`INGEST-1002-400`) are out of scope. It’s optimized for daily use and clears old outputs each run for fresh results.

## Prerequisites
- **Environment**: Runs inside **AEP Platform Jupyter Notebook** (Data Science Workspace). No local setup required.
- **AEP API Access**: Requires the following credentials:
  - Client ID
  - Client Secret
  - Organization ID

These can be obtained via the [Adobe Developer Console](https://developer.adobe.com/console/43621/home).

## Setup
1. **Open AEP Jupyter Notebook**:
   - Log into AEP, go to Data Science Workspace, and start a Jupyter Notebook.
2. **Paste the Script**:
   - Copy `AEP_DCVS_BatchBlaster.py` and paste it into a new notebook cell.
3. **Update Credentials**:
   - Replace placeholder API credentials with your own:
     ```python
     CLIENT_ID = "your_client_id"
     CLIENT_SECRET = "your_client_secret"
     ORG_ID = "your_org_id"
     ```

## Running the Script
- **Execution**: Run the notebook cell with Shift+Enter.
- **Runtime**: Takes ~10 minutes, depending on batch volume.
- **Output**: Generates a folder like `output_DD_MMMM_YYYY` (e.g., `output_23_March_2025`). Inside:
  - `failed_batches_last24hrs_prod_DD_MMMM_YYYY.csv`: Metadata on failed batches.
  - `failed_batches_ndjson/`: NDJSON files with error details.
  - `evar245_dcvserrors_with_message_count_DD_MMMM_YYYY.csv`: DCVS error summary.
- **Logging**: The notebook output logs progress and any errors encountered.

## Usage Tips
- **Daily Runs**: Run it each morning to catch the previous day's failures.
- **Error Analysis**: Open CSVs in Excel to identify frequent issues (e.g., missing eVars, schema mismatches).

## Troubleshooting
- **Script Won’t Start?** Check your API credentials for typos.
- **No Output?** If logs show no failures, AEP is error-free.
- **Further Debugging?** Review the logs in the notebook for details.

## Future Enhancements
- Filtering by specific DCVS codes.
- Email/Slack alerts for failures.
- Expanding beyond the last 24 hours.

## Notes
- **Scope**: Targets DCVS errors (`DCVS-1104-400`, `DCVS-1111-400`, `DCVS-1106-400`, `DCVS-1105-400`). Ingestion errors (`INGEST-1002-400`) are out of scope.
- **Performance**: CPU-intensive due to NDJSON processing.

## Contributing
Have suggestions or found a bug? Open an issue or pull request.

## License
Licensed under the BatchBlaster Attribution & Commercial Use License:
- Free for non-commercial use with attribution.
- Commercial use requires permission, acknowledgment, and a negotiated fee.
- See LICENSE for details. For commercial inquiries, contact [Your Email].

## Acknowledgments
Fueled by data pipeline challenges and the need for a streamlined DCVS error resolution process.

