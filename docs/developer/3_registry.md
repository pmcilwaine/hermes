# Configuration Registry

The Hermes CMS contains a configuration registry. The system has dependencies on several configuration registry files, however the configuration registry is flexible to allow additional configurations to be added.

Each configuration registry is a json file stored in Amazon Simple Storage Service (S3). Configuration files are listed below.

| File       | Description                                                                                                                                                         |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| document   | Stores the document types. Assigns each document type to a class handler, ability to configure the administration add document screen, and url rules to be applied. |
| blueprint  | Stores blueprint module import paths for Flask                                                                                                                      |
| region     | The region the CMS cloud is in                                                                                                                                      |
| database   | The configuration for the Amazon RDS                                                                                                                                |
| cloud      | The name of the cloud                                                                                                                                               |
| storage    | The name of the storage bucket                                                                                                                                      |
| files      | The name of the files bucket. This is where uploaded files are stored                                                                                               |
| logs       | The name of the logs bucket, and location of the logs server                                                                                                        |
| metrics    | Metrics to be retrieved by the cloudwatch service                                                                                                                   |
| public_elb | The DNS used for the public elb.

Below explains in detail each configuration registry file.

## Document (document)

The document configuration registry contains the document types, the class handlers and url rules. Below is an example file.

```
{
    "type": [
        "Page",
        "File",
        "MultiPage",
        "Redirect"
    ],
    "Page": {
        "templates": [
            {
                "filename": "index.html",
                "name": "Homepage",
            },
            {
                "filename": "page.html",
                "name": "Standard Page"
            }
        ],
        "template_lookup": [
            "hermes_cms.templates"
        ],
        "document_module": "hermes_cms.document",
        "document_class": "Page"
    },
    "rules": {
        "exclude": [
            "/static",
            "/login",
            "/admin",
            {"type": "MultiPage"}
        ]
    }
}
```

| Key    | Description                                                                                                         | Optional |
|--------|---------------------------------------------------------------------------------------------------------------------|----------|
| type   | A list of document types. A document type object must also be specified so the system knows how to handle it.       | N        |
| :type: | :type: should be replaced with the same value as each item listed in type. There are required properties to a type. | N        |
| rules  | URL Rules that the system uses to assist in URL validation.                                                         | Y        |

### Type

Each type will have its own required properties however each document type requires a minimum of the listed below properties.

| Key             | Description                                             | Optional |
|-----------------|---------------------------------------------------------|----------|
| document_module | The absolute path to the module that contains the class | N        |
| document_class  | The class name of the document type to use              | N        |

### Rules

Rules only exclude URL from the system. No URL can start with any URL rule listed. 

## Blueprint (blueprint)

The blueprint configuration registry file stores the module that has a blueprint for the system to store.

```
{
    "blueprint": [
        {
            "module": "hermes_cms.views.admin",
            "name": "route"
        },
        {
            "module": "hermes_cms.views.main",
            "name": "route"
        }
    ]
}
```

| Key    | Description                                                        | Optional |
|--------|--------------------------------------------------------------------|----------|
| module | The full python module path                                        | N        |
| name   | The blueprint variable within the module. By default this is route | Y        |

## Region (region)

The region is an auto-generated registry file by Create Cloud, and can be specified during the Create Cloud process. Below is an example file.

```
{
    "region": "ap-southeast-2"
}
```

| Key    | Description        | Optional |
|--------|--------------------|----------|
| region | A valid AWS region | N        |

## Database (database)

The database is an auto-generated registry file by Create Cloud. Below is an example file.

```
{
    "host": "localhost",
    "username": "user",
    "password": "password",
    "port": 5432,
    "db_name": "my_cms",
    "driver": "postgres"
}
```

| Key      | Description                                                                             | Optional |
|----------|-----------------------------------------------------------------------------------------|----------|
| host     | The host of the database                                                                | N        |
| username | The username to login to database with                                                  | N        |
| password | The password to login to database with                                                  | N        |
| port     | The port used to connect to database                                                    | N        |
| name     | The database name to use                                                                | N        |
| driver   | The database driver to use. Options are postgres and mysql. By default this is postgres | Y        |

## Cloud (cloud)

The cloud is an auto-generated registry file by Create Cloud. It is the name passed to Create Cloud. Below is an example file.

```
{
    "name": "hermes_cms"
}
```

| Key  | Description                                         | Optional |
|------|-----------------------------------------------------|----------|
| name | The name of the cloud specified during Create Cloud | N        |

## Storage (storage)

The storage file is auto-generated by Create Cloud. Below is an example file.

```
{
    "name": "storage"
}
```

| Key  | Description                 | Optional |
|------|-----------------------------|----------|
| name | The full name of the bucket | N        |

## Files (files)

The "files" file is auto-generated by Create Cloud. Below is an example file.

```
{
    "name": "files"
}
```

| Key  | Description                 | Optional |
|------|-----------------------------|----------|
| name | The full name of the bucket | N        |

## Logs (logs)

The logs file is auto-generated by Create Cloud. Below is an example file.

```
{
    "name": "logs"
}
```

| Key  | Description                 | Optional |
|------|-----------------------------|----------|
| name | The full name of the bucket | N        |

## Metrics (metrics)

The metrics file is created as data for the create cloud process. It is supposed to be updated by a developer. Below is an example file.

```
{
    "filter_namespaces": [
        "AWS/EC2"
    ],
    "frequency_seconds": 15 * 60,
    "delay_seconds": 60 * 60,
    "period_seconds": 60,
    "filter_metrics": [
        {
            "metric": "MetricName",
            "statistics": ["Sum"],
            "dimensions": {
                "Key": "Value"
            },
            "unit" "Seconds"
        }
    ]
}
```

| Key               | Description                                                                                                                                        | Optional |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| filter_namespaces | A list of namespaces to use. If empty all AWS Namespaces will be retrived                                                                          | Y        |
| frequency_seconds | This is the query range for metrics                                                                                                                | N        |
| delay_seconds     | This is used to set a delay on the query so it queries x seconds behind time (useful for jobs that critically need to be eventually consistent)    | N        |
| period_seconds    | The granularity, in seconds, of the returned datapoints. Period must be at least 60 seconds and must be a multiple of 60. The default value is 60. | Y        |
| filter_metrics    | Will retrieve all metrics specified. If omitted all the metrics will be retrieved.                                                                 | Y        |

## Public ELB (public_elb)

The public_elb is an auto-generated configuration registry file by Create Cloud. Below is an example file.

```
{
    "host": "http://dns-host-name.aws.com/",
    "domain": "http://mydomain.com/"
}
```

| Key    | Description                                                                                          | Optional |
|--------|------------------------------------------------------------------------------------------------------|----------|
| host   | The ELB DNS retrieved during the create cloud                                                        | N        |
| domain | The domain that is used for public use. If a CNAME is used for the ELB DNS, this should be specified | Y        |
