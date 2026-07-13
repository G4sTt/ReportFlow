import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=1
        ))

        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#4a4a4a'),
            spaceAfter=20
        ))

        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        ))

    def generate(self, input_file: str, output_file: str) -> dict:
        logger.info(f"Генерация отчёта: {input_file} → {output_file}")

        try:
            df = self._read_data(input_file)
            stats = self._calculate_stats(df)

            doc = SimpleDocTemplate(
                output_file,
                pagesize=A4,
                rightMargin=2 * cm,
                leftMargin=2 * cm,
                topMargin=2 * cm,
                bottomMargin=2 * cm
            )

            story = []

            story.append(Paragraph("Analytics Report", self.styles['ReportTitle']))
            story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph("Summary", self.styles['ReportSubtitle']))
            story.append(Paragraph(
                f"<b>Total records:</b> {stats['total_rows']}",
                self.styles['ReportBody']
            ))
            story.append(Paragraph(
                f"<b>Columns count:</b> {stats['columns_count']}",
                self.styles['ReportBody']
            ))
            story.append(Paragraph(
                f"<b>Numeric columns:</b> {stats['numeric_columns_count']}",
                self.styles['ReportBody']
            ))
            story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph("Columns Information", self.styles['ReportSubtitle']))
            story.append(self._create_columns_table(df))
            story.append(Spacer(1, 0.3 * inch))

            if stats['numeric_columns_count'] > 0:
                story.append(Paragraph("Numeric Statistics", self.styles['ReportSubtitle']))
                story.append(self._create_statistics_table(df))
                story.append(Spacer(1, 0.3 * inch))

                chart_path = self._create_chart(df, output_file.replace('.pdf', '_chart.png'))
                if chart_path:
                    story.append(Paragraph("Data Visualization", self.styles['ReportSubtitle']))
                    story.append(Image(chart_path, width=6 * inch, height=3 * inch))
                    story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph("Data Preview (first 10 rows)", self.styles['ReportSubtitle']))
            story.append(self._create_data_preview(df))

            doc.build(story)

            logger.info(f"Отчёт успешно сгенерирован: {output_file}")
            return stats

        except Exception as e:
            logger.error(f"Ошибка генерации отчёта: {e}", exc_info=True)
            raise

    def _read_data(self, file_path: str) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")

    def _calculate_stats(self, df: pd.DataFrame) -> dict:
        return {
            'total_rows': len(df),
            'columns_count': len(df.columns),
            'numeric_columns_count': len(df.select_dtypes(include=['number']).columns),
            'columns': list(df.columns)
        }

    def _create_columns_table(self, df: pd.DataFrame) -> Table:
        data = [['Column Name', 'Type', 'Non-Null Count', 'Unique Values']]

        for col in df.columns:
            data.append([
                str(col),
                str(df[col].dtype),
                str(df[col].notna().sum()),
                str(df[col].nunique())
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))

        return table

    def _create_statistics_table(self, df: pd.DataFrame) -> Table:
        numeric_df = df.select_dtypes(include=['number'])
        desc = numeric_df.describe().round(2)

        data = [['Statistic'] + list(desc.columns)]
        for idx in desc.index:
            row = [str(idx)] + [str(val) for val in desc.loc[idx]]
            data.append(row)

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a7fba')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))

        return table

    def _create_chart(self, df: pd.DataFrame, output_path: str) -> str:
        try:
            numeric_df = df.select_dtypes(include=['number'])
            if numeric_df.empty:
                return None

            col = numeric_df.columns[0]

            plt.figure(figsize=(10, 5))
            plt.style.use('seaborn-v0_8-darkgrid')

            plt.hist(numeric_df[col].dropna(), bins=30, color='#1a5490', alpha=0.7, edgecolor='black')
            plt.title(f'Distribution of {col}', fontsize=14, fontweight='bold')
            plt.xlabel(col, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return output_path

        except Exception as e:
            logger.warning(f"Не удалось создать график: {e}")
            return None

    def _create_data_preview(self, df: pd.DataFrame) -> Table:
        preview_df = df.head(10).fillna('')

        data = [list(df.columns)]
        for _, row in preview_df.iterrows():
            data.append([str(val)[:30] for val in row])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4a4a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))

        return table