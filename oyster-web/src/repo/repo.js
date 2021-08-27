'use strict'
import axios from 'axios'

const BASE_URL = "http://localhost:8000/"
// const BASE_URL = process.env.BASE_URL
const URL_DATASET = BASE_URL + "dataset"
const URL_DEMO_MODELS = BASE_URL + "model"
const URL_DEMO_TEST = BASE_URL + "test/model"

const axios_client = axios.create({
    baseURL: BASE_URL,
    timeout: 10000, // indicates, 1000ms ie. 1 second
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    }
})

function Repo() {}

// 
// CMS
Repo.prototype.getAllDatasets = () => axios_client.get(URL_DATASET)
Repo.prototype.getDatasetRows = (datasetID) => axios_client.get(URL_DATASET + "/" + datasetID)
Repo.prototype.getDemoModels = () => axios_client.get(URL_DEMO_MODELS)
Repo.prototype.testModel = (modelID, text) => axios_client.get(URL_DEMO_TEST + "/" + modelID + "?text=" + text)

export default Repo;