-- refresh {{schema | sqlsafe}}.reporting_ocpallcostlineitem_project_daily_summary aws platform records
-- Step 1: Remove records from table between {{start_date}} and {{end_date}}
--         for source_type {{source_type}} and provider {{source_uuid}}
DELETE
  FROM {{schema | sqlsafe}}.reporting_ocpallcostlineitem_project_daily_summary
 WHERE usage_start >= {{start_date}}
   AND usage_start <= {{end_date}}
   AND source_type = {{source_type}}
   AND source_uuid = {{source_uuid}};

-- refresh {{schema | sqlsafe}}.reporting_ocpallcostlineitem_project_daily_summary aws platform records
-- Step 2: Add aggregated records between {{start_date}} and {{end_date}}
--         for source_type {{source_type}} and provider {{source_uuid}}
INSERT
  INTO {{schema | sqlsafe}}.reporting_ocpallcostlineitem_project_daily_summary
       (
           source_type,
           cluster_id,
           cluster_alias,
           data_source,
           namespace,
           node,
           pod_labels,
           resource_id,
           usage_start,
           usage_end,
           usage_account_id,
           account_alias_id,
           product_code,
           product_family,
           instance_type,
           region,
           availability_zone,
           usage_amount,
           unit,
           unblended_cost,
           project_markup_cost,
           pod_cost,
           currency_code,
           source_uuid
       )
SELECT {{source_type}} as source_type,
       cluster_id,
       max(cluster_alias) as cluster_alias,
       data_source,
       namespace::text as namespace,
       node::text as node,
       pod_labels,
       resource_id,
       usage_start,
       usage_end,
       usage_account_id,
       max(account_alias_id) as account_alias_id,
       product_code,
       product_family,
       instance_type,
       region,
       availability_zone,
       sum(usage_amount) as usage_amount,
       max(unit) as unit,
       sum(unblended_cost) as unblended_cost,
       sum(project_markup_cost) as project_markup_cost,
       sum(pod_cost) as pod_cost,
       max(currency_code) as currency_code,
       {{source_uuid}}::uuid as source_uuid
  FROM {{schema | sqlsafe}}.{{project_daily_summary_table}}
 WHERE usage_start >= {{start_date}}
   AND usage_start <= {{end_date}}
   AND source_uuid = {{source_uuid}}::uuid
 GROUP
    BY usage_start,
       usage_end,
       cluster_id,
       data_source,
       namespace,
       node,
       usage_account_id,
       resource_id,
       product_code,
       product_family,
       instance_type,
       region,
       availability_zone,
       pod_labels;
