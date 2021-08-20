METADATA_TAG_Dataset = 'Dataset'
METADATA_TAG_DataProcessing = 'Data Preprocessing'
METADATA_TAG_Experiment = 'Experiment'
METADATA_TAG_ProcessedDataset = 'Processed dataset'
METADATA_TAG_MLModel = 'ML Model Operations'

api_tags_metadata = [
    {
        "name": METADATA_TAG_Dataset,
        "description": "Operations with Raw Datasets.",
    },
    {
        "name": METADATA_TAG_DataProcessing,
        "description": "Raw Datasets preprocessing APIs.",
    },
    {
        "name": METADATA_TAG_Experiment,
        "description": "APIs related to experiment. Model will used for showing UI elements.",
    },
    {
        "name": METADATA_TAG_MLModel,
        "description": "APIs related to ML model.",
    },
    {
        "name": METADATA_TAG_ProcessedDataset,
        "description": "APIs related to training datasets. EntityTagsSet will save the row ids along with tag details.",
    },
    ]