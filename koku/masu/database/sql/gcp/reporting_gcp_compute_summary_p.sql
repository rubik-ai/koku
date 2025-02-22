DELETE FROM {{schema | sqlsafe}}.reporting_gcp_compute_summary_p
WHERE usage_start >= {{start_date}}::date
    AND usage_start <= {{end_date}}::date
    AND source_uuid = {{source_uuid}}
    AND invoice_month = {{invoice_month}}
;

INSERT INTO {{schema | sqlsafe}}.reporting_gcp_compute_summary_p (
    id,
    usage_start,
    usage_end,
    instance_type,
    usage_amount,
    unit,
    unblended_cost,
    markup_cost,
    currency,
    source_uuid,
    invoice_month,
    credit_amount
)
    SELECT uuid_generate_v4() as id,
        usage_start,
        usage_start as usage_end,
        instance_type,
        sum(usage_amount) as usage_amount,
        MAX(unit) AS unit,
        SUM(unblended_cost) AS unblended_cost,
        SUM(markup_cost) AS markup_cost,
        MAX(currency) AS currency,
        source_uuid,
        invoice_month,
        SUM(credit_amount) AS credit_amount
    FROM {{schema | sqlsafe}}.reporting_gcpcostentrylineitem_daily_summary
    WHERE usage_start >= {{start_date}}::date
        AND usage_start <= {{end_date}}::date
        AND source_uuid = {{source_uuid}}
        AND invoice_month = {{invoice_month}}
    GROUP BY usage_start, instance_type, source_uuid, invoice_month
;
