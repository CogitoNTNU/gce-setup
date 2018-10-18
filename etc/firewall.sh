gcloud compute firewall-rules create tcp-all \
--action allow \
--rules 'tcp:0-65535' \
--target-tags 'tcp-all'
