# Header: Adobe Batch Processing and Error Analysis Script
# Description: This script retrieves failed batches from Adobe API, downloads detailed failure data,
# extracts specific error information, and generates a summarized report with dated outputs.
# Author: Barry Mann barrymann.com
# Date: March 13, 2025 (Updated for March 23, 2025 output format)

import logging
import requests
import pandas as pd
import json
import os
import shutil
from datetime import datetime, timedelta
import time

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("AdobeBatchProcessor")

# --- Adobe API Credentials and Configuration ---
CLIENT_ID = "xxxx-xxxxxxxx"
CLIENT_SECRET = "p8e-xxxxxxfx0eIt8Z*****"
ORG_ID = "988D095F54BD18520A*****@AdobeOrg"

OAUTH_URL = "https://ims-na1.adobelogin.com/ims/token"
API_URL = "https://platform.adobe.io/data/foundation/catalog/batches"
PRODUCTION_SANDBOX = "prod"
META_SCOPE = "openid,AdobeID,read_organizations,additional_info.projectedProductContext,session"

# --- Output Directory Setup with Date (23 March 2025 Format) ---
CURRENT_DATE = datetime.now().strftime("%d_%B_%Y")  # e.g., 23_March_2025
BASE_OUTPUT_DIR = f"output_{CURRENT_DATE}"
FAILED_BATCHES_CSV = f"{BASE_OUTPUT_DIR}/failed_batches_last24hrs_prod_{CURRENT_DATE}.csv"
NDJSON_DIR = f"{BASE_OUTPUT_DIR}/failed_batches_ndjson"
FINAL_REPORT_CSV = f"{BASE_OUTPUT_DIR}/evar245_dcvserrors_with_message_count_{CURRENT_DATE}.csv"

# --- Clean Output Directory ---
# Purpose: Delete existing output folder contents if it exists
def clean_output_directory():
    if os.path.exists(BASE_OUTPUT_DIR):
        logger.info(f"Deleting previous contents of {BASE_OUTPUT_DIR}")
        shutil.rmtree(BASE_OUTPUT_DIR)
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    os.makedirs(NDJSON_DIR, exist_ok=True)
    logger.info(f"Created fresh output directory: {BASE_OUTPUT_DIR}")

# --- Authentication Block ---
# Purpose: Obtain OAuth token for Adobe API access
def get_oauth_token():
    logger.info("Requesting OAuth token...")
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": META_SCOPE
    }
    try:
        response = requests.post(OAUTH_URL, data=data)
        response.raise_for_status()
        logger.info("OAuth token received successfully.")
        return response.json()["access_token"]
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error retrieving token: {e}")
        raise

# --- Failed Batch Retrieval Block ---
# Purpose: Fetch failed batches from the last 24 hours
def get_failed_batches(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "x-api-key": CLIENT_ID,
        "x-gw-ims-org-id": ORG_ID,
        "x-sandbox-name": PRODUCTION_SANDBOX,
        "Accept": "application/json"
    }
    
    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int((datetime.utcnow() - timedelta(hours=24)).timestamp() * 1000)
    
    all_batches = {}
    limit = 100
    offset = 0
    
    while True:
        params = {
            "status": "failed",
            "createdAfter": start_time,
            "createdBefore": end_time,
            "limit": limit,
            "offset": offset,
            "orderBy": "desc:created"
        }
        
        logger.info(f"Fetching batches with offset {offset}")
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        batches = response.json()
        
        if not batches:
            break
        
        all_batches.update(batches)
        logger.info(f"Retrieved {len(batches)} batches")
        
        if len(batches) < limit:
            break
        
        offset += limit
    
    logger.info(f"Total failed batches retrieved: {len(all_batches)}")
    return all_batches

# --- Batch Processing and CSV Saving Block ---
# Purpose: Convert batch data to DataFrame and save as CSV with date
def process_and_save_batches(batches):
    batch_list = []
    for batch_id, batch_info in batches.items():
        batch_data = {
            "Batch ID": batch_id,
            "Status": batch_info.get("status"),
            "Created": datetime.utcfromtimestamp(batch_info.get("created") / 1000).strftime('%Y-%m-%d %H:%M:%S GMT'),
            "Updated": datetime.utcfromtimestamp(batch_info.get("updated") / 1000).strftime('%Y-%m-%d %H:%M:%S GMT')
        }
        
        related_objects = batch_info.get("relatedObjects", [])
        for idx, obj in enumerate(related_objects):
            batch_data[f"Related Object {idx+1} Type"] = obj.get("type", "N/A")
            batch_data[f"Related Object {idx+1} ID"] = obj.get("id", "N/A")
        
        batch_list.append(batch_data)

    df = pd.DataFrame(batch_list)
    
    # No need to delete here since clean_output_directory handles it
    df.to_csv(FAILED_BATCHES_CSV, index=False)
    logger.info(f"Failed batch data saved to '{FAILED_BATCHES_CSV}'")
    return df

