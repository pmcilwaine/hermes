\newpage

# Documents

This section describes how to use documents within the Hermes Content Management System.

![Document List](assets/document-list.png "Document List")

## What is a Document?

A document is a uniquely accessible URL within the Content Management System (CMS). Documents are versioned so they can be restored from a certain point in time, as well as no document is deleted so is recoverable.

\newpage

## Create a Page

In the Document List view, click on add Document.

![Document Form](assets/document-form.png "Document Form")

1. Enter the name of the document
1. Enter the menu title, this is displayed in the navigation
1. If documents already exist the document being created can be a child to that existing document. Select the appropriate parent document.
1. Enter a unique URL. It must not start with / or end with a /
1. Select the Type of Page.
1. Select the template to use for this Page. Options are currently only Standard
1. Checking the Publish Document checkbox will ensure the document is available to the public.
1. Checking Show in Navigation will ensure the document is visible in the navigation.
1. Click next to continue finalise the document.

\newpage

10. Use the WYSIWYG Editor to enter the content for the page. If you know the link to existing documents you can link to these documents.

![Page Form](assets/page-form.png "Page Form")

It may take some time for the submit to be successful as its saving the data into the Database as well as storing a document object within Amazon S3.

\newpage

## Create a File 

In the Document List view, click on add Document.

![Document Form](assets/document-form.png "Document Form")

1. Enter the name of the document
1. Enter the menu title, this is displayed in the navigation
1. If documents already exist the document being created can be a child to that existing document. Select the appropriate parent document.
1. Enter a unique URL. It must not start with / or end with a /
1. Select the Type of File.
1. Checking the Publish Document checkbox will ensure the document is available to the public.
1. Checking Show in Navigation will ensure the document is visible in the navigation.
1. Click next to continue finalise the document.

\newpage

10. Click the Choose File or Browse button to select the file to be uploaded.

![File Form](assets/file-form.png "File Form")

It may take some time for the submit to be successful as its saving the data into the Database as well as storing a document object within Amazon S3.

\newpage

## Create a MultiPage

In the Document List view, click on add Document.

![Document Form](assets/document-form.png "Document Form")

1. Enter the name of the document
1. Enter the menu title, this is displayed in the navigation
1. If documents already exist the document being created can be a child to that existing document. Select the appropriate parent document.
1. Enter a unique URL. It must not start with / or end with a /
1. Select the Type of MultiPage.
1. Checking the Publish Document checkbox will ensure the document is available to the public.
1. Checking Show in Navigation will ensure the document is visible in the navigation.
1. Click next to continue finalise the document.

\newpage

10. Click the Choose File or Browse button to select the file to be uploaded. This file must be a ZIP file.

![MultiPage Form](assets/multipage-form.png "MultiPage Form")

It may take some time for the submit to be successful as its saving the data into the Database as well as storing a document object within Amazon S3.

\newpage

## Modify Document

![Document List](assets/document-list.png "Document List")

To modify a document find the document you want to modify and click the "Edit" button. You will be then shown the appropriate document. If you get a No permission message displayed, it means the account you have logged in with does not allow you to modify documents.

\newpage

![Modify Document](assets/page-edit.png "Modify Document")

All validation of fields apply when modifying a document.

\newpage

## Delete Document

![Document List](assets/document-list.png "Document List")

To delete a document find the document you want to delete and click the "Delete" button. This will will remove the document from the list. See Restore Document to find out how to restore a document. 

If you get a "No Permission" error message, it means the account you are logged in with does not have permission to delete documents. You will need to get an Administrator to give you additional permissions.

\newpage

## Restore Document

![Document List](assets/document-list.png "Document List")

Click on the Document Restore button.

![Document Restore](assets/document-restore.png "Document Restore")

Find the document to restore and click Restore. Once clicked the document will be restored and will be visible on the Document List.

\newpage

## Restore Version Document

![Document List](assets/document-list.png "Document List")

Find the document you need to restore a particular version. Then click on the version button. 

\newpage

![Restore Document Version](assets/document-version.png "Restore Document Version")

This will display a list of versions of the document. Select the version of the document you wish to restore. This will now become the latest document version.

You cannot view the contents of the document to compare against at this stage.

\newpage

## Download Archive

![Document List](assets/document-list.png "Document List")

In the above Figure there are checkboxes which can be checked to mark documents to be part of the Download ZIP Archive. If a document has children these pages will automatically be added to the ZIP. When ready to create the Download ZIP archive a modal will be displayed so you can name the Archive. This name is used as the name on the Job list page so you can track the job. When ready you can download from the Job page.

![Download Migration Archive](assets/migration-download.png "Download Migration Archive")

If you get a "No Permission" error message, it means the account you are logged in with does not have permission to delete documents. You will need to get an Administrator to give you additional permissions.

\newpage

## Upload Migration Archive

To upload a migration archive to the system. You will need to ensure you have first downloaded an archive. On the download list page click on the "Upload Migration" button

![Upload Migration](assets/migration-upload.png "Upload Migration")

You will need to ensure that you upload the correct ZIP archive. When the ZIP file is uploaded a Job is created (See Jobs) where you can track the upload. An invalid Migration archive will fail.

If you get a "No Permission" error message, it means the account you are logged in with does not have permission to delete documents. You will need to get an Administrator to give you additional permissions.

\newpage

## View Document

Documents are available publicly, by going to e.g. [http://hermescms.paulmcilwaine.com/](http://hermescms.paulmcilwaine.com/) and entering a valid path after the domain
