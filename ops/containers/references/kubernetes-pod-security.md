# Kubernetes Workload Security

This reference covers workload manifests. Cluster-wide admission policy, control-plane configuration, CNI installation,
and operator installation require separate cluster-administration guidance and authority.

## Start with the Current Pod Security Standard

Check the Kubernetes version and current Restricted Pod Security Standard before authoring a workload. Linux-only
requirements differ for Windows pods, and the standard evolves across Kubernetes releases.

A typical Linux application container compatible with the Restricted profile includes:

```yaml
spec:
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: registry.example/app@sha256:<resolved-digest>
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        runAsNonRoot: true
```

`readOnlyRootFilesystem` and CPU or memory requests and limits are useful workload controls, but the Restricted Pod
Security Standard does not require them. Add them from the workload's writes and resource measurements. Supply explicit
writable volumes for paths that need persistence or temporary storage.

Use `kubectl apply --dry-run=server` only when the user has authorized access to the target cluster. Admission behavior
depends on namespace labels, policy engines, feature gates, and the server version; local schema validation cannot prove
admission.

## Limit Network Reachability

NetworkPolicy takes effect only when the cluster's network implementation enforces it. Confirm support before relying on
a policy. Start with namespace-appropriate default deny, then add the exact ingress, egress, peer selectors, IP ranges,
and ports the workload needs. Preserve DNS and control-plane access when required.

Changing a default-deny or allow policy can interrupt live traffic. Inspect selected pods and existing policies, then
apply only with authority for that namespace and blast radius. Verify both allowed and denied paths after deployment.

## Limit API Access

Disable automatic service-account token mounting when the workload does not call the Kubernetes API. Otherwise use a
dedicated service account and grant the smallest namespace-scoped verbs and resources required.

Use `resourceNames` for named-object access only when the client can make compatible requests. A `list` or `watch`
request restricted by `resourceNames` must include a matching `metadata.name` field selector. Prefer `get` for a known
ConfigMap or Secret when listing is unnecessary.

Workload identity can replace long-lived cloud credentials where the target provider supports it. Its annotations,
trust policy, and permissions are provider-specific, so consult the provider's current documentation.

## Validate the Workload

Validate the rendered manifest, inspect its image digests, and compare every container and init container with the
target Pod Security Standard. After an authorized deployment, inspect admission events, effective service-account
access, network behavior, writable paths, termination, and resource use. Record any exception and the policy that
approved it.
