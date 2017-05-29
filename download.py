# Imports the Google Cloud client library
from google.cloud import storage, exceptions
import io
import os
import sys

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("credentials/richcompute-767d27eac0c0.json")

    # Instantiates a client
    storage_client = storage.Client()
    
    # The name of the bucket
    bucket_name = 'richcompute'

    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        print('Error - Cannot find bucket {}.'.format(bucket_name))
        sys.exit(1)
    
    filename = 'data/transactions.json'
    
    blob = bucket.get_blob(filename)
    json = blob.download_as_string()
      
    with open("data/downloaded.json", "w") as jsonfile:
        print >> jsonfile, json
  
if __name__ == '__main__':
    main()
