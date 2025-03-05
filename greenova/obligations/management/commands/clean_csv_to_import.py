import pandas as pd
import numpy as np
import re
import logging
import os
from typing import Any, Dict, List
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Django management command to clean CSV data for import.

    Formats dirty CSV data to match the required schema for Django models.
    """
    help = 'Clean CSV data to match Django models schema'

    def add_arguments(self, parser):
        """
        Add command line arguments.
        """
        parser.add_argument('input_file', type=str, help='Path to the dirty CSV file')
        parser.add_argument(
            '--output',
            dest='output_file',
            type=str,
            help='Path where the cleaned CSV will be saved',
            default='clean_output_with_nullsV2.csv'
        )

    def handle(self, *args, **options):
        """
        Execute the command to clean a CSV file.

        Args:
            input_file: Path to the dirty CSV file
            output_file: Path where the cleaned CSV will be saved
        """
        input_file = options['input_file']
        output_file = options['output_file']

        if not os.path.exists(input_file):
            self.stderr.write(self.style.ERROR(f"Input file not found: {input_file}"))
            return

        try:
            self.clean_csv(input_file, output_file)
            self.stdout.write(self.style.SUCCESS(f"Successfully cleaned CSV data and saved to {output_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error cleaning CSV: {str(e)}"))

    def clean_csv(self, input_file: str, output_file: str) -> None:
        """
        Clean and format CSV data to match Django models schema.

        Args:
            input_file: Path to the dirty CSV file
            output_file: Path where the cleaned CSV will be saved
        """
        logger.info(f"Reading CSV file from {input_file}")

        # Read the dirty CSV file, handling potential encoding issues
        try:
            df = pd.read_csv(input_file, encoding='utf-8')
        except UnicodeDecodeError:
            # Try with another common encoding if utf-8 fails
            df = pd.read_csv(input_file, encoding='ISO-8859-1')

        # Skip header row if it contains instructions instead of data
        if df.shape[0] > 0 and ('project name' in str(df.iloc[0].values).lower() or
                              'this is now the project name' in str(df.iloc[0].values).lower()):
            self.stdout.write(f"Skipping instruction row")
            df = df.iloc[1:].reset_index(drop=True)

        # Define the column mapping based on clean_output_with_nulls.csv
        column_mapping = {
            'Project_Name': 'project__name',
            'Primary_Environmental_Mechanism': 'primary__environmental__mechanism',
            'Procedure': 'procedure',
            'Environmental_Aspect': 'environmental__aspect',
            'Obligation Number': 'obligation__number',
            'Obligation': 'obligation',
            'Accountability': 'accountability',
            'Responsibility': 'responsibility',
            'ProjectPhase': 'project_phase',
            'Action_DueDate': 'action__due_date',
            'Close_Out_Date': 'close__out__date',
            'Status': 'status',
            'Supporting Information': 'supporting__information',
            'General Comments': 'general__comments',
            'Compliance Comments': 'compliance__comments',
            'NonConformance Comments': 'non_conformance__comments',
            'Evidence': 'evidence',
            'PersonEmail': 'person_email',
            'Recurring Obligation': 'recurring__obligation',
            'Recurring Frequency': 'recurring__frequency',
            'Recurring Status': 'recurring__status',
            'Recurring Forcasted Date': 'recurring__forcasted__date',
            'Inspection': 'inspection',
            'Inspection Frequency': 'inspection__frequency',
            'Site or Desktop': 'site_or__desktop',
            'New Control, action required ': 'new__control__action_required',
            'Obligation type': 'obligation_type',
            'Gap Analysis': 'gap__analysis',
            'Notes for Gap Analysis': 'notes_for__gap__analysis',
            'Covered in which inspection checklist?': 'covered_in_which_inspection_checklist'
        }

        # Print available columns in the CSV for debugging
        self.stdout.write(f"Available columns in CSV: {df.columns.tolist()}")

        # Check if all expected columns exist
        for original_col in column_mapping.keys():
            if original_col not in df.columns:
                self.stdout.write(self.style.WARNING(f"Column not found in CSV: '{original_col}'"))

        # Rename the columns
        df.rename(columns=column_mapping, inplace=True)

        # Convert columns with potential line breaks to clean strings
        text_columns = [
            'supporting__information', 'general__comments', 'compliance__comments',
            'non_conformance__comments', 'obligation', 'procedure', 'evidence',
            'gap__analysis', 'notes_for__gap__analysis'
        ]

        for col in text_columns:
            if col in df.columns:
                # Replace line breaks with dash and clean special characters
                df[col] = df[col].astype(str).apply(
                    lambda x: re.sub(r'[\r\n•\u2022\u2013\u2019]', '-', x) if pd.notna(x) and x != 'nan' else ''
                )

        # Clean boolean fields - ensure these are properly processed
        bool_columns = ['recurring__obligation', 'inspection', 'new__control__action_required']

        for col in bool_columns:
            if col in df.columns:
                self.stdout.write(f"Processing boolean column: {col}")
                # Convert to string first to handle various input types
                df[col] = df[col].astype(str).str.strip().str.lower()
                # Print unique values for debugging
                unique_vals = df[col].unique()
                self.stdout.write(f"Unique values in {col}: {unique_vals}")
                # Convert various boolean indicators to Python boolean values
                df[col] = df[col].apply(
                    lambda x: True if x in ('yes', 'y', 'true', '1', 'yes ', 'y ', 'true ') else
                              False if x in ('no', 'n', 'false', '0', 'no ', 'n ', 'false ', 'nan', '') else
                              None
                )
                # Count values after conversion
                true_count = (df[col] == True).sum()
                false_count = (df[col] == False).sum()
                null_count = df[col].isna().sum()
                self.stdout.write(f"After conversion: True={true_count}, False={false_count}, Null={null_count}")

        # Convert and clean date columns - fix all date formats
        date_columns = ['action__due_date', 'close__out__date', 'recurring__forcasted__date']

        for col in date_columns:
            if col in df.columns:
                self.stdout.write(f"Processing date column: {col}")
                # Show original date formats
                non_null_dates = df[col][df[col].notna()]
                if len(non_null_dates) > 0:
                    self.stdout.write(f"Sample dates before processing: {non_null_dates.iloc[:5].tolist()}")

                # Handle common date formats
                try:
                    # First try to handle explicit formats
                    df[col] = pd.to_datetime(df[col], errors='coerce',
                                           format=None, dayfirst=False)

                    # For any values that failed conversion, try different formats
                    mask = df[col].isna() & df[col].notna()
                    if mask.any():
                        for date_format in ['%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y-%m-%d']:
                            df.loc[mask, col] = pd.to_datetime(
                                df.loc[mask, col], errors='coerce', format=date_format
                            )

                    # Fix dates far in the future (likely typos)
                    df[col] = df[col].apply(
                        lambda x: pd.Timestamp(x.year - 100, x.month, x.day)
                        if pd.notna(x) and x.year > 2100
                        else x
                    )

                    # Show processed dates
                    non_null_processed = df[col][df[col].notna()]
                    if len(non_null_processed) > 0:
                        self.stdout.write(f"Sample dates after processing: {non_null_processed.iloc[:5].tolist()}")

                except Exception as e:
                    self.stderr.write(f"Error processing dates in column {col}: {str(e)}")

        # Normalize status values to match model choices
        if 'status' in df.columns:
            # Convert to lowercase and handle slight variations
            df['status'] = df['status'].astype(str).str.lower().str.strip()

            # Replace variations with standardized values
            status_mapping = {
                'in progress': 'in progress',
                'inprogress': 'in progress',
                'in-progress': 'in progress',
                'completed': 'completed',
                'complete': 'completed',
                'not started': 'not started',
                'notstarted': 'not started',
                'not-started': 'not started',
                'null': 'not started',
                'nan': 'not started',
                '': 'not started'
            }

            df['status'] = df['status'].apply(lambda x: status_mapping.get(x, 'not started'))

        # Ensure project_phase has valid values
        valid_phases = ['Pre-Construction', 'Construction', 'Operation', 'Decommissioning', 'Post-Closure', 'Other']
        if 'project_phase' in df.columns:
            # Map variations to standardized values
            df['project_phase'] = df['project_phase'].astype(str).apply(
                lambda x: 'Construction' if 'construction' in x.lower() or 'design and construction' in x.lower()
                else 'Pre-Construction' if any(term in x.lower() for term in ['pre', 'design'])
                else 'Operation' if 'operation' in x.lower()
                else 'Throughout the project' if 'throughout' in x.lower()
                else x if pd.notna(x) and x != 'nan' and x != 'NULL' and x != '' else None
            )

        # Ensure environmental_aspect has valid values
        valid_aspects = ['Air', 'Water', 'Waste', 'Energy', 'Biodiversity', 'Noise', 'Chemicals', 'Soil', 'Other', 'Administration', 'Cultural Heritage Management', 'Terrestrial Fauna Management']
        if 'environmental__aspect' in df.columns:
            # Convert to proper format
            df['environmental__aspect'] = df['environmental__aspect'].astype(str).apply(
                lambda x: x.title() if pd.notna(x) and x != 'nan' and x != 'NULL' and x != '' else 'Other'
            )

        # Ensure site_or_desktop has valid values (Site or Desktop)
        if 'site_or__desktop' in df.columns:
            df['site_or__desktop'] = df['site_or__desktop'].astype(str).apply(
                lambda x: 'Site' if 'site' in x.lower()
                else 'Desktop' if 'desktop' in x.lower()
                else None if pd.isna(x) or x == 'nan' or x == 'NULL' or x == ''
                else x
            )

        # Clean up email addresses
        if 'person_email' in df.columns:
            df['person_email'] = df['person_email'].astype(str).apply(
                lambda x: x.strip() if pd.notna(x) and x != 'nan' and '@' in x else None
            )

        # Ensure obligation numbers are in the correct format (PCEMP-XXX)
        if 'obligation__number' in df.columns:
            df['obligation__number'] = df['obligation__number'].apply(
                lambda x: f"PCEMP-{x.split('-')[1]}" if isinstance(x, str) and '-' in x else
                          f"PCEMP-{x}" if isinstance(x, str) and x.isdigit() else x
            )

        # Fill missing values with appropriate defaults
        df['status'].fillna('not started', inplace=True)

        # Replace remaining NaN values with None/NULL
        df = df.replace({np.nan: None})

        # Explicitly check for missing required columns and add them
        required_columns = set([v for v in column_mapping.values()])
        missing_columns = required_columns - set(df.columns)

        for col in missing_columns:
            df[col] = None
            logger.warning(f"Added missing column: {col}")

        # Print the first few rows for verification
        self.stdout.write("First 2 rows of processed data:")
        for index, row in df.head(2).iterrows():
            self.stdout.write(f"Row {index}:")
            for col in required_columns:
                if col in row:
                    self.stdout.write(f"  {col}: {row[col]}")

        # Export the cleaned data to a new CSV file with proper date formatting
        df.to_csv(output_file, index=False, date_format='%Y-%m-%d')
        logger.info(f"Cleaned data exported to {output_file}")
        self.stdout.write(f"CSV exported with {len(df)} rows and {len(df.columns)} columns")


# This will only run if the script is executed directly, not when imported as a Django command
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    input_file = 'dirty.csv'
    output_file = 'clean_output_with_nulls.csv'
    command = Command()
    command.clean_csv(input_file, output_file)
