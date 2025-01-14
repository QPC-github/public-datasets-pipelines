# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="city_health_dashboard.city_health_dashboard",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    chdb_data_city = kubernetes_pod.KubernetesPodOperator(
        task_id="chdb_data_city",
        startup_timeout_seconds=600,
        name="city_health_dashboard_chdb_data_city_all",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.city_health_dashboard.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cityhealthdashboard.com/drupal/media/23/download",
            "SOURCE_FILE": "files/chdb_data_city_data.zip",
            "TARGET_FILE": "files/chdb_data_city_data_output.csv",
            "CHUNKSIZE": "500000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "city_health_dashboard",
            "TABLE_ID": "chdb_data_city_all",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/city_health_dashboard/chdb_data_city_all/data_output.csv",
            "SCHEMA_PATH": "data/city_health_dashboard/schema/chdb_data_city_schema.json",
            "DROP_DEST_TABLE": "N",
            "TRUNCATE_TABLE": "Y",
            "INPUT_FIELD_DELIMITER": ",",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "INPUT_CSV_HEADERS": '[\n  "state_abbr","state_fips","city_fips","stpl_fips","stcosub_fips","city_name","metric_name","metric_number","group_name",\n  "group_number","num","denom","est","lci","uci","county_indicator","multiplier_indicator","data_yr_type","data_yr",\n  "geo_level","date_export","census_year","version","NCHS_disclaimer","suggested_citation"\n]',
            "DATA_DTYPES": '{\n  "state_abbr": "str",\n  "state_fips": "str",\n  "city_fips": "str",\n  "stpl_fips": "str",\n  "stcosub_fips": "str",\n  "city_name": "str",\n  "metric_name": "str",\n  "metric_number": "str",\n  "group_name": "str",\n  "group_number": "str",\n  "num": "str",\n  "denom": "str",\n  "est": "str",\n  "lci": "str",\n  "uci": "str",\n  "county_indicator": "str",\n  "multiplier_indicator": "str",\n  "data_yr_type": "str",\n  "data_yr": "str",\n  "geo_level": "str",\n  "date_export": "str",\n  "census_year": "str",\n  "version": "str",\n  "NCHS_disclaimer": "str",\n  "suggested_citation": "str"\n}',
            "OUTPUT_CSV_HEADERS": '[\n  "state_abbr","state_fips","city_fips","stpl_fips","stcosub_fips","city_name","metric_name","metric_number","group_name",\n  "group_number","num","denom","est","lci","uci","county_indicator","multiplier_indicator","data_yr_type","data_yr",\n  "geo_level","date_export","census_year","version","NCHS_disclaimer","suggested_citation","source_url",\n  "etl_timestamp"\n]',
            "RENAME_HEADERS_LIST": '{\n  "state_abbr": "state_abbr",\n  "state_fips": "state_fips",\n  "city_fips": "city_fips",\n  "stpl_fips": "stpl_fips",\n  "stcosub_fips": "stcosub_fips",\n  "city_name": "city_name",\n  "metric_name": "metric_name",\n  "metric_number": "metric_number",\n  "group_name": "group_name",\n  "group_number": "group_number",\n  "num": "num",\n  "denom": "denom",\n  "est": "est",\n  "lci": "lci",\n  "uci": "uci",\n  "county_indicator": "county_indicator",\n  "multiplier_indicator": "multiplier_indicator",\n  "data_yr_type": "data_yr_type",\n  "data_yr": "data_yr",\n  "geo_level": "geo_level",\n  "date_export": "date_export",\n  "census_year": "census_year",\n  "version": "version",\n  "NCHS_disclaimer": "NCHS_disclaimer",\n  "suggested_citation": "suggested_citation"\n}',
            "TABLE_DESCRIPTION": "City Health Dashboard Data Tract",
            "PIPELINE_NAME": "chdb_data_city_all",
            "FILE_NAME_PREFIX": "CHDB_data_city_all_v15.1",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Run CSV transform within kubernetes pod
    chdb_data_tract = kubernetes_pod.KubernetesPodOperator(
        task_id="chdb_data_tract",
        startup_timeout_seconds=600,
        name="city_health_dashboard_chdb_data_tract_all",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.city_health_dashboard.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cityhealthdashboard.com/drupal/media/23/download",
            "SOURCE_FILE": "files/chdb_data_tract_data.zip",
            "TARGET_FILE": "files/chdb_data_tract_data_output.csv",
            "CHUNKSIZE": "500000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "city_health_dashboard",
            "TABLE_ID": "chdb_data_tract_all",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/city_health_dashboard/chdb_data_tract_all/data_output.csv",
            "SCHEMA_PATH": "data/city_health_dashboard/schema/chdb_data_tract_schema.json",
            "DROP_DEST_TABLE": "N",
            "TRUNCATE_TABLE": "Y",
            "INPUT_FIELD_DELIMITER": ",",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "INPUT_CSV_HEADERS": '[\n  "state_abbr","state_fips","county_name","city_fips","stpl_fips","stcosub_fips","stcotr_fips","city_name","metric_name",\n  "metric_number","group_name","group_number","num","denom","est","lci","uci","data_yr_type","data_yr","geo_level",\n  "date_export","census_year","version","suggested_citation"\n]',
            "DATA_DTYPES": '{\n  "state_abbr": "str",\n  "state_fips": "str",\n  "county_name": "str",\n  "city_fips": "str",\n  "stpl_fips": "str",\n  "stcosub_fips": "str",\n  "stcotr_fips": "str",\n  "city_name": "str",\n  "metric_name": "str",\n  "metric_number": "str",\n  "group_name": "str",\n  "group_number": "str",\n  "num": "str",\n  "denom": "str",\n  "est": "str",\n  "lci": "str",\n  "uci": "str",\n  "data_yr_type": "str",\n  "data_yr": "str",\n  "geo_level": "str",\n  "date_export": "str",\n  "census_year": "str",\n  "version": "str",\n  "suggested_citation": "str"\n}',
            "OUTPUT_CSV_HEADERS": '[\n  "state_abbr","state_fips","county_name","city_fips","stpl_fips","stcosub_fips","stcotr_fips","city_name","metric_name",\n  "metric_number","group_name","group_number","num","denom","est","lci","uci","data_yr_type","data_yr","geo_level",\n  "date_export","census_year","version","suggested_citation","source_url","etl_timestamp"\n]',
            "RENAME_HEADERS_LIST": '{\n  "state_abbr": "state_abbr",\n  "state_fips": "state_fips",\n  "county_name": "county_name",\n  "city_fips": "city_fips",\n  "stpl_fips": "stpl_fips",\n  "stcosub_fips": "stcosub_fips",\n  "stcotr_fips": "stcotr_fips",\n  "city_name": "city_name",\n  "metric_name": "metric_name",\n  "metric_number": "metric_number",\n  "group_name": "group_name",\n  "group_number": "group_number",\n  "num": "num",\n  "denom": "denom",\n  "est": "est",\n  "lci": "lci",\n  "uci": "uci",\n  "data_yr_type": "data_yr_type",\n  "data_yr": "data_yr",\n  "geo_level": "geo_level",\n  "date_export": "date_export",\n  "census_year": "census_year",\n  "version": "version",\n  "suggested_citation": "suggested_citation"\n}',
            "TABLE_DESCRIPTION": "City Health Dashboard Data Tract",
            "PIPELINE_NAME": "chdb_data_tract_all",
            "FILE_NAME_PREFIX": "CHDB_data_tract_all_v15.1",
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    [chdb_data_tract, chdb_data_city]
