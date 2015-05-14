FORMAT: 1A

# Hermes Administration REST API 1.0

# Data Structures

## Users (array[UserResponse], required)

## UserResponse (object)
+ guid: `09cefabf-c484-43b2-9861-f90119de8119` (string)
+ email: `test@example.org` (string)
+ first_name: `Test` (string)
+ last_name: `User` (string)

## User (object)
+ email: test@example.org (string, required)
+ password: password (string)
+ firstName: Test (string)
+ lastName: User (string)

## Page Information (object)
+ offset: 0 (number) ... The amount of results to skip 
+ limit: 50 (number) ... The amount of results to show

## Field Error (object)
+ fieldname: Error Message for field (string) ... Each field that has an error will be in added.

## Form Error (object)
+ fields (Field Error)

## Authentication Error (object)
+ title: `A title goes here` (string, required) ... The title of the issue
+ message: `Message to be shown` (string, required) ... The message explaining the issue

## Authorisation Error (object)
+ title: `A title goes here` (string, required) ... The title of the issue
+ message: `Message to be shown` (string, required) ... The message explaining the issue

## Page Not Found (object)
+ title: `Not found` (string, required) ... The title of the issue
+ message: `Item not found` (string, required) ... The message explaining the issue

## Document (object)
+ guid: `09cefabf-c484-43b2-9861-f90119de8119` (string, required)
+ name: `Name of Page` (string, required)
+ menutitle: `Name of Menu` (string, required)
+ url: /path/to/page (string, required)
+ published: false (boolean, required)
+ showInMenu: true (boolean, required)

## Upload URL (object)
+ uploadUrl: http://s3.amazon.com/hash (string, required) ... An upload URL generated to use for file upload.

## Module (object)
+ name: Name (string, required)

## Page (object)
+ template: Template Name (string, required) ... The name of the template to use.
+ sectionName (array[Module], required) ... Sections which are specified by the template.

## File (object)
+ s3Path: s3://bucket/path/to/key (string, required)
+ contentType: Image (string, required)

# Group Users
## Users [/users]

### List Users [GET]

+ Response 200 (application/json)
    + Attributes (object)
        + users (Users, required) ... The user objects
        + meta (Page Information)

### New User [POST]
+ Request (application/json)
    + Attributes (User)

+ Response 201 (application/json)
    + Attributes (UserResponse)

+ Response 400 (application/json)
Form error
    + Attributes (Form Error)

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

## User [/users/{guid}]
### Save User [PUT]

+ Parameters
    + guid (string) ... The record id
    
+ Request (application/json)
    + Attributes (User)

+ Response 200 (application/json)
    + Attributes (UserResponse)
    
+ Response 400 (application/json)
    + Attributes (Form Error)

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

+ Response 404 (application/json)
    + Attributes (Page Not Found)

### Delete User [DELETE]
+ Parameters
    + guid (string) ... The record id
    
+ Response 204

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

+ Response 404 (application/json)
    + Attributes (Page Not Found)

# Group Documents

## Documents [/admin/document]

### List Documents [GET]

+ Response 200 (application/json)
    + Attributes (object)
        + documents (Document)
        + meta (Page Information)

### Create new Page [POST]

+ Response 200 (application/json)
    + Attributes
        + document (Document)
        + page (Page)

### Create new File [POST]

+ Response 200 (application/json)
    + Attributes
        + document (Document)
        + file (File)
        
## Single Document [/admin/document/{guid}]
### Delete Document [DELETE]
+ Parameters
    + guid (string) ... The record id
    
+ Response 204

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

+ Response 404 (application/json)
    + Attributes (Page Not Found)
    
## Update Page [PUT]

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

+ Response 404 (application/json)
    + Attributes (Page Not Found)
    
## Update File [PUT]

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)

+ Response 404 (application/json)
    + Attributes (Page Not Found)
    
## Restore Document [/admin/document/{guid}/restore]
### Restore Document [PUT]

+ Response 200 (application/json)

# Group Generate Signed Upload URL
## Create new Signed Upload URL [/admin/upload_url]
### Create new Upload URL [POST]

+ Response 201 (application/json)
    + Attributes (Upload URL)

+ Response 401 (application/json)
    + Attributes (Authentication Error)

+ Response 403 (application/json)
    + Attributes (Authorisation Error)
