# 🎥 **TMDB Movie Dataset Analysis and Dashboard**

## 📖 **About the Project**
This project explores the TMDB dataset, uncovering insights about movies' financial and popularity metrics. The interactive dashboard allows users to dynamically explore trends and relationships in the dataset.

### **Source**
- [Kaggle](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
### ** View the Dashboard Here!**
- https://movie-testing-yapmatt.streamlit.app/

---

## 📂 **Dataset Overview**
| Feature                | Description                                                      |
|------------------------|------------------------------------------------------------------|
| `title`               | Movie title                                                     |
| `genres`              | Movie genres                                                   |
| `release_date`        | Release date of the movie                                       |
| `revenue_musd`        | Revenue in millions of USD                                      |
| `budget_musd`         | Budget in millions of USD                                       |
| `profit_musd`         | Calculated as `revenue_musd - budget_musd`                     |
| `vote_average`        | Average rating by users                                         |
| `production_countries`| Countries where the movie was produced                         |
| `original_language`   | Original language of the movie                                  |

---

## 🛠️ **Data Cleaning Process**

The dataset was cleaned to ensure consistent, reliable, and actionable insights. Below are the steps undertaken:

---

### **1. Handling Missing Values**
- Columns with missing values such as `budget`, `revenue`, and `runtime` were either:
  - Imputed with appropriate values.
  - Dropped if they contained excessive missing data.
  
**Reasoning:** Missing values in critical columns could skew analysis.

---

### **2. Dropping Duplicates**
- Identified duplicate rows using the `title`, `release_date`, and `id` columns.
- Removed duplicate entries from the dataset.

**Reasoning:** Retaining duplicates could result in inflated metrics like revenue or popularity.

---

### **3. Parsing and Splitting Nested Data**
- Columns such as `genres`, `production_countries`, and `spoken_languages` contained comma-separated values.
- Split these strings and exploded them for granular analysis.

**Example:**
| **Original**                 | **Cleaned**       |
|-------------------------------|-------------------|
| `Action,Adventure,Sci-Fi`     | Separate rows for `Action`, `Adventure`, and `Sci-Fi` |

---

### **4. Calculating Additional Metrics**
- Added a derived column:  
  `profit_musd = revenue_musd - budget_musd`

**Reasoning:** This metric helps measure a movie's financial success beyond just revenue.

---

### **5. Normalizing Currency Values**
- Standardized `revenue` and `budget` values to millions of USD:
  - `revenue_musd`
  - `budget_musd`

**Reasoning:** Simplifies comparisons across movies with vastly different financial scales.

---

### **6. Formatting Dates**
- Converted the `release_date` column to a standard datetime format.
- Created new columns for:
  - `release_year`
  - `release_month`

**Reasoning:** Facilitates temporal analysis like movie releases by year or month.

---

### **7. Removing Ambiguous or Non-Informative Rows**
- Excluded entries with `Unknown` values in `genres` or `production_countries`.
- Dropped movies with `revenue_musd` or `budget_musd` of 0 if no imputation was feasible.

**Reasoning:** Ensures the data reflects meaningful and accurate information.

---

This cleaning process guarantees a high-quality dataset suitable for generating actionable insights and accurate visualizations.


---

## 📊 **Interactive Dashboard**
### **1. Static Insights:**
   - Top 10 genres by revenue, budget, and popularity.
   - Top production countries and languages by revenue.
   - Most profitable movies of all time.

### **2. Dynamic Insights:**
   - Filter trends by genre, release year, and language.
   - Explore financial and popularity metrics interactively.

---
## 📚 Future Enhancements
   - Integrate machine learning models to predict movie success based on budget and genre.
   - Provide a global map visualization for production country insights.

