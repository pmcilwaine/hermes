# Baking

## Creating Hermes Linux

```
packer build -var version=$(date +%Y%m%d%H%M) -var base_ami=%amazon linux% -var image_name=hermes_linux base.json
```

## Creating Hermes SELinux

```
packer build -var version=$(date +%Y%m%d%H%M) -var base_ami=%hermes_linux% -var image_name=hermes_selinux selinux.json
```

## Create Jenkins Image

```
packer build -var version=$(date +%Y%m%d%H%M) -var base_ami=%hermes_linux% -var image_name=hermes_jenkins one_role.json
```
