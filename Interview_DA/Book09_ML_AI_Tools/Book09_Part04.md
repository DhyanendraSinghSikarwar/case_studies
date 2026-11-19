# Book 9 — Basic ML + AI Tools for Analysts | Part 4: Clustering and Customer Segmentation (k-means, RFM) 🟡

**Target:** 60 questions | **Actual:** 66 questions
**Scope:** clustering vs classification, k-means mechanics and sklearn code, choosing k, scaling, RFM scoring and segment actions, validating and presenting segments, with HR flavour where natural.

### Q1 ⭐⭐⭐ 🟢 What is clustering, and how is it different from classification?
**Asked at:** commonly asked (no company-specific report found); the question appears in fresher-level ML question banks (AmbitionBox, InterviewBit style lists, seen only as search snippets, unverified as real company questions).
**What the interviewer is checking:** Whether you know the difference between "no answer column" (unsupervised) and "known answer column" (supervised).
**Say this in the interview:** "Clustering groups similar records together without being told the groups in advance. Classification predicts a known label, like 'will leave' or 'will stay', using past examples where the answer is already known."
**Explain simply:**
- A **label** is the answer column you want to predict (for example `left_company = Yes/No`). **Features** are the columns used to predict it (tenure, salary, absence days).
- Classification is **supervised**: it learns from rows that already have labels, then predicts the label for new rows.
- Clustering is **unsupervised**: there is no label. The algorithm only looks at how close records are to each other and forms groups.
- Output differs too: classification gives a known category (and often a probability); clustering gives group numbers (0, 1, 2) that you must name yourself after studying them.
**Worked example (concept questions):** HR has 1,000 past employees with a column "left within a year". A classifier learns from that column and predicts whether a new joiner is likely to leave. With the same 1,000 rows but no such column, clustering might still find, say, "new and disengaged", "long-serving and stable" and "high-absence" groups.
**Alternative / pitfalls:** Clusters are not "true" categories; they depend on the features you chose and how you scaled them. Do not report them as facts about people.
**Likely follow-ups:** 1) *Name a clustering and a classification algorithm.* K-means for clustering; logistic regression or decision tree for classification. 2) *Can you check a clustering against labels?* Only if some labels exist for a side check; usually you judge by business usefulness.
**Common mistakes:** Calling clustering "classification without labels" and stopping there; expecting clusters to have names automatically; mixing up supervised and unsupervised.

### Q2 ⭐⭐⭐ 🟢 What is customer segmentation, and why do businesses do it?
**Asked at:** commonly asked (no company-specific report found); segmentation prompts appear in candidate-shared lists (for example a Flipkart Glassdoor snippet about analysing customer behaviour, unverified).
**What the interviewer is checking:** That you connect segmentation to a business action, not just to an algorithm.
**Say this in the interview:** "Segmentation splits customers into groups that behave alike, so each group can get a different offer, message or service. It is done because one-size-fits-all marketing wastes money and misses what each group actually values."
**Explain simply:**
- A **segment** is a group of customers who are similar on something that matters (how recently, how often and how much they buy; their age band; their city).
- Why: targeted offers cost less and convert better, you can protect your best customers, win back customers who are drifting away, and spend budget where it pays.
- Segments can be rules (spend above 10,000 INR) or found by an algorithm (k-means).
- A segment is only useful if the business can act differently on it.
**Worked example (concept questions):** An online shop has 10,000 customers. A 10% discount to everyone costs the same for a loyal buyer who would have bought anyway and a lapsed buyer who needs a nudge. Giving the discount only to customers inactive for 90+ days spends the budget where it can change behaviour.
**Alternative / pitfalls:** Segments that cannot be reached (no contact data) or that no team acts on are decoration.
**Likely follow-ups:** 1) *Types of segmentation?* Demographic, behavioural, value-based (RFM), needs-based. 2) *How do you know it worked?* Compare a targeted group against a similar untargeted group (see Q52 in this part).
**Common mistakes:** Describing only the maths; creating too many segments to act on; ignoring privacy.

### Q3 ⭐⭐⭐ 🟢 Explain k-means clustering to a non-technical marketing manager in plain words.
**Asked at:** commonly asked (no company-specific report found); k-means explanation is the opening theme in most prep-site k-means lists (unverified); a Tiger Analytics (June 2020) technical round was reported to include k-means (single anonymous report seen as a snippet).
**What the interviewer is checking:** Whether you can explain without jargon and without drawing a formula.
**Say this in the interview:** "Imagine placing a few flags on a map of customers. Each customer joins the nearest flag, then each flag moves to the middle of its customers. We repeat until the flags stop moving. The groups around the flags are the segments."
**Explain simply:**
- You choose the number of groups (k) first, for example 4.
- "Nearest" is measured by distance on columns such as recency, frequency and spend.
- The "flag" is called a **centroid**: simply the average position of the group.
- It stops when no customer changes group. The result is k groups where members are close to their own group average.
- It does not name the groups; you read each group's averages and name it.
**Worked example (concept questions):** Customers described by "days since last purchase" and "orders per year". Flag A ends up at (10 days, 20 orders): frequent and recent. Flag B ends up at (120 days, 1 order): lapsed. Marketing now sees two different audiences.
**Alternative / pitfalls:** It works best when groups are roughly round and similar in size, and when columns are on the same scale (see Q7).
**Likely follow-ups:** 1) *How do you pick the number of groups?* Elbow, silhouette and business need (Q6). 2) *Is the result unique?* Not always; the starting flags matter (see Q39 in this part).
**Common mistakes:** Using formulas with a marketing audience; saying k-means "finds the true segments"; forgetting that someone has to name the groups.

### Q4 ⭐⭐⭐ 🟢 What are the steps of the k-means algorithm?
**Asked at:** commonly asked (no company-specific report found); a standard item in k-means question banks (Towards AI, vitalflux style, unverified).
**What the interviewer is checking:** That you know the assign-then-update loop and the stopping rule.
**Say this in the interview:** "Pick k and starting centroids; assign every point to its nearest centroid; recompute each centroid as the average of its points; repeat the last two steps until assignments stop changing or a maximum number of rounds is reached."
**Explain simply:**
- Step 1: choose k and place k starting **centroids** (group centres). sklearn uses a smart start called k-means++ so they begin spread apart.
- Step 2: **assign**: each point goes to the centroid with the smallest distance (usually straight-line Euclidean distance).
- Step 3: **update**: move each centroid to the mean of the points now in its group.
- Step 4: repeat steps 2 and 3 until nothing changes (converged) or the iteration limit is hit.
- Every round the total squared distance to the centroids can only stay the same or fall, so it always settles, but possibly on a "good enough" answer rather than the best one.
**Worked example (concept questions):** Q8 below runs one full round by hand with 4 points: P2 stays with c1, P3 switches to c2, and the centroids move to (1.5, 1) and (4.5, 3.5).
**Alternative / pitfalls:** Different starts can give different final groups, so run several starts (`n_init`).
**Likely follow-ups:** 1) *What does it minimise?* Within-cluster sum of squared distances (Q17). 2) *What if it does not converge?* It almost always does; raise `max_iter` if sklearn warns.
**Common mistakes:** Forgetting the update step; saying k-means uses medians (it uses means); skipping scaling.

### Q5 ⭐⭐⭐ 🟢 What does RFM stand for, and what does each letter measure?
**Asked at:** commonly asked (no company-specific report found); RFM definitions come from educational and vendor blogs (HubSpot style), not from reported interviews.
**What the interviewer is checking:** The three definitions, their direction (which way is good) and why they work together.
**Say this in the interview:** "Recency is how many days since the last purchase, frequency is how many purchases in the period, monetary is how much was spent in total. Low recency is good; high frequency and high monetary are good."
**Explain simply:**
- **Recency (R):** days between the last purchase and a reference date. Smaller is better, because a recent buyer is more likely to buy again.
- **Frequency (F):** number of orders (or active days) in the period. Larger is better.
- **Monetary (M):** total (or average) money spent. Larger is better.
- Together they describe a customer using only a transaction table: customer, date, amount.
- Typical use: score each from 1 to 5, or feed the three columns to k-means.
**Worked example (concept questions):** A customer with last order on 2026-03-25, 5 orders and 4,000 INR, measured on 2026-04-01, has R = 7 days, F = 5, M = 4,000 INR.
**Alternative / pitfalls:** The same idea works for employees (days since last training, number of trainings, hours): the letters stay, the meaning changes.
**Likely follow-ups:** 1) *Why is recency reversed when scoring?* Because fewer days is better, so the smallest days get the highest score. 2) *Monetary: total or average?* State your choice; total is common.
**Common mistakes:** Treating high recency as good; mixing up frequency (count) and monetary (value); forgetting the reference date.

### Q6 ⭐⭐⭐ 🟡 How do you choose the number of clusters k in k-means?
**Asked at:** a Tiger Analytics (June 2020) technical round was reported to ask about choosing k, and Fractal Glassdoor snippets mention the number of clusters (anonymous reports seen only as search summaries; exact mapping unverified); also common in prep-site lists.
**What the interviewer is checking:** That you use more than one tool and that you finish with business judgement.
**Say this in the interview:** "I try a range of k, look at the elbow in the inertia curve and at silhouette scores, check that the clusters are stable and large enough, and then pick the k that is both statistically reasonable and actionable for the business."
**Explain simply:**
- **Elbow method:** plot **inertia** (total squared distance of points to their centroid; lower is tighter) against k. Pick where the curve bends, because after that extra clusters add little.
- **Silhouette score:** for each point, how much closer it is to its own cluster than to the next one, from -1 to 1. Higher average is better.
- **Stability:** rerun with different seeds or on a sample; good clusters repeat.
- **Business need:** a team may only be able to run 4 campaigns, so 12 segments are no use.
**Worked example (concept questions):** Synthetic data with 3 real groups (300 points, seed 42, `make_blobs`), k from 2 to 6:

| k | Inertia | Silhouette |
|---|---|---|
| 2 | 5763.5 | 0.705 |
| 3 | 566.9 | 0.848 |
| 4 | 496.4 | 0.664 |
| 5 | 427.1 | 0.490 |
| 6 | 375.0 | 0.517 |

Inertia collapses at k = 3 and falls slowly afterwards; silhouette peaks at k = 3. Both agree.
**Alternative / pitfalls:** Real customer data rarely gives a clean bend; then lean on stability and interpretability (Q55, Q56).
**Likely follow-ups:** 1) *Why not pick the k with the lowest inertia?* Inertia always falls as k grows (k = number of points gives 0). 2) *Other methods?* Gap statistic, dendrogram (from memory, rarely needed).
**Common mistakes:** Relying on the elbow alone; picking k from inertia only; ignoring cluster size and usefulness.

### Q7 ⭐⭐⭐ 🟡 Why must you scale the features before running k-means, and how do you do it in sklearn?
**Asked at:** Fractal Glassdoor snippets mention normalising before k-means (anonymous, seen as search summaries, mapping unverified); common in k-means interview lists.
**What the interviewer is checking:** That you understand k-means uses distance, so big-number columns dominate.
**Say this in the interview:** "K-means is built on distances, so a column in thousands, like salary, drowns out a column in single digits, like rating. I standardise each column to mean 0 and spread 1 with StandardScaler before clustering."
**Explain simply:**
- **Scaling** means converting columns to comparable units. **Standardising** subtracts the column mean and divides by the column standard deviation (spread).
- Without it, the column with the largest numbers decides almost everything.
- After it, each column has mean 0 and standard deviation 1, so each counts about equally.
- Scale first, cluster second, and keep the scaler to treat new data the same way (Q47).
**Sample data:** five customers (`recency` in days, `monetary` in INR).
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame({
    "customer_id": ["C1", "C2", "C3", "C4", "C5"],
    "recency": [5, 40, 12, 90, 20],
    "monetary": [52000, 3000, 41000, 1500, 8000],
})

features = customers[["recency", "monetary"]]

# Subtract each column's mean and divide by its spread
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

print(scaled_features.round(2))
print("column means:", scaled_features.mean(axis=0).round(2))
print("column spreads:", scaled_features.std(axis=0).round(2))
```
**Output:**
```text
[[-0.93  1.46]
 [ 0.22 -0.86]
 [-0.7   0.94]
 [ 1.85 -0.93]
 [-0.44 -0.62]]
column means: [0. 0.]
column spreads: [1. 1.]
```
**What it means:** Both columns now sit on the same scale. Before scaling, the raw distance between C1 and C2 was about 49,000.01, where recency (a gap of 35 days) added almost nothing; after scaling, both columns matter.
**Alternative / pitfalls:** MinMaxScaler squeezes into 0 to 1 (Q58). Do not fit the scaler on data that includes future or test rows if you are evaluating a model; for segmentation, fit on the customers you are segmenting and reuse that scaler for new ones.
**Likely follow-ups:** 1) *Are tree models affected?* No, trees do not use distance. 2) *Must dummy (0/1) columns be scaled?* Think about it; they are already small.
**Common mistakes:** Forgetting to scale; scaling the customer_id; clustering raw INR next to counts.

### Q8 ⭐⭐⭐ 🟡 Perform one k-means iteration by hand: which cluster does P3 join, and what are the new centroids?
Points: P1 (1, 1), P2 (2, 1), P3 (4, 3), P4 (5, 4). Initial centroids: c1 = (1, 1) and c2 = (5, 4). Use Euclidean distance; the P1/P4 assignments are given by the centroids themselves, so assign P2 and P3 and recompute both centroids.
**Asked at:** commonly asked (no company-specific report found); hand-calculation of one k-means round is a standard question in prep-site lists (unverified).
**What the interviewer is checking:** Distance arithmetic and understanding of the assign-then-average loop.
**Say this in the interview:** "P3 is 1.41 from c2 and 3.61 from c1, so it joins c2. P2 joins c1. New centroids: c1 = (1.5, 1) and c2 = (4.5, 3.5)."
**Explain simply:**
- Euclidean distance = square root of (difference in x squared + difference in y squared).
- P2 to c1: sqrt(1) = 1.00; P2 to c2: sqrt(9 + 9) = 4.24, so P2 joins c1.
- P3 to c1: sqrt(9 + 4) = 3.61; P3 to c2: sqrt(1 + 1) = 1.41, so P3 joins c2.
- Clusters: {P1, P2} and {P3, P4}.
- New centroid = average of members: c1 = ((1+2)/2, (1+1)/2) = (1.5, 1); c2 = ((4+5)/2, (3+4)/2) = (4.5, 3.5).
**Sample data:** distances computed by script.

| Point | To c1 (1, 1) | To c2 (5, 4) | Joins |
|---|---|---|---|
| P1 | 0.000 | 5.000 | c1 |
| P2 | 1.000 | 4.243 | c1 |
| P3 | 3.606 | 1.414 | c2 |
| P4 | 5.000 | 0.000 | c2 |

**What it means:** After one round the centroids moved; a second round would find no point changing group, so k-means stops here.
**Alternative / pitfalls:** Comparing squared distances gives the same winner and skips the square root; sklearn does this internally.
**Likely follow-ups:** 1) *Would a second round change anything?* No: P1, P2 are closer to (1.5, 1) and P3, P4 closer to (4.5, 3.5). 2) *What if a cluster ended up empty?* Implementations re-seed it.
**Common mistakes:** Adding coordinates instead of squaring differences; forgetting to recompute centroids; averaging the wrong points.

### Q9 ⭐⭐⭐ 🟡 Using the table below, calculate recency in days, average order value and say which customer is the most recent buyer.
Reference date: 2026-04-01.
| Customer | Last purchase | Orders | Total spend (INR) |
|---|---|---|---|
| C1 | 2026-03-25 | 5 | 4,000 |
| C2 | 2026-01-10 | 12 | 9,600 |
| C3 | 2026-03-30 | 1 | 500 |
**Asked at:** commonly asked (no company-specific report found); a hands-on RFM calculation, not tied to a reported company question.
**What the interviewer is checking:** Date subtraction, a simple ratio, and reading "most recent" as the smallest recency.
**Say this in the interview:** "Recency is reference date minus last purchase: C1 is 7 days, C2 is 81, C3 is 2. Average order value is spend divided by orders: 800, 800 and 500 INR. C3 is the most recent buyer."
**Explain simply:**
- Recency (days) = 2026-04-01 minus last purchase date.
- Average order value (AOV) = total spend divided by number of orders.
- Most recent buyer = smallest recency, so C3 (2 days).
- Note C3 has a single order; recent does not mean loyal.
**Code (what you write in the interview):**
```python
import pandas as pd

