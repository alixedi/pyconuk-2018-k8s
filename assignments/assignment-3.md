Assignment, run step 3: 
   * Remove the old service and deployment:
    ```
    kubectl delete service webconsole
    kubectl delete deployment webconsole
    ```
   * Build: `./step3/build.sh`
   * Apply the manifest: `kubectl apply -f step3/consolehub/deployment.yaml`
   * grab the service ip:
   `export CONSOLEHUB_IP=$(kubectl get service consolehub -o go-template="{{ .spec.clusterIP  }}")`
   * Use the application, check if the problem is solved, example:
    ```python
    import requests
    import os
    requests.post(f'http://{ os.environ["CONSOLEHUB_IP"] }/api/paul/start/').json()
    requests.post(f'http://{ os.environ["CONSOLEHUB_IP"] }/api/paul/run/',
                    json={'input': 'a = 1'}).json()
    requests.post(f'http://{ os.environ["CONSOLEHUB_IP"] }/api/paul/run/',
                    json={'input': 'print(a)'}).json()
    ```
