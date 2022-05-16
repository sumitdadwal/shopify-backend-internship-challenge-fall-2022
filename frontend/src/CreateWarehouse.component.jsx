import React, { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import './CreateWarehouse.styles.css';

const BASE_URL = 'http://localhost:8000/'


const CreateWarehouse = () => {

    const [warehouseName, setWarehouseName] = useState('')
    const [warehouseAddress, setWarehouseAddress] = useState('')
    const [type, setType] = useState('')
    const [selectManager, setSelectManager] = useState([])
    const [managers, setManagers] = useState([])

    useEffect(() => {
        fetch(BASE_URL + 'manager/all/')
            .then(response => {
                const json =response.json()
                console.log(json)
                if (response.ok) {
                    return json
                }
                throw response
            })
            .then(data => {
                setManagers(data)
            })
            .catch(error => {
                console.log(error)
            })
    }, [])


    const uploadWarehouse = () => {

        const json_string = JSON.stringify({
            'warehosue_name': warehouseName,
            'warehouse_address': warehouseAddress,
            'type': type,
            'manager_id' : selectManager
            
        })
    
        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: json_string

        }

        fetch(BASE_URL + 'warehouse', requestOptions)
            .then(response => {
                if (response.ok) {
                    console.log(response.json())
                    return response.json()
                    
                }
                throw response
            })
            .then(data => {
                window.location.reload()
                window.scrollTo(0, 0)
            })
            .catch(error => {
                console.log(error)
            })
    }

    const handleUpload = (e) => {
        e?.preventDefault();

        uploadWarehouse(data);
        setWarehouseName('')
        setWarehouseAddress('')
        setType('')
        setSelectManager(null)
    }

    return (
        <div>
            <span className='createWarehouse'>
            <input
                type="text"
                placeholder='Warehouse Name'
                onChange = {(event) => {
                    setWarehouseName(event.target.value)
                    console.log(event.target)
                }}
                value={warehouseName}
            />
            <input
                type="text"
                placeholder='Warehouse Address'
                onChange = {(event) => {
                    setWarehouseAddress(event.target.value)
                    console.log(event.target.value)
                }}
                value={warehouseAddress}
            />
            <input
                type="text"
                placeholder='Warehouse Type'
                onChange = {(event) => {
                    setType(event.target.value)
                    console.log(event.target.value)
                }}
                value={type}
            />
            <h5>Select Warehouse Manager:</h5>
            <select 
                name="select manager"
                id="managers"
                value={selectManager}
                onChange={(event) => {
                    setSelectManager(event.target.value)
                }}
                >
                    {
                        managers.map((manager) => {
                            return(
                                <option value={manager.manager_id}>{manager.manager_id} : {manager.manager_name}</option>                            )
                        })
                    }
            </select>
            
            <Button className='warehouseupload_button' onClick={handleUpload}>Upload</Button>
            </span>
        </div>
    )

};

export default CreateWarehouse;
