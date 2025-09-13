<p align="center">
<img alt="Logo" src="assets/progesterone.png" height="100px">
</p>

<h1 align="center">Turinabolum</h1>

<p align="center">
In progress. This is going to be awesome. 
</p>

> [!NOTE]
> This is a web service for automating the investigation of cybersecurity incidents.

> [!IMPORTANT]
> The idea of ​​the service: an investigation case is created for an incident, one or more dumps are loaded to the case, then the service extracts all the information from the dumps and looks for matches in Threat Intelligence feeds.

> [!TIP]
> As a result, the service should build a timeline of events and display matches in TI feeds, forming an approximate course of the attack, thereby removing a lot of routine work from the investigator. 

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
