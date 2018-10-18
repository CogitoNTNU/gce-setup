gcloud compute instances create cogito-%(id)s \
--project=%(project)s \
--image-family='tf-latest-gpu' \
--image-project=deeplearning-platform-release \
--zone='europe-west1-b' \
--metadata='install-nvidia-driver=True,ssh-keys=%(user)s:%(key)s' \
--maintenance-policy=TERMINATE \
--accelerator='type=nvidia-tesla-k80,count=1' \
--tags='http-server,https-server,tcp-all'
