import os
import pandas as pd
from django.core.management.base import BaseCommand
from teamproductivity.models import Teams, Sprint, Issue


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            # base dir is two levels up from this file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            dev_path = os.path.join(base_dir, 'Teams_data.csv')
            sprint_path = os.path.join(base_dir, 'sprint_data.csv')
            issue_path = os.path.join(base_dir, 'issues_data.csv')

            # Developer Data
            df_dev = pd.read_csv(dev_path)
            for _, row in df_dev.iterrows():
                Teams.objects.create(id=row['id'], name=row['name'])

            # Sprint Data
            df_sprint = pd.read_csv(sprint_path)
            for _, row in df_sprint.iterrows():
                Sprint.objects.create(
                    id=row['id'],
                    name=row['name'],
                    start_date=row['start_date'],
                    end_date=row['end_date']
                )

            # Issue Data
            df_issues = pd.read_csv(issue_path)
            for _, row in df_issues.iterrows():
                Issue.objects.create(
                    id=row['id'],
                    title=row['title'],
                    created_at=row['created_at'],
                    resolved_at=row['resolved_at'],
                    team=Teams.objects.get(id=row['Team_id']),
                    sprint=Sprint.objects.get(id=row['sprint_id'])
                )

            self.stdout.write(self.style.SUCCESS("Dummy data loaded successfully!"))

        except FileNotFoundError as e:
            self.stderr.write(self.style.ERROR(f" File not found: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f" Error loading data: {e}"))
