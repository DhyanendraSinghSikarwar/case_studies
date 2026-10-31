"""Decide a model version bump from change labels, tag a git repo, build a composite release id."""
import subprocess, sys, re, datetime

MAJOR = {"input-schema-change", "output-meaning-change", "label-set-change"}
MINOR = {"retrain-new-data", "new-optional-feature", "new-output-field"}
PATCH = {"preprocessing-bugfix", "threshold-tweak", "metadata-fix"}


def bump(version, labels):
    unknown = set(labels) - MAJOR - MINOR - PATCH
    if unknown:
        raise ValueError(f"unknown labels: {sorted(unknown)}")
    major, minor, patch = map(int, version.split("."))
    if set(labels) & MAJOR:
        return f"{major + 1}.0.0"
    if set(labels) & MINOR:
        return f"{major}.{minor + 1}.0"
    if set(labels) & PATCH:
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("no labels: refuse to release")


def release_id(version, data_version, sha):
    return f"{version}+data.{data_version}.git.{sha}"


def git(*a, cwd):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def latest(cwd):
    tags = git("tag", "--list", "model-v*", "--sort=-v:refname", cwd=cwd).splitlines()
    return re.sub(r"^model-v", "", tags[0]) if tags else "0.0.0"


if __name__ == "__main__":
    repo, data_version = sys.argv[1], sys.argv[2]
    labels = sys.argv[3:]
    cur = latest(repo)
    new = bump(cur, labels)
    sha = git("rev-parse", "--short=7", "HEAD", cwd=repo)
    rid = release_id(new, data_version, sha)
    git("tag", "-a", f"model-v{new}", "-m", f"release {rid}; labels={','.join(labels)}", cwd=repo)
    print(f"{cur} + {labels} -> {new}   id={rid}")
