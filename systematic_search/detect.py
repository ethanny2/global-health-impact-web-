
#----------------------------------------------OCR SCRIPT---------------------------------------------------------------------------------
'''
-Already uploaded a sample PDF pertaining to Artemether-Lumefantrine efficacy Malaria
    *PDF URL : https://ac.els-cdn.com/S0140673605664173/1-s2.0-S0140673605664173-main.pdf?_tid=76d5857c-88f1-4664-9564-3165804fc41c&acdnat=1539717010_54e933e14e8dc338baab25b3dbcb3f15
    *Google Scholar Parsed URL: https://www.sciencedirect.com/science/article/pii/S0140673605664173
    
    *Link Url on Google Cloud Storage Bucket: https://console.cloud.google.com/storage/browser/global_health_bucket 
    *Link for GS Util on Google Cloud Storage Bucket: gs://global_health_bucket/test.pdf


-Whats the format for the gcs_source_url and destination url ?
-DOCUMENT PAGES FOR REFERENCE: https://googleapis.github.io/google-cloud-python/latest/vision/index.html

json_format.Parase(text,message)
Parses a JSON representation of a protocol message into a message.
Args:
  text: Message JSON representation.
  message: A protocol beffer message to merge into.
  
'''


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    from google.cloud import vision
    from google.cloud import storage
    from google.protobuf import json_format

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    #Necessary for set up to make client call to OCR parser in cloud. 
    client = vision.ImageAnnotatorClient()

    #Use type DOCUMENT_TEXT_DETECTION from the vision Features enums to parse PDFs and tiff files
    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    #parse the passed in gcs_source_url to get a GcsSource object
    #Use that object to creaete InputConfig object
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    #Do that same for the destination uri to get an output config object 
    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    #Create asynchronous request object using the feature from enum, input config and output config.
    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    #"Annotating files" means scanning them with OCR and creating appropriate markup
    # Call it with the created async object
    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    #Specify timeout in seconds
    operation.result(timeout=1000)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    # storage is imported from external Google Library
    storage_client = storage.Client()
    #regex to pick bucket name from passed in gsc_destination_uri
    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    print("prefix is " + prefix)
    #Use imported storage_client class to get a reference object to the bucket
    bucket = storage_client.get_bucket(bucket_name=bucket_name)

    # List objects with the given prefix.
    # Trying to output names of the result of the parsed files from the bucket.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]
    json_string = output.download_as_string()
    #See top of file for parameter/function definition
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())


    # The actual response for the first page of the input file.
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print(u'Full text:\n{}'.format(
        annotation.text))




source_uri = 'gs://ghitest2_bucket/test.pdf'
dest_uri = 'gs://ghitest2_bucket'

async_detect_document(source_uri,dest_uri)