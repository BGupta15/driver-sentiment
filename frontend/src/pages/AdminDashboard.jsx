import { useEffect, useState } from "react"
import axios from "axios"
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts"
import { useNavigate } from "react-router-dom"

export default function AdminDashboard() {

  const [drivers, setDrivers] = useState([])
  const [ranking, setRanking] = useState([])
  const [selectedDriver, setSelectedDriver] = useState("")
  const [summary, setSummary] = useState({})
  const [historyData, setHistoryData] = useState([])
  const [driverName, setDriverName] = useState("")
  const [toast, setToast] = useState("")
  const [toastType, setToastType] = useState("success")
  const [alerts, setAlerts] = useState([])

  const navigate = useNavigate()

  const loadDrivers = async () => {
    try {
      const res = await axios.get("http://localhost:5000/drivers")
      setDrivers(res.data)
    } catch {
      navigate("/admin")
    }
  }

  const loadRanking = async () => {
    try {
      const res = await axios.get("http://localhost:5000/driver-ranking")
      setRanking(res.data)
    } catch {
    }
  }

  useEffect(() => {
    loadDrivers()
    loadRanking()
  }, [])

  useEffect(() => {
    const interval = setInterval(async () => {
        try {
        await loadDrivers()
        await loadRanking()

        const alertRes = await axios.get("http://localhost:5000/low-score-alerts")
        setAlerts(alertRes.data)

        } catch {}
    }, 4000) // every 4 seconds

    return () => clearInterval(interval)

    }, [])
  useEffect(() => {
    if (selectedDriver) {
      axios.get(`http://localhost:5000/driver-summary/${selectedDriver}`)
        .then(res => setSummary(res.data))

      axios.get(`http://localhost:5000/driver-history/${selectedDriver}`)
        .then(res => setHistoryData(res.data))
    }
  }, [selectedDriver])

  useEffect(() => {
    const interval = setInterval(async () => {
        try {
        const res = await axios.get("http://localhost:5000/low-score-alerts")
        setAlerts(res.data)
        } catch {}
    }, 4000)

    return () => clearInterval(interval)
    }, [])
  const addDriver = async () => {
    try {
      await axios.post("http://localhost:5000/add-driver", {
        name: driverName
      })
      setToast("Driver added!")
      setToastType("success")
      setDriverName("")
      loadDrivers()
      loadRanking()
    } catch (err) {
      setToast(err.response?.data?.error || "Error")
      setToastType("error")
    }
    hideToast()
  }

  const deleteDriver = async (id) => {
    await axios.delete(`http://localhost:5000/delete-driver/${id}`)
    setToast("Driver deleted")
    setToastType("success")
    loadDrivers()
    loadRanking()
    hideToast()
  }

  const logout = async () => {
    await axios.post("http://localhost:5000/logout")
    navigate("/")
  }

  const hideToast = () => {
    setTimeout(() => setToast(""), 3000)
  }

  return (
    <div className="dashboard">
      {alerts.length > 0 && (
        <div className="alert-container fade-in">
            ⚠ Low Performance Alert
            {alerts.map((a, i) => (
            <div key={i}>
                {a.name} — Score: {a.average_score.toFixed(2)}
            </div>
            ))}
        </div>
        )}
      <h2 className="fade-in">Admin Dashboard</h2>

      <button onClick={logout}>Logout</button>

      {/* Add Driver */}
      <div className="fade-in">
        <input
          placeholder="Driver Name"
          value={driverName}
          onChange={(e)=>setDriverName(e.target.value)}
        />
        <button onClick={addDriver}>Add Driver</button>
      </div>

      {/* Ranking Table */}
      <h3 className="fade-in">Driver Ranking</h3>
      <table className="fade-in">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Avg Score</th>
            <th>Feedback</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
        {ranking.map((d, index) => {

            const medal =
            index === 0 ? "🥇" :
            index === 1 ? "🥈" :
            index === 2 ? "🥉" :
            ""

            return (
            <tr key={d.id}>
                <td>{medal || index + 1}</td>
                <td>{d.name}</td>
                <td>{d.average_score?.toFixed(2)}</td>
                <td>{d.total_feedbacks}</td>
                <td>
                <button onClick={()=>deleteDriver(d.id)}>Delete</button>
                </td>
            </tr>
            )
        })}
        </tbody>
      </table>

      {/* Driver Selection */}
      <select
        value={selectedDriver}
        onChange={(e)=>setSelectedDriver(e.target.value)}
      >
        <option value="">Select Driver</option>
        {drivers.map(d => (
          <option key={d.id} value={d.id}>{d.name}</option>
        ))}
      </select>

      {selectedDriver && (
        <>
          <LineChart width={700} height={350} data={historyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="created_at" />
            <YAxis domain={[0,5]} />
            <Tooltip />
            <Line type="monotone" dataKey="sentiment_score" stroke="#3498db" />
          </LineChart>

          <div className="cards">
            <div className="card">
              <h3>Average Score</h3>
              <p>{summary.average_score?.toFixed(2)}</p>
            </div>
            <div className="card">
              <h3>Total Feedback</h3>
              <p>{summary.total_feedbacks}</p>
            </div>
          </div>
        </>
      )}

      {toast && <div className={`toast ${toastType}`}>{toast}</div>}
    </div>
  )
}