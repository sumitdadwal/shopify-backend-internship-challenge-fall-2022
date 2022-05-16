import { Button, makeStyles, Modal } from "@mui/material";
import { useState, useEffect } from 'react';
import Product from './Product.component';
import CreateProduct from './CreateProduct.component';
import {  BrowserRouter, Routes, Route } from "react-router-dom"
import updateProduct from './UpdateProducts.component';
import Home from './Home.component';


const BASE_URL = 'http://localhost:8000/';

const App = () => {
      return (
        <div>
          <div>
            <Home />
          </div>
        
      </div>
    
  )
};

export default App;


