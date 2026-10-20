# Book 1 Part 06 sources: Time series & forecasting (researched 2026-10-20)

## Method and honesty notes
- WebSearch worked (US-only, standard mode): 4 searches plus 4 page fetches. WebFetch of datainterview.com returned HTTP 429 (blocked); its content is known only from the search-result snippet.
- Glassdoor, AmbitionBox, Blind, LeetCode Discuss: no dedicated time-series interview threads retrievable. No first-hand 2025 Flipkart, Swiggy, PhonePe, Amazon India, Microsoft IDC, JPMC, Spotify, Zalando, Booking or Klarna time-series interview reports were found. A Telegram post (t.me/s/geekycod) on a Swiggy DS process lists coding and classical ML only (undated, seen in search only). A Glassdoor Blinkit review (Feb 2025, glassdoor.com.mx/Entrevista/Blinkit-Entrevista-E1007293-RVW104543889.htm, seen in search) shows recsys/classical-ML focus, no forecasting.
- Therefore "frequency" below counts independent question banks/postings listing the topic, not first-hand interview counts. Stars are partly expert judgement; "Asked at" tags in the question file are typical-role tags, not verified reports, except Prepfully (Disney, Novartis, Marqeta, Rovio).

## Sources actually opened or seen
| ID | URL | What it gave | Recency |
|---|---|---|---|
| S1 | https://hyring.com/jobseeker-toolkit/interview-questions/technical/time-series | Opened. 45 questions: fundamentals, practical (lag features, split, metrics, holidays, stockouts, multi-step, many series, intervals, monitoring, retraining), advanced (random split, 1-step vs 12-step, MAPE low volume, new product, promo, weather feature unknown at forecast time, reconciliation, intervals miss, late data, deep vs baseline) | 2026 |
| S2 | https://github.com/devinterview-io/time-series-interview-questions | Opened. Stationarity, white noise vs random walk, differencing, AR/MA/ARMA/ARIMA, ACF/PACF, lag selection, SARIMA | undated |
| S3 | https://prepfully.com/answers/time-series-forecasting?show=true | Opened. "Explain TS forecasting to a non-expert"; asked to DS at Disney, Novartis, Marqeta; Rovio DS interview reported 29 Jul 2025 | 2025 |
| S4 | https://www.datainterview.com/blog/time-series-interview-questions | Snippet only (fetch 429). Trend, seasonality, stationarity, lag/rolling, horizons, backtesting, metrics, monitoring; leakage edge cases | 2025-26 |
| S5 | https://dataford.io/questions/describe-your-approach-to-time-series-forecasting (and sibling dataford pages incl. FedEx) | Seen in search only. Experience/approach questions | 2025-26 |
| S6 | https://jobs.aumovio.com/en/detail-page/job-detail/REF8750P-p-d5465bdd7137cece831989f88918ccd9/data-scientist-ai-for-demand-forecasting-m-f-d-/ | Seen in search. Job posting: reconciliation (bottom-up/top-down/MinT), ARIMA/ETS to XGBoost/LightGBM to TFT/N-BEATS | 2025-26 |
| S7 | https://engrxiv.org/preprint/view/6726 | Seen in search. Walmart hierarchical reconciliation study | 2025 |
| S8 | https://arxiv.org/html/2403.07815v1 ; https://arxiv.org/pdf/2412.12834 ; https://dev.to/andrew-ooo/timesfm-25-review-googles-time-series-foundation-model-14kp | Seen in search. Chronos, TimesFM, zero-shot limits (background for AI-era Qs, not interview reports) | 2024-26 |
| S9 | https://www.hirist.tech/j/data-scientist-time-series-forecasting-1668082 | Seen in search. India forecasting job: ARIMA/ETS/Prophet/XGBoost/LightGBM | 2025-26 |

