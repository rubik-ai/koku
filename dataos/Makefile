
aws-source:
ifndef aws_name
	$(error param aws_name is not set)
endif
	(printenv CARETAKER_USAGE_SOURCE_URL > /dev/null 2>&1) || (echo 'CARETAKER_USAGE_SOURCE_URL is not set in .env' && exit 1)
	(printenv AWS_RESOURCE_NAME > /dev/null 2>&1) || (echo 'AWS_RESOURCE_NAME is not set in .env' && exit 1)
	(printenv AWS_BUCKET > /dev/null 2>&1) || (echo 'AWS_BUCKET is not set in .env' && exit 1)
	curl -d '{"name": "$(aws_name)", "source_type": "AWS", "authentication": {"credentials": {"role_arn":"${AWS_RESOURCE_NAME}"}}, "billing_source": {"data_source": {"bucket": "${AWS_BUCKET}}}' -H "Content-Type: application/json" -X POST ${CARETAKER_USAGE_SOURCE_URL}

gcp-source:
ifndef gcp_name
	$(error param gcp_name is not set)
endif
	(printenv GCP_DATASET > /dev/null 2>&1) || (echo 'GCP_DATASET is not set in .env' && exit 1)
	(printenv GCP_TABLE_ID > /dev/null 2>&1) || (echo 'GCP_TABLE_ID is not set in .env' && exit 1)
	(printenv GCP_PROJECT_ID > /dev/null 2>&1) || (echo 'GCP_PROJECT_ID is not set in .env' && exit 1)
	curl -d '{"name": "$(gcp_name)", "source_type": "GCP", "authentication": {"credentials": {"project_id":"${GCP_PROJECT_ID}"}}, "billing_source": {"data_source": {"table_id": "${GCP_TABLE_ID}", "dataset": "${GCP_DATASET}"}}}' -H "Content-Type: application/json" -X POST ${CARETAKER_USAGE_SOURCE_URL}

azure-source:
ifndef azure_name
	$(error param azure_name is not set)
endif
	(printenv AZURE_RESOURCE_GROUP > /dev/null 2>&1) || (echo 'AZURE_RESOURCE_GROUP is not set in .env' && exit 1)
	(printenv AZURE_STORAGE_ACCOUNT > /dev/null 2>&1) || (echo 'AZURE_STORAGE_ACCOUNT is not set in .env' && exit 1)
	(printenv AZURE_SUBSCRIPTION_ID > /dev/null 2>&1) || (echo 'AZURE_SUBSCRIPTION_ID is not set in .env' && exit 1)
	(printenv AZURE_TENANT_ID > /dev/null 2>&1) || (echo 'AZURE_TENANT_ID is not set in .env' && exit 1)
	(printenv AZURE_CLIENT_ID > /dev/null 2>&1) || (echo 'AZURE_CLIENT_ID is not set in .env' && exit 1)
	(printenv AZURE_CLIENT_SECRET > /dev/null 2>&1) || (echo 'AZURE_CLIENT_SECRET is not set in .env' && exit 1)
	(printenv AZURE_CLOUD > /dev/null 2>&1) || (echo 'AZURE_CLOUD is not set in .env' && exit 1)
	curl -d '{"name": "$(azure_name)", "source_type": "Azure", "authentication": {"credentials": {"subscription_id":"${AZURE_SUBSCRIPTION_ID}", "tenant_id": "${AZURE_TENANT_ID}", "client_id": "${AZURE_CLIENT_ID}", "client_secret": "${AZURE_CLIENT_SECRET}", "cloud": "${AZURE_CLOUD}"}}, "billing_source": {"data_source": {"resource_group": "${AZURE_RESOURCE_GROUP}", "storage_account": "${AZURE_STORAGE_ACCOUNT}"}}}' -H "Content-Type: application/json" -X POST ${CARETAKER_USAGE_SOURCE_URL}

