# E2E Data Pipeline

This repository contains Apache Airflow pipeline for ETL and CI/CD pipeline to deploy docker image to Kubernetes cluster

## AirFlow Pipeline

This pipeline consists of three tasks which are run sequentially as a DAG:
- extract: retrieve current week menu
- transform: extract recipe information and identify top 10 recipes based on customer ratings and export to two seperate .csv files
- load: load .csv files to S3 bucket

To configure this pipeline
- change the API URL in config.ini and AWS credentials 
- ensure that config.ini has the necessary configurations for the scheduler 
- install docker in your local environment
- steps to run locally:
	build: docker build --rm -t hello-fresh/docker-airflow .
	run: docker run -d -p 8080:8080 hello-fresh/docker-airflow webserver
	to load DAGs examples: docker run -d -p 8080:8080 -e LOAD_EX=y hello-fresh/docker-airflow

Tests for ETL pipeline can be found in test folder. 


## CI/CD pipeline

This pipeline is configured to build a docker container, publish it to Google Container Registry and reply to Google Kubernetes Engine (GKE) when a commit is made. 

- google.yml
- job.yml
- kustomization.yaml

To configure this pipeline
- set up secrets in your workspace: GKE_PROJECT and GKE_SA_KEY
- change the values of GKE_CLUSTER and GKE_ZONE if necesssary


To trigger the pipeline when a release is created, change "kind" to "Release" in job.yaml