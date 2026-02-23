import { useState, useEffect } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function FeedbackForm() {

  const [drivers, setDrivers] = useState([])
  const [driverId, setDriverId] = useState("")
  const [text, setText] = useState("")
  const [toast, setToast] = useState("")
  const [toastType, setToastType] = useState("success")

  const navigate = useNavigate()

  useEffect(() => {
    axios.get("http://localhost:5000/public-drivers")
      .then(res => setDrivers(res.data))
      .catch(() => {
        setToast("Please login as admin first")
        setToastType("error")
      })
  }, [])

  const submit = async () => {

    if (!driverId || !text.trim()) {
      setToast("Select driver and enter feedback")
      setToastType("error")
      hideToast()
      return
    }

    try {
      await axios.post("http://localhost:5000/submit-feedback", {
        driver_id: driverId,
        text: text
      })

      setToast("Feedback submitted successfully!")
      setToastType("success")

      setTimeout(() => {
        navigate("/")
      }, 2000)

    } catch {
      setToast("Error submitting feedback")
      setToastType("error")
      hideToast()
    }
  }

  const hideToast = () => {
    setTimeout(() => {
      setToast("")
    }, 3000)
  }

  return (
    <>
      <select onChange={(e)=>setDriverId(e.target.value)}>
        <option value="">Select Driver</option>
        {drivers.map(d => (
          <option key={d.id} value={d.id}>{d.name}</option>
        ))}
      </select>

      <input
        placeholder="Write Feedback"
        value={text}
        onChange={(e)=>setText(e.target.value)}
      />

      <button onClick={submit}>Submit</button>

      {toast && (
        <div className={`toast ${toastType}`}>
          {toast}
        </div>
      )}
    </>
  )
}