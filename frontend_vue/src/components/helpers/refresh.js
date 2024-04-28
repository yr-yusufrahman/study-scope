import axios from 'axios'


export default function refresh(router) {
    const refresh_url = "http://127.0.0.1:8000/auth/refresh"
    const request_data = {
      refresh: localStorage.getItem('refresh')
    }
    
    axios.post(refresh_url, request_data)
    .then(response => {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('refresh', response.data.refresh_token)
        router.push('/courses')
    }).catch(error => {
        console.log('Error: not authenticated.', error)
        localStorage.removeItem('token')
        localStorage.removeItem('refresh')
        router.push('/login')
    })
}