customers = pd.DataFrame({
    "customer": ["C1", "C2", "C3"],
    "last_purchase": pd.to_datetime(["2026-03-25", "2026-01-10", "2026-03-30"]),
    "orders": [5, 12, 1],
    "total_spend": [4000, 9600, 500],
})

reference_date = pd.Timestamp("2026-04-01")

# Days between the reference date and the last purchase
customers["recency_days"] = (reference_date - customers["last_purchase"]).dt.days

# Average spend per order
customers["avg_order_value"] = customers["total_spend"] / customers["orders"]

print(customers)
```
**Output:**
```text
  customer last_purchase  orders  total_spend  recency_days  avg_order_value
0       C1    2026-03-25       5         4000             7            800.0
1       C2    2026-01-10      12         9600            81            800.0
2       C3    2026-03-30       1          500             2            500.0
```
**What it means:** C3 bought most recently (2 days ago) but has spent least; C2 buys often but went quiet 81 days ago, a possible win-back target.
**Alternative / pitfalls:** In Excel: `=DATE(2026,4,1)-B2`. January has 31 days, February 28 (2026), March 31, so Jan 10 to Apr 1 is 21 + 28 + 31 + 1 = 81; the script confirms it.
**Likely follow-ups:** 1) *Who has the highest frequency?* C2 with 12. 2) *Why might C1 and C2 have equal AOV?* Both spend 800 INR per order despite different volumes.
**Common mistakes:** Subtracting in the wrong direction (negative days); calling the largest recency the most recent; forgetting that 1 order gives AOV equal to total spend.

### Q10 ⭐⭐⭐ 🟡 Write pandas code that builds an RFM table (recency, frequency, monetary) per customer from an orders table.
Table `orders` has columns `customer_id`, `order_date` (datetime), `amount`. Use the day after the last order date in the data as the reference date.
**Asked at:** commonly asked (no company-specific report found); the hands-on RFM-table task is a typical analyst exercise, not a reported company question.
**What the interviewer is checking:** `groupby` with several aggregates and a sensible reference date.
**Say this in the interview:** "I set the reference date to the day after the last order, then group by customer: recency is reference date minus the customer's latest order, frequency is the order count, monetary is the sum of amount."
**Explain simply:**
- Using the day after the last order means the most recent buyer in the data has recency 1, not 0, and the result does not depend on when you run the code.
- `groupby("customer_id")` makes one row per customer.
- `agg` calculates three columns in one go: latest date, row count, amount sum.
**Sample data:** six orders, three customers (invented).
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.DataFrame({
    "customer_id": ["C1", "C1", "C2", "C2", "C2", "C3"],
    "order_date": pd.to_datetime(["2026-03-01", "2026-03-25", "2026-01-10",
                                  "2026-02-15", "2026-03-05", "2026-03-30"]),
    "amount": [1500, 2500, 3000, 3200, 3400, 500],
})

# Day after the last order in the data
reference_date = orders["order_date"].max() + pd.Timedelta(days=1)

rfm = orders.groupby("customer_id").agg(
    recency=("order_date", lambda dates: (reference_date - dates.max()).days),
    frequency=("order_date", "count"),
    monetary=("amount", "sum"),
).reset_index()

print(rfm)
```
**Output:**
```text
  customer_id  recency  frequency  monetary
0          C1        6          2      4000
1          C2       26          3      9600
2          C3        1          1       500
```
**What it means:** Reference date is 2026-03-31. C3 bought yesterday (recency 1) but only once; C2 has the highest spend and frequency but is 26 days quiet.
**Alternative / pitfalls:** First compute `last_order = orders.groupby("customer_id")["order_date"].max()` and subtract in a separate line if the lambda feels heavy. Refunds (negative amounts) should be handled first (Q33).
**Likely follow-ups:** 1) *How do you score them?* `pd.qcut` into 5 buckets (Q12). 2) *What if order_date is text?* Convert with `pd.to_datetime` first.
**Common mistakes:** Using `datetime.now()` so results change daily; forgetting `reset_index`; counting amount rows with `sum` instead of `count`.

### Q11 ⭐⭐⭐ 🟡 Write sklearn code that scales three RFM columns, fits k-means with 4 clusters, and attaches the cluster label to each customer.
DataFrame `rfm` has columns `customer_id`, `recency`, `frequency`, `monetary`.
**Asked at:** commonly asked (no company-specific report found); the standard scale-then-fit pattern from k-means tutorials and question banks (unverified).
**What the interviewer is checking:** The scale, fit, label pattern, and not including `customer_id` as a feature.
**Say this in the interview:** "I standardise the three RFM columns, fit KMeans with 4 clusters, a fixed random_state and several starts, and store the labels in a new `cluster` column. I then profile each cluster by its average R, F and M."
**Explain simply:**
- Pick only the three numeric columns; an ID is just a label, not a feature.
- `StandardScaler` puts them on the same scale.
- `n_init=10` runs 10 different starts and keeps the best; `random_state=42` makes the result repeatable.
- `fit_predict` fits and returns one cluster number per row.
**Sample data:** 12 invented customers (shows four visible groups).
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rfm = pd.DataFrame({
    "customer_id": ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12"],
    "recency":   [5, 8, 6, 40, 45, 38, 90, 100, 95, 20, 25, 150],
    "frequency": [20, 18, 22, 5, 6, 4, 2, 1, 2, 10, 12, 1],
    "monetary":  [50000, 45000, 52000, 12000, 14000, 10000, 3000, 2000, 2500, 25000, 28000, 1000],
})

# Put the three columns on the same scale (mean 0, spread 1)
rfm_scaled = StandardScaler().fit_transform(rfm[["recency", "frequency", "monetary"]])

# Fit k-means with 4 clusters; n_init=10 tries 10 starting points and keeps the best
kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

print(rfm)
print(rfm.groupby("cluster")[["recency", "frequency", "monetary"]].mean().round(1))
```
**Output:**
```text
   customer_id  recency  frequency  monetary  cluster
0           C1        5         20     50000        1
1           C2        8         18     45000        1
2           C3        6         22     52000        1
3           C4       40          5     12000        0
4           C5       45          6     14000        0
5           C6       38          4     10000        0
6           C7       90          2      3000        2
7           C8      100          1      2000        2
8           C9       95          2      2500        2
9          C10       20         10     25000        3
10         C11       25         12     28000        3
11         C12      150          1      1000        2
         recency  frequency  monetary
0           41.0        5.0   12000.0
1            6.3       20.0   49000.0
2          108.8        1.5    2125.0
3           22.5       11.0   26500.0
```
**What it means:** Cluster 1 is recent, frequent, high-spend (best customers); cluster 2 is long inactive with low spend; clusters 0 and 3 sit in between. The cluster numbers themselves mean nothing; they can change on another run or data (Q60). Output depends on the seed (42) and the data.
**Alternative / pitfalls:** `kmeans.fit(...)` then `kmeans.labels_` is the same thing. Note C12 (150 days) was pulled into cluster 2, a hint that outliers shape clusters (Q37).
**Likely follow-ups:** 1) *Why n_init?* Different starts can give different results; keep the best (Q39). 2) *How do you profile clusters?* Group by cluster and take means in original units, as above.
**Common mistakes:** Including `customer_id`; clustering unscaled data; reading cluster numbers as rankings.

### Q12 ⭐⭐⭐ 🟡 Given these 10 recency values (days since last purchase), assign R scores from 1 to 5 using quintiles, where 5 is the best score.
Recency days for 10 customers: 3, 5, 9, 14, 20, 30, 45, 60, 90, 120.
**Asked at:** commonly asked (no company-specific report found); RFM scoring is standard in educational RFM guides, not tied to a reported company question.
**What the interviewer is checking:** Quintiles (5 equal-sized buckets) and the reversed direction for recency.
**Say this in the interview:** "I cut the values into five equal-sized groups with qcut and give the label 5 to the smallest recency, since recent is best. With 10 customers that is two per score: 3 and 5 get 5; 9 and 14 get 4; 20 and 30 get 3; 45 and 60 get 2; 90 and 120 get 1."
**Explain simply:**
- A **quintile** splits sorted data into 5 groups of equal count (here 2 each).
- For recency, small is good, so labels run 5, 4, 3, 2, 1 from smallest to largest.
- The cut points are the 20th, 40th, 60th and 80th percentiles: 8.2, 17.6, 36.0 and 66.0 days.
**Code (what you write in the interview):**
```python
import pandas as pd

recency_days = pd.Series([3, 5, 9, 14, 20, 30, 45, 60, 90, 120])

# Smaller recency is better, so the labels run from 5 down to 1
r_score = pd.qcut(recency_days, q=5, labels=[5, 4, 3, 2, 1])

print(pd.DataFrame({"recency_days": recency_days, "R_score": r_score}))
```
**Output:**
```text
   recency_days R_score
