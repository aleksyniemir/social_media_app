import { Children } from "react"
import { useLocation, Navigate} from "react-router-dom"

export const setToken = (token) => {
    console.log("Zapisujemy token w ciastkach")
    localStorage.setItem('token', token)
}

export const fetchToken = (token) => {
    console.log("Fetchujemy token z ciastek")
    return localStorage.getItem('token')
}

export function RequireToken({children}) {
    console.log("WCHODZIMY W REQUIRETOKEN")
    let auth = fetchToken()
    let location = useLocation()
    console.log("Autoryzacja rozpoczęta")
    console.log(auth + " auth")
    if (!auth) {
        return <Navigate to='/' state ={{from : location}}/>;
    }

    return children
    
}