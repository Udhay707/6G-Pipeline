Clone the PCF repo (forked by Yun) and build the image:

```bash
# clone the repo somewhere outside of this project folder.
git clone https://gitlab.eurecom.fr/yuntang/oai-cn5g-pcf.git

# checkout the develop branch
cd oai-cn5g-pcf
git checkout develop

# update the submodules
git submodule init
git submodule update

# build the image
docker build -t oai-pcf:local -f docker/Dockerfile.pcf.ubuntu .
```

Make sure the core network is using the local PCF image. Check `docker-compose-core.yaml` file and confirm that:

```yaml
...
    oai-pcf:
        container_name: "oai-pcf"
        image: oai-pcf:local
...
```