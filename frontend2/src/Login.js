import { useNavigate } from "react-router-dom"
import { fetchToken, setToken } from "./Auth.js"
import {useState, useEffect} from 'react';
import axios from 'axios';

export default function Login() {
    const navigate = useNavigate();
    var [username, setUsername] = useState("");
    var [password, setPassword] = useState("");





    async function login()  {
        // do wyjebania
        setUsername("olekniemirka")
        setPassword("haslo123")
        // if ((username == "") & (password == "")) {
        //     return
        // }
        // else {
            const payload = {
                username: "olekniemirka",
                password: "haslo123"
            }
            // const payload = new FormData()
            // payload.append('username', username)
            // payload.append('password', password)
            console.log("Za chwile dane zostana wyslane na serwer")
            //console.log(payload.values())
            console.log("LECT AXIOS")
            const promise = await axios({
                method: 'post', 
                url: 'http://127.0.0.1:8000/users/token',
                data: payload,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
            })
            .then(response => {
                console.log(response);
                console.log(response.data);
            })
            .then(function (response) {
                console.log("AXIOS wszedł w .then")
                navigate("/main")
                        console.log(response.data.access_token +  " response.data.access_token");
                        //if (response.data) {
                            setToken(response.data);
                        //}
                    })
            .catch(error => {
                console.error(error)
            });
            console.log("KONIEC AXIOSU")
        //}
    }

    return  (
        <>
          <div style={{ minHeight: 800, marginTop: 30 }}>
            <h1>login page</h1>
            <div style={{ marginTop: 30 }}>
            {fetchToken() ? (
                <p>you are logged in</p>
            ) : (
                

                <div>
                  <form>
                    <label style={{ marginRight: 10 }}>Input Username</label>
                    <input
                      type="text"
                      onChange={(e) => setUsername(e.target.value)}
                    />
    
                    <label style={{ marginRight: 10 }}>Input Password</label>
                    <input
                      type="text"
                      onChange={(e) => setPassword(e.target.value)}
                      
                    />
    
                    <button onClick={login}>Login</button>
                  </form>
                </div>
                )}
            </div>
          </div>
        </>
      );
    }




    



//    

    
    //const axios = require('axios');

    // axios.get('http://127.0.0.1:8000/users/dupa')
    // .then(response => {
    //     console.log(response);
    // })
    
    // axios({
    //     method: 'get',
    //     url: 'http://127.0.0.1:8000/users/dupa',
    //     data: '',
    //     headers: {
    //         "Accept": "application/json",
    //         //'Content-Type': 'application/x-www-form-urlencoded'
    //     },
    // })
    // .then(response => {
    //     console.log(response);
    // })
    // .catch(error => {
    //     console.error(error);
    // });
        
    // const a=1






    // return (
    //     <>
    //       <div style={{ minHeight: 800, marginTop: 30 }}>
    //         <h1>login page</h1>
    //       </div>
    //     </>
    //   );



    // const test = () =>{ 
    //     axios
    //         .get("http://localhost:8000/users/dupa", {
    //         })
    //         .then(function (response) {
    //             console.log(response.data.token, "response.data.token");
    //             if (response.data.token) {
    //                 setToken(response.data.token);
    //                 navigate("/main")
    //             }
    //         })
    //         .catch(function (error) {
    //             console.log(error, "error");
    //         });
    // }  
    // username = "olekniemirka"
    // password = "haslo123"
    // const payload = new FormData()
    // payload.append('username', username)
    // payload.append('password', password)
    // console.log("Za chwile dane zostana wyslane na serwer")
    // let object = {};
    // payload.forEach(function(value, key){
    //     object[key] = value;
    // });
    // let json = JSON.stringify(object);
    // console.log(json)
    // console.log("LECT AXIOS")
    // axios({
    //     method: 'post', 
    //     url: 'http://127.0.0.1:8000/users/token',
    //     data: payload,
    //     headers: {
    //         'Accept': 'application/json',
    //         'Content-Type': 'application/x-www-form-urlencoded'
    //     },
    // })
    // .then(response => {
    //     console.log(response);
    // })
    // .then(function (response) {
    //             console.log(response.data.token, "response.data.token");
    //             if (response.data.token) {
    //                 setToken(response.data.token);
    //                 navigate("/main")
    //             }
    //         })
    // .catch(error => {
    //     console.error(error)
    // });













    
            //api call to backend
            // axios
            //     .post("http://localhost:8000/users/login", {
            //         username: username,
            //         password: password,
            //     })
            //     .then(function (response) {
            //         console.log(response.data.token, "response.data.token");
            //         if (response.data.token) {
            //             setToken(response.data.token);
            //             navigate("/main")
            //         }
            //     })
            //     .catch(function (error) {
            //         console.log(error, "error");
            //     });


            // axios.get('http://127.0.0.1:8000/users/dupa')
            // .then(response => {
            //     console.log(response);
            // })