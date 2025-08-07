import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import generate_pdf_report

def robust_read_csv(file):
    from io import StringIO

    # Try multiple delimiters and encodings
    delimiters = [',', '\t', ';', '|']
    encodings = ['utf-8', 'latin1']

    file_bytes = file.read()  # Read entire content once

    for encoding in encodings:
        for delim in delimiters:
            try:
                decoded = file_bytes.decode(encoding)
                df = pd.read_csv(StringIO(decoded), delimiter=delim)
                if df.shape[1] > 1:  # Must have more than one column
                    return df
            except Exception:
                continue
    return None

st.set_page_config(page_title="CSV Insight Analyzer", layout="wide")

st.title("📊 CSV Insight Analyzer")
st.write("Upload your CSV file and get instant insights!")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = robust_read_csv(uploaded_file)
    
    if df is None:
        st.error("❌ Could not read the file. Please make sure it's a valid CSV or TSV file.")
        st.stop()
    
    st.subheader("📌 File Preview")
    st.dataframe(df.head())  # Show first 5 rows

    st.subheader("🧠 Basic Data Insights")

    # Shape
    rows, cols = df.shape
    st.markdown(f"**🔹 Number of Rows:** {rows}")
    st.markdown(f"**🔹 Number of Columns:** {cols}")

    # Column names & data types
    st.markdown("**📋 Column Names & Data Types:**")
    dtypes_df = pd.DataFrame(df.dtypes, columns=['Data Type']).reset_index()
    dtypes_df.columns = ['Column Name', 'Data Type']
    st.dataframe(dtypes_df)

    # Missing values
    st.markdown("**⚠️ Missing Values:**")
    missing_df = pd.DataFrame(df.isnull().sum(), columns=['Missing Values'])
    missing_df['% Missing'] = (missing_df['Missing Values'] / rows * 100).round(2)
    st.dataframe(missing_df)

    # Memory usage
    st.markdown(f"**💾 Approx. Memory Usage:** {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    st.subheader("📈 Statistical Summary")

    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns

    if len(numeric_cols) > 0:
        st.markdown("**🔢 Numeric Column Stats**")
        stats_df = df[numeric_cols].agg(['mean', 'median', 'std', 'min', 'max']).transpose()
        stats_df.columns = ['Mean', 'Median', 'Std Dev', 'Min', 'Max']
        st.dataframe(stats_df)

    if len(categorical_cols) > 0:
        st.markdown("**🔤 Categorical Column Unique Values**")
        for col in categorical_cols:
            st.markdown(f"**{col}**: {df[col].nunique()} unique values")
            st.write(df[col].unique().tolist())    

    st.subheader("📊 Visualizations")

    # Histogram for numeric columns
    if len(numeric_cols) > 0:
        st.markdown("**🔹 Histograms (Numeric Columns)**")
        selected_num_col = st.selectbox("Select a numeric column", numeric_cols)
    
        fig, ax = plt.subplots()
        sns.histplot(df[selected_num_col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {selected_num_col}")
        st.pyplot(fig)

    # Bar chart for categorical columns
    if len(categorical_cols) > 0:
        st.markdown("**🔹 Bar Chart (Categorical Columns)**")
        selected_cat_col = st.selectbox("Select a categorical column", categorical_cols)
    
        fig, ax = plt.subplots()
        df[selected_cat_col].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f"Value Counts of {selected_cat_col}")
        ax.set_xlabel(selected_cat_col)
        ax.set_ylabel("Count")
        st.pyplot(fig)

    st.subheader("📝 Download Summary Report")

    # Build report content
    report_lines = []

    report_lines.append("=== CSV Insight Summary ===\n")
    report_lines.append(f"Filename: {uploaded_file.name}")
    report_lines.append(f"Rows: {rows}, Columns: {cols}\n")

    report_lines.append("== Column Data Types ==\n")
    for col in df.columns:
        report_lines.append(f"{col}: {df[col].dtype}")

    report_lines.append("\n== Missing Values ==\n")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        percent = round((null_count / rows) * 100, 2)
        report_lines.append(f"{col}: {null_count} missing ({percent}%)")

    if len(numeric_cols) > 0:
        report_lines.append("\n== Numeric Stats ==\n")
        stats = df[numeric_cols].agg(['mean', 'median']).transpose()
        for col in stats.index:
            mean = stats.loc[col, 'mean']
            median = stats.loc[col, 'median']
            report_lines.append(f"{col}: Mean = {mean:.2f}, Median = {median:.2f}")

    # Join lines and create downloadable file
    report_text = "\n".join(report_lines)
    
    # PDF download
    pdf_bytes = generate_pdf_report(df, uploaded_file)

    st.download_button(
        label="📄 Download Report (.pdf)",
        data=pdf_bytes,
        file_name="csv_insight_report.pdf",
        mime="application/pdf"
    )



