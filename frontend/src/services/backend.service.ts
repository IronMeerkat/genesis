// Credit to https://gist.github.com/paulsturgess/ebfae1d1ac1779f18487d3dee80d1258
import React, { useState, useEffect, useContext } from 'react';
import axios, {AxiosInstance, AxiosRequestConfig} from "axios";
import { Redirect } from 'react-router-dom'
import { Context } from '../components';

const BASE_URL = 'http://localhost:8000/api'

const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true'
 }

const handleSuccess = (response: any) => {
    return response;
}

const handleError = (error: { response: { status: any; }; }) => {
    // switch (error.response.status) {
    //     case 401:
    //         window.location.href = BASE_URL + '/401';
    //         break;
    //     case 404:
    //         console.log(error)
    //         window.location.href = BASE_URL + '/404';
    //         break;
    //     default:
    //         window.location.href = BASE_URL + '/500';
    //         break;
    // }
    return Promise.reject(error)
}

class Backend {

    private service: AxiosInstance;

    constructor(token?: string) {

        let service = axios.create({
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
             }, // get the auth header here automatically somehow
            baseURL: BASE_URL,
        });
        service.interceptors.response.use(this.handleSuccess, this.handleError);
        this.service = service;
    }

    handleSuccess(response: any) {
        return response;
    }

    handleError = (error: { response: { status: any; }; }) => {
        // switch (error.response.status) {
        //     case 401:
        //         window.location.href = BASE_URL + '/401';
        //         break;
        //     case 404:
        //         console.log(error)
        //         window.location.href = BASE_URL + '/404';
        //         break;
        //     default:
        //         window.location.href = BASE_URL + '/500';
        //         break;
        // }
        return Promise.reject(error)
    }


    async get(path: string) {
        return await this.service.get(path).then(
            (response) => {
                return response
            }
        );

    }

    async patch(path: string, payload: any, callback: (arg0: number, arg1: any) => any) {
        return await this.service.request({
            method: 'PATCH',
            url: path,
            responseType: 'json',
            data: payload
        }).then((response) => callback(response.status, response.data));
    }

    async post(path: string, payload: any, callback: (arg0: number, arg1: any) => any) {
        return await this.service.request({
            method: 'POST',
            url: path,
            responseType: 'json',
            data: payload
        }).then((response) => callback(response.status, response.data));
    }

    async upload(path: string, {files}: any, callback: (arg0: number, arg1: any) => any){

        const [file] = files;
        const fileReader = new FileReader();
        fileReader.onload = async (e:{target: any}) => {
            const payload = e.target.result;
            let formData = new FormData();
            formData.append('file', payload);
            return await this.service.request({
                method: 'POST',
                url: path,
                responseType: 'json',
                data: formData
            }).then((response) => callback(response.status, response.data));
        };
        fileReader.readAsDataURL(file);


    }
}

const instantiateAxios = () => {
    axios.defaults.baseURL = 'http://localhost:8000/api'
    axios.defaults.headers({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': 'true'
   })

   axios.interceptors.response.use(handleSuccess, handleError);
}

const upload = async (path: string, {files}: any, callback: (arg0: number, arg1: any) => any) => {

    const [file] = files;
    const fileReader = new FileReader();
    fileReader.onload = async (e:{target: any}) => {
        const payload = e.target.result;
        let formData = new FormData();
        formData.append('file', payload);
        return await axios.request({
            method: 'POST',
            url: path,
            responseType: 'json',
            data: formData
        }).then((response) => callback(response.status, response.data));
    };
    fileReader.readAsDataURL(file);
}

export { Backend, upload}