\newpage

# Configuration Registry

The Hermes CMS contains a configuration registry. The system has dependencies on several configuration registry files, however the configuration registry is flexible to allow additional configurations to be added.

Each configuration registry is a json file stored in Amazon Simple Storage Service (S3). Configuration files are listed below.

+------------+-----------------------------------------------------------------+
| File       | Description                                                     |
+============+=================================================================+
| admin_rules| This stores all the URL Rules for the Administration as well as |
|            | the methods that are supported                                  |
+------------+-----------------------------------------------------------------+
| document   | Stores the document types. Assigns each document type to a      |
|            | class handler, ability to configure the administration add      |
|            | document screen, and url rules to be applied.                   |
+------------+-----------------------------------------------------------------+
| blueprint  | Stores blueprint module import paths for Flask                  |
+------------+-----------------------------------------------------------------+
| jobs       | This stores the configuration of the background jobs such as    |
|            | multipage                                                       |
+------------+-----------------------------------------------------------------+
| region     | The region the CMS cloud is in                                  |
+------------+-----------------------------------------------------------------+
| database   | The configuration for the Amazon RDS                            |
+------------+-----------------------------------------------------------------+
| storage    | The name of the storage bucket                                  |
+------------+-----------------------------------------------------------------+
| files      | The name of the files bucket. This is where uploaded files are  | 
|            | stored                                                          |
+------------+-----------------------------------------------------------------+
| cms        | The DNS used for the public elb as well as its name             |
+------------+-----------------------------------------------------------------+
| queues     | Contains the name of the Queue and the ARN URI                  | 
+------------+-----------------------------------------------------------------+
| topics     | Contains the name of the Topic and the ARN URI                  |
+------------+-----------------------------------------------------------------+

Below explains in detail each configuration registry file.

## Document (document)

The document configuration registry contains the document types, the class handlers and url rules. Below is an example file.

```
{
    "type": [
        "Page",
        "File",
        "MultiPage"
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
    }
}
```

+--------+----------------------------------------------------------+----------+
| Key    | Description                                              | Optional |
+========+==========================================================+==========+
| type   | A list of document types. A document type object must    |          |
|        | also be specified so the system knows how to handle it.  | N        |
+--------+----------------------------------------------------------+----------+
| :type: | :type: should be replaced with the same value as each    | N        |
|        | item listed in type. There are required properties to a  |          |
|        | type.                                                    |          |
+------------+------------------------------------------------------+----------+

### Type

Each type will have its own required properties however each document type requires a minimum of the listed below properties.

+-----------------+-------------------------------------------------+----------+
| Key             | Description                                     | Optional |
+=================+=================================================+==========+
| document_module | The absolute path to the module that contains   | N        |
|                 | the class                                       |          |
+-----------------+-------------------------------------------------+----------+
| document_class  | The class name of the document type to use      | N        |
+-----------------+-------------------------------------------------+----------+

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

+--------+----------------------------------------------------------+----------+
| Key    | Description                                              | Optional |
+========+==========================================================+==========+
| module | The full python module path                              | N        |
+--------+----------------------------------------------------------+----------+
| name   | The blueprint variable within the module. By default     | Y        |
|        | this is route                                            |          |
+--------+----------------------------------------------------------+----------+

## Region (region)

The region is an auto-generated registry file by Create Cloud, and can be specified during the Create Cloud process. Below is an example file.

```
{
    "region": "ap-southeast-2"
}
```
+--------+--------------------+----------+
| Key    | Description        | Optional |
+========+====================+==========+
| region | A valid AWS region | N        |
+--------+--------------------+----------+

## Database (database)

The database is an auto-generated registry file by Create Cloud. Below is an example file.

```
{
    "database": "driver://username:password@host:port/name"
}
```

+----------+--------------------------------------------------------+----------+
| Key      | Description                                            | Optional |
+==========+========================================================+==========+
| host     | The host of the database                               | N        |
+----------+--------------------------------------------------------+----------+
| username | The username to login to database with                 | N        |
+----------+--------------------------------------------------------+----------+
| password | The password to login to database with                 | N        |
+----------+--------------------------------------------------------+----------+
| port     | The port used to connect to database                   | N        |
+----------+--------------------------------------------------------+----------+
| name     | The database name to use                               | N        |
+----------+--------------------------------------------------------+----------+
| driver   | The database driver to use. Options are postgres and   | N        |
|          | mysql. By default this is postgres                     |          |
+----------+--------------------------------------------------------+----------+

## Storage (storage)

The storage file is auto-generated by Create Cloud. Below is an example file.

```
{
    "name": "storage"
}
```

+------+-----------------------------+----------+
| Key  | Description                 | Optional |
+======+=============================+==========+
| name | The full name of the bucket | N        |
+------+-----------------------------+----------+

## Files (files)

The "files" file is auto-generated by Create Cloud. Below is an example file.

```
{
    "name": "files"
}
```

+------+-----------------------------+----------+
| Key  | Description                 | Optional |
+======+=============================+==========+
| name | The full name of the bucket | N        |
+------+-----------------------------+----------+

## CMS (cms)

The public_elb is an auto-generated configuration registry file by Create Cloud. Below is an example file.

```
{
    "dns": "http://dns-host-name.aws.com/",
    "name": "load-balancer-name"
}
```

+--------+----------------------------------------------------------+----------+
| Key    | Description                                              | Optional |
+========+==========================================================+==========+
| dns    | The ELB DNS retrieved during the create cloud            | N        |
+--------+----------------------------------------------------------+----------+
| name   | The Name of the ELB created during cloudformation        | N        |
+--------+----------------------------------------------------------+----------+

## Queues

The queue contains the name of the queue and the ARN as key/value pairs. This file is auto-generated by Create Cloud

```
{
    "queue": {
        "name": "arn://uri"
    }
}
```

## Topics

The topics contains the name of the topic and the ARN as key/value pairs. This file is auto-generated by Create Cloud

```
{
    "topic": {
        "name": "arn://uri"
    }
}
```
