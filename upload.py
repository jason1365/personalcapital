# Imports the Google Cloud client library
from google.cloud import storage, exceptions
import io
import os

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("credentials/richcompute-767d27eac0c0.json")

    # Instantiates a client
    storage_client = storage.Client()

    # print all existing buckets
    #for bucket in storage_client.list_buckets():
    #    print(bucket)
    
    # The name of the bucket
    bucket_name = 'richcompute'

    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        print('Error - Cannot find bucket {}.'.format(bucket_name))
        sys.exit(1)
    
    filename = 'data/transactions.json'
    
    with io.open(filename) as upload_file:
        blob = bucket.blob(filename)
        blob.upload_from_string(upload_file.read(),content_type='application/json')
     
    print "The public URL is {}".format(blob.public_url)
  
if __name__ == '__main__':
    main()
