import io from 'socket.io-client'

//http://192.168.2.29:5000
//http://192.168.2.102:5000
//http://localhost:5000

const socket = io(import.meta.env.VITE_APP_URL)

export { socket }