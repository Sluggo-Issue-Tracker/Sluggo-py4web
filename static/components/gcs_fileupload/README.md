# File Upload to GCS


### Configure the uploads bucket on GCS

* Create a bucket in one of your projects.  
* Create a "service account", with a name such as `filemanager@yourproject.iam.gserviceaccount.com`, where `filemanager` is the name of the "user" for the account, and `yourproject` is the name of the service account. 
* Download the json credentials for the above service account, and store them in a file in `private/gcs_keys.json` in this app.  Make sure the file is also in `.gitignore`!
* Go to the Google Cloud Console, then to Storage, then to Browse.  Click on the bucket options, and the service account with the permission _Storage Object Admin_ to the bucket permissions. 
* Set up the bucket for CORS.  Install `gsutils` if needed, then do:
    
    gsutil cors set cors_json_file.json gs://bucketname



### Notes

Due to an old Python on my Mac I had to do:

    export CLOUDSDK_PYTHON="/Users/path/to/anaconda3/envs/myenv/bin/python"