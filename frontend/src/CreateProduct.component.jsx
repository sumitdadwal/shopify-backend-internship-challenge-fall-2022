import React, { useEffect, useState } from 'react';
import { Button } from '@mui/material';
import './CreateProduct.styles.css';


const BASE_URL = 'http://localhost:8000/'

const CreateProduct = () => {

    const [productName, setProductName] = useState('')
    const [quantity, setQuantity] = useState(0)
    const [description, setDescription] = useState('')
    const [selectWarehouse, setSelectWarehouse] = useState(null)
    const [warehouses, setWarehouses] = useState([])
    const [image, setImage] = useState(null)

    useEffect(() => {
        fetch(BASE_URL + 'warehouse/all_warehouses')
            .then(response => {
                const json = response.json()
                console.log(json)
                if (response.ok) {
                    return json
                }
                throw response
            })
            .then(data => {
                setWarehouses(data)
            })
            .catch(error => {
                console.log(error);

            })

    }, []);

    const handleChange = (e) => {
        if (e.target.files[0]) {
            setImage(e.target.files[0])
        }    
    }

    const handleUpload = (e) => {
        e?.preventDefault();

        const formData = new FormData()
        formData.append('image', image)

        const requestOptions = {
            method: 'POST',
            body: formData
        }

        fetch(BASE_URL + 'product/image', requestOptions)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw response
            })
            .then (data => {
                setImage(null)
                uploadProduct(data.filename)
            })
            .catch(error => {
                console.log(error);
            })
            .finally(() => {
                setQuantity('')
                setImage(null)
                setDescription('')
                setSelectWarehouse(null)
                document.getElementById('fileInput').value = null
            })
    }
    
    const uploadProduct = (imageUrl) => {

        const json_string = JSON.stringify({
            'product_name': productName,
            'product_description': description,
            'product_count': quantity,
            'image_url': imageUrl,
            'image_url_type': 'relative',
            'warehouse_id': selectWarehouse
        })


        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: json_string
        }

        fetch(BASE_URL + 'product/create', requestOptions)
            .then(response => {
                if (response.ok) {
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

    


  return (
    <div>
        <span className='createProduct'>
            <input
                type="text"
                placeholder='Product Name'
                onChange = {(event) => {
                    setProductName(event.target.value)
                    console.log(event.target)
                }}
                value={productName}
            />
            <input
                type="number"
                placeholder='Item Quantity'
                onChange = {(event) => {
                    setQuantity(event.target.value)
                    console.log(event.target.value)
                }}
                value={quantity}
            />
            <input
                type="text"
                placeholder='Item Description'
                onChange = {(event) => setDescription(event.target.value)}
                value={description}
            />
            <h5>Select Product's warehouse:</h5>
            <select 
                name="select warehouse" 
                id="warehouses" 
                value={selectWarehouse}
                onChange={(event) => {
                    setSelectWarehouse(event.target.value)
                    console.log(event.target.value)
                }}
                >
                
                {
                        warehouses.map((warehouse) => {
                            return (
                                
                                    <option value={warehouse.warehouse_id}>ID - {warehouse.warehouse_id} : {warehouse.warehouse_name}</option>
                                
                            )
                        }
            
                )}
            </select>

            {/* <form>
                {
                    warehouses.map((warehouse) => {
                        return(
                            <div key={warehouse.id}>
                                <input 
                                    type="radio"
                                    id={warehouse.warehouse_name}
                                    name="Select Warehouse"
                                    onChange= {(event) => {
                                        setSelectWarehouse(event.target.value)
                                        console.log(event.target.value)
                                    }}
                                    value = {selectWarehouse} 
                                    
                                />
                                <label for={warehouse.warehouse_name}>{warehouse.id}</label>
                            </div>
                        )
                    })
                }  
            </form> */}
            <input
                type="file"
                id="fileInput"
                onChange={handleChange}
            />
            <Button className='productupload_button' onClick={handleUpload}>Upload</Button>
        </span>
    </div>
  )
}

export default CreateProduct
