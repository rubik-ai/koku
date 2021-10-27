# Generated by Django 3.1.13 on 2021-10-25 17:37
from django.db import migrations
from django.db import models

sql_tmpl = """
alter table {} alter column id set default uuid_generate_v4();
"""
r_sql = "select 1;"


class Migration(migrations.Migration):

    dependencies = [("reporting", "0199_aws_perspective_colname_idx")]

    operations = [
        migrations.AddField(
            model_name="ocpallcomputesummarypt", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(
            model_name="ocpallcostsummarybyaccountpt", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(
            model_name="ocpallcostsummarybyregionpt", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(
            model_name="ocpallcostsummarybyservicept", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(model_name="ocpallcostsummarypt", name="source_type", field=models.TextField(default="")),
        migrations.AddField(
            model_name="ocpalldatabasesummarypt", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(
            model_name="ocpallnetworksummarypt", name="source_type", field=models.TextField(default="")
        ),
        migrations.AddField(
            model_name="ocpallstoragesummarypt", name="source_type", field=models.TextField(default="")
        ),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_compute_summary_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_cost_summary_by_account_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_cost_summary_by_region_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_cost_summary_by_service_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_cost_summary_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_database_summary_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_network_summary_pt"), reverse_sql=r_sql),
        migrations.RunSQL(sql=sql_tmpl.format("reporting_ocpall_storage_summary_pt"), reverse_sql=r_sql),
    ]
