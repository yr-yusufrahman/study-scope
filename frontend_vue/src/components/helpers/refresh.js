import axios from 'axios'


export default async function refresh() {
    const refresh_url = "http://127.0.0.1:8000/auth/refresh"
    const request_data = {
      refresh: localStorage.getItem('refresh')
    }
    
    try {
        const response = await axios.post(refresh_url, request_data)
        const data = await response.data
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('refresh', data.refresh_token)
        return true
    } catch (error) {
        console.log('Error: not authenticated.', error)
        localStorage.removeItem('token')
        localStorage.removeItem('refresh')
        return false
    }
}