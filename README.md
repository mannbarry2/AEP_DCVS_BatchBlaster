# AEP_DCVS_BatchBlaster

## Overview

**AEP_DCVS_BatchBlaster** is a Python script designed to resolve Data Collection Validation Service (DCVS) errors in Adobe Experience Platform (AEP). If you’re dealing with failed ingestion batches and unclear DCVS error codes, this tool automates the process of fetching failed batches, downloading error details, extracting insights, and generating actionable reports in about 10 minutes.

Simply paste it into an AEP Jupyter Notebook, update your credentials, and let it run—no local setup required.

## The Business Problem

Data ingestion powers AEP’s analytics, personalization, and insights, but DCVS validation errors can disrupt workflows. These errors occur during ingestion validation and include:

- **`DCVS-1104-400`**: Data type mismatches (e.g., a string where a number is expected).
- **`DCVS-1111-400`**: Missing required fields (e.g., a required eVar is absent).
- **`DCVS-1106-400`**: Enum violations (e.g., an invalid option in a predefined list).
- **`DCVS-1105-400`**: Format errors (e.g., incorrect timestamp format or invalid date structure).

Unlike ingestion errors (e.g., `INGEST-1002-400` for upload failures), DCVS errors are validation-specific and often undocumented. This leads to time-consuming manual investigations, delaying fixes, impacting data quality, and holding up use cases!

Adobe Analytics is far more forgiving and isn't affected by these ingestion errors. Whether "1234" or 1234, it doesn’t matter. We had it easy for years. However, CJA, AJO, RT-CDP, and all other AEP applications are affected.

## The Solution

**AEP_DCVS_BatchBlaster** automates DCVS error handling in four steps:

1. **Batch Retrieval**: Queries the AEP API for batches that failed in the last 24 hours.
2. **Detail Download**: Extracts NDJSON files containing error specifics.
3. **Insight Extraction**: Parses DCVS errors, messages, and key fields like eVars.
4. **Report Generation**: Creates CSV files summarizing errors to guide data fixes.

This tool focuses on DCVS errors—general ingestion failures (`INGEST-1002-400`) are out of scope. It’s optimized for daily use and clears old outputs each run for fresh results. Future enhancements include automatic daily execution and configurable time periods (e.g., retrieving failures from the last 7 days).

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
- **Output**:
  - `failed_batches_last24hrs_prod_DD_MMMM_YYYY.csv`: A list of the failed batches only, corresponding to the red bars visible in the UX.
  - `failed_batches_ndjson/`: The actual NDJSON files with error details. File size can be large, typically 600k - 1200k for 'daytime' batches and much smaller for nighttime. You can download batch files and inspect them manually, similar to Postman.
  - `evar245_dcvserrors_with_message_count_DD_MMMM_YYYY.csv`: DCVS error summary. This is the golden 'helicopter view' that will allow you to get a grip on your implementation!
- **Logging**: The notebook output logs progress and any errors encountered.

## Usage Tips

- **Daily Runs**: Planned as a future enhancement for automatic execution.
- **Extended Timeframes**: Configure it to fetch errors from the last 7 days if needed.
- **Error Analysis**: Open CSVs in Excel to identify frequent issues (e.g., missing eVars, schema mismatches).

## Troubleshooting

- **Script Won’t Start?** Check your API credentials for typos—usually the trickiest part.
- **No Output?** If logs show no failures, AEP is error-free. However, in practice, it's an ongoing game of whack-a-mole. Be use-case-led instead of trying to fix everything.
- **Further Debugging?** Review the logs in the notebook for details.

## Future Enhancements

- Email/Slack alerts for failures.
- Programmable longer duration, e.g., 7/14 days.
- Scheduling.

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

Thanks to various MeasureSlack community members for their valuable input.

For more insights, visit [Barry Mann's website](https://barrymann.com).

Fueled by data pipeline challenges and the need for a streamlined DCVS error resolution process.
