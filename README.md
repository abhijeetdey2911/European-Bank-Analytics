# European Bank Customer Analytics

<<<<<<< HEAD
## Customer Engagement & Product Utilization Analytics for Retention Strategy

A Financial Analytics internship project focused on understanding customer engagement, product utilization, and customer retention patterns using European Bank customer data.

The project includes an interactive Streamlit dashboard that helps identify churn patterns, disengaged high-value customers, product-related risk segments, and relationship strength.

---

## Project Overview

Customer retention is influenced by more than financial value alone.

This project analyzes whether customer engagement, product utilization, and financial characteristics are associated with customer churn.

The analysis focuses on identifying:

- Engagement patterns associated with churn
- Product utilization and retention
- High-balance but inactive customers
- Relationship strength
- Geographic differences in churn
- Potential customer segments requiring retention attention

---

## Objectives

The main objectives of this project are:

1. Analyze the relationship between customer engagement and churn.
2. Evaluate product utilization and customer retention.
3. Identify high-balance customers who are inactive.
4. Analyze relationship strength using engagement and product usage.
5. Identify customer segments that may require targeted retention strategies.
6. Provide actionable business insights for improving customer retention.

---

## Dataset

The project uses the `European_Bank.csv` dataset containing 10,000 customer records.

### Dataset Features

| Feature | Description |
|---|---|
| Year | Dataset year |
| CustomerId | Unique customer identifier |
| Surname | Customer surname |
| CreditScore | Customer credit score |
| Geography | Customer country |
| Gender | Customer gender |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products used |
| HasCrCard | Credit card ownership |
| IsActiveMember | Customer engagement indicator |
| EstimatedSalary | Estimated customer salary |
| Exited | Customer churn indicator |

`Exited = 0` represents retained customers.

`Exited = 1` represents churned customers.

---

## Methodology

The project follows the following analytical workflow:

### 1. Data Ingestion

The customer dataset is loaded using Pandas.

### 2. Data Validation

The dataset was checked for:

- Missing values
- Duplicate records
- Data types
- Dataset dimensions
- Category distributions

### 3. Customer Engagement Analysis

Customers are classified based on their active membership status.

Churn rates are compared between active and inactive customers.

### 4. Product Utilization Analysis

Customer churn is analyzed according to the number of products used.

Customers with 3 or more products are treated as a separate risk group because of their unusually high churn pattern.

### 5. High-Value Customer Analysis

The 75th percentile of customer balance is used as the high-balance threshold.

Customers who have:

- High balance
- Inactive membership

are identified as high-value disengaged customers.

### 6. Relationship Strength Analysis

Relationship strength is evaluated using customer engagement and product utilization.

The project uses the following exploratory segmentation:

- Strong
- Moderate
- Weak
- Product-Risk

---

## Key Findings

### Overall Churn

The overall customer churn rate is:

**20.37%**

Out of 10,000 customers:

- 7,963 customers stayed
- 2,037 customers churned

---

### Customer Engagement

Active customers show a lower churn rate than inactive customers.

| Engagement | Churn Rate |
|---|---:|
| Active | 14.27% |
| Inactive | 26.85% |

This represents a difference of approximately **12.58 percentage points**.

The result suggests that customer engagement is strongly associated with retention.

---

### High-Value Disengaged Customers

The 75th percentile balance threshold is approximately:

**127,644**

There are:

**1,247 high-balance inactive customers**

within the dataset.

Their churn rate is approximately:

**30.47%**

This indicates that financial value alone does not necessarily imply customer loyalty.

---

### Geographic Churn

| Geography | Churn Rate |
|---|---:|
| Germany | 32.44% |
| Spain | 16.67% |
| France | 16.15% |

Germany shows the highest churn rate among the three countries.

---

### Product Utilization

Customers using 2 products show substantially lower churn than customers using 1 product.

However, customers with 3 or more products form a relatively small but unusually high-churn segment.

The churn rate among all customers with 3+ products is approximately:

**85.89%**

Because this group is relatively small, the result should be treated as a risk signal requiring further investigation rather than evidence that having more products causes churn.

---

### Credit Card Stickiness

Credit card ownership shows only a small difference in churn.

Therefore, credit card ownership alone does not appear to be a major retention factor in this dataset.

---

## Dashboard

The project includes an interactive Streamlit dashboard with five analytical modules:

### 1. Overview

Provides:

- Total customers
- Churn rate
- Active customers
- High-value disengaged customers
- Customer status
- Churn by engagement
- Churn by geography
- Customer summary
- Key insights

### 2. Engagement Analysis

Analyzes:

- Active versus inactive customers
- Customer distribution
- Churn rate by engagement
- Engagement summary

### 3. Product Analysis

Analyzes:

- Product utilization
- Churn by number of products
- Product count + engagement
- High-risk product segments

### 4. High-Value Customers

Identifies:

- High-balance customers
- Inactive high-balance customers
- Their churn rate
- At-risk customer records
- Downloadable CSV list

### 5. Relationship Strength

Analyzes:

- Strong relationships
- Moderate relationships
- Weak relationships
- Product-risk customers
- Churn by relationship category

---

## Business Recommendations

Based on the analysis, the following strategies are recommended:

### 1. Improve Customer Engagement

Develop targeted engagement campaigns for inactive customers.

Examples include:

- Personalized communication
- Product usage reminders
- Relevant offers
- Relationship-manager outreach

### 2. Prioritize High-Value Disengaged Customers

Customers with high balances but low engagement should receive targeted retention attention.

### 3. Investigate the 3+ Product Segment

The unusually high churn rate among customers with 3+ products should be investigated further.

Possible areas for investigation include:

- Product combinations
- Customer experience
- Pricing
- Service issues
- Product suitability
- Account complexity

### 4. Focus on High-Churn Geography

Germany has the highest observed churn rate and should receive additional customer-retention analysis.

### 5. Avoid Using Financial Value Alone

High account balances should not be treated as a guarantee of loyalty.

Customer value should be evaluated alongside engagement and product utilization.

---

## Technology Stack

- Python
- Pandas
- Matplotlib
- Streamlit
- GitHub

---
=======
### Customer Engagement & Product Utilization Analytics for Retention Strategy

A Financial Analytics project that analyzes customer engagement, product utilization, and churn patterns to identify retention opportunities.

## Key Insights

- Overall churn rate: **20.37%**
- Active customer churn: **14.27%**
- Inactive customer churn: **26.85%**
- High-balance inactive customers: **1,247**
- High-balance inactive churn: **30.47%**
- Highest geographic churn: **Germany – 32.44%**
- 3+ product customer churn: **85.89%**

## Dashboard

The interactive Streamlit dashboard includes:

- Customer Overview
- Engagement Analysis
- Product Utilization Analysis
- High-Value Customer Detection
- Relationship Strength Analysis
- Interactive filters
- At-risk customer identification
- CSV export

## Tech Stack

**Python • Pandas • Matplotlib • Streamlit**
>>>>>>> 0729d3b5abb910a515063b41dec011243a9ac6c3

## Project Structure

```text
European-Bank-Analytics/
<<<<<<< HEAD
│
├── data/
│   └── European_Bank.csv
│
├── app.py
├── requirements.txt
└── README.md
=======
├── data/
│   └── European_Bank.csv
├── app.py
├── requirements.txt
└── README.md
>>>>>>> 0729d3b5abb910a515063b41dec011243a9ac6c3
