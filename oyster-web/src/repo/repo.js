'use strict'
import axios from 'axios'

const BASE_URL = "http://localhost:8000/"
// const BASE_URL = process.env.BASE_URL
const URL_DATASET = BASE_URL + "dataset"

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

export default Repo;
