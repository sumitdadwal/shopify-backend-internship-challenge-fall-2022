import './Home.styles.css';
import {API} from './backend'
import { Button, makeStyles, Modal } from "@mui/material";
import { useState, useEffect } from 'react';
import Product from './Product.component';
import CreateProduct from './CreateProduct.component';
import { Routes, Route } from "react-router-dom"
import updateProduct from './UpdateProducts.component';
import CreateWarehouse from './CreateWarehouse.component';



const BASE_URL = 'http://localhost:8000/';

const Home = () => {

  const [products, setProducts] = useState([]);
  const [searchValue, setSearchValue] = useState('')
  

  useEffect(() => {
    fetch(BASE_URL + `product/`)
      .then(response => {
        const json = response.json()
        console.log(json);
        if (response.ok) {
          return json
        }
        throw response
      })
      .then(data => {
        const result = data.sort((a, b)=>{
          const time_a = a.timestamp.split(/[-T:]/);
          const time_b = b.timestamp.split(/[-T:]/);
          const date_a = new Date(Date.UTC(time_a[0], time_a[1]-1, time_a[2], time_a[3], time_a[4], time_a[5]));
          const date_b = new Date(Date.UTC(time_b[0], time_b[1]-1, time_b[2], time_b[3], time_b[4], time_b[5]));
          return date_b - date_a
        })
        return result
      })
      .then(data => {
        setProducts(data)
      })
      .catch(error => {
        console.log(error);
        alert(error)
      })
  }, [])

//   const searchBox = () => {
//       return (
//           <div>
//               <input
//                 className="search-box"
//                 type="search"
//                 placeholder='Search Product'
//                 onChange={(event) => {
//                     setSearchValue(event.target.value.toLocaleLowerCase())
//                 }}
//                 />
//             </div>
//       )
//   }


  return (
    <div className='app'>


      <div className="app_header">
        <img className="app_headerImage"
            src = "https://www.seekpng.com/png/detail/334-3345000_inventory-packaging-vector-logo.png"
            alt = "ProductInventory" />
      
        <div>
            {/* <searchBox /> */}
        </div>
      </div>
      <div className='app_product'>
          {
            products.map((product, index) => {
              return(
                <div key={index}>
                  <Product product={product} />
        
                </div>
              )
            })
          }
      </div>
      <CreateProduct />
      <CreateWarehouse />
    </div>
    
  )
};

export default Home;


