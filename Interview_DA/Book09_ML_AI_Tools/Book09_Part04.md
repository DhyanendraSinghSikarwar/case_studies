# Book 9 — Basic ML + AI Tools for Analysts | Part 4: Clustering and Customer Segmentation (k-means, RFM) 🟡

**Target:** 60 questions | **Actual:** 66 questions
**Scope:** clustering vs classification, k-means mechanics and sklearn code, choosing k, scaling, RFM scoring and segment actions, validating and presenting segments, with HR flavour where natural.

### Q1 ⭐⭐⭐ 🟢 What is clustering, and how is it different from classification?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is customer segmentation, and why do businesses do it?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Explain k-means clustering to a non-technical marketing manager in plain words.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What are the steps of the k-means algorithm?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What does RFM stand for, and what does each letter measure?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you choose the number of clusters k in k-means?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Why must you scale the features before running k-means, and how do you do it in sklearn?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Perform one k-means iteration by hand: which cluster does P3 join, and what are the new centroids?
Points: P1 (1, 1), P2 (2, 1), P3 (4, 3), P4 (5, 4). Initial centroids: c1 = (1, 1) and c2 = (5, 4). Use Euclidean distance; the P1/P4 assignments are given by the centroids themselves, so assign P2 and P3 and recompute both centroids.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Using the table below, calculate recency in days, average order value and say which customer is the most recent buyer.
Reference date: 2026-04-01.
| Customer | Last purchase | Orders | Total spend (INR) |
|---|---|---|---|
| C1 | 2026-03-25 | 5 | 4,000 |
| C2 | 2026-01-10 | 12 | 9,600 |
| C3 | 2026-03-30 | 1 | 500 |
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Write pandas code that builds an RFM table (recency, frequency, monetary) per customer from an orders table.
Table `orders` has columns `customer_id`, `order_date` (datetime), `amount`. Use the day after the last order date in the data as the reference date.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Write sklearn code that scales three RFM columns, fits k-means with 4 clusters, and attaches the cluster label to each customer.
DataFrame `rfm` has columns `customer_id`, `recency`, `frequency`, `monetary`.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Given these 10 recency values (days since last purchase), assign R scores from 1 to 5 using quintiles, where 5 is the best score.
Recency days for 10 customers: 3, 5, 9, 14, 20, 30, 45, 60, 90, 120.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How is RFM segmentation different from k-means clustering, and when would you use each?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 A manager asks you to split customers into high, medium and low value groups using their last 12 months of purchase history. What approach do you take?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 You have named segments such as Champions, Loyal, At Risk and Hibernating. What marketing or retention action would you suggest for each?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 How do you decide whether a set of customer segments is actually useful to the business?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What does k-means actually minimise, and what is inertia?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Does k-means need labelled data, and what does that mean for how you judge the result?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 What does a high RFM score such as 555 mean, compared with 155 and 511?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How is k-means different from k-nearest neighbours (KNN)?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is the difference between segments, cohorts and personas?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Using the inertia values below, which k would you choose with the elbow method, and why?
k = 1 to 6, inertia: 1000, 520, 300, 260, 240, 228.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Using the silhouette scores below, which k looks best, and what else would you check before deciding?
k = 2, 3, 4, 5, 6 gives silhouette scores 0.41, 0.48, 0.55, 0.43, 0.36.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Calculate the silhouette value of a single point where its average distance to its own cluster is 2 and its average distance to the nearest other cluster is 5. What would a value of -0.25 tell you?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Compute the inertia (within-cluster sum of squared distances) for the two clusters below.
One-dimensional data. Cluster A: 2, 4, 6. Cluster B: 10, 12.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Compare the Euclidean distance between two customers before and after standardising, and explain what it shows.
Customer A: age 50, income 100,000. Customer B: age 30, income 40,000. Age has mean 40 and standard deviation 10; income has mean 60,000 and standard deviation 20,000.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Apply the rules below to label each customer by RFM score.
Rules in order: Champions if R >= 4 and F >= 4; At Risk if R <= 2 and F >= 4; New if R >= 4 and F <= 2; otherwise Hibernating if R <= 2 and F <= 2; anything else Other.
| Customer | R | F | M |
|---|---|---|---|
| C1 | 5 | 5 | 5 |
| C2 | 1 | 5 | 4 |
| C3 | 2 | 1 | 1 |
| C4 | 4 | 2 | 3 |
| C5 | 3 | 3 | 3 |
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Work out the average recency, frequency and monetary values of this cluster and suggest a label for it.
Customers in the cluster (recency in days, orders, spend in INR): (10, 8, 5,000), (20, 6, 4,000), (30, 10, 6,000).
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Given the cluster sizes and revenue shares below, which segments deserve the most attention and why?
10,000 customers in total. Cluster sizes (customers): 4,000; 3,000; 2,000; 800; 200. Share of revenue: 10%, 20%, 20%, 25%, 25% respectively.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Read the code below. What do `labels_`, `cluster_centers_` and `inertia_` contain, and what does the last line print?
```python
km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_scaled)
print(km.labels_[:5], km.cluster_centers_.shape, km.inertia_)
print(len(km.labels_) == len(X_scaled))
```
`X_scaled` has 500 rows and 4 columns.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 What is wrong with this segmentation code, and how would you fix it?
```python
X = df[['customer_id', 'recency', 'monetary']]
km = KMeans(n_clusters=4).fit(X)
```
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Why do analysts often apply a log transform to the monetary value before k-means, and what happens if they do not?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you treat customers with a single purchase, and returns or refunds, when building RFM?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you choose the reference date for recency, and what goes wrong if you pick it carelessly?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How many segments should you create in practice, and what limits the number?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 One of your k-means clusters contains only 2 customers. What do you do?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do outliers affect k-means, and how do you handle them?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What are the main limitations of k-means?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Does k-means always find the best solution? Explain initialisation, k-means++ and the role of n_init and random_state.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How does hierarchical clustering differ from k-means, and how do you read a dendrogram?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How can k-means handle categorical variables such as city or payment method?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Two of your clustering features are highly correlated. Does it matter for k-means?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 How do you handle missing values before clustering?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How would you visualise clusters when there are more than three features?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Should recency, frequency and monetary carry equal weight in RFM, and what if frequency and monetary are strongly correlated?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 How do you check that your segments are stable and not an accident of one random run?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 You have fitted a k-means model and a new batch of customers arrives. How do you assign them to segments?
Assume `scaler` and `km` were fitted earlier on the training data.
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 Write a SQL query that computes recency, frequency and monetary per customer and assigns 1 to 5 scores with NTILE.
Table `orders(customer_id, order_date, amount)`. Reference date: 2026-04-01. Any SQL dialect is fine; state which one you use.
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 You are asked to segment employees by tenure, absence days and engagement score for a retention programme. Describe your approach and one risk.
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 You have a cluster profile table in original units. Describe how you would turn it into named segments for the HR team.
| Cluster | Avg tenure (years) | Avg absence days | Avg engagement (1-5) | Employees |
|---|---|---|---|---|
| 0 | 1.2 | 3 | 3.1 | 300 |
| 1 | 6.8 | 4 | 4.2 | 250 |
| 2 | 4.5 | 14 | 2.3 | 90 |
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 How would you present customer segments to a marketing team that does not know statistics?
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 After you target a segment with a campaign, how do you measure whether the segmentation actually helped?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 What privacy and fairness concerns arise when you segment customers or employees, and how do you handle them?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 A cluster is described as 'Segment 2' with no further meaning. A stakeholder asks what it is. What would a good analyst do?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 When the elbow curve is smooth with no clear bend, what do you do?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🔴 Is the clustering result 'right'? How do you defend your choice of k when the silhouette score favours 3 and the business wants 5 segments?
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟡 What is DBSCAN, and when would you prefer it to k-means?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 Compare StandardScaler and MinMaxScaler for clustering. Does the choice change the clusters?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟡 What would happen to inertia if you set k=1, and if you set k equal to the number of points?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟡 Why do cluster numbers change between runs, and how do you keep segment names consistent month to month?
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 Can you use cluster labels as an input feature in a supervised model, and what risks does that carry?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟡 What is a Gaussian mixture model, and how does it differ from k-means?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟡 What is mini-batch k-means, and when would you use it?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟡 How do k-modes and k-medoids differ from k-means, and when are they useful?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🔴 Describe an end-to-end customer segmentation project you would run for an e-commerce company, from raw data to an action plan, including how you would validate it.
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🔴 How is RFM related to customer lifetime value, and where does RFM fall short as a predictive tool?
<!-- ANSWER_PENDING -->
