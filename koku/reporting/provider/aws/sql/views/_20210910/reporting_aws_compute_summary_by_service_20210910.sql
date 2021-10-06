DROP INDEX IF EXISTS aws_compute_summary_service;
DROP MATERIALIZED VIEW IF EXISTS reporting_aws_compute_summary_by_service;

CREATE MATERIALIZED VIEW reporting_aws_compute_summary_by_service AS (
    SELECT ROW_NUMBER() OVER(ORDER BY c.usage_start, c.usage_account_id, c.product_code, c.product_family, c.instance_type) AS id,
        c.usage_start,
        c.usage_start as usage_end,
        c.usage_account_id,
        c.account_alias_id,
        c.organizational_unit_id,
        c.product_code,
        c.product_family,
        c.instance_type,
        r.resource_ids,
        CARDINALITY(r.resource_ids) AS resource_count,
        c.usage_amount,
        c.unit,
        c.unblended_cost,
        c.savingsplan_effective_cost,
        c.markup_cost,
        c.currency_code,
        c.source_uuid
    FROM (
        -- this group by gets the counts
        SELECT usage_start,
            usage_account_id,
            MAX(account_alias_id) as account_alias_id,
            MAX(organizational_unit_id) as organizational_unit_id,
            product_code,
            product_family,
            instance_type,
            SUM(usage_amount) AS usage_amount,
            MAX(unit) AS unit,
            SUM(unblended_cost) AS unblended_cost,
            SUM(savingsplan_effective_cost) AS savingsplan_effective_cost,
            SUM(markup_cost) AS markup_cost,
            MAX(currency_code) AS currency_code,
            MAX(source_uuid::text)::uuid as source_uuid
        FROM reporting_awscostentrylineitem_daily_summary
        WHERE usage_start >= DATE_TRUNC('month', NOW() - '2 month'::interval)::date
            AND instance_type IS NOT NULL
        GROUP BY usage_start, usage_account_id, product_code, product_family, instance_type
    ) AS c
    JOIN (
        -- this group by gets the distinct resources running by day
        SELECT usage_start,
            usage_account_id,
            max(account_alias_id) as account_alias_id,
            product_code,
            product_family,
            instance_type,
            ARRAY_AGG(DISTINCT resource_id ORDER BY resource_id) as resource_ids
        FROM (
            SELECT usage_start,
                usage_account_id,
                account_alias_id,
                product_code,
                product_family,
                instance_type,
                UNNEST(resource_ids) AS resource_id
            FROM reporting_awscostentrylineitem_daily_summary
            WHERE usage_start >= DATE_TRUNC('month', NOW() - '2 month'::interval)::date
                AND instance_type IS NOT NULL
        ) AS x
        GROUP BY usage_start, usage_account_id, product_code, product_family, instance_type
    ) AS r
        ON c.usage_start = r.usage_start
            AND c.product_code = r.product_code
            AND c.product_family = r.product_family
            AND c.instance_type = r.instance_type
            AND c.usage_account_id = r.usage_account_id
)
WITH DATA
;

CREATE UNIQUE INDEX aws_compute_summary_service
    ON reporting_aws_compute_summary_by_service (usage_start, usage_account_id, product_code, product_family, instance_type)
;
