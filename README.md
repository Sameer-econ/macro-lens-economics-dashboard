# MacroLens — Economic Intelligence Dashboard

> A dark, interactive macroeconomic dashboard built with Python, Streamlit, Pandas and Plotly.

MacroLens lets you explore GDP growth, inflation and unemployment trends across five countries. It includes filters, KPI cards, line and bar charts, a macro overview heatmap, a filtered data table and CSV export.

## ⚠️ Data note

**The included dataset is synthetic and illustrative. It is not official economic data.** The values are designed to make the dashboard usable immediately while you learn. Do not cite them as real-world statistics. Before using MacroLens for research or decision-making, replace the sample file with sourced data and document each indicator's definition, unit, source and download date.

## Preview

After starting the app, the dashboard includes:
- Country and year filters
- Selectable macroeconomic indicator
- KPI cards for the current view
- Interactive trend chart and latest-year country comparison
- Heatmap of the latest observations
- Filtered data table and CSV download
- Notes on interpretation and correlation versus causation

## Tech stack

- **Python** — application logic
- **Pandas** — loading and filtering tabular data
- **Streamlit** — web dashboard interface
- **Plotly Express** — interactive charts

## Run locally

### 1. Install Python

Install a current version of Python 3 from [python.org](https://www.python.org/downloads/). During Windows installation, tick **Add Python to PATH** if the installer offers it.

### 2. Download the project

On GitHub, open this repository and select **Code → Download ZIP**, then extract the folder. Or clone it:

```bash
git clone https://github.com/YOUR-USERNAME/macrolens-economic-dashboard.git
cd macrolens-economic-dashboard
```

Replace `YOUR-USERNAME` with your GitHub username.

### 3. Create a virtual environment (recommended)

**Windows:**
```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Launch MacroLens

```bash
python -m streamlit run app.py
```

Streamlit will show a local address, usually `http://localhost:8501`, to open in your browser.

## Project structure

```text
macrolens-economic-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_economic_data.csv
└── screenshots/
    └── (add your dashboard screenshot here)
```

## Data schema

`data/sample_economic_data.csv` has one observation per country, year and indicator.

| Column | Meaning |
|---|---|
| `year` | Observation year |
| `country` | Country label |
| `indicator` | GDP growth, inflation or unemployment |
| `value` | Illustrative percentage value |
| `data_type` | Explicit synthetic-data label |

## How to replace the sample data

1. Download data from a trustworthy, documented source such as the [World Bank Data portal](https://data.worldbank.org/), [IMF](https://www.imf.org/en/Data), [OECD Data Explorer](https://data-explorer.oecd.org/) or a national statistical agency.
2. Keep the CSV columns and indicator names consistent, or update the app to match your new schema.
3. Record the source URL, retrieval date, unit and definition in the documentation.
4. Do not combine incompatible definitions without explaining the difference.
5. Remove or revise the demo-data warning in `app.py` only after the synthetic data has been replaced and verified.

## Suggested next improvements

- Add a real-data ingestion script with documented API sources
- Add a source and methodology page
- Add year-over-year change and moving averages
- Add downloadable chart images and a comparison summary
- Add automated tests for data validation

## Learning goals

This project demonstrates beginner-friendly skills: reading CSV files, filtering rows, grouping observations, creating interactive charts, building a sidebar interface, and exporting data.

## Disclaimer

MacroLens is an educational project, not investment advice or an official statistical publication.
