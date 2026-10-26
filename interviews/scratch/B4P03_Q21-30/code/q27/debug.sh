#!/usr/bin/env bash
# Ordered checks for "Service returns nothing". NOT executed here (no kubectl, no cluster).
NS=ml-serving; SVC=model-api
kubectl -n $NS get pods -l app=$SVC -o wide --show-labels      # 1 are pods Ready (1/1)? do labels match?
kubectl -n $NS get svc $SVC -o jsonpath='{.spec.selector}{"\n"}{.spec.ports}{"\n"}'   # 2 selector + ports
kubectl -n $NS get endpointslices -l kubernetes.io/service-name=$SVC   # 3 empty = no Ready pod matches
kubectl -n $NS describe pod -l app=$SVC | grep -A5 -i readiness      # 4 probe path/port, failures
kubectl -n $NS exec deploy/$SVC -- sh -c 'ss -ltn || netstat -ltn'  # 5 which address:port is bound
kubectl -n $NS port-forward deploy/$SVC 8080:8080                  # 6 bypass Service: does the app answer?
kubectl -n $NS run dbg --rm -it --image=curlimages/curl --restart=Never -- curl -sv http://$SVC.$NS.svc.cluster.local/healthz   # 7 via Service DNS
kubectl -n $NS get networkpolicy                                   # 8 anything isolating the pod?
kubectl -n $NS get ingress -o yaml                                 # 9 backend service name, port, path rewrite
