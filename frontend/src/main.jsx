import {createRoot} from 'react-dom/client'
import {BrowserRouter} from 'react-router-dom'
import App from './App.jsx'
import './App.css'
import './index.css'
import axios from "axios"
axios.defaults.withCredentials = true
createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)
