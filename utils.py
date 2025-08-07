from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pdf_report(df, uploaded_file):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("CSV Insight Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Filename: {uploaded_file.name}", styles["Normal"]))
    story.append(Paragraph(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Column types
    story.append(Paragraph("== Column Data Types ==", styles["Heading3"]))
    for col in df.columns:
        story.append(Paragraph(f"{col}: {df[col].dtype}", styles["Normal"]))

    story.append(Spacer(1, 12))

    # Missing values
    story.append(Paragraph("== Missing Values ==", styles["Heading3"]))
    for col in df.columns:
        null_count = df[col].isnull().sum()
        percent = round((null_count / df.shape[0]) * 100, 2)
        story.append(Paragraph(f"{col}: {null_count} missing ({percent}%)", styles["Normal"]))

    story.append(Spacer(1, 12))

    # Numeric stats
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        story.append(Paragraph("== Numeric Column Stats ==", styles["Heading3"]))
        stats = df[numeric_cols].agg(['mean', 'median', 'std', 'min', 'max']).transpose()
        for col in stats.index:
            row = stats.loc[col]
            story.append(Paragraph(
                f"{col} → Mean: {row['mean']:.2f}, Median: {row['median']:.2f}, Std: {row['std']:.2f}, "
                f"Min: {row['min']:.2f}, Max: {row['max']:.2f}", styles["Normal"]
            ))

    story.append(Spacer(1, 12))

    # Categorical stats
    categorical_cols = df.select_dtypes(include='object').columns
    if len(categorical_cols) > 0:
        story.append(Paragraph("== Categorical Column Unique Values ==", styles["Heading3"]))
        for col in categorical_cols:
            uniques = df[col].dropna().unique().tolist()
            story.append(Paragraph(f"{col} → {len(uniques)} unique values", styles["Normal"]))
            story.append(Paragraph(str(uniques), styles["Normal"]))

    story.append(Spacer(1, 20))

    # 📊 Charts
    story.append(Paragraph("== Charts & Visualizations ==", styles["Heading3"]))

    if len(numeric_cols) > 0:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"Histogram: {col}")
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight')
            plt.close(fig)
            img_buffer.seek(0)
            story.append(Image(img_buffer, width=400, height=250))
            story.append(Spacer(1, 12))

    if len(categorical_cols) > 0:
        for col in categorical_cols:
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"Bar Chart: {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight')
            plt.close(fig)
            img_buffer.seek(0)
            story.append(Image(img_buffer, width=400, height=250))
            story.append(Spacer(1, 12))

    # Final build
    doc.build(story)
    buffer.seek(0)
    return buffer
