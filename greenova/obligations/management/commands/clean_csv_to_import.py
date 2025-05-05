import logging
import os
import re

from django.core.management.base import BaseCommand

# Set up logger at module level
logger = logging.getLogger(__name__)

# Check for pandas and numpy before importing
try:
    import numpy as np
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.error(
        "pandas and/or numpy modules not found. Please install them with: "
        "pip install pandas numpy"
    )


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
            default='clean_output_with_nulls.csv'
        )

    def handle(self, *args, **options):
        """
        Execute the command to clean a CSV file.

        Args:
            input_file: Path to the dirty CSV file
            output_file: Path where the cleaned CSV will be saved
        """
        if not PANDAS_AVAILABLE:
            self.stderr.write(
                self.style.ERROR(
                    "This command requires pandas and numpy. "
                    "Please install them with: pip install pandas numpy"
                )
            )
            return

        file_path = options['input_file']
        out_path = options['output_file']

        if not os.path.exists(file_path):
            self.stderr.write(
                self.style.ERROR(f"Input file not found: {file_path}")
            )
            return

        try:
            self.clean_csv(file_path, out_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully cleaned CSV data and saved to {out_path}"
                )
            )
        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            self.stderr.write(
                self.style.ERROR(f"Error parsing CSV file: {str(e)}")
            )
        except OSError as e:
            self.stderr.write(
                self.style.ERROR(f"File I/O error: {str(e)}")
            )
        except ValueError as e:
            self.stderr.write(
                self.style.ERROR(f"Value error: {str(e)}")
            )
        except Exception as e:  # pylint: disable=broad-except
            # This is intentionally broad as a last resort for unexpected errors
            self.stderr.write(
                self.style.ERROR(f"Unexpected error cleaning CSV: {str(e)}")
            )

    def clean_csv(self, filepath: str, outpath: str) -> None:
        """
        Clean and format CSV data to match Django models schema.

        Args:
            filepath: Path to the dirty CSV file
            outpath: Path where the cleaned CSV will be saved
        """
        logger.info("Reading CSV file from %s", filepath)

        # Read the dirty CSV file, handling potential encoding issues
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            # Try with another common encoding if utf-8 fails
            df = pd.read_csv(filepath, encoding='ISO-8859-1')

        # Skip header row if it contains instructions instead of data
        if (df.shape[0] > 0 and
                ('project name' in str(df.iloc[0].values).lower() or
                 'this is now the project name' in str(df.iloc[0].values).lower())):
            self.stdout.write("Skipping instruction row")
            df = df.iloc[1:].reset_index(drop=True)

        df = self._map_columns(df)
        df = self._clean_text_fields(df)
        df = self._process_boolean_fields(df)
        df = self._clean_date_fields(df)
        df = self._normalize_status_values(df)
        df = self._clean_project_phases(df)
        df = self._clean_environmental_aspects(df)
        df = self._clean_site_desktop_values(df)
        df = self._clean_email_addresses(df)
        df = self._format_obligation_numbers(df)
        df = self._apply_defaults_and_nulls(df)

        # Export the cleaned data to a new CSV file with proper date formatting
        df.to_csv(outpath, index=False, date_format='%Y-%m-%d')
        logger.info("Cleaned data exported to %s", outpath)
        self.stdout.write(f"CSV exported {len(df)} rows and {len(df.columns)} columns")

    def _map_columns(self, df):
        """Map original column names to our expected format."""
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
            'Notes for Gap Analysis': 'notes_for__gap__analysis'
        }

        # Print available columns in the CSV for debugging
        self.stdout.write(f"Available columns in CSV: {df.columns.tolist()}")

        # Check if all expected columns exist
        for original_col in column_mapping:
            if original_col not in df.columns:
                self.stdout.write(
                    self.style.WARNING(f"Column not found in CSV: '{original_col}'")
                )

        # Rename the columns
        df.rename(columns=column_mapping, inplace=True)

        # Explicitly check for missing required columns and add them
        required_columns = set(column_mapping.values())
        missing_columns = required_columns - set(df.columns)

        for col in missing_columns:
            df[col] = None
            logger.warning("Added missing column: %s", col)

        return df

    def _clean_text_fields(self, df):
        """Clean text fields by removing line breaks and special characters."""
        text_columns = [
            'supporting__information', 'general__comments', 'compliance__comments',
            'non_conformance__comments', 'obligation', 'procedure', 'evidence',
            'gap__analysis', 'notes_for__gap__analysis'
        ]

        for col in text_columns:
            if col in df.columns:
                # Replace line breaks with dash and clean special characters
                df[col] = df[col].astype(str).apply(
                    lambda x: re.sub(r'[\r\n•\u2022\u2013\u2019]', '-', x)
                    if pd.notna(x) and x != 'nan' else ''
                )
        return df

    def _process_boolean_fields(self, df):
        """Process fields with boolean values."""
        bool_columns = [
            'recurring__obligation', 'inspection', 'new__control__action_required'
        ]

        # Define conv. values outside loop to avoid cell variable defined loop error
        true_values = ['yes', 'y', 'true', '1', 'yes ', 'y ', 'true ']
        false_values = ['no', 'n', 'false', '0', 'no ', 'n ', 'false ', '']

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
                    lambda x: True if x in true_values else
                    False if x in false_values else None
                )

                # Count values after conversion
                true_count = (df[col] is True).sum()
                false_count = (df[col] is False).sum()
                null_count = df[col].isna().sum()

                self.stdout.write(
                    f"After conversion: True={true_count}, False={false_count}, "
                    f"Null={null_count}"
                )
        return df

    def _clean_date_fields(self, df):
        """Convert date fields to standard format."""
        date_columns = [
            'action__due_date',
            'close__out__date',
            'recurring__forcasted__date'
        ]

        for col in date_columns:
            if col in df.columns:
                df[col] = (pd.to_datetime(df[col], errors='coerce')
                           .dt.strftime('%Y-%m-%d'))
        return df

    def _normalize_status_values(self, df):
        """Normalize status values to match model choices."""
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

            df['status'] = df['status'].apply(
                lambda x: status_mapping.get(x, 'not started')
            )
        return df

    def _clean_project_phases(self, df):
        """Clean and standardize project phase values."""
        if 'project_phase' in df.columns:
            # Define valid phases for validation
            valid_phases = {
                'Pre-Construction',
                'Construction',
                'Operation',
                'Throughout the project'
            }

            # Map variations to standardized values
            df['project_phase'] = df['project_phase'].astype(str).apply(
                lambda x: 'Construction'
                if 'construction' in x.lower() or 'design and construction' in x.lower()
                else 'Pre-Construction'
                if any(term in x.lower() for term in ['pre', 'design'])
                else 'Operation'
                if 'operation' in x.lower()
                else 'Throughout the project'
                if 'throughout' in x.lower()
                else x if (pd.notna(x) and
                           x != 'nan' and
                           x != 'NULL' and
                           x != '' and
                           x in valid_phases)
                else None
            )
        return df

    def _clean_environmental_aspects(self, df):
        """Clean and standardize environmental aspect values."""
        if 'environmental__aspect' in df.columns:
            # Define valid aspects for validation
            valid_aspects = {
                'Soil', 'Water', 'Air', 'Noise', 'Hazardous Materials',
                'Waste', 'Flora', 'Fauna', 'Heritage', 'Community', 'Other'
            }

            # Convert to proper format and validate against valid aspects
            df['environmental__aspect'] = df['environmental__aspect'].astype(str).apply(
                lambda x: x.title()
                if (pd.notna(x) and
                    x != 'nan' and
                    x != 'NULL' and
                    x != '' and
                    x.title() in valid_aspects)
                else 'Other'
            )
        return df

    def _clean_site_desktop_values(self, df):
        """Clean and standardize site or desktop values."""
        if 'site_or__desktop' in df.columns:
            df['site_or__desktop'] = df['site_or__desktop'].astype(str).apply(
                lambda x: 'Site' if 'site' in x.lower()
                else 'Desktop' if 'desktop' in x.lower()
                else None if pd.isna(x) or x == 'nan' or x == 'NULL' or x == ''
                else x
            )
        return df

    def _clean_email_addresses(self, df):
        """Clean email addresses."""
        if 'person_email' in df.columns:
            df['person_email'] = df['person_email'].astype(str).apply(
                lambda x: x.strip()
                if pd.notna(x) and x != 'nan' and '@' in x
                else None
            )
        return df

    def _format_obligation_numbers(self, df):
        """Format obligation numbers consistently."""
        if 'obligation__number' in df.columns:
            df['obligation__number'] = df['obligation__number'].apply(
                lambda x: f"PCEMP-{x.split('-')[1]}"
                if isinstance(x, str) and '-' in x
                else f"PCEMP-{x}"
                if isinstance(x, str) and x.isdigit()
                else x
            )
        return df

    def _apply_defaults_and_nulls(self, df):
        """Apply default values and handle nulls."""
        # Fill missing values with appropriate defaults
        if 'status' in df.columns:
            df['status'].fillna('not started', inplace=True)

        # Replace remaining NaN values with None/NULL
        df = df.replace({np.nan: None})
        return df


# This will only run if script is executed directly, not when as a Django command
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    cmd = Command()
    cmd.clean_csv('dirty.csv', 'clean_output_with_nulls.csv')