# --- NDJSON Download Block ---
# Purpose: Download detailed failure data for each batch as NDJSON
def process_failed_batches(failed_batches_df, access_token):
    total_batches = len(failed_batches_df)
    logger.info(f"Processing {total_batches} failed batches for NDJSON download...")
    
    for index, row in failed_batches_df.iterrows():
        failed_batch_id = row['Batch ID']
        logger.info(f"Processing batch {index + 1}/{total_batches}: Batch ID {failed_batch_id}")
        
        api_url = f"https://platform.adobe.io/data/foundation/export/batches/{failed_batch_id}/failed"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-api-key": CLIENT_ID,
            "x-gw-ims-org-id": ORG_ID,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            
            if 'data' in json_data and json_data['data']:
                for file_info in json_data['data']:
                    file_href = file_info['_links']['self']['href']
                    file_name = file_href.split('path=')[-1]
                    logger.info(f"Found file: {file_name}")
                    
                    download_url = f"https://platform.adobe.io/data/foundation/export/batches/{failed_batch_id}/failed?path={file_name}"
                    download_response = requests.get(download_url, headers=headers)
                    
                    if download_response.status_code == 200:
                        file_path = os.path.join(NDJSON_DIR, f"{failed_batch_id}.ndjson")
                        with open(file_path, 'w') as f:
                            f.write(download_response.text)
                        logger.info(f"Saved NDJSON for Batch ID {failed_batch_id} to {file_path}")
                    else:
                        logger.error(f"Download failed for Batch ID {failed_batch_id}, Status: {download_response.status_code}")
            else:
                logger.warning(f"No file data found for Batch ID {failed_batch_id}")
        except Exception as e:
            logger.error(f"Error processing batch {failed_batch_id}: {e}")

# --- Error Extraction and Reporting Block ---
# Purpose: Extract error details from NDJSON files and generate a summary report with date
def extract_and_report_errors():
    evar245_values = []
    dcvs_error_codes = []
    dcvs_error_messages = []
    counter = 0
    
    if not os.path.exists(NDJSON_DIR):
        logger.error(f"NDJSON directory '{NDJSON_DIR}' does not exist.")
        return
    
    logger.info(f"Extracting error data from NDJSON files in {NDJSON_DIR}")
    for filename in os.listdir(NDJSON_DIR):
        if filename.endswith('.ndjson'):
            file_path = os.path.join(NDJSON_DIR, filename)
            logger.info(f"Processing file: {file_path}")
            
            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        counter += 1
                        
                        # Extract eVar245
                        evar245_value = record.get('body', {}).get('xdmEntity', {}).get('_experience', {}).get('analytics', {}).get('customDimensions', {}).get('eVars', {}).get('eVar245')
                        evar245_values.append(evar245_value)
                        
                        # Extract DCVS errors
                        error = record.get('_errors', {}).get('_streamingValidation', [{}])[0]
                        dcvs_error_codes.append(error.get('code'))
                        dcvs_error_messages.append(error.get('message'))
                        
                        if counter % 100 == 0:
                            logger.info(f"Processed {counter} records...")
                    except json.JSONDecodeError:
                        continue
    
    # Create and save report
    df = pd.DataFrame({
        'DCVS_Error_Code': dcvs_error_codes,
        'Message': dcvs_error_messages,
        'evar245': evar245_values
    })
    
    grouped_df = df.groupby(['DCVS_Error_Code', 'Message', 'evar245']).size().reset_index(name='Count')
    sorted_df = grouped_df.sort_values(by='Count', ascending=False)
    
    logger.info("Generated report preview:")
    logger.info(sorted_df.head().to_string())
    
    if not sorted_df.empty:
        sorted_df.to_csv(FINAL_REPORT_CSV, index=False)
        logger.info(f"Processed {counter} records. Report saved to {FINAL_REPORT_CSV}")
    else:
        logger.warning("No data extracted. Report is empty.")

# --- Main Execution Block ---
# Purpose: Orchestrate the entire workflow
def main():
    start_time = time.time()
    logger.info("Starting Adobe Batch Processing Script...")
    
    try:
        # Step 0: Clean output directory
        clean_output_directory()
        
        # Step 1: Get token and failed batches
        token = get_oauth_token()
        failed_batches = get_failed_batches(token)
        failed_batches_df = process_and_save_batches(failed_batches)
        
        # Step 2: Download NDJSON details
        process_failed_batches(failed_batches_df, token)
        
        # Step 3: Extract errors and generate report
        extract_and_report_errors()
        
    except Exception as e:
        logger.error(f"Main process error: {e}")
    
    end_time = time.time()
    logger.info(f"Script completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()