import React, { useState, useEffect } from 'react'
import './Product.styles.css'
import { Avatar, Button, Modal, Input } from "@mui/material";
import { makeStyles } from '@mui/styles';
import { useNavigate } from 'react-router-dom'
import { createTheme } from '@mui/system';


const BASE_URL = 'http://localhost:8000/'


const Product = ({ product }) => {


  const [imageUrl, setImageUrl] = useState('')

  // let navigate = useNavigate()

  useEffect(() => {
    if (product.image_url_type == 'absolute') {
      setImageUrl(product.image_url)
    } else {
      setImageUrl(BASE_URL + product.image_url)
    }
  }, [])

  const handleDelete = (event) => {
    event?.preventDefault();

    const requestOptions = {
      method : 'DELETE'
    }

    fetch(BASE_URL + 'product/delete/' + product.id, requestOptions)
      .then(response => {
        if (response.ok) {
          window.location.reload()
        }
        throw response
      })
      .catch(error => {
        console.log(error)
      })
  }

  


  return (
    <div className='product'>
      <div >
        <img 
          className='product_image'
          src={imageUrl}
        />
         <div>
         <h4 className="product_count"><b>Product Name</b>: {product.product_name}</h4>
         <h4 className="product_count"><b>Product Description</b>: {product.product_description}</h4>
          <h4 className="product_count"><b>Product Count</b>: {product.product_count}</h4>
        </div>
        <div>
          <h4 className='product_warehouse'><b>Warehouses</b>: {product.warehouse.warehouse_name}</h4>
          <h4 className='product_warehouse_address'><b>Warehouse Address</b>: {product.warehouse.warehouse_address}</h4>
          <h4 className='product_warehouse'><b>Manager ID</b>: {product.warehouse.manager_id}</h4>
          <h4 className="product_count"><b>Created at</b>: {product.timestamp}</h4>
        </div>
        <span>
          <Button className='product-delete' onClick={handleDelete} >Delete</Button>
        </span>
        

      </div>
    </div>
  )
}//continue from adding product count and warehouse dets

export default Product;

