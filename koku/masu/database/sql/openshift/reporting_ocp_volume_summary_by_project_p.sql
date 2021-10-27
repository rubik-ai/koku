DELETE FROM {{schema | sqlsafe}}.reporting_ocp_volume_summary_by_project_p
WHERE usage_start >= {{start_date}}::date
    AND usage_start <= {{end_date}}::date
    AND source_uuid = {{source_uuid}}
;

INSERT INTO {{schema | sqlsafe}}.reporting_ocp_volume_summary_by_project_p (
    id,
    usage_start,
    usage_end,
    cluster_id,
    cluster_alias,
    namespace,
    data_source,
    resource_ids,
    resource_count,
    supplementary_usage_cost,
    infrastructure_usage_cost,
    infrastructure_raw_cost,
    infrastructure_markup_cost,
    pod_usage_cpu_core_hours,
    pod_request_cpu_core_hours,
    pod_limit_cpu_core_hours,
    cluster_capacity_cpu_core_hours,
    pod_usage_memory_gigabyte_hours,
    pod_request_memory_gigabyte_hours,
    pod_limit_memory_gigabyte_hours,
    cluster_capacity_memory_gigabyte_hours,
    supplementary_monthly_cost_json,
    infrastructure_monthly_cost_json,
    source_uuid
)
    SELECT uuid_generate_v4() as id,
        usage_start as usage_start,
        usage_start as usage_end,
        cluster_id,
        cluster_alias,
        namespace,
        max(data_source) as data_source,
        array_agg(DISTINCT resource_id) as resource_ids,
        count(DISTINCT resource_id) as resource_count,
        json_build_object(
            'cpu', sum((supplementary_usage_cost->>'cpu')::decimal),
            'memory', sum((supplementary_usage_cost->>'memory')::decimal),
            'storage', sum((supplementary_usage_cost->>'storage')::decimal)
        ) as supplementary_usage_cost,
        json_build_object(
            'cpu', sum((infrastructure_usage_cost->>'cpu')::decimal),
            'memory', sum((infrastructure_usage_cost->>'memory')::decimal),
            'storage', sum((infrastructure_usage_cost->>'storage')::decimal)
        ) as infrastructure_usage_cost,
        sum(infrastructure_raw_cost) as infrastructure_raw_cost,
        sum(infrastructure_markup_cost) as infrastructure_markup_cost,
        sum(persistentvolumeclaim_usage_gigabyte_months) as persistentvolumeclaim_usage_gigabyte_months,
        sum(volume_request_storage_gigabyte_months) as volume_request_storage_gigabyte_months,
        sum(persistentvolumeclaim_capacity_gigabyte_months) as persistentvolumeclaim_capacity_gigabyte_months,
        json_build_object(
            'cpu', sum(((coalesce(supplementary_project_monthly_cost, '{"cpu": 0}'::jsonb))->>'cpu')::decimal),
            'memory', sum(((coalesce(supplementary_project_monthly_cost, '{"memory": 0}'::jsonb))->>'memory')::decimal),
            'pvc', sum(((coalesce(supplementary_project_monthly_cost, '{"pvc": 0}'::jsonb))->>'pvc')::decimal)
        ) as supplementary_monthly_cost_json,
        json_build_object(
            'cpu', sum(((coalesce(infrastructure_project_monthly_cost, '{"cpu": 0}'::jsonb))->>'cpu')::decimal),
            'memory', sum(((coalesce(infrastructure_project_monthly_cost, '{"memory": 0}'::jsonb))->>'memory')::decimal),
            'pvc', sum(((coalesce(infrastructure_project_monthly_cost, '{"pvc": 0}'::jsonb))->>'pvc')::decimal)
        ) as infrastructure_monthly_cost_json,
        {{source_uuid}}::uuid as source_uuid
    FROM {{schema | sqlsafe}}.reporting_ocpusagelineitem_daily_summary
    WHERE usage_start >= {{start_date}}::date
        AND usage_start <= {{end_date}}::date
        AND source_uuid = {{source_uuid}}
        AND data_source = 'Storage'
    GROUP BY usage_start, cluster_id, cluster_alias, namespace
;
