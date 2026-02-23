import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function AdminLogin(){

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [toast, setToast] = useState("")
  const navigate = useNavigate()

  const login = async () => {
    try {
      await axios.post("http://localhost:5000/admin-login", {
        username,
        password
      })

      navigate("/admin/dashboard")

    } catch {
      setToast("Invalid Credentials")
      setTimeout(() => setToast(""), 3000)
    }
  }

  return (
    <div className="login-container">
      <h2>Admin Login</h2>

      <input
        placeholder="Username"
        onChange={(e)=>setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={login}>Login</button>

      {toast && (
        <div className="toast error">
          {toast}
        </div>
      )}
    </div>
  )
}