## Frequency by topic (count of S1-S9 mentioning)
| Topic | Sources | Count |
|---|---|---|
| Stationarity | S1,S2,S4 | 3 |
| Random split / time-based split / backtesting / walk-forward | S1,S4 | 2 |
| ARIMA, ACF/PACF, differencing, SARIMA | S1,S2,S4,S9 | 4 |
| Lag/rolling features, leakage | S1,S4,S9 | 3 |
| Metrics (MAPE/WAPE/MASE) | S1,S4 | 2 |
| Holidays/promos/exogenous | S1,S6 | 2 |
| Hierarchical reconciliation | S1,S6,S7 | 3 |
| Many related series / global models | S1,S6 | 2 |
| Stockouts, new product, intermittent | S1 | 1 |
| Monitoring/retraining | S1,S4 | 2 |
| Deep models (TFT/N-BEATS) | S6 | 1 |
| Foundation models (Chronos/TimesFM) | S8 | 1 (non-interview) |
| Explain to non-technical | S3 | 1 (several companies) |

## AI-era changes noted
- Foundation TS models (Chronos, TimesFM, Moirai) appear in job descriptions and senior discussions; expect "zero-shot vs tuned GBM" questions.
- Code-review rounds with LLM-generated forecasting code: classic bugs are shuffled splits, scaler/feature leakage, future-looking rolling windows.
- Emphasis on leakage and backtest honesty (S4) over model-zoo recitation; "can an LLM forecast?" is a plausible GenAI follow-up.
- Pure ARIMA-derivation questions declining; GBM-with-lags and backtesting dominate for product companies.

