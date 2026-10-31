**Follow-ups:**
- Could you align the two spaces with a learned linear map? Sometimes approximately, but it needs paired data and loses quality; a full re-embed is the safe answer when the corpus is not huge.
- What if the corpus is huge? Migrate by shard into a new index while serving from the old, and switch only when the whole index is on one version; never mix inside one search.
- What belongs on the deploy gate? Fixed-query hit rate by segment, the embedding version tag check, and a latency check.

**Common mistakes:**
- Embedding only new documents with the new model "to save cost".
- Merging results from two indexes by raw similarity score.
- No model-version metadata, so nobody can tell which vectors are which.
- Judging only the overall hit rate and missing the old-versus-new split.
- Rebuilding the index in place with no rollback copy.
