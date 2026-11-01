"""Docker-built images are OCI-compatible. Classify manifest media types from two samples."""
import json
SAMPLES = {
  "older docker v2 manifest": {"schemaVersion": 2, "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "config": {"mediaType": "application/vnd.docker.container.image.v1+json"},
      "layers": [{"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip"}]},
  "OCI manifest": {"schemaVersion": 2, "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "config": {"mediaType": "application/vnd.oci.image.config.v1+json"},
      "layers": [{"mediaType": "application/vnd.oci.image.layer.v1.tar+gzip"}]},
}
for name, m in SAMPLES.items():
    fam = "OCI" if "oci" in m["mediaType"] else "Docker schema 2"
    print(f"{name:26} -> {fam}; layers are tar+gzip: {all('gzip' in l['mediaType'] for l in m['layers'])}")
print("A CRI runtime (containerd, CRI-O) pulls and runs both; the 'Docker' in the image format is just a format.")
