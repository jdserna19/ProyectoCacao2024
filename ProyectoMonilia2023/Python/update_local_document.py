from document_local_writer import DocumentLocalWriter

DOCUMENT_PATH = "data/13072018144114/lot_3/"
COMMAND = "L3\n"
DEVELOPMENT_STAGE = 3

document_local_writer = DocumentLocalWriter()
document_path = document_local_writer.add_development_stage_to_document(document_path=DOCUMENT_PATH, command=COMMAND,
                                                                        development_stage=DEVELOPMENT_STAGE)
if document_path is not None:
    # The document was updated successfully.
    print("{} was updated.".format(document_path))
else:
    # The given document could not be found.
    print("Document was not found.")