0             3       5
1             5       5
2             9       4
3            14       4
4            20       3
5            30       3
6            45       2
7            60       2
8            90       1
9           120       1
```
**What it means:** Customers active within about 8 days score 5; those silent for more than about 66 days score 1.
**Alternative / pitfalls:** For frequency, many ties can break `qcut` ("bin edges must be unique"); use `pd.qcut(f.rank(method="first"), 5, labels=[1,2,3,4,5])`. Quintile scores are relative to your own customers, not absolute.
**Likely follow-ups:** 1) *What about F and M?* Same, but labels 1 to 5 in ascending order. 2) *Why not fixed day cut-offs?* They can be used if the business defines "active"; quintiles adapt to the data.
**Common mistakes:** Giving 5 to the largest recency; using `cut` (equal-width) instead of `qcut` (equal-count); not checking for ties.

### Q13 ⭐⭐⭐ 🟡 How is RFM segmentation different from k-means clustering, and when would you use each?
**Asked at:** commonly asked (no company-specific report found); a candidate-shared segmentation prompt reported a candidate answering only "RFM" and being pushed to go further (snippet, unverified).
**What the interviewer is checking:** That you see RFM as a rule-based scoring method and k-means as a data-driven grouping method.
**Say this in the interview:** "RFM scores each customer on three business-defined measures and combines the scores with rules, so it is simple, transparent and easy to explain. K-means lets the algorithm find the groups in the data, including on more than three features, but the results need profiling and naming. I start with RFM for explainability and use k-means when I want data-driven groups or more variables."
**Explain simply:**
- RFM: you decide the features (R, F, M) and the rules ("R >= 4 and F >= 4 is a Champion"). Same rules every month, easy to compare over time.
- K-means: features can be anything numeric; the groups come from distances. Labels are unstable run to run and need scaling.
- RFM is a **feature set**; k-means is an **algorithm**. You can run k-means on RFM columns (Q11), so they are not opposites.
- Use RFM for CRM campaigns that managers must understand; use k-means to discover patterns or include extra behaviour (categories bought, discount use).
**Worked example (concept questions):** RFM rule: "R >= 4 and F >= 4 = Champion" is stated on one line. A k-means group "recent, frequent, high spend" is described only after you look at its averages, and its boundary can shift when new data arrives.
**Alternative / pitfalls:** Combining both: k-means on scaled RFM, then name clusters with RFM-style labels.
**Likely follow-ups:** 1) *Which is more explainable?* RFM rules. 2) *Which needs scaling?* K-means.
**Common mistakes:** Treating them as the same thing; saying k-means is "better" without a reason; forgetting RFM needs a reference date.

### Q14 ⭐⭐⭐ 🟡 A manager asks you to split customers into high, medium and low value groups using their last 12 months of purchase history. What approach do you take?
**Asked at:** commonly asked (no company-specific report found); a "high, medium, low value from one year of purchases" prompt appears in candidate-shared lists (snippet, unverified as a real company question).
**What the interviewer is checking:** That you clarify the goal and start simple before reaching for an algorithm.
**Say this in the interview:** "I first clarify what 'value' means: revenue, profit or future potential. Then I build per-customer totals for the last 12 months, check the distribution, and start with simple rules such as spend terciles or the top 20% and next 30%. I only add RFM or k-means if the manager needs more than a spend ranking."
**Explain simply:**
- Clarify: value by revenue or margin? Include returns? Are new customers (under 12 months) treated differently? What will the groups be used for?
- Prepare data: one row per customer, total spend (net of refunds) and order count in the 12-month window.
- Group: e.g. top 20% = high, next 30% = medium, rest = low; or Pareto cut-offs from the business.
- Check: share of revenue by group, size of each group, a few sample customers.
- Present with plain names and one action each. Review quarterly.
**Alternative / pitfalls:** Spend alone ignores recency (a big spender who left). Add RFM if churn matters. Customers with one huge order can look "high value" but are not repeat buyers.
**Likely follow-ups:** 1) *Why not k-means directly?* Cut-offs from clustering are hard to explain; rules are easy for a manager to use. 2) *What cut-offs?* Agree them with the business and test sensitivity.
**Common mistakes:** Jumping to an algorithm without asking what "value" means; ignoring refunds; leaving out new customers without saying so.

### Q15 ⭐⭐⭐ 🟡 You have named segments such as Champions, Loyal, At Risk and Hibernating. What marketing or retention action would you suggest for each?
**Asked at:** commonly asked (no company-specific report found); segment names and actions come from RFM guides (HubSpot style), not from reported interviews.
**What the interviewer is checking:** That every segment ends in a specific, proportionate action.
**Say this in the interview:** "Champions get recognition and early access, Loyal customers get upsell and referral nudges, At Risk customers get a personal win-back offer before they are gone, and Hibernating customers get a low-cost reactivation attempt and then are suppressed if they do not respond."
**Explain simply:**
- **Champions** (bought recently, often, big): reward, early access, ask for reviews and referrals. Do not discount heavily; they already buy.
- **Loyal** (frequent, decent spend): loyalty points, cross-sell and bundles, move them toward Champion.
- **At Risk** (used to buy often, now silent): personal outreach, "we miss you" offer, ask for feedback. Highest return on effort.
- **Hibernating** (long inactive, low value): cheap reactivation email once or twice, then stop spending on them.
- Track each action's result; size the budget by segment value.
**Worked example (concept questions):** 10,000 customers: 5% At Risk (500 people). A 100 INR coupon to all 500 costs 50,000 INR at most; if 60 return and spend 1,500 INR each, revenue is 90,000 INR. Illustrative numbers only; test before scaling.
**Alternative / pitfalls:** HR twin: employees who were highly engaged but now show falling scores and rising absence are "at risk"; the action is a manager conversation, not a coupon.
**Likely follow-ups:** 1) *Why not discount Champions?* Margin loss with no extra purchases. 2) *How to check it worked?* Compare with a holdout group (Q52).
**Common mistakes:** One generic offer for all; naming segments without actions; spending the most on the least valuable group.

### Q16 ⭐⭐⭐ 🟡 How do you decide whether a set of customer segments is actually useful to the business?
**Asked at:** commonly asked (no company-specific report found); validating segments with business meaning appears in question-bank discussions (snippet, unverified).
**What the interviewer is checking:** That "useful" means distinct, sizeable, understandable, actionable and stable, not only a good silhouette score.
**Say this in the interview:** "I check that segments are clearly different from each other, big enough to matter, easy to describe, reachable with a different action, and stable over time. Then I test with a small campaign to see if the segments respond differently."
**Explain simply:**
- **Distinct:** averages differ clearly, and the differences matter in business terms.
- **Sizeable:** enough customers and revenue to justify a campaign.
- **Actionable:** you can reach them and treat them differently.
- **Explainable:** a manager can describe each in one sentence.
- **Stable:** similar groups come back on a re-run or next month (Q46).
- **Proven:** a pilot campaign or holdout test shows different behaviour (Q52).
**Alternative / pitfalls:** A statistically neat clustering can still be useless if the segments cannot be acted on.
**Likely follow-ups:** 1) *What metric would you quote?* Silhouette as a technical check, plus revenue share and response rate by segment. 2) *What if business wants fewer segments?* Merge similar ones and re-check.
**Common mistakes:** Judging only by silhouette; creating segments no one can act on; never testing with real behaviour.

### Q17 ⭐⭐ 🟢 What does k-means actually minimise, and what is inertia?
**Asked at:** commonly asked (no company-specific report found); the objective function is a standard theme in k-means question banks (unverified).
**What the interviewer is checking:** That you know the objective is within-cluster squared distance and that inertia reports it.
**Say this in the interview:** "K-means tries to make each cluster as tight as possible: it minimises the total squared distance from each point to its own cluster centre. sklearn reports that number as `inertia_`; lower means tighter clusters for the same k."
**Explain simply:**
- Take every point, measure the distance to its cluster centroid, square it, add them all up. That total is the **inertia** (also called within-cluster sum of squares).
- Squaring punishes far-away points more, which is why outliers pull centroids.
- Inertia always falls as k rises, so it cannot choose k on its own (elbow method uses its shape).
- Compare inertia only between runs on the same data and same scaling.
**Worked example (concept questions):** Cluster A: 1 and 3 (centroid 2): squared distances 1 + 1 = 2. Cluster B: 10 and 14 (centroid 12): 4 + 4 = 8. Inertia = 2 + 8 = 10 (checked by script).
**Alternative / pitfalls:** Different scaling gives different inertia numbers; they are not comparable across scalings.
**Likely follow-ups:** 1) *Why squared?* It is smooth and makes the mean the best centre. 2) *Is lower inertia always better?* Only for the same k.
**Common mistakes:** Saying it minimises distance between clusters; picking the lowest-inertia k; comparing inertia across differently scaled datasets.

### Q18 ⭐⭐ 🟢 Does k-means need labelled data, and what does that mean for how you judge the result?
**Asked at:** commonly asked (no company-specific report found); supervised versus unsupervised themes appear in fresher ML lists (unverified).
**What the interviewer is checking:** That you know there is no "accuracy" for clustering and can name other checks.
**Say this in the interview:** "No, k-means is unsupervised: it needs only features, no answer column. So there is no accuracy score; I judge it by internal measures like silhouette, by stability across runs, and above all by whether the segments make business sense and respond differently to actions."
**Explain simply:**
- Without labels there is no "correct" answer to compare against, so accuracy, precision and recall do not apply directly.
- **Internal checks:** inertia, silhouette score (how well separated clusters are).
- **Stability:** same groups on re-runs or samples.
- **Business checks:** can you name each group, and do they behave differently on something you did not cluster on (churn rate, revenue next quarter)?
- If labels exist later (for example "churned"), you can compare clusters with them as a side check, not as the goal.
**Alternative / pitfalls:** Beware of judging by a pretty plot only; a plot in 2D can hide overlap.
**Likely follow-ups:** 1) *Can you use labels to check?* Yes, as an external check if they exist. 2) *Would you report accuracy?* No.
**Common mistakes:** Quoting "accuracy" for clusters; trusting silhouette alone; skipping business review.

### Q19 ⭐⭐ 🟢 What does a high RFM score such as 555 mean, compared with 155 and 511?
**Asked at:** commonly asked (no company-specific report found); RFM score codes come from RFM guides, not reported interviews.
**What the interviewer is checking:** That you read each digit (R, F, M in order) and know 5 is best on each.
**Say this in the interview:** "The digits are R, F and M, each scored 1 to 5 with 5 best. 555 is a customer who bought recently, buys often and spends a lot: a top customer. 155 bought long ago but was frequent and high-spend, so a valuable customer who may be lost. 511 bought very recently but rarely and little, so a new or low-engagement customer."
**Explain simply:**
- Position matters: first digit R, second F, third M.
- Recency is scored so that recent = 5 (reversed from days).
- **555:** protect and reward.
- **155:** at risk of leaving; high past value, so run a win-back.
- **511:** probably a new customer; nurture toward a second and third order.
**Alternative / pitfalls:** Different combinations can have the same total (for example 155 and 551), so do not add the digits blindly; keep the digits or use named rules (Q27).
**Likely follow-ups:** 1) *What about 111?* Lost or lapsed, low value. 2) *Is 555 a rank?* It is a code, not a rank.
**Common mistakes:** Reading the digits in the wrong order; treating 155 as a bad customer; adding R, F and M as if equal in meaning.

### Q20 ⭐⭐ 🟢 How is k-means different from k-nearest neighbours (KNN)?
**Asked at:** a Tiger Analytics (June 2020) technical round was reported to include KNN and k-means (anonymous snippet, mapping unverified); k-means vs KNN is a classic bank question (unverified).
**What the interviewer is checking:** That you separate unsupervised grouping from supervised prediction, and the two different meanings of "k".
**Say this in the interview:** "K-means is unsupervised: it groups unlabelled data into k clusters. KNN is supervised: it predicts a label for a new point by looking at the k closest labelled points and taking a vote. The k in k-means is the number of clusters; the k in KNN is the number of neighbours."
**Explain simply:**
- K-means: no labels; learns centroids; outputs group numbers.
- KNN: needs labelled data; does no real training, it simply stores the data and looks up the neighbours at prediction time.
- Both use distance, so both need scaled features.
- K-means is for discovering segments; KNN is for predicting something known (will this employee leave?).
**Worked example (concept questions):** A new employee's 5 most similar past employees (by tenure, salary, engagement) include 4 who left: KNN with k = 5 predicts "likely to leave" (80% of neighbours). K-means, with no leave column, would just place the employee into a group.
**Alternative / pitfalls:** Both are distance-based, so unscaled features cause the same problem.
**Likely follow-ups:** 1) *Do both need scaling?* Yes. 2) *Which is supervised?* KNN.
**Common mistakes:** Saying the "k" is the same; thinking KNN builds clusters.

### Q21 ⭐⭐ 🟢 What is the difference between segments, cohorts and personas?
**Asked at:** commonly asked (no company-specific report found); a gap-fill concept question, not tied to a reported interview.
**What the interviewer is checking:** Three terms that sound alike but answer different questions.
**Say this in the interview:** "A segment is a group of customers who are similar now, for example by behaviour. A cohort is a group who share a starting event or time, like everyone who joined in January, tracked over time. A persona is a fictional, human-sounding profile that summarises a segment for storytelling."
**Explain simply:**
- **Segment:** based on characteristics or behaviour (RFM group). Customers can move between segments.
- **Cohort:** based on a shared start point (join month, first purchase month). Used to see retention or performance over time, for example "of January joiners, how many still active after 3 months".
- **Persona:** a made-up person ("Priya, 29, buys weekly on mobile") built from a segment's data to help teams remember who they are serving.
- HR twin: segment = engagement bands; cohort = the 2025 hiring batch; persona = "Ravi, a 5-year-tenure analyst who wants growth".
**Worked example (concept questions):** Of 200 joiners in January, 150 are still active at month 3: that cohort retention is 75%. Within the same people, "high spenders" is a segment, not a cohort.
**Alternative / pitfalls:** A persona must come from data, not imagination; otherwise it becomes stereotype.
**Likely follow-ups:** 1) *Can a cohort be segmented?* Yes. 2) *When use cohorts?* Retention and lifetime-value tracking.
**Common mistakes:** Using the words interchangeably; building personas with no data behind them.

### Q22 ⭐⭐ 🟡 Using the inertia values below, which k would you choose with the elbow method, and why?
k = 1 to 6, inertia: 1000, 520, 300, 260, 240, 228.
**Asked at:** commonly asked (no company-specific report found); reading an elbow curve is a standard exercise in clustering tutorials (unverified).
**What the interviewer is checking:** That you look at the size of each drop, not just the shape in general.
**Say this in the interview:** "I would choose k = 3. Inertia drops by 480, then 220, then only 40, 20 and 12. After k = 3 each extra cluster adds very little, so the elbow is at 3."
**Explain simply:**
- The elbow is where adding a cluster stops paying off.
- Drops computed from the table: k1 to k2: 480 (48%); k2 to k3: 220 (42.3% of the k = 2 value); k3 to k4: 40 (13.3%); k4 to k5: 20 (7.7%); k5 to k6: 12 (5%).
- Big gains until 3, small gains after: the bend is at k = 3.
- At k = 3 the clusters explain 70% of the starting variation (1000 down to 300).
**Sample data:**

| k | Inertia | Drop from previous k |
|---|---|---|
| 1 | 1000 | n/a |
| 2 | 520 | 480 |
| 3 | 300 | 220 |
| 4 | 260 | 40 |
| 5 | 240 | 20 |
| 6 | 228 | 12 |

**What it means:** Report k = 3 as a good statistical choice; k = 4 is a defensible alternative if the business wants one more group, because the loss is small. Confirm with silhouette and business meaning (Q6).
**Alternative / pitfalls:** If the bend were not clear, use silhouette and interpretability (Q55). Inertia alone never picks the "best" k, since it keeps falling.
**Likely follow-ups:** 1) *Would you choose k = 4?* Only if the business can use four segments and the extra group is meaningful. 2) *What if drops were 100, 90, 85, 80?* No elbow; use other methods.
**Common mistakes:** Picking the largest k because inertia is lowest; picking k = 2 because the first drop is biggest; ignoring business sense.

### Q23 ⭐⭐ 🟡 Using the silhouette scores below, which k looks best, and what else would you check before deciding?
k = 2, 3, 4, 5, 6 gives silhouette scores 0.41, 0.48, 0.55, 0.43, 0.36.
**Asked at:** commonly asked (no company-specific report found); "choosing the number of clusters" appears in unverified candidate reports (for example Fractal, Tiger Analytics) and silhouette is covered in sklearn and tutorial pages.
**What the interviewer is checking:** Whether you read a metric sensibly and know it is one input, not the final verdict.
**Say this in the interview:** "k = 4 has the highest silhouette (0.55), so it is the statistical favourite. Before deciding I would check cluster sizes, whether the segments make business sense, and whether they stay stable when I rerun with different seeds or samples."
**Explain simply:**
- The **silhouette score** measures, for each customer, how much closer they are to their own cluster than to the next nearest cluster. It runs from -1 to +1; higher means tighter, better separated groups.
- Scores rise from k = 2 to k = 4 (0.41, 0.48, 0.55), then fall (0.43, 0.36). The clear peak is at 4.
- Still check: (1) no cluster is tiny, (2) the profile of each cluster is describable and actionable, (3) the result is stable across seeds, (4) the elbow plot of inertia agrees, (5) the business can act on 4 groups.
- If the business needs 5 groups and 0.43 is not far behind, say so openly and present both.
**What it means:** Report: "k = 4, silhouette 0.55, cluster sizes and profiles checked." A score around 0.5 or more is usually read as reasonable structure (rough rule of thumb, from memory, unverified).
**Likely follow-ups:** 1) *Is 0.55 "good"?* It is moderate to good; relative comparison across k matters more than the absolute value. 2) *Does silhouette work for any cluster shape?* It favours round, similar-sized clusters.
**Common mistakes:** Picking the maximum without looking at the clusters; comparing silhouette scores across different scalings or feature sets.

### Q24 ⭐⭐ 🟡 Calculate the silhouette value of a single point where its average distance to its own cluster is 2 and its average distance to the nearest other cluster is 5. What would a value of -0.25 tell you?
**Asked at:** commonly asked (no company-specific report found); a silhouette calculation is a gap-fill question, not tied to a reported company.
**What the interviewer is checking:** That you know the formula and can interpret the sign.
**Say this in the interview:** "Silhouette = (b - a) / max(a, b). Here a = 2 and b = 5, so (5 - 2) / 5 = 0.6: the point sits comfortably in its cluster. A value of -0.25 means the point is closer to another cluster than to its own, so it is probably in the wrong cluster."
**Explain simply:**
- **a** = average distance from the point to the other members of its own cluster (smaller is better).
- **b** = average distance from the point to the members of the nearest other cluster (bigger is better).
- Close to +1: clearly belongs. Around 0: on the border between two clusters. Negative: looks misassigned.
- Calculation: (5 - 2) / max(2, 5) = 3 / 5 = 0.6.
- For -0.25, a is larger than b. For example a = 4 and b = 3 gives (3 - 4) / 4 = -0.25.
**What it means:** 0.6 is a well-placed point. -0.25 is a warning; if many points are negative, k may be too high, the clusters overlap, or the features do not separate the groups.
**Likely follow-ups:** 1) *How do you get one score for the whole model?* Average the silhouette of all points (`silhouette_score`). 2) *What if a cluster has one point?* Its silhouette is set to 0 by convention (from memory, unverified).
**Common mistakes:** Dividing by the sum instead of the larger of a and b; reading a negative value as "bad customer" rather than "awkward cluster fit".

### Q25 ⭐⭐ 🟡 Compute the inertia (within-cluster sum of squared distances) for the two clusters below.
One-dimensional data. Cluster A: 2, 4, 6. Cluster B: 10, 12.
**Asked at:** commonly asked (no company-specific report found); inertia and the k-means objective come up in k-means question banks (unverified).
**What the interviewer is checking:** That you know inertia is measured from each cluster's own average, not from the overall average.
**Say this in the interview:** "Cluster A has mean 4, so its squared distances are 4, 0 and 4, giving 8. Cluster B has mean 11, so 1 and 1, giving 2. Total inertia is 10."
**Explain simply:**
- **Inertia** = for every point, square the distance to its cluster centre (the cluster average), then add everything up. Smaller means tighter clusters.
- By hand: A: (2-4)² + (4-4)² + (6-4)² = 4 + 0 + 4 = 8. B: (10-11)² + (12-11)² = 1 + 1 = 2.
**Sample data:** `cluster_a = np.array([2, 4, 6])`, `cluster_b = np.array([10, 12])`
**Code (what you write in the interview):**
```python
# Inertia = sum of squared distances from each point to its own cluster mean
inertia_a = ((cluster_a - cluster_a.mean()) ** 2).sum()
inertia_b = ((cluster_b - cluster_b.mean()) ** 2).sum()

print("Cluster A:", inertia_a)
print("Cluster B:", inertia_b)
print("Total inertia:", inertia_a + inertia_b)
```
**Output:**
```text
Cluster A: 8.0
Cluster B: 2.0
Total inertia: 10.0
```
**What it means:** The total of 10 is the number k-means tries to minimise. On its own it has no meaning; compare it with the inertia for other values of k on the same data.
**Likely follow-ups:** 1) *Does sklearn `inertia_` match?* Yes, it is this same total. 2) *Why squared?* Squaring penalises far-away points more and makes the mean the best centre.
**Common mistakes:** Measuring from the grand mean (7.2) instead of each cluster's own mean; forgetting to square.

### Q26 ⭐⭐ 🟡 Compare the Euclidean distance between two customers before and after standardising, and explain what it shows.
Customer A: age 50, income 100,000. Customer B: age 30, income 40,000. Age has mean 40 and standard deviation 10; income has mean 60,000 and standard deviation 20,000.
**Asked at:** commonly asked (no company-specific report found); "normalise before k-means" appears in unverified candidate reports (for example Fractal).
**What the interviewer is checking:** That you understand why scaling matters for distance-based methods.
**Say this in the interview:** "On raw numbers the distance is about 60,000, and almost all of it comes from income; the 20-year age gap barely registers. After standardising, both features are in 'standard deviations' and the distance is 3.61, where age and income both contribute."
**Explain simply:**
- **Euclidean distance** is the straight-line distance: square each difference, add, take the square root.
- **Standardising** (z-score) = (value - mean) / standard deviation. It converts every feature to "how many standard deviations from average", so units no longer matter.
- Raw: sqrt(20² + 60,000²) = 60,000.0 (age adds only 400 to a sum of 3.6 billion).
- Scaled: A = (1, 2), B = (-1, -1); differences are 2 and 3; sqrt(4 + 9) = 3.61.
**Sample data:** Given in the question; the code below types it in.
**Code (what you write in the interview):**
```python
customer_a = np.array([50, 100000])
customer_b = np.array([30, 40000])
means = np.array([40, 60000])
stds = np.array([10, 20000])

# Distance on the raw numbers
raw_distance = np.sqrt(((customer_a - customer_b) ** 2).sum())

# Standardise: (value - mean) / standard deviation, then measure again
a_scaled = (customer_a - means) / stds
b_scaled = (customer_b - means) / stds
scaled_distance = np.sqrt(((a_scaled - b_scaled) ** 2).sum())

print("Raw distance:", round(raw_distance, 2))
print("Scaled A:", a_scaled, "Scaled B:", b_scaled)
print("Scaled distance:", round(scaled_distance, 2))
```
**Output:**
```text
Raw distance: 60000.0
Scaled A: [1. 2.] Scaled B: [-1. -1.]
Scaled distance: 3.61
```
**What it means:** Without scaling, k-means would effectively cluster on income alone. Scaling lets age count fairly.
**Likely follow-ups:** 1) *Which scaler?* `StandardScaler` is the usual default; `MinMaxScaler` squeezes to 0-1. 2) *Do you scale binary columns?* Be careful; see the categorical-data question.
**Common mistakes:** Comparing raw and scaled distances as if they were the same unit; scaling the full dataset including test data before a train/test split.

### Q27 ⭐⭐ 🟡 Apply the rules below to label each customer by RFM score.
Rules in order: Champions if R >= 4 and F >= 4; At Risk if R <= 2 and F >= 4; New if R >= 4 and F <= 2; otherwise Hibernating if R <= 2 and F <= 2; anything else Other.
| Customer | R | F | M |
|---|---|---|---|
| C1 | 5 | 5 | 5 |
| C2 | 1 | 5 | 4 |
| C3 | 2 | 1 | 1 |
| C4 | 4 | 2 | 3 |
| C5 | 3 | 3 | 3 |
**Asked at:** commonly asked (no company-specific report found); RFM segment naming is an educational-blog topic, not a reported interview question.
**What the interviewer is checking:** That you can turn business rules into code and apply them in order.
**Say this in the interview:** "I check the rules top to bottom and the first match wins. C1 Champions, C2 At Risk, C3 Hibernating, C4 New, C5 Other."
**Explain simply:**
- **R, F, M** are scores from 1 to 5 for Recency (how recently they bought), Frequency (how often) and Monetary (how much). 5 is best.
- C1: R 5, F 5 matches Champions. C2: R 1, F 5 is a once-loyal buyer gone quiet, At Risk. C3: R 2, F 1, low on both, Hibernating. C4: R 4, F 2, recent but few orders, New. C5: middle scores, matches nothing, Other.
- The order matters: a customer could match two rules, and the earlier one wins.
**Sample data:** The table in the question, loaded into a DataFrame called `customers`.
**Code (what you write in the interview):**
```python
def label_customer(row):
    # Rules are checked in the order given; the first match wins
    if row["R"] >= 4 and row["F"] >= 4:
        return "Champions"
    if row["R"] <= 2 and row["F"] >= 4:
        return "At Risk"
    if row["R"] >= 4 and row["F"] <= 2:
        return "New"
    if row["R"] <= 2 and row["F"] <= 2:
        return "Hibernating"
    return "Other"

customers["segment"] = customers.apply(label_customer, axis=1)
print(customers)
```
**Output:**
```text
  customer  R  F  M      segment
0       C1  5  5  5    Champions
1       C2  1  5  4      At Risk
2       C3  2  1  1  Hibernating
3       C4  4  2  3          New
4       C5  3  3  3        Other
```
**What it means:** Every customer gets exactly one label, which the marketing team can act on. Rules like these are business choices, so write them down.
**Likely follow-ups:** 1) *Where does M come in?* These rules ignore M; you could add a money rule for high spenders. 2) *Excel version?* Nested IF or IFS, same order.
**Common mistakes:** Putting a broad rule first so it swallows the specific ones; leaving gaps with no "Other" bucket.

### Q28 ⭐⭐ 🟡 Work out the average recency, frequency and monetary values of this cluster and suggest a label for it.
Customers in the cluster (recency in days, orders, spend in INR): (10, 8, 5,000), (20, 6, 4,000), (30, 10, 6,000).
**Asked at:** commonly asked (no company-specific report found); cluster profiling is a gap-fill question.
**What the interviewer is checking:** That you can turn cluster numbers into a business description.
**Say this in the interview:** "The averages are 20 days since last purchase, 8 orders and INR 5,000 spend. That is recent, frequent and high-spending, so I would call it 'Loyal high-value customers', in effect the Champions. I would confirm 'high' by comparing with the other clusters."
**Explain simply:**
- Recency average: (10 + 20 + 30) / 3 = 20 days. Frequency: (8 + 6 + 10) / 3 = 8 orders. Monetary: (5,000 + 4,000 + 6,000) / 3 = INR 5,000.
- A label only makes sense relative to the other clusters; "8 orders" is high only if the typical customer has 2.
- Keep the label to what the numbers show: recent, frequent, high spend. Do not invent traits (such as "price-sensitive") the data does not show.
**Sample data:** `cluster` DataFrame with columns `recency_days`, `orders`, `spend_inr` and the three rows above.
**Code (what you write in the interview):**
```python
print(cluster.mean())
```
**Output:**
```text
recency_days      20.0
orders             8.0
spend_inr       5000.0
dtype: float64
```
**What it means:** This is a "profile": one line describing the typical member. Tell the manager the label plus the three numbers behind it.
**Likely follow-ups:** 1) *Mean or median?* Median if there are outliers. 2) *What action?* Reward and retain: early access, loyalty perks.
**Common mistakes:** Labelling a cluster without comparing it to others; giving a label that sounds good but is not supported by the numbers.

### Q29 ⭐⭐ 🟡 Given the cluster sizes and revenue shares below, which segments deserve the most attention and why?
10,000 customers in total. Cluster sizes (customers): 4,000; 3,000; 2,000; 800; 200. Share of revenue: 10%, 20%, 20%, 25%, 25% respectively.
**Asked at:** commonly asked (no company-specific report found); a gap-fill interpretation question.
**What the interviewer is checking:** Whether you look at revenue per customer, not just totals, and think about both protection and growth.
**Say this in the interview:** "The smallest cluster, 200 customers (2%), brings 25% of revenue, about 12.5 times its headcount share. The next, 800 customers, brings 25% too. Those two are 10% of customers and half the revenue, so I protect them first, and then look at moving the big low-value group up."
**Explain simply:**
- Customer share = size / 10,000 = 40%, 30%, 20%, 8%, 2%.
- **Revenue index** = revenue share / customer share. Above 1 means the group earns more than its headcount; below 1, less.
- Cluster 5 (200 customers) has an index of 12.5 and cluster 4 about 3.1, while cluster 1 (4,000 customers) has 0.25.
- Losing a few customers in clusters 4 and 5 costs far more than losing the same number in cluster 1.
**Sample data:** `clusters` DataFrame with `customers` and `revenue_share_pct`.
**Code (what you write in the interview):**
```python
clusters["customer_share_pct"] = clusters["customers"] / clusters["customers"].sum() * 100

# Revenue share divided by customer share: above 1 means the group earns more than its headcount suggests
clusters["revenue_index"] = clusters["revenue_share_pct"] / clusters["customer_share_pct"]
print(clusters.round(2))
```
**Output:**
```text
   customers  revenue_share_pct  customer_share_pct  revenue_index
0       4000                 10                40.0           0.25
1       3000                 20                30.0           0.67
2       2000                 20                20.0           1.00
3        800                 25                 8.0           3.12
4        200                 25                 2.0          12.50
```
**What it means:** (Cluster 4 is exactly 3.125; the table shows 3.12 because of rounding.) Retention effort for the top two clusters; a cheap upgrade or cross-sell programme for the large low-index group.
**Alternative / pitfalls:** Revenue is not profit; a high-revenue group with heavy discounts or returns may be less valuable. Revenue concentration is also a risk: if one cluster is 25% of revenue from 200 people, a few departures hurt.
**Likely follow-ups:** 1) *Would you ignore cluster 1?* No; a small uplift on 4,000 customers can be large in total. 2) *What data next?* Margin, returns, churn rate per cluster.
**Common mistakes:** Focusing only on the biggest cluster by headcount; treating revenue share as profit.

### Q30 ⭐⭐ 🟡 Read the code below. What do `labels_`, `cluster_centers_` and `inertia_` contain, and what does the last line print?
```python
km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_scaled)
print(km.labels_[:5], km.cluster_centers_.shape, km.inertia_)
print(len(km.labels_) == len(X_scaled))
```
`X_scaled` has 500 rows and 4 columns.
**Asked at:** commonly asked (no company-specific report found); reading sklearn attributes is a gap-fill code-reading question.
**What the interviewer is checking:** That you know what a fitted k-means model stores.
**Say this in the interview:** "`labels_` is one cluster number per customer, 500 of them. `cluster_centers_` is the 3 centres, each with 4 numbers, shape (3, 4). `inertia_` is the total squared distance to the centres. The last line prints True because there is one label per row."
**Explain simply:**
- `labels_`: a list of 500 numbers (0, 1 or 2), the cluster of each customer in row order. `labels_[:5]` shows the first five.
- `cluster_centers_`: a 3 x 4 table; each row is the average position of a cluster across the 4 (scaled) features.
- `inertia_`: one number, the total squared distance of points to their centres (smaller = tighter).
- `random_state=42` makes the run repeatable; `n_init=10` tries 10 starting positions and keeps the best.
**Sample data:** `X_scaled` is not given, so the output below uses invented random data with three groups (seed 42, 500 rows, 4 columns). Your first five labels and inertia would differ with real data; the shape and the final True would not.
**Output:**
```text
[1 2 1 0 0] (3, 4) 1999.454322780442
True
```
**What it means:** Shape (3, 4) and True are fixed by the setup; the label numbers and inertia depend on the data. Cluster numbers (0, 1, 2) are arbitrary names, not rankings.
**Likely follow-ups:** 1) *How do I label new customers?* `km.predict(new_scaled)`. 2) *Are the centres in original units?* No, they are in scaled units; convert back or profile with the raw data.
**Common mistakes:** Thinking `labels_` is sorted or means "low to high"; reading the centres as raw rupee or day values.

### Q31 ⭐⭐ 🟡 What is wrong with this segmentation code, and how would you fix it?
```python
X = df[['customer_id', 'recency', 'monetary']]
km = KMeans(n_clusters=4).fit(X)
```
**Asked at:** commonly asked (no company-specific report found); a buggy-code review is a gap-fill question.
**What the interviewer is checking:** That you spot data-preparation mistakes that silently ruin clustering.
**Say this in the interview:** "Four problems: the customer ID is a label, not behaviour, so it must not be a feature; the features are not scaled, so monetary dominates; there is no `random_state`, so results change every run; and the cluster labels are never saved back to the customers."
**Explain simply:**
- **customer_id** is just a number that identifies someone. Clustering on it makes customers with nearby IDs look similar, which means nothing.
- **Scaling:** k-means uses distance, so a column in rupees swamps one in days. For two sample customers, 99.996% of the squared distance came from monetary, 0.004% from recency and almost nothing from the ID.
- **Randomness:** the start positions are random; fix `random_state` and use several starts (`n_init=10`).
- **Labels not kept:** use `fit_predict` and store the result.
- Also choose k from evidence (elbow, silhouette), not by default; here 2 is used for the tiny sample.
**Sample data:** 8 invented customers in `df` with `customer_id`, `recency`, `frequency`, `monetary`.
**Code (what you write in the interview):**
```python
# Use only behaviour columns (no ID) and put them on the same scale
features = df[["recency", "monetary"]]
X_scaled = StandardScaler().fit_transform(features)

# Fixed seed and several starts so the result is repeatable
km = KMeans(n_clusters=2, n_init=10, random_state=42)

# Keep the cluster label next to each customer
df["cluster"] = km.fit_predict(X_scaled)
print(df)
```
**Output:**
```text
   customer_id  recency  frequency  monetary  cluster
0         1001        5         20     50000        1
1         1002       12         15     42000        1
2         1003      300          1      1500        0
3         1004      280          2      2000        0
4         1005        8         18     47000        1
5         1006       15         14     39000        1
6         1007      310          1      1200        0
7         1008      290          2      2500        0
```
**What it means:** Recent, high-spend customers form cluster 1; lapsed, low-spend customers form cluster 0. The buggy code happens to give the same split here, because this sample is very clear-cut, but it would not on real data.
**Likely follow-ups:** 1) *Why not scale?* See Q26. 2) *Add frequency?* Yes, for full RFM.
**Common mistakes:** Leaving IDs, dates or categories as numeric inputs; trusting results that change on each run.

### Q32 ⭐⭐ 🟡 Why do analysts often apply a log transform to the monetary value before k-means, and what happens if they do not?
**Asked at:** commonly asked (no company-specific report found); a gap-fill preprocessing question.
**What the interviewer is checking:** That you understand skewed spending data and how outliers hijack k-means.
**Say this in the interview:** "Spend is right-skewed: most customers spend a little and a few spend a lot. Without a log transform, k-means spends its clusters on the few big spenders and lumps everyone else together. A log compresses the big values so the clusters describe the ordinary customers too."
**Explain simply:**
- **Skewed** means a long tail on one side. Spend is bounded at zero but has no upper limit.
- The **log transform** replaces each value with its logarithm; it turns "10x bigger" into "a fixed step bigger". `np.log1p` is log(1 + x) and handles zero safely.
- After the log, segment boundaries are in relative (percentage) terms, which often matches how marketers think.
**Worked example:** 300 invented customers with skewed spend (mean 1,692, median 1,006, max 20,209, which is 8 standard deviations above the mean). Three clusters on raw spend:
**Sample data:** `customers` DataFrame with one column `monetary` (generated with seed 42).
**Code (what you write in the interview):**
```python
customers["monetary_log"] = np.log1p(customers["monetary"])

for column in ["monetary", "monetary_log"]:
    scaled = StandardScaler().fit_transform(customers[[column]])
    labels = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(scaled)
    print(column, "cluster sizes:", np.bincount(labels))
```
**Output:**
```text
monetary cluster sizes: [270 27 3]
monetary_log cluster sizes: [ 85 158  57]
```
**What it means:** Raw spend gives one huge cluster of 270, and a cluster of just 3 whales. After the log, the three clusters are balanced and more useful. Remember to describe the clusters in original rupees afterward.
**Alternative / pitfalls:** Cap extreme values, or use ranks/quintile scores (as in RFM). Log needs non-negative values; refunds can make spend negative.
**Likely follow-ups:** 1) *Log of recency or frequency too?* Often yes if they are also skewed. 2) *Does log change the meaning?* Yes, distances become ratios.
**Common mistakes:** Forgetting to transform back when reporting; taking the log of zero or negative values.

### Q33 ⭐⭐ 🟡 How do you treat customers with a single purchase, and returns or refunds, when building RFM?
**Asked at:** commonly asked (no company-specific report found); a gap-fill RFM data-cleaning question.
**What the interviewer is checking:** Whether you handle the messy cases real order data has.
**Say this in the interview:** "I keep one-time buyers: frequency 1 is a real value, and they often form a 'new customer' group. For refunds I use net spend (sales minus refunds), count only real purchases for frequency, and flag fully refunded customers for separate review."
**Explain simply:**
- **Single purchase:** the customer has recency and monetary, frequency = 1. Do not drop them. Check whether they are recent (new) or old (one-and-done).
- **Refund rows** are usually negative amounts. If you leave them as "orders", frequency is inflated and a refunded customer looks active.
- Decide the rule with the business: net monetary is common; some teams exclude cancelled and fully returned orders entirely.
- For recency, a refund is not a purchase, so use the last real sale date.
**Worked example (numbers by script):** A bought twice (1,000 and 1,500), then returned the 1,500 order; B bought once (2,000); C bought once (800) and returned it.
**Sample data:** `orders` with `customer_id`, `order_date`, `amount` (refunds are negative).
**Code (what you write in the interview):**
```python
# Keep sales for frequency; use net amount (sales minus refunds) for monetary
sales = orders[orders["amount"] > 0]

rfm = sales.groupby("customer_id").agg(
    last_order=("order_date", "max"),
    frequency=("order_date", "count"),
)
rfm["monetary"] = orders.groupby("customer_id")["amount"].sum()

# Customers whose net spend is zero or negative were fully refunded: review them separately
print(rfm)
```
**Output:**
```text
            last_order  frequency  monetary
customer_id                                
A           2026-09-10          2      1000
B           2026-10-20          1      2000
C           2026-07-05          1         0
```
**What it means:** C has net spend of 0 and should not be treated as a customer worth marketing as "active"; B is a genuine one-time buyer.
**Alternative / pitfalls:** Matching each refund to its original order is more exact; the simple net amount is a good start. Very high refund rates may deserve their own flag.
**Likely follow-ups:** 1) *Many one-time buyers dominate a cluster?* Fine; it is a real segment, treat separately. 2) *Cancelled orders?* Exclude them before building RFM.
**Common mistakes:** Counting refunds as orders; dropping single-purchase customers; letting negative spend into the log transform.

### Q34 ⭐⭐ 🟡 How do you choose the reference date for recency, and what goes wrong if you pick it carelessly?
**Asked at:** commonly asked (no company-specific report found); a gap-fill RFM question.
**What the interviewer is checking:** That you know recency depends on a "today" and that it must match the data.
**Say this in the interview:** "I use a snapshot date: the day after the last order in the data, or the agreed analysis date if the data is complete up to it. I use the same date for every customer, and I record it so the analysis can be repeated."
**Explain simply:**
- **Recency** = reference date minus last purchase date. Everyone must use the same reference date, or the comparison is unfair.
- If the data stops on 30 Oct and you use today's date (19 Nov), every customer looks 20 days more "lapsed" than they are, and the scores shift.
- Using each customer's own latest date, or `max()` per customer, would make recency zero for everyone.
- Fixing the date also makes monthly reruns comparable: say "snapshot as of 31 Oct".
**Worked example (computed by script):** Last orders: A 30 Oct, B 1 Oct, C 15 Jun (all 2026).
**Sample data:** `orders` with `customer_id`, `order_date`.
**Code (what you write in the interview):**
```python
# Reference date = the day after the last order in the data (the snapshot date)
snapshot_date = orders["order_date"].max() + pd.Timedelta(days=1)

