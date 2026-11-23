# ⚡ Momentum MF Screener

A lightweight web application built with **Python** and **Streamlit** to screen, shortlist, and rank Indian mutual funds based on their **1-year momentum (percentage NAV return)** using live market data.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)

---

## 📌 Overview

Comparing 1-year performance across multiple Indian mutual fund schemes manually requires switching between portals and spreadsheets. **Momentum MF Screener** streamlines this workflow into a single interactive dashboard:

1. Pulls the complete directory of Indian mutual fund schemes via API.
2. Lets users filter and build a custom watchlist without duplicates.
3. Fetches historical Net Asset Value (NAV) data for each selected scheme, calculates 1-year percentage change, and ranks funds from highest to lowest momentum.

---

## ✨ Key Features

- **Live Mutual Fund Directory:** Dynamically fetches up-to-date scheme codes and names from [MFapi.in](https://www.mfapi.in/).
- **Keyword Filtering & Multi-Select:** Quickly narrow down thousands of schemes using case-insensitive keyword search.
- **Stateful Watchlist Management:** Uses Streamlit `session_state` to maintain a custom shortlist across interactions, with built-in duplicate prevention and one-click reset.
- **Automated 1-Year Momentum Ranking:** Retrieves latest and 1-year historical NAVs, computes percentage returns, and renders a sorted comparison table.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **Frontend / UI** | Streamlit |
| **Data Manipulation** | Pandas |
| **HTTP / API Integration** | Requests |
| **Data Source** | [MFapi.in](https://www.mfapi.in/) (AMFI NAV Data) |

---

## ⚙️ How It Works

1. **Scheme Ingestion:** Calls `GET https://api.mfapi.in/mf` on load and parses `schemeCode` and `schemeName` into a Pandas DataFrame.
2. **Watchlist Curation:** Users filter by keyword, select schemes, and append unique `{name, code}` pairs to `st.session_state.selected_funds`.
3. **NAV Retrieval & Calculation:** On clicking **Fetch NAV Data**, the app queries `GET https://api.mfapi.in/mf/{schemeCode}` for each shortlisted fund, extracts the latest NAV and the NAV from 365 days prior, and computes:
   $$\text{1-Year Return (\%)} = \left(\frac{\text{Latest NAV} - \text{1-Year Ago NAV}}{\text{1-Year Ago NAV}}\right) \times 100$$
4. **Ranked Output:** Aggregates results into a Pandas DataFrame sorted in descending order of 1-year return.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/shubhamharwani/momentum-mf.git](https://github.com/shubhamharwani/momentum-mf.git)
   cd momentum-mf
