# NOT EXECUTED here (no helm binary, download blocked). Typical flow, check `helm help` for your version.
helm lint ./chart/modelserver                                  # static checks on chart structure and templates
helm template churn ./chart/modelserver -f prod.yaml           # render YAML locally, no cluster needed
helm install churn ./chart/modelserver -n ml -f prod.yaml --set image.tag=1.4.2
helm upgrade churn ./chart/modelserver -n ml -f prod.yaml --set image.tag=1.4.3
helm history churn -n ml                                       # one row per revision
helm rollback churn 1 -n ml                                    # creates a NEW revision with revision 1's content
helm get values churn -n ml                                    # values the release was installed with
kubectl get secret -n ml -l owner=helm                         # release records: sh.helm.release.v1.churn.v<N>