last_order = orders.groupby("customer_id")["order_date"].max()
recency_days = (snapshot_date - last_order).dt.days
print(snapshot_date.date())
print(recency_days)

# Careless choice: today's date (2026-11-19) when the data stops on 2026-10-30
careless_recency = (pd.Timestamp("2026-11-19") - last_order).dt.days
print(careless_recency)
```
**Output:**
```text
2026-10-31
customer_id
A      1
B     30
C    138
Name: order_date, dtype: int64
customer_id
A     20
B     49
C    157
Name: order_date, dtype: int64
```
**What it means:** The careless date adds 19 days to everyone; if the data has a gap, recent customers look inactive and the segments mislead.
**Alternative / pitfalls:** If the data feed lags (orders still arriving), pick a date after it is complete. Do not mix reference dates between months without saying so.
**Likely follow-ups:** 1) *Why +1 day?* So the most recent buyer has recency 1, not 0 (a convention). 2) *Does the choice change quintile scores?* Only if it differs between customers; a shared shift leaves ranks unchanged.
**Common mistakes:** Using `today()` in code that reruns later; different reference dates for different customers.

### Q35 ⭐⭐ 🟡 How many segments should you create in practice, and what limits the number?
**Asked at:** commonly asked (no company-specific report found); a gap-fill practical question related to choosing k.
**What the interviewer is checking:** Whether you balance statistics with what a business can actually act on.
**Say this in the interview:** "In practice, about 4 to 6, from statistics and from the business. A segment only exists if the business will treat it differently, so the number is limited by the marketing team's capacity, the size of each group and how stable the groups are."
**Explain simply:**
- **Statistical limit:** elbow and silhouette suggest a range, not one number.
- **Actionability:** each segment needs its own message or offer. If two segments get the same campaign, merge them.
- **Size:** very small groups are not worth a campaign or may be noise. For example, with 10,000 customers, a 2% segment is 200 people.
- **Stability:** the segment should survive a rerun next month or a different sample.
- **Understandability:** stakeholders remember about 5 groups; 15 are forgotten.
**Worked example:** 10,000 customers, 5 segments: a 2% segment is 200 customers, about right for a premium programme; a 0.1% segment (10 customers) would not be a segment, it is a list of exceptions.
**Alternative / pitfalls:** The "4 to 6" range is a common rule of thumb, not a law; a large retailer with many teams may use more.
**Likely follow-ups:** 1) *Business wants 8?* Show the benefit of each extra segment; merge those with the same action. 2) *Too few?* Segments become too general to act on.
**Common mistakes:** Letting the elbow method alone decide; creating segments no one has a campaign for.

### Q36 ⭐⭐ 🟡 One of your k-means clusters contains only 2 customers. What do you do?
**Asked at:** commonly asked (no company-specific report found); outlier handling in k-means appears in unverified candidate reports (for example Fractal).
**What the interviewer is checking:** That you investigate before acting, and recognise outliers pulling a cluster.
**Say this in the interview:** "A cluster of 2 is almost always outliers. I look at who they are first: genuine very big buyers, data errors, or test accounts. Then I handle them separately (set aside, cap, or log transform) and rerun with a sensible k."
**Explain simply:**
- Inspect the 2 customers: very high spend? Duplicated or test accounts? Wrong currency?
- If they are errors, fix or remove them. If they are real VIPs, treat them as a "key accounts" list managed by a person, and cluster the rest.
- Other options: log transform or cap values, or lower k so the small group merges.
**Worked example (computed by script, invented data):** 298 ordinary customers plus 2 with INR 900,000 and 1,200,000 spend and over 150 orders. k = 4 gives clusters of 104, 98, 96 and 2. The 2-customer cluster averages monetary 1,050,000 against 1,500 to 7,854 for the others.
**Sample data:** `customers` DataFrame with `recency`, `frequency`, `monetary` (300 rows; the last two are the whales).
**Code (what you write in the interview):**
```python
X_scaled = StandardScaler().fit_transform(customers)
customers["cluster"] = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X_scaled)

# How big is each cluster, and what does each one look like?
print(customers["cluster"].value_counts())
print(customers.groupby("cluster").mean().round(0))
```
**Output:**
```text
cluster
2    104
3     98
0     96
1      2
Name: count, dtype: int64
         recency  frequency  monetary
cluster                                
0          200.0        2.0     1500.0
1            6.0      165.0  1050000.0
2           29.0        8.0     7854.0
3          101.0        4.0     3846.0
```
**What it means:** Cluster 1 is a tiny group of extreme buyers, not a segment. Set them aside and the other 298 customers get three clear groups, a better use of k.
**Alternative / pitfalls:** Wasting a cluster on 2 people means you effectively have k - 1 useful clusters.
**Likely follow-ups:** 1) *Delete them?* Only if they are errors; real VIPs are valuable. 2) *Could a different algorithm help?* DBSCAN flags outliers explicitly (from memory, unverified details).
**Common mistakes:** Presenting a 2-person cluster as a "segment"; deleting outliers without checking that they are errors.

### Q37 ⭐⭐ 🟡 How do outliers affect k-means, and how do you handle them?
**Asked at:** commonly asked (no company-specific report found); outliers and k-means are named in unverified candidate reports (for example Fractal) and question banks.
**What the interviewer is checking:** That you understand centres are averages and averages are fragile.
**Say this in the interview:** "K-means centres are averages and distances are squared, so one extreme point pulls a centre towards it and can take over a cluster. I check for outliers first, then cap, transform or set them aside, depending on whether they are errors or real."
**Explain simply:**
- Squared distance makes far-away points count heavily in the objective, so k-means will try to accommodate them.
- Handling: (1) investigate (error or real?), (2) fix or remove errors, (3) log transform skewed features, (4) cap at a percentile, (5) set real extremes aside as a separate group, (6) consider a method more robust to outliers (k-medoids or DBSCAN; from memory, unverified).
**Worked example (computed by script):** Four customers spend 900 to 1,200 (average 1,050). Add one at 50,000: the average jumps to 10,840, a value no real customer is near. The median only moves to 1,100.
**Sample data:** `spend = np.array([900, 1000, 1100, 1200])` and the same list with 50000 appended.
**Code (what you write in the interview):**
```python
# One extreme customer drags the average (the k-means centre) far away from everyone else
print("Centre without outlier:", spend.mean())
print("Centre with outlier:", spend_with_outlier.mean())

# The median barely moves, which is why it is the safer summary
print("Median with outlier:", np.median(spend_with_outlier))
```
**Output:**
```text
Centre without outlier: 1050.0
Centre with outlier: 10840.0
Median with outlier: 1100.0
```
**What it means:** A centre of 10,840 describes nobody. K-means centres behave like the average, not the median, so they are vulnerable.
**Likely follow-ups:** 1) *How do you spot outliers?* Box plot, or values far beyond the 99th percentile. 2) *Always remove them?* No; high spenders may be your best customers.
**Common mistakes:** Removing outliers without asking the business; ignoring them and getting a cluster of 2.

### Q38 ⭐⭐ 🟡 What are the main limitations of k-means?
**Asked at:** commonly asked (no company-specific report found); k-means limitations appear in unverified candidate reports and question banks (for example Tiger Analytics, k-means vs hierarchical).
**What the interviewer is checking:** That you know where the method fails, not just how it works.
**Say this in the interview:** "You must choose k up front; it assumes roughly round, similar-sized clusters; it is sensitive to scale and outliers; it can land on a poor answer depending on the start; it works on numbers only; and it always returns clusters, even when the data has no real groups."
**Explain simply:**
- **Choose k yourself:** no automatic answer; elbow and silhouette only guide you.
- **Round clusters:** it draws straight boundaries around centres, so long, curved or nested shapes are cut badly.
- **Similar size and density:** it tends to split big clusters and merge small ones.
- **Scale and outliers:** both distort distances (see Q26, Q37).
- **Local best:** a random start can produce a worse answer (see Q39).
- **Numeric only:** categories need encoding or a different method (see Q41).
- **Hard assignment:** every customer belongs fully to one cluster; no "70% A, 30% B".
- **Always gives an answer:** clusters can be a mathematical accident; judge them with business sense and stability, not just a metric.
**Alternative / pitfalls:** Alternatives: hierarchical, DBSCAN, Gaussian mixtures, k-medoids, k-modes. Each fixes one limitation and brings its own.
**Likely follow-ups:** 1) *When is k-means still a good choice?* Fast, simple, many numeric features, round-ish groups. 2) *Biggest practical risk?* Unscaled or skewed data.
**Common mistakes:** Listing limitations without saying what you would do about them; saying k-means "finds the true groups".

### Q39 ⭐⭐ 🟡 Does k-means always find the best solution? Explain initialisation, k-means++ and the role of n_init and random_state.
**Asked at:** commonly asked (no company-specific report found); initialisation and local optima appear in k-means question banks (unverified, for example Towards AI, vitalflux).
**What the interviewer is checking:** That you know k-means can get stuck, and how to protect against it.
**Say this in the interview:** "No. It starts from guessed centres and improves step by step, but it can get stuck at a decent-but-not-best answer. K-means++ picks well-spread starting centres, `n_init` repeats the whole run from several starts and keeps the lowest inertia, and `random_state` fixes the randomness so the result is repeatable."
**Explain simply:**
- **Initialisation** = choosing the first centres. Bad starts (two centres inside one group) can lead to a bad final answer, called a **local optimum**.
- **k-means++** (the sklearn default, `init="k-means++"`, verified in the signature) picks starting centres that are far apart from each other.
- **`n_init`**: how many times to restart; the run with the lowest inertia wins. In sklearn 1.9 the default is `"auto"` (verified in the signature); how many starts "auto" means is from memory, unverified.
- **`random_state`**: a seed number; same seed, same answer.
**Worked example (computed by script, invented data with 6 clear groups, 60 points each):**
**Sample data:** `X_scaled`, 360 rows by 2 columns, in six blobs.
**Code (what you write in the interview):**
```python
# One random start each time: different seeds can land on different answers
for seed in range(5):
    km = KMeans(n_clusters=6, init="random", n_init=1, random_state=seed).fit(X_scaled)
    print("seed", seed, "inertia", round(km.inertia_, 1))

# Ten starts, keep the best: stable and repeatable
best = KMeans(n_clusters=6, n_init=10, random_state=42).fit(X_scaled)
print("best of 10 starts:", round(best.inertia_, 1))
```
**Output:**
```text
seed 0 inertia 666.4
seed 1 inertia 1590.3
seed 2 inertia 666.4
seed 3 inertia 666.4
seed 4 inertia 1597.0
best of 10 starts: 666.4
```
**What it means:** Two seeds got stuck at an inertia more than double the best (1,590 and 1,597 against 666.4). Output depends on the seeds shown (0 to 4 and 42). More starts or k-means++ avoids that.
**Likely follow-ups:** 1) *Does random_state make it "correct"?* No, only repeatable. 2) *Why not use many starts always?* Cost grows with each start.
**Common mistakes:** Treating `random_state` as improving quality; not setting it and getting different segments each run.

### Q40 ⭐⭐ 🟡 How does hierarchical clustering differ from k-means, and how do you read a dendrogram?
**Asked at:** commonly asked (no company-specific report found); k-means vs hierarchical is reported in an unverified Tiger Analytics (June 2020) technical round summary.
**What the interviewer is checking:** That you know both methods and can read a dendrogram.
**Say this in the interview:** "K-means needs k up front and moves centres around; hierarchical clustering builds a tree by repeatedly merging the two closest groups, so you decide how many clusters afterwards by cutting the tree. In a dendrogram, the height of a join shows how far apart the groups were; a tall join means very different groups."
**Explain simply:**
- **Agglomerative hierarchical clustering:** start with every customer alone, merge the closest pair, repeat until one group remains. The record of merges is the **dendrogram** (tree diagram).
- Read it bottom to top: the vertical axis is the distance at which groups join. Draw a horizontal line at a chosen height; the number of vertical lines it crosses is the number of clusters. Cut where there is a long gap with no joins.
- Compared with k-means: no k needed in advance and you get a full picture of nested groups; but it is slower on large data and cannot undo a merge.
**Worked example (computed by script):** six customers' monthly spend (thousand INR): 1, 2, 9, 10, 11, 30. Each row of the output is one merge.
**Sample data:** `spend = np.array([[1], [2], [9], [10], [11], [30]])`
**Code (what you write in the interview):**
```python
merges = linkage(spend, method="ward")

# Each row: the two groups joined, the distance at the join, and the new group size
print(merges.round(2))
```
**Output:**
```text
[[ 0.    1.    1.    2.  ]
 [ 2.    3.    1.    2.  ]
 [ 4.    7.    1.73  3.  ]
 [ 6.    8.   13.17  5.  ]
 [ 5.    9.   30.21  6.  ]]
```
**What it means:** The first three joins are at small heights (1, 1, 1.73): 1 with 2, 9 with 10, then 11 joins them. The join at 13.17 is much taller, so cutting just below it gives clusters {1, 2} and {9, 10, 11} and {30}; the last join at 30.21 is the outlier 30 being added, so a cut between 13 and 30 gives 2 clusters. Row numbers 6 onward in the output refer to merged groups.
**Likely follow-ups:** 1) *Which linkage?* Ward is a common default for compact clusters. 2) *Large datasets?* Use k-means; hierarchical is slow.
**Common mistakes:** Cutting at a random height; reading the horizontal order of leaves as meaningful distance.

### Q41 ⭐⭐ 🟡 How can k-means handle categorical variables such as city or payment method?
**Asked at:** commonly asked (no company-specific report found); categorical data and k-means is covered in k-means question banks (unverified).
**What the interviewer is checking:** That you know k-means needs numbers and the traps of encoding categories.
**Say this in the interview:** "K-means uses averages and distances, so categories must become numbers. The usual way is one-hot encoding (a 0/1 column per category), then scaling. For mostly categorical data I would use k-modes or Gower distance with a different algorithm, since averaging 0/1 columns is awkward."
**Explain simply:**
- **One-hot encoding:** a column per category: `payment_method_UPI` is 1 if UPI, else 0.
- Do not label-encode (UPI = 1, Card = 2, Cash = 3): it invents an order and distances that do not exist.
- Trap: each 0/1 column, once scaled, counts as much as a spend column, and a category with many values adds many columns that can dominate. Check results with and without them.
- Alternatives: **k-modes** for all-categorical data, or **k-prototypes** for a mix (from memory, unverified; they need an extra library not part of sklearn).
**Sample data:** 4 invented customers, `customers` DataFrame with `monthly_spend`, `orders`, `payment_method`.
**Code (what you write in the interview):**
```python
# Turn each category into a 0/1 column (one-hot encoding)
encoded = pd.get_dummies(customers, columns=["payment_method"], dtype=int)

# Scale everything so the 0/1 columns and the money column are comparable
X_scaled = StandardScaler().fit_transform(encoded)
print(encoded)
print(X_scaled.round(2))
```
**Output:**
```text
   monthly_spend  orders  payment_method_Card  payment_method_UPI
0           2000       3                    0                   1
1           2200       4                    1                   0
2           8000      12                    0                   1
3           7800      11                    1                   0
[[-1.03 -1.12 -1.    1.  ]
 [-0.96 -0.87  1.   -1.  ]
 [ 1.03  1.12 -1.    1.  ]
 [ 0.96  0.87  1.   -1.  ]]
