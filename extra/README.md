# Extra info

## Virtual appliance

- Download Ubuntu 18.04.1 server from osboxes.org
- Run the following commands:

```
    sudo ufw allow in on cbr0
    sudo ufw allow out on cbr0
    sudo ufw default allow routed
    sudo ufw allow ssh
    sudo ufw enable
    
    sudo snap install microk8s --classic --edge
    sudo snap alias microk8s.docker docker
    sudo snap alias microk8s.kubectl kubectl
    microk8s.enable dns dashboard
    sudo add-apt-repository universe
    sudo apt install python3-pip
    docker pull python:3.7.0
    git clone https://github.com/alixedi/pyconuk-2018-k8s
```

- Add the following to your `~/.bashrc`:

```
    export PATH=$PATH:$HOME/.local/bin 
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
```

## RBAC

If RBAC is enabled on your cluster (which it should be in production environments),
this will restrict what an api client is allowed to do. To change this you can apply a service
account with the right permissions to a pod.

For the toy application, you can use rbac.yaml in this folder. You also have to add
`serviceAccount: provisioner` to the pod's spec.