## Question -> origin (54 questions; "found in sources" = topic present in S1-S9, "expert gap-check" = added by me)
| Q | Stars | Origin |
|---|---|---|
| Q1 What is stationarity, why does it matter for time series models, and how do | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q2 What are the components of a time series (trend, seasonality, cyclic, noise | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q3 Why is a random train/test split wrong for time series, and how should you  | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q4 How would you explain time series forecasting to a non-technical stakeholde | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q5 Which baselines would you build first (naive, seasonal naive, moving averag | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q6 What is differencing, how do you choose d, and what goes wrong with over-di | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q7 How do you read ACF and PACF plots to choose p and q for an ARIMA model? | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q8 Explain ARIMA(p,d,q). How do you select orders (AIC/BIC, auto_arima) and wh | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q9 What is walk-forward validation / backtesting? Compare expanding vs rolling | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q10 How do you build lag and rolling-window features for a GBM (XGBoost/LightGB | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q11 Which forecast metric would you choose (MAE, RMSE, MAPE, sMAPE, MASE, WAPE) | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q12 ARIMA vs Prophet vs GBM with lag features vs deep learning: how do you choo | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q13 How do you model holidays, promotions and other external regressors (exogen | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q14 How do you handle missing timestamps, missing values and outliers in a time | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q15 How do you forecast multiple steps ahead (recursive, direct, multi-output)? | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q16 Design an end-to-end demand/sales forecasting solution: data, features, mod | ⭐⭐⭐ | found in sources (topic lists / postings) |
| Q17 What is the difference between white noise and a random walk, and why does  | ⭐⭐ | found in sources (topic lists / postings) |
| Q18 Explain AR, MA and ARMA models. What does each term capture intuitively? | ⭐⭐ | found in sources (topic lists / postings) |
| Q19 How do you do cross-validation with sklearn TimeSeriesSplit? What does the  | ⭐⭐ | expert gap-check |
| Q20 How does SARIMA handle seasonality, and how do you pick seasonal orders (P, | ⭐⭐ | found in sources (topic lists / postings) |
| Q21 Explain exponential smoothing (SES, Holt, Holt-Winters/ETS). When is it bet | ⭐⭐ | found in sources (topic lists / postings) |
| Q22 How does Prophet work (trend, seasonality, holidays, changepoints), and wha | ⭐⭐ | found in sources (topic lists / postings) |
| Q23 How do you encode calendar features for ML forecasters (day-of-week, month, | ⭐⭐ | expert gap-check |
| Q24 When do you use a log or Box-Cox transform in forecasting, and how do you b | ⭐⭐ | expert gap-check |
| Q25 How do you diagnose a fitted forecasting model using residuals (Ljung-Box,  | ⭐⭐ | expert gap-check |
| Q26 How do you produce prediction intervals / uncertainty ranges (analytic, boo | ⭐⭐ | found in sources (topic lists / postings) |
| Q27 Global vs local models: how do you forecast thousands of related series, an | ⭐⭐ | found in sources (topic lists / postings) |
| Q28 Why does a demand forecast under-forecast after stockouts, and how do you h | ⭐⭐ | found in sources (topic lists / postings) |
| Q29 How do you forecast a new product or new store with no history (cold start) | ⭐⭐ | found in sources (topic lists / postings) |
| Q30 How do you forecast intermittent / lumpy demand? Explain Croston, SBA, TSB  | ⭐⭐ | found in sources (topic lists / postings) |
| Q31 When would you use LSTM/GRU/1D-CNN for forecasting instead of GBM, and why  | ⭐⭐ | found in sources (topic lists / postings) |
| Q32 How do you monitor a deployed forecast model and decide retraining frequenc | ⭐⭐ | found in sources (topic lists / postings) |
| Q33 One-step-ahead forecasts look good but 12-step-ahead forecasts fail. What a | ⭐⭐ | found in sources (topic lists / postings) |
| Q34 A useful feature (e.g. weather, ad spend) is not known at forecast time. Ho | ⭐⭐ | found in sources (topic lists / postings) |
| Q35 How do you handle structural breaks, regime shifts (COVID, pricing change)  | ⭐⭐ | found in sources (topic lists / postings) |
| Q36 A deep model beats the baseline in training but not in backtesting. What do | ⭐⭐ | found in sources (topic lists / postings) |
| Q37 How do you pick a forecast loss when over- and under-forecasting have diffe | ⭐⭐ | found in sources (topic lists / postings) |
| Q38 How does late-arriving or revised recent data affect forecasting, and how d | ⭐⭐ | found in sources (topic lists / postings) |
| Q39 A promotion changes the demand pattern. How do you separate baseline demand | ⭐⭐ | found in sources (topic lists / postings) |
| Q40 Why does autocorrelation in residuals break OLS regression assumptions, and | ⭐⭐ | expert gap-check |
| Q41 What is forecast combination/ensembling and why does averaging models often | ⭐⭐ | expert gap-check |
| Q42 What is hierarchical forecasting? Explain bottom-up, top-down and MinT reco | ⭐⭐ | found in sources (topic lists / postings) |
| Q43 How do you tune hyperparameters of a forecasting model (e.g. LightGBM, Prop | ⭐ | expert gap-check |
| Q44 Implement from scratch in NumPy: moving average, simple exponential smoothi | ⭐ | expert gap-check |
| Q45 AI-era: review this LLM-generated forecasting code. Spot leakage (shuffled  | ⭐ | expert gap-check |
| Q46 Which probabilistic forecast metrics do you use (pinball loss, CRPS, covera | ⭐ | expert gap-check |
| Q47 What is conformal prediction for time series, and why do standard conformal | ⭐ | expert gap-check |
| Q48 Compare modern deep forecasters: DeepAR, N-BEATS, Temporal Fusion Transform | ⭐ | found in sources (topic lists / postings) |
| Q49 AI-era: What are time-series foundation models (Chronos, TimesFM, Moirai)?  | ⭐ | found in sources (topic lists / postings) |
| Q50 AI-era: Can you prompt an LLM to forecast numbers? What works, what fails,  | ⭐ | expert gap-check |
| Q51 Explain VAR, Granger causality and cointegration. When is each appropriate? | ⭐ | expert gap-check |
| Q52 What is a state-space model / Kalman filter and how does it relate to expon | ⭐ | expert gap-check |
| Q53 What is GARCH / volatility modelling and when do you model variance instead | ⭐ | expert gap-check |
| Q54 How would you use Bayesian structural time series / counterfactual forecast | ⭐ | expert gap-check |