```
**What it means:** After scaling, the payment columns (about +/-1) are as large as the spend columns, and Card and UPI are mirror images (two columns saying the same thing). Customers 0 and 1 have almost equal spend but look quite different because of payment type, so categories can steer the clusters more than you intend.
**Likely follow-ups:** 1) *Drop one dummy column?* Often yes when only two categories. 2) *Better to cluster on behaviour and profile by category?* Often, yes.
**Common mistakes:** Label-encoding nominal categories; leaving high-cardinality columns (like city) in without thought.

### Q42 ⭐⭐ 🟡 Two of your clustering features are highly correlated. Does it matter for k-means?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question tied to RFM frequency and monetary overlap.
**What the interviewer is checking:** That you know correlated features double-count in distance.
**Say this in the interview:** "Yes, it can matter. K-means treats features as independent, so two features carrying the same information count twice, and that direction dominates the distance. I check the correlation, and if it is very high I keep one, combine them, or reduce with PCA."
**Explain simply:**
- **Correlation** (from -1 to +1) measures how closely two features move together. Orders and spend often correlate strongly.
- If both go in, "how big a buyer" counts twice and the other features (such as recency) count once.
- Fixes: drop one, create a combined measure (spend per order), reduce with PCA (principal component analysis, which merges overlapping features), or deliberately weight the features.
**Worked example (computed by script, invented data, 200 customers):** orders and spend correlate at 0.96; recency correlates with neither (-0.03, -0.02). After scaling, the first PCA axis (the "how big a buyer" direction) holds 65% of all variation (two of the three features point that way), recency alone holds 33%, and the last 1% is noise. So the clusters are pulled about twice as hard by size of buyer as by recency.
**Sample data:** `customers` DataFrame with `orders`, `spend` (about 900 per order plus noise), `recency`.
**Code (what you write in the interview):**
```python
print(customers.corr().round(2))

# Orders and spend carry almost the same message, so after scaling they count twice in the distance
```
**Output:**
```text
         orders  spend  recency
orders     1.00   0.96    -0.03
spend      0.96   1.00    -0.02
recency   -0.03  -0.02     1.00
```
**What it means:** Orders and spend are 96% correlated, so they are nearly one feature counted twice. Recency is independent. Report it as: "I will keep one of the pair, or combine them, before clustering."
**Alternative / pitfalls:** In RFM, frequency and monetary are often correlated; scoring each on its own 1 to 5 scale is simple, and the overlap is accepted. Dropping a feature loses a little information.
**Likely follow-ups:** 1) *Does it break k-means?* No, it tilts the result towards the duplicated signal. 2) *Is dropping always best?* Check you are not losing a useful difference (for example spend per order).
**Common mistakes:** Leaving near-duplicate features in "just in case"; dropping a feature without looking at what it adds.

### Q43 ⭐⭐ 🟡 How do you handle missing values before clustering?
**Asked at:** commonly asked (no company-specific report found); a gap-fill preprocessing question.
**What the interviewer is checking:** That you know k-means cannot run on gaps and that fills have consequences.
**Say this in the interview:** "K-means cannot take blanks, so I first find out how many there are and why. Few missing: drop them. Moderate: fill with the median (or a smarter fill) and keep a flag column. Many missing in one column: drop that column. I always check that the fill does not distort the segments."
**Explain simply:**
- First ask why it is missing: a customer with no orders has no recency, which is information, not a data error.
- **Median fill** (`SimpleImputer`) is robust to outliers; mean fill is pulled by them.
- Add a "was missing" 0/1 column if the gap itself may mean something.
- Never fill with 0 blindly; for recency, 0 means "bought today".
**Sample data:** 6 invented customers with one gap in each of `recency`, `frequency`, `monetary`.
**Code (what you write in the interview):**
```python
from sklearn.impute import SimpleImputer

# How many gaps per column?
print(customers.isna().sum())

# Fill gaps with the column median (robust to extreme values)
imputer = SimpleImputer(strategy="median")
filled = pd.DataFrame(imputer.fit_transform(customers), columns=customers.columns)
print(filled)
```
**Output:**
```text
recency      1
frequency    1
monetary     1
dtype: int64
   recency  frequency  monetary
0     10.0       12.0    9000.0
1     25.0        8.0    6000.0
2     40.0        6.0    5000.0
3     40.0        6.0    4500.0
4    200.0        1.0    5000.0
5    180.0        2.0     900.0
```
**What it means:** Customer 4 was last seen 200 days ago with 1 order, yet the median fill gave them spend of 5,000, typical of an active customer. A fill can place a customer in the wrong group, so check imputed rows.
**Alternative / pitfalls:** Group-wise or model-based fills (for example KNN imputation) are an option; with very few missing rows, dropping them is simplest. Fit the imputer on training data only if you will score new customers.
**Likely follow-ups:** 1) *Mean or median?* Median for skewed data. 2) *Drop or fill?* Drop if under a few percent and random; otherwise fill and flag.
**Common mistakes:** Filling with 0; not checking how many rows were filled.

### Q44 ⭐⭐ 🟡 How would you visualise clusters when there are more than three features?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** That you can show high-dimensional results simply and honestly.
**Say this in the interview:** "I squash the features into two axes with PCA and draw a scatter plot coloured by cluster, and I always pair it with a table of each cluster's average per feature, because the plot alone does not say what the clusters mean."
**Explain simply:**
- **PCA** (principal component analysis) builds two new summary axes from your features that keep as much of the variation as possible. It is a flat photograph of a 5-D cloud; some detail is lost.
- Check the share of variation kept; if it is low (say 40%), the picture hides structure.
- Other options: pairs of features in a scatter-matrix, a heatmap or bar chart of cluster averages, a radar chart for 2 to 3 clusters, or t-SNE/UMAP (from memory, unverified; good for pictures, not for measuring distance).
- The cluster-profile table (averages per cluster) is what the business reads.
**Sample data:** 300 invented customers, 5 features (`recency`, `frequency`, `monetary`, `tenure`, `returns`), 3 clusters from k-means (seed 42).
**Code (what you write in the interview):**
```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Squash 5 features into 2 "summary" axes for a flat picture
pca = PCA(n_components=2)
points_2d = pca.fit_transform(X_scaled)
print("Share of variation kept:", pca.explained_variance_ratio_.round(2))

plt.scatter(points_2d[:, 0], points_2d[:, 1], c=labels)
plt.xlabel("Axis 1")
plt.ylabel("Axis 2")
plt.show()

# Companion table: average of each feature per cluster
print(customers.groupby(labels).mean().round(2))
```
**Output:**
```text
Share of variation kept: [0.46 0.29]
   recency  frequency  monetary  tenure  returns
0     5.00       5.09      0.11   -0.19    -0.24
1     0.02       5.07      4.82    5.11    -0.04
2    -0.03      -0.02      0.02    0.01    -0.04
```
**What it means:** The two axes keep 75% of the variation (0.46 + 0.29), enough for a fair picture. The table shows what makes each group: cluster 0 has high recency and frequency values, cluster 1 high frequency, monetary and tenure. (The scatter plot itself is a picture, not printed text; the invented features are in arbitrary units.)
**Likely follow-ups:** 1) *Is the 2-D plot exact?* No, it is a projection. 2) *Does PCA need scaling first?* Yes, scale first.
**Common mistakes:** Treating overlap on the plot as proof the clusters are bad; showing a plot with no profile table.

### Q45 ⭐⭐ 🟡 Should recency, frequency and monetary carry equal weight in RFM, and what if frequency and monetary are strongly correlated?
**Asked at:** commonly asked (no company-specific report found); RFM scoring questions appear in prep-site banks (unverified), not tied to a named company.
**What the interviewer is checking:** Whether you know that RFM weights are a business choice, and that correlated inputs quietly count the same signal twice.
**Say this in the interview:** "Equal weights are the neutral default, but the right weights depend on the goal. For a subscription business recency matters most; for a bulk-buying business monetary does. If frequency and monetary move together, I would check the correlation, and then drop one, combine them, or log-transform, so one idea does not get double the vote."
**Explain simply:**
- **RFM** = Recency (days since last purchase), Frequency (number of purchases), Monetary (total spend). Weights are how much each letter counts in a combined score.
- Equal weight means a simple average of the three 1-5 scores. A weighted score (for example 0.5 R, 0.3 F, 0.2 M) is fine if the business can justify it; write the reason down.
- **Correlated** means two columns rise and fall together. On a made-up 300-customer table, frequency and monetary correlate at 0.85. With k-means, that makes "how much they buy" count about twice.
- Fixes: keep R plus one of F or M; average F and M into one "value" column; or use PCA (a method that merges overlapping columns into new ones). Log-transform skewed spend first.
**Worked example (concept questions):** Customers A, B, C have scores R/F/M of 5/4/4, 2/5/5 and 4/1/1. Equal weights give 4.33, 4.00, 2.00 (A ranks first). With weights 0.5/0.3/0.2, A scores 4.5, B 3.5 and C 2.5; B drops because it is weak on recency. On the 300-customer data, k-means with 3 clusters on R and F only gave nearly the same segments as with all three (agreement score 0.93, where 1.0 means identical), which shows how much M adds once F is in.
**Alternative / pitfalls:** Do not pick weights to get a "nice-looking" result. For quintile scores, correlated F and M just give similar numbers, which is harmless for reporting but misleading inside a distance-based model.
**Likely follow-ups:** 1) *How would you choose weights?* Ask the business which behaviour predicts the goal (repeat purchase, churn) and test it on past data. 2) *Does scaling fix correlation?* No; scaling fixes units, not overlap.
**Common mistakes:** Saying "equal weights are always correct"; ignoring that spend is skewed; never checking the correlation table.

### Q46 ⭐⭐ 🟡 How do you check that your segments are stable and not an accident of one random run?
**Asked at:** commonly asked (no company-specific report found); k-means initialisation and "is this result reliable" questions appear in prep-site banks (unverified).
**What the interviewer is checking:** Whether you treat clustering as something to test, not a one-shot answer.
**Say this in the interview:** "I rerun the clustering with different random starts and on resampled data, then measure how much the groupings agree using the adjusted Rand index. If agreement is high, the segments are real; if it is low, they are partly an accident and I should use fewer segments or a different method."
**Explain simply:**
- k-means starts from random centres, so different seeds can land on different answers (local optima). `n_init=10` already tries 10 starts and keeps the best.
- **Adjusted Rand index (ARI):** a number comparing two groupings of the same people. 1.0 means identical groups (the labels may be renamed); near 0 means no better than chance.
- **Bootstrap:** refit on a random resample of customers (with replacement), assign everyone to the nearest resulting centre, and compare with the original grouping.
- Also check that segment sizes, profiles and silhouette stay similar, and that the segments still appear next month.
**Worked example (concept questions):** On the made-up 300-customer data (3 real groups), 10 single-start runs with different seeds all matched the best run with ARI 0.99 to 1.0. In 20 bootstrap refits, 3 segments averaged ARI 0.95 (worst 0.83); asking for 5 segments dropped to an average of 0.82 (worst 0.55). So 3 segments are stable here and 5 are shaky.
**Alternative / pitfalls:** High stability does not prove the segments are useful; it only shows they are not random. Perfectly stable clusters can still be meaningless if the features were poor.
**Likely follow-ups:** 1) *What if stability is low?* Reduce k, remove noisy features, or try another method. 2) *Why not just fix `random_state`?* That hides the instability; it does not remove it.
**Common mistakes:** Running once with a fixed seed and calling it final; comparing raw label numbers between runs (they swap names, see Q60).

### Q47 ⭐⭐ 🟡 You have fitted a k-means model and a new batch of customers arrives. How do you assign them to segments?
Assume `scaler` and `km` were fitted earlier on the training data.
**Asked at:** commonly asked (no company-specific report found); "predict on new data" appears in prep-site k-means banks (unverified).
**What the interviewer is checking:** That you reuse the saved scaler and model, and do not refit on the new batch.
**Say this in the interview:** "I transform the new customers with the same fitted scaler, then call predict on the fitted k-means. Each customer is assigned to the nearest existing centre. I never refit on the new batch, because that would change the segments and break comparability."
**Explain simply:**
- `scaler.transform` applies the training means and spreads to new rows; `fit` would learn new ones.
- `km.predict` measures the distance to each saved centre and picks the closest.
- Refit on a schedule (for example quarterly), not on every batch, and keep naming consistent (Q60).
**Sample data:** 8 training customers (made-up, 2 segments) and 3 new ones.

| recency_days | frequency | monetary |
|---|---|---|
| 12 | 11 | 800 |
| 190 | 1 | 50 |
| 60 | 4 | 250 |

**Code (what you write in the interview):**
```python
# Same scaler as training: transform only, never fit again
new_scaled = scaler.transform(new_customers)

# Assign each new customer to the nearest saved centre
new_customers["segment"] = km.predict(new_scaled)
print(new_customers)
```
**Output:**
```text
   recency_days  frequency  monetary  segment
0            12         11       800        0
1           190          1        50        1
2            60          4       250        1
```
**What it means:** Segment 0 is the active big spenders and segment 1 the lapsed low spenders (training labels were [0 0 0 1 1 1 0 0]). The third customer (60 days, 4 orders) is borderline: its distance to centre 1 was 1.75 against 2.12 for centre 0, so check how close the call is.
**Alternative / pitfalls:** Customers far from every centre (new behaviour) still get a label; flag large distances (`km.transform`) as "new type, review". Save the scaler and model with joblib so production uses the same objects.
**Likely follow-ups:** 1) *What if the new batch looks very different?* Monitor drift and refit. 2) *Could you fit on old plus new?* Yes, on a schedule, and then map the new labels to the old names.
**Common mistakes:** Calling `fit_transform` on the new batch; forgetting to scale at all; refitting and comparing label numbers.

### Q48 ⭐⭐ 🟡 Write a SQL query that computes recency, frequency and monetary per customer and assigns 1 to 5 scores with NTILE.
Table `orders(customer_id, order_date, amount)`. Reference date: 2026-04-01. Any SQL dialect is fine; state which one you use.
**Asked at:** commonly asked (no company-specific report found); RFM-in-SQL is a standard analyst exercise in prep-site banks (unverified), and SQL is central in analyst loops generally.
**What the interviewer is checking:** GROUP BY aggregates, a CTE, window function NTILE, and the direction of the recency score.
**Say this in the interview:** "I use SQLite here. A CTE computes per-customer days since last order, order count and total spend. Then NTILE(5) splits customers into five equal-sized groups. Recency is sorted descending so the most recent customers get score 5, the same direction as frequency and monetary."
**Explain simply:**
- **NTILE(5)** sorts rows by the given column and cuts them into 5 buckets of equal size; the bucket number is the score.
- Smaller recency is better, so sort it from largest to smallest (`DESC`); for F and M larger is better (`ASC`).
- Dates: SQLite uses `julianday()` to subtract dates; in SQL Server it is `DATEDIFF(day, ..., ...)` and in PostgreSQL date subtraction (from memory, unverified).
**Sample data:** 12 orders, 10 customers (made-up; the real table would be much larger).

| customer_id | order_date | amount |
|---|---|---|
| 1 | 2026-03-28 | 120 |
| 1 | 2026-02-10 | 80 |
| 2 | 2026-03-20 | 45 |
| 3 | 2026-03-01 | 300 |
| 4 | 2026-02-15 | 60 |
| 5 | 2026-01-20 | 500 |
| 5 | 2025-12-05 | 150 |
| 6 | 2026-01-05 | 35 |
| 7 | 2025-11-30 | 90 |
| 8 | 2025-10-12 | 200 |
| 9 | 2025-09-01 | 25 |
| 10 | 2025-07-15 | 70 |

**Code (what you write in the interview):**
```sql
-- SQLite
WITH customer_rfm AS (
    SELECT
        customer_id,
        -- days since the last order (smaller = more recent)
        CAST(julianday('2026-04-01') - julianday(MAX(order_date)) AS INTEGER) AS recency_days,
        COUNT(*)    AS frequency,
        SUM(amount) AS monetary
    FROM orders
    WHERE order_date < '2026-04-01'
    GROUP BY customer_id
)
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    -- most recent customers get 5, so sort recency from largest to smallest
    NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
    NTILE(5) OVER (ORDER BY frequency ASC)     AS f_score,
    NTILE(5) OVER (ORDER BY monetary ASC)      AS m_score
