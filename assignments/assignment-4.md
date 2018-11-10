Assignment 4: Rolling Update
----------------------------

You probably haven't covered this in class. It gives you a chance to understand the
rolling update process.  So long as you are quick enough with your monitoring, you
should see new pods spinning up. Once the new pods are responding to health checks,
Kubernetes switches the service to the new pods and kills the old ones. This allows
a relatively smooth switchover between versions.

For extra marks, try observing the HTTP responses from the deployed application to
determine the point at which the switchover occurs.

The following steps are required to do the rolling update:
   * Build: `./step4/build.sh`
   * Apply the manifest: `kubectl apply -f step4/k8s_manifests`
   * use `kubectl get pods` to see pods shutdown and start in a rolling way
