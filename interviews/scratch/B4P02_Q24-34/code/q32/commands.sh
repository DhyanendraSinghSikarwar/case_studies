# NOT EXECUTED: none of these tools are installed here and there is no image to scan.
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 registry.example.com/team/model-api:1.4.0
trivy image --format json -o scan.json registry.example.com/team/model-api:1.4.0     # feed policy_check.py
trivy image --format cyclonedx -o sbom.cdx.json registry.example.com/team/model-api:1.4.0   # an SBOM
grype registry.example.com/team/model-api:1.4.0 --fail-on high
docker scout cves registry.example.com/team/model-api:1.4.0                          # check current docs
cosign sign registry.example.com/team/model-api@sha256:"$DIGEST"                      # sign the DIGEST, not the tag
cosign verify registry.example.com/team/model-api@sha256:"$DIGEST" --certificate-identity="$IDENTITY" --certificate-oidc-issuer="$ISSUER"