FROM customer_rfm
ORDER BY customer_id;
```
**Output:**
```text
customer_id  recency_days  frequency  monetary  r_score  f_score  m_score
1            4             2          200.0     5        5        4
2            12            1          45.0      5        2        2
3            31            1          300.0     4        4        5
4            45            1          60.0      4        2        2
5            71            2          650.0     3        5        5
6            86            1          35.0      3        1        1
7            122           1          90.0      2        3        3
8            171           1          200.0     2        4        4
9            212           1          25.0      1        1        1
10           260           1          70.0      1        3        3
```
(Real run in SQLite 3.53.1; columns aligned by hand for reading.)
**What it means:** Customer 1 is recent, frequent and a good spender (5, 5, 4); customer 9 is the opposite (1, 1, 1).
**Alternative / pitfalls:** Ties: NTILE splits equal values across buckets arbitrarily (here most customers have frequency 1, yet get scores 1 to 4), so tied customers can get different scores. In real data, use frequency bands by rule or rank first. With fewer customers than 5 buckets the scores are meaningless. Exclude refunds and cancelled orders in the WHERE clause.
**Likely follow-ups:** 1) *How do you combine the scores?* Concatenate (for example 555) or average, then map to named segments. 2) *Why filter order_date before the reference date?* To avoid negative recency from future-dated rows.
**Common mistakes:** Scoring recency in the wrong direction; using today's date instead of the stated reference date; forgetting GROUP BY.

### Q49 ⭐⭐ 🟡 You are asked to segment employees by tenure, absence days and engagement score for a retention programme. Describe your approach and one risk.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured segmentation is a gap-fill scenario here, not a reported company question.
**What the interviewer is checking:** A sensible end-to-end approach, and awareness that people data needs care.
**Say this in the interview:** "I would first agree the goal with HR: who needs support to stay. Then clean the three columns, standardise them so units do not dominate, run k-means for a few values of k, pick k using silhouette, stability and usefulness, profile each cluster in original units and name them. The main risk is that a segment label sticks to people as a judgement, or is used for decisions it was never built for."
**Explain simply:**
- **Standardise** means rescaling each column to average 0 and spread 1. Without it, absence days (0 to 30) would swamp engagement (1 to 5). Example: two employees differing by 1 engagement point but 5 absence days look 5.0 apart raw, against 2.2 when only tenure and engagement differ; scale first.
- Check missing engagement scores (survey non-response is not random), and outliers such as long-term leave.
- Name segments from the profile table, then work out one retention action each.
- **Risks:** stereotyping or stigma ("the absent group"); using absence as a proxy that affects people with health conditions or caring duties; small groups that make individuals identifiable; clusters that look like gender or age groups. Segmentation describes groups; it does not predict who will resign.
**Alternative / pitfalls:** For predicting who leaves, a supervised attrition model is the right tool; clustering only helps design programmes. Keep results aggregated, restrict access, and get HR and legal sign-off (data-protection rules such as India's DPDP Act or GDPR: from memory, unverified, confirm with legal).
**Likely follow-ups:** 1) *How many segments?* Usually 3 to 5 so HR can act on each. 2) *Would you include age or gender?* No; exclude protected attributes, but check results by group for unfair impact.
**Common mistakes:** Skipping scaling; presenting clusters as "types of people"; no action plan per segment.

### Q50 ⭐⭐ 🟡 You have a cluster profile table in original units. Describe how you would turn it into named segments for the HR team.
| Cluster | Avg tenure (years) | Avg absence days | Avg engagement (1-5) | Employees |
|---|---|---|---|---|
| 0 | 1.2 | 3 | 3.1 | 300 |
| 1 | 6.8 | 4 | 4.2 | 250 |
| 2 | 4.5 | 14 | 2.3 | 90 |
**Asked at:** commonly asked (no company-specific report found); turning clusters into named segments is a gap-fill item, in the spirit of "validate segments with business meaning" advice on prep sites (unverified).
**What the interviewer is checking:** Can you read a profile table, compare with the overall average, and label groups in plain, respectful words with an action.
**Say this in the interview:** "I compare each cluster with the company average, pick what stands out, give it a short descriptive name, and attach one action. Cluster 0 is new joiners, cluster 1 settled loyal staff, and cluster 2 a smaller group with high absence and low engagement who need a stay conversation."
**Explain simply:**
- Company averages (weighted by head count, 640 employees): tenure 3.85 years, absence 4.9 days, engagement 3.42.
- **Cluster 0, "New joiners" (47%):** 1.2 years, engagement near average. Action: strengthen onboarding and 90-day check-ins.
- **Cluster 1, "Settled and engaged" (39%):** long tenure, highest engagement. Action: recognise, use as mentors, watch for stagnation.
- **Cluster 2, "At-risk and disengaged" (14%, 90 people):** absence 14 days, engagement 2.3, mid tenure. Action: manager conversations, workload and wellbeing review.
- Names describe behaviour, not character; avoid labels like "problem group".
**Alternative / pitfalls:** Averages hide spread; check medians or ranges inside cluster 2. Confirm that clusters are stable (Q46). Cluster 2's absence may have legitimate causes (illness, leave), so frame the action as support. Keep the 90-person group in aggregate; do not list names without a clear purpose and approval.
**Likely follow-ups:** 1) *How would you test whether cluster 2 really leaves more?* Compare later attrition across clusters. 2) *What if two clusters look alike?* Merge them (reduce k).
**Common mistakes:** Naming from cluster numbers alone; judging only on the biggest difference; forgetting the head counts.

### Q51 ⭐⭐ 🟡 How would you present customer segments to a marketing team that does not know statistics?
**Asked at:** commonly asked (no company-specific report found); communication of results is a standard analyst-interview theme.
**What the interviewer is checking:** Whether you can translate clusters into names, sizes, value and actions, without algorithm talk.
**Say this in the interview:** "I lead with the decision, not the method: four customer groups, who they are, how much revenue each brings, and what we should do for each. I use names and one-line personas, a single simple chart, and a table of size, value and recommended action. The method goes in an appendix."
**Explain simply:**
- One slide per segment: name, size (% of customers), share of revenue, typical behaviour in plain units ("orders every 3 weeks, spends about 450"), and the action.
- Use comparisons to the average ("buys 3 times more often than average") rather than standardised scores.
- Use a bar chart of revenue share vs customer share; avoid scatter plots of principal components.
- Make it concrete: show a sample customer from each group.
- Add confidence: "the groups stayed the same when we re-ran the analysis".
**Worked example (concept questions):** From the made-up 300-customer data: "Champions" are 26% of customers (77) but 65% of revenue; "Regulars" are 45% (134) and 27% of revenue; "Lapsed" are 30% (89) but 8% of revenue. The headline: protect the 26% that bring two thirds of revenue.
**Alternative / pitfalls:** Do not hide limitations: segments are a simplification and some customers sit between groups. Avoid more than 5 segments; the team cannot act on 9.
**Likely follow-ups:** 1) *Which chart?* Bar of size vs revenue share, plus a table. 2) *What if marketing disagrees with a name?* Rename; names are for communication, not statistics.
**Common mistakes:** Showing silhouette scores or centroids; using "cluster 3" as a name; no recommended action.

### Q52 ⭐⭐ 🟡 After you target a segment with a campaign, how do you measure whether the segmentation actually helped?
**Asked at:** commonly asked (no company-specific report found); campaign measurement is a gap-fill item linking segmentation to A/B-style thinking.
**What the interviewer is checking:** That you use a control group and a business metric, not just "the segment bought more".
**Say this in the interview:** "I keep a holdout: within the segment, randomly leave some customers out of the campaign and compare conversion or revenue against those who got it. To show the segmentation itself helped, I also compare the targeted campaign against a generic one sent to a random group of the same size."
**Explain simply:**
- **Holdout (control) group:** customers randomly kept from the campaign; the difference between treated and holdout is the **lift** (the extra effect caused by the campaign).
- Two questions: did the campaign work (treated vs holdout) and did segmenting add value (segment-tailored message vs one-size-fits-all message).
- Pick the metric first (conversion, revenue per customer, repeat rate, margin), and the time window.
- Check statistical significance (a z-test for two proportions) and the cost of the campaign.
**Worked example (concept questions):** 1,500 customers got the segment offer and 1,500 were held out. Conversion was 6.0% (90) against 4.2% (63): lift of 1.8 percentage points, about 43% relative; the two-proportion z-test gave p about 0.025, so unlikely to be chance. If a generic campaign converts about 4.0% (an exercise input), the targeted one beat it by 2 points; multiply by customers and margin per order to get money.
**Alternative / pitfalls:** Without random assignment, targeted customers may simply be better customers. Watch for novelty effects, segments changing between runs (Q60), and small samples.
**Likely follow-ups:** 1) *What if you cannot hold out?* Use matched or earlier-period comparison and say it is weaker. 2) *Is p below 0.05 enough?* Also report size of effect and cost.
**Common mistakes:** Comparing treated segment to the average of everyone; reporting only revenue, not margin; no control.

### Q53 ⭐⭐ 🟡 What privacy and fairness concerns arise when you segment customers or employees, and how do you handle them?
**Asked at:** commonly asked (no company-specific report found); privacy and fairness are a gap-fill item, increasingly asked in HR-analytics roles.
**What the interviewer is checking:** Responsible-data judgement.
**Say this in the interview:** "Segments can expose or amplify personal information and treat groups unfairly. I use only the data needed for the purpose, keep outputs aggregated and access-controlled, avoid protected attributes and obvious proxies, and check outcomes across groups before anyone acts. For employees I involve HR leadership and legal."
**Explain simply:**
- **Privacy:** collect only what the purpose needs; remove or pseudonymise names and IDs; small groups (for example 4 people) can identify individuals; follow consent and retention rules (India's DPDP Act, GDPR: from memory, unverified, confirm with IT or legal).
- **Fairness:** a **proxy** is a column that stands in for a protected trait (postcode for community, part-time status for gender). Clusters may reproduce past bias.
- **Employee risk:** segments used for promotion, pay or dismissal decisions are high stakes; use them for support programmes only.
- **Handle:** document purpose; check cluster make-up by gender, age and location; set a minimum group size for reporting; keep a human in every decision; allow review.
**Worked example (concept questions):** Suppose the "high absence" cluster is 70% women while the company is 45% women (invented numbers). Targeting it for performance review would hit women unevenly; investigate causes (for example caring leave) and change the action to support.
**Alternative / pitfalls:** Dropping a sensitive column does not remove bias if proxies remain. Fairness checks need the sensitive attribute, held separately for auditing only.
**Likely follow-ups:** 1) *Can customers be segmented by gender?* Avoid unless there is a justified, lawful reason. 2) *Who should see the segment lists?* Only those who need them, ideally aggregated.
**Common mistakes:** Treating privacy as only "remove names"; ignoring proxies; using segments for individual decisions.

### Q54 ⭐⭐ 🟡 A cluster is described as 'Segment 2' with no further meaning. A stakeholder asks what it is. What would a good analyst do?
**Asked at:** commonly asked (no company-specific report found); gap-fill item on turning clusters into meaning.
**What the interviewer is checking:** That you do not shrug; you profile, compare, name and check the segment.
**Say this in the interview:** "I would not say 'it is just what the algorithm found'. I would profile it: size, average and median of each feature against the overall figures, plus other fields not used in clustering, such as city or product mix. Then I give it a plain name and an action, and check it is stable."
**Explain simply:**
- **Profile:** for every feature, compare the segment to the overall average, in original units.
- Look at fields **not** used to build the clusters; if the segment also differs there, it is likely real.
- Check size and revenue share; if it holds 3 people, it may be noise.
- Name it by behaviour and test it with the stakeholder ("does this match what you see?").
**Worked example (concept questions):** In the made-up 300-customer data, segment 2 has 134 customers with median recency 68 days (overall 71), 4 orders (overall 4) and median spend 108 (overall 108). It looks like an average group: "Regulars", 27% of revenue. Segment 1 (77 customers; 14 days, 15 orders, 443 spend; 65% of revenue) would be "Champions". Segment 0 (89 customers; 159 days, 2 orders, 41 spend) is "Lapsed".
**Alternative / pitfalls:** Numbers like 0, 1, 2 are arbitrary and can change next run (Q60). A segment that looks "average" may mean k is too large or features are poor.
**Likely follow-ups:** 1) *What if no story emerges?* Try fewer clusters or different features. 2) *Where do you store the name?* In a mapping table tied to centre profiles.
**Common mistakes:** Giving only the centroid in scaled units; inventing a story without checking; leaving "Segment 2" in the deck.

### Q55 ⭐⭐ 🟡 When the elbow curve is smooth with no clear bend, what do you do?
**Asked at:** commonly asked (no company-specific report found); a Fractal Glassdoor report on choosing the number of clusters was reported via a search summary (unverified, mapping not confirmed), and the "smooth elbow" caveat appears in tutorials.
**What the interviewer is checking:** That you know the elbow is a hint, not a rule, and have other tools.
**Say this in the interview:** "A smooth elbow means the data has no obvious number of groups, so I stop relying on it. I add the silhouette score, check stability, and ask which number of segments the business can use. I then report a choice with reasons and the alternatives."
**Explain simply:**
- **Elbow method:** plot **inertia** (total squared distance from points to their cluster centre; lower is tighter) for k = 1, 2, 3...; pick the bend where extra clusters stop helping much.
- **Silhouette** (-1 to 1): how well each point fits its own cluster compared with the nearest other; higher is better.
- Also try the gap statistic, stability (Q46), and practical limits (campaign budget, team capacity).
**Worked example (concept questions):** On a made-up 300-point, 3-feature dataset, inertia fell 900.0, 640.8, 391.0, 309.4, 241.5, 199.8 for k=1 to 6. The percentage drops were 28.8% (k=2), 39.0% (k=3), 20.9%, 22.0%, 17.3%: no sharp break, just a slow slide. Silhouette: 0.316 (k=2), 0.440 (k=3), 0.420 (k=4), 0.404 (k=5), 0.363 (k=6). Silhouette favours 3, with 4 and 5 close behind.
**Alternative / pitfalls:** Silhouette scores near 0.25 or below suggest weak structure; segments may be a convenient partition, not natural groups. Say so.
**Likely follow-ups:** 1) *Can you automate the pick?* Possible, but I still review it. 2) *Does scaling matter?* Yes, always scale before computing inertia.
**Common mistakes:** Forcing an elbow that is not there; using inertia alone, which always falls as k grows.

### Q56 ⭐⭐ 🔴 Is the clustering result 'right'? How do you defend your choice of k when the silhouette score favours 3 and the business wants 5 segments?
**Asked at:** commonly asked (no company-specific report found); "choosing k" and validating with business meaning appear in candidate reports (unverified, for example Tiger Analytics, Fractal).
**What the interviewer is checking:** Mature judgement: no clustering is "right"; you balance statistics and usefulness, and communicate trade-offs.
**Say this in the interview:** "Clustering has no single right answer, only more or less useful ones. I would show the numbers for 3 and 5 side by side: silhouette, stability, segment sizes and whether each segment supports a different action. If 5 is only a little worse and the extra segments are stable and actionable, I would go with 5; if not, I would use 3, and perhaps split the big segment later."
**Explain simply:**
- Statistics say how separated the groups are; the business says how many it can treat differently.
- Compare k=3 and k=5 on: silhouette, stability, smallest segment size, and distinct actions.
- A compromise: 3 core segments, with 2 sub-segments of the largest.
**Worked example (concept questions):** On the made-up dataset from Q55, silhouette was 0.440 at k=3 and 0.404 at k=5, a small gap. Stability over 20 bootstrap refits: k=3 averaged agreement 0.98 (worst 0.95); k=5 averaged 0.89 (worst 0.54), so some k=5 segments are shaky. Sizes at k=5: 59, 96, 58, 45, 42 (all workable). Recommendation: 3 solid segments are safest; go to 5 only if marketing confirms five different actions and the shaky pair can be merged.
**Alternative / pitfalls:** Never hide that the data really contains 3 groups; presenting 5 as "natural" would mislead. Agree the criteria before looking at results to avoid arguing from a favourite.
**Likely follow-ups:** 1) *What if marketing insists on 5?* Deliver 5 with a note on overlap, and test it with a campaign (Q52). 2) *What would change your mind?* Evidence that the extra segments respond differently.
**Common mistakes:** Treating silhouette as the final word; ignoring the business constraint; claiming the clusters are "true".

### Q57 ⭐ 🟡 What is DBSCAN, and when would you prefer it to k-means?
**Asked at:** commonly asked (no company-specific report found); k-means alternatives appear in prep-site banks (unverified).
**What the interviewer is checking:** That you know a density-based alternative and its trade-offs.
**Say this in the interview:** "DBSCAN groups points that sit in dense regions and labels isolated points as noise. Unlike k-means it does not need the number of clusters in advance, can find curved shapes, and flags outliers. I would prefer it when clusters are irregular or there are outliers I want identified."
**Explain simply:**
- Two settings: `eps` (how close counts as a neighbour) and `min_samples` (how many neighbours make a dense area).
- Points in dense areas form clusters; points with too few neighbours get label -1 (noise).
- k-means assumes round, similar-sized clusters and forces every point into a group.
- Weakness: choosing `eps` is hard, and it struggles when densities differ. It also behaves poorly in many dimensions.
**Worked example (concept questions):** On a made-up two-crescent shaped dataset (300 points), k-means with k=2 cut across the crescents (agreement with the true shapes 0.25 on a 0 to 1 scale), while DBSCAN with eps=0.2 and min_samples=5 recovered both crescents perfectly (1.0). Adding 3 far-away points, DBSCAN labelled exactly those 3 as noise.
**Alternative / pitfalls:** For ordinary customer RFM data (blob-like groups), k-means is usually simpler and easier to explain. Scale features first, since `eps` is a distance.
**Likely follow-ups:** 1) *How do you pick eps?* Plot sorted nearest-neighbour distances and look for a bend; then check results. 2) *Can DBSCAN predict new points?* Not directly in sklearn.
**Common mistakes:** Using it without scaling; expecting a fixed number of clusters.

### Q58 ⭐ 🟡 Compare StandardScaler and MinMaxScaler for clustering. Does the choice change the clusters?
**Asked at:** commonly asked (no company-specific report found); a Fractal Glassdoor report mentioning normalising before k-means was surfaced via a search summary (unverified).
**What the interviewer is checking:** That you know both scalers and when the choice matters.
**Say this in the interview:** "Both put features on a comparable scale. StandardScaler centres to mean 0 and spread 1; MinMaxScaler squeezes values into 0 to 1. On clean data the clusters are usually nearly identical, but with outliers MinMax gets squeezed, so the choice can change the result."
**Explain simply:**
- **StandardScaler:** (value - mean) / standard deviation. Outliers have large values but still affect the mean and spread.
- **MinMaxScaler:** (value - min) / (max - min). One huge outlier makes everyone else close to 0.
- Clustering uses distances, so any unscaled column with large numbers (spend in rupees) would dominate.
- Heavily skewed columns benefit from a log transform before either scaler.
**Worked example (concept questions):** On the made-up 300-customer data, both scalers gave the same three segment sizes (about 89, 77, 134 vs 90, 77, 133; agreement 0.99). After adding one customer who spent 20,000, standard scaling isolated that customer as a cluster of 1 (sizes 122, 178, 1), while MinMax kept three normal-sized clusters (59, 120, 122) but with different boundaries (agreement between the two results 0.61).
**Alternative / pitfalls:** Neither is "correct"; try both and check stability. Handle outliers deliberately (cap, log, or analyse separately).
**Likely follow-ups:** 1) *Do you scale before or after the train/test split?* Fit on train, transform both. 2) *RobustScaler?* Uses median and IQR; less sensitive to outliers (from memory, unverified).
**Common mistakes:** Not scaling; scaling the cluster labels; fitting the scaler on all data and then splitting.

### Q59 ⭐ 🟡 What would happen to inertia if you set k=1, and if you set k equal to the number of points?
**Asked at:** commonly asked (no company-specific report found); inertia questions appear in k-means banks (unverified).
**What the interviewer is checking:** That you understand inertia as total squared distance and why it always falls with k.
**Say this in the interview:** "With k=1 there is one centre, the overall mean, so inertia equals the total variation in the data, the maximum. With k equal to the number of points, every point is its own centre, so inertia is zero. Both are useless as segmentations, which is why inertia alone cannot choose k."
**Explain simply:**
- **Inertia** = sum over points of the squared distance to the nearest centre.
- k=1: inertia is the total sum of squares around the overall mean.
- k=n: each point sits on its own centre, distance 0, inertia 0.
- Between the two, inertia only goes down as k rises, so you look for diminishing returns (elbow), not the lowest value.
**Worked example (concept questions):** Six made-up customers with two features: (1,2), (2,2), (3,4), (8,8), (9,9), (10,8). k=1 gives inertia 129.0 (the same as the total sum of squares computed by hand); k=6 gives 0.0. Silhouette is not defined for k=1 or k=n.
**Alternative / pitfalls:** Very large k overfits: clusters of one customer are meaningless. Also, inertia depends on the scale of the data, so you cannot compare it across datasets.
**Likely follow-ups:** 1) *Is lower inertia better?* Only at the same k. 2) *What is the sensible range of k?* 2 to about 8 for business segmentation.
**Common mistakes:** Choosing k by minimum inertia; saying inertia can rise as k grows (it cannot, with good initialisation).

### Q60 ⭐ 🟡 Why do cluster numbers change between runs, and how do you keep segment names consistent month to month?
**Asked at:** commonly asked (no company-specific report found); label switching is a differentiator question, not tied to a company.
**What the interviewer is checking:** That you know cluster IDs are arbitrary and know how to keep naming stable.
**Say this in the interview:** "Cluster numbers are just labels from a random start; the same groups can come out as 0, 1, 2 one run and 2, 0, 1 the next. To keep names stable I save the model and assign new data to the saved centres, or, if I refit, I match new centres to last month's by nearest distance and carry the names across."
**Explain simply:**
- This is called **label switching**: the grouping can be identical while the numbers differ.
- Best option: keep the fitted model and name the centres; only refit at planned intervals.
- If you must refit, match each new centre to the closest old centre (the Hungarian method in `scipy.optimize.linear_sum_assignment` does this optimally), then rename.
- Alternatively assign names by rule ("highest spend = Champions") rather than by number.
**Worked example (concept questions):** On the made-up 300-customer data, two single-start runs (seeds 1 and 2) gave customer 1 the label 2 in one run and 0 in the other, yet the groupings agreed (ARI 0.99). Matching by centre distance mapped {0 to 2, 1 to 1, 2 to 0}; after renaming, 99.7% of customers had the same label in both runs.
**Alternative / pitfalls:** If behaviour truly shifts, a segment may merge or split; flag that rather than forcing a match. Track a **migration table** (how many customers moved from segment A to B) for the business.
**Likely follow-ups:** 1) *Why does `random_state` fix it?* It fixes the start, so the same numbering repeats on the same data. 2) *What if segment count changes?* Document it and compare at the profile level.
**Common mistakes:** Comparing label numbers across runs; hard-coding "cluster 2 = VIP".

### Q61 ⭐ 🟡 Can you use cluster labels as an input feature in a supervised model, and what risks does that carry?
**Asked at:** commonly asked (no company-specific report found); gap-fill item on combining unsupervised and supervised methods.
**What the interviewer is checking:** That you can use clusters as engineered features and spot leakage.
**Say this in the interview:** "Yes, a cluster label can be a feature, treated as a category and not a number. The risks are leakage, if clustering saw the test data or the target, unstable labels between runs, and little added value if the cluster is just a function of features already in the model."
**Explain simply:**
- A **feature** is an input column; a cluster label compresses several columns into one behaviour type.
- It is a **category**, so one-hot encode it (cluster 2 is not "twice" cluster 1).
- **Leakage:** fit the scaler and k-means on the training data only, then assign test rows; fitting on everything lets test information into training.
- Never include the target in the clustering features.
- Instability: if the labels get renumbered (Q60), the supervised model breaks; keep the saved clustering model.
- Check the benefit by comparing model scores with and without the label on held-out data.
**Worked example (concept questions):** Predicting attrition from tenure, absence and engagement: the cluster "high absence, low engagement" can be a feature. If the cluster was built using the attrition column too, the model is cheating, and its accuracy will look too good.
**Alternative / pitfalls:** Tree models can usually find these patterns themselves; the benefit is bigger for simple linear models. Cluster-wise models (one model per segment) are another option, but need enough rows in each.
**Likely follow-ups:** 1) *Distance to each centre as features?* Also possible. 2) *Does it help interpretability?* Often yes, since named segments are easy to explain.
**Common mistakes:** Feeding the label as a number; clustering before the train/test split; including the target.

### Q62 ⭐ 🟡 What is a Gaussian mixture model, and how does it differ from k-means?
**Asked at:** commonly asked (no company-specific report found); k-means alternatives appear in prep-site banks (unverified).
**What the interviewer is checking:** A basic grasp of soft vs hard clustering.
**Say this in the interview:** "A Gaussian mixture model assumes the data is a blend of several bell-shaped groups and gives each customer a probability of belonging to each group. K-means gives one hard label. A mixture model also allows groups of different shapes and sizes, and tells me who sits on a border."
**Explain simply:**
- **Hard assignment:** each point belongs to exactly one cluster (k-means). **Soft assignment:** a probability per cluster (mixture model).
- k-means implies round, similar-sized clusters; a mixture can stretch each group in different directions.
- In sklearn: `GaussianMixture(n_components=3)`, then `predict_proba`.
- It is slower, has more settings and can be unstable on small data; it still needs scaling and a choice of the number of groups (BIC is a common guide; from memory, unverified here).
**Worked example (concept questions):** On the made-up 300-customer data (3 groups), 94.7% of customers had a top probability above 0.9, but 4 had below 0.7. One customer (12 days, 7 orders, spend 196) got probabilities 0.00, 0.48 and 0.52: k-means labelled this customer firmly as segment 2, but the model shows they sit between two groups. The mixture and k-means groupings agreed at 0.68.
**Alternative / pitfalls:** For a simple segmentation in a business setting, k-means is usually enough; use the mixture when borderline customers matter, for example in targeting thresholds.
**Likely follow-ups:** 1) *Is k-means a special case?* Loosely yes: equal round groups with hard assignment. 2) *How to pick the number of components?* Compare BIC for several values.
**Common mistakes:** Believing probabilities prove the groups are real; skipping scaling.

### Q63 ⭐ 🟡 What is mini-batch k-means, and when would you use it?
**Asked at:** commonly asked (no company-specific report found); a scalability item from prep-site banks (unverified).
**What the interviewer is checking:** That you know a faster variant for large data.
**Say this in the interview:** "Mini-batch k-means updates the centres using small random chunks of data instead of the full dataset each step. It is much faster and uses less memory, with a slight loss in accuracy. I would use it with millions of rows, such as clickstream or transaction logs."
**Explain simply:**
- Regular k-means looks at every point in every round; mini-batch looks at a random sample (the batch, for example 1,024 rows) per round.
- Result: nearly the same centres at much lower cost.
- In sklearn: `MiniBatchKMeans(n_clusters=5, batch_size=1024, random_state=42)`.
- For the tens of thousands of customers an analyst usually segments, normal k-means is fast enough and simpler.
**Worked example (concept questions):** On made-up data of 200,000 rows and 5 features, regular k-means reached inertia 999,194 and mini-batch 999,572, only 0.04% worse, and the two groupings agreed fully (1.0). In this run, mini-batch took about half the time (0.12 seconds vs 0.22 seconds; timings depend on the machine, and the difference grows with data size).
**Alternative / pitfalls:** Results can differ a bit between runs; fix `random_state` and compare with full k-means on a sample before trusting it.
**Likely follow-ups:** 1) *Does it give exactly the same answer?* No, a close approximation. 2) *Other ways to scale?* Cluster a sample, then assign all rows.
**Common mistakes:** Using it on small data where it brings no benefit; forgetting scaling.

### Q64 ⭐ 🟡 How do k-modes and k-medoids differ from k-means, and when are they useful?
**Asked at:** commonly asked (no company-specific report found); categorical-data clustering appears in prep-site k-means banks (unverified).
**What the interviewer is checking:** That you know k-means limits and the standard alternatives.
**Say this in the interview:** "K-means uses averages of numbers, so it does not suit categories like city or payment type. K-modes uses the most common category as the centre and counts mismatches. K-medoids uses a real data point as the centre, so it is more robust to outliers. I would use k-modes for categorical data and k-medoids when outliers distort the mean."
**Explain simply:**
- **k-means:** the centre is the **mean**; works for numbers.
- **k-modes:** the centre is the **mode** (most frequent value in each column); distance = number of columns that differ. Suits categories such as city, device, payment method.
- **k-medoids:** the centre is an actual customer (the **medoid**), the most central one; resistant to outliers and works with other distance measures.
- Mixed data (numbers plus categories): k-prototypes (from memory, unverified).
- These are in separate packages (`kmodes`, `scikit-learn-extra`), neither installed here, so I have not run them; confirm availability before relying on them.
**Worked example (concept questions):** Customers in Pune paying by UPI on mobile vs Pune on web paying COD differ in 2 of 3 columns (distance 2 for k-modes, computed by hand). For spends 10, 12, 11, 13 and 300, the mean is 69.2 (pulled by the outlier), while the medoid is 12 (a real customer), which better describes the group.
**Alternative / pitfalls:** One-hot encoding categories and running k-means is a common shortcut, but distances then become awkward. Gower distance with hierarchical clustering is another option (from memory, unverified).
**Likely follow-ups:** 1) *Which for payroll bands?* Ordered categories may be better as numbers with k-means. 2) *Is k-medoids slower?* Yes, typically.
**Common mistakes:** Running k-means on label-encoded categories (1, 2, 3 imply an order); thinking medoids are averages.

### Q65 ⭐ 🔴 Describe an end-to-end customer segmentation project you would run for an e-commerce company, from raw data to an action plan, including how you would validate it.
**Asked at:** commonly asked (no company-specific report found); the prompt "split customers into groups from a year of purchases" appears in candidate-shared prompts (unverified), and this is a typical case-study question.
**What the interviewer is checking:** Structured thinking from business goal to action and measurement.
**Say this in the interview:** "I start with the business goal, then build one row per customer from orders, compute RFM and a few behaviour fields, clean and scale, cluster with k-means across a few k, choose using silhouette, stability and usefulness, profile and name the segments, recommend one action each, and measure them with a holdout test."
**Explain simply:**
1. **Goal:** for example "reduce churn" or "raise repeat purchase"; it decides features and the number of segments.
2. **Data:** orders, customers, returns; one row per customer; cut-off date; remove test orders and refunds; handle one-time buyers.
3. **Features:** recency, frequency, monetary (log-transformed if skewed), maybe category mix, discount use, return rate.
4. **Prepare:** treat outliers and missing values, scale.
5. **Model:** k-means for k = 2 to 8; compare silhouette and stability (bootstrap agreement).
6. **Profile and name:** table in original units, size and revenue share; one action each.
7. **Validate:** stability, business sense, and a campaign holdout test (Q52). Add a monitoring plan: re-score monthly with the saved model.
8. **Deliver:** short deck, segment list in the CRM, an owner and metrics.
**Worked example (concept questions):** On the made-up 300-customer data, the result is 3 segments: Champions (77 customers, 65% of revenue), Regulars (134, 27%) and Lapsed (89, 8%). Actions: loyalty rewards for Champions, cross-sell to Regulars, win-back offers with a cost cap for Lapsed.
**Alternative / pitfalls:** Rules-based RFM scoring is easier to explain and may be enough; compare it with k-means. Customer data is personal: keep it inside approved tools, minimise it, and follow company policy (Q53).
**Likely follow-ups:** 1) *How long would it take?* Depends on data readiness; most time goes into cleaning. 2) *How would you know it worked?* Lift against a holdout.
**Common mistakes:** Starting with the algorithm; no action plan; no validation or monitoring.

### Q66 ⭐ 🔴 How is RFM related to customer lifetime value, and where does RFM fall short as a predictive tool?
**Asked at:** commonly asked (no company-specific report found); CLV is a differentiator question, not tied to a company.
**What the interviewer is checking:** That you see RFM as descriptive and CLV as forward-looking, and know the gap.
**Say this in the interview:** "RFM describes past behaviour, and its parts are the ingredients of customer lifetime value: how often someone buys, how much they spend, and how recently they were active, which signals whether they will stay. But RFM only ranks customers by the past; CLV tries to predict future value."
**Explain simply:**
- **CLV (customer lifetime value):** the total profit expected from a customer over their relationship.
- A simple CLV: yearly margin per customer divided by the churn rate (1 minus the retention rate). A fuller version discounts future years.
- Frequency x monetary relates to yearly value; recency hints at whether the customer is still active (retention).
- Gaps in RFM: no explicit future prediction; the same score can mean different things (a new customer with one big order vs a long-term regular); ignores margin, returns, seasonality, product mix and customer age; scores are relative (quintiles), not in money.
- Better tools: probabilistic models such as BG/NBD with Gamma-Gamma (from memory, unverified), or a supervised model predicting next-12-month spend.
**Worked example (concept questions):** Average order 800, 3 orders per year, 25% margin gives 600 yearly margin. With 70% yearly retention, simple CLV = 600 / (1 - 0.7) = 2,000 (undiscounted; these are exercise inputs). At 80% retention, CLV becomes 3,000: retention changes value more than small changes in order size.
**Alternative / pitfalls:** Validate any CLV prediction on a later period (train on year 1, check year 2). Do not use RFM alone for high-stakes decisions such as credit.
**Likely follow-ups:** 1) *Can you add RFM to a predictive model?* Yes, as features. 2) *What is the simplest honest fix?* Report average future spend per RFM segment from past data.
**Common mistakes:** Equating a high RFM score with high lifetime value; ignoring margin; forgetting that retention drives CLV.

