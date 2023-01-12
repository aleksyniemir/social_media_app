//import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'

import { Routes, Route } from "react-router-dom";
import Login from "./Login";
import Main from "./Main";

import { RequireToken } from './Auth';

function App() {

  return (
    <div className="App">
      <Routes>
       <Route path="/" element = {<Login/>}/>
       <Route 
        path="/main" 
        element = {
          <RequireToken>
            <Main/>
          </RequireToken>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
