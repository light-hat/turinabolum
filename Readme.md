<p align="center">
<img alt="Logo" src="assets/progesterone.png" height="100px">
</p>

<h1 align="center">Turinabolum</h1>

<p align="center">
In progress. This is going to be awesome. 
</p>

## Pre-release

> [!WARNING]
> This preview release implements microservices for dump processing and timeline building. The timeline is currently accessed via the Opensearch Dashboards interface. A nice web interface and other announced features will be implemented in the future.

## Quick start

```bash
sudo sysctl -w vm.max_map_count=512000
cd opensearch
rm -rf certs/
chmod +x generate-certs.sh
./generate-certs.sh
cd ..
chown -R 1000:1000 opensearch
sudo docker compose up -d --build
sudo docker compose exec os01 bash -c "chmod +x plugins/opensearch-security/tools/securityadmin.sh && bash plugins/opensearch-security/tools/securityadmin.sh -cd config/opensearch-security -icl -nhnv -cacert config/certificates/ca/ca.pem -cert config/certificates/ca/admin.pem -key config/certificates/ca/admin.key -h localhost"
```


Go to `https://127.0.0.1:5601`
