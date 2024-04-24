import { createSlice } from '@reduxjs/toolkit'
import { redirect } from 'react-router-dom'

export const loggedInUserSlice = createSlice({
    name: 'loggedInUser',
    initialState: {
        value: {},
        loginStatus: {
            isLoggedIn: false,
            toggle: "pending"
        }
    },
    reducers: {
        loginSucceeded: (state, action) => {
            state.value = action.payload
            state.loginStatus = {
                isLoggedIn: true,
                toggle: "succeeded"
            }
        },
        loginPending: (state) => {
            state.loginStatus = {
                isLoggedIn: false, 
                toggle: "pending"
            }
        },
        loginFailed: (state) => {
            state.loginStatus = {
                isLoggedIn: false,
                toggle: "failed"
            }
        },
        logoutSucceeded: (state) => {
            state.value = {}
            state.loginStatus = {
                isLoggedIn: false,
                toggle: "pending"
            }
        },
        logoutPending: () => {
            // return {message: "Logout status is pending"}
        },
        logoutFailed: () => {
            // return {message: "Network error. Could not logout"}
        }
    }
})

//thunk action creators and thunk functions
export function fetchUser(value){
    return async (dispatch, getState) => {
        dispatch(loginPending())
        await fetch('/login', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        }).then((r)=>{
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Error, could not find username or password in database")
            throw new Error("Network Error")
        }).then((r) => {
            dispatch(loginSucceeded(r))
            redirect("/")
        }).catch((err) => {
            dispatch(loginFailed())
            console.log(err)
        })
    }
}

export function logoutUser(){
    return async (dispatch, getState) => {
        dispatch(logoutPending())
        await fetch('/logout', {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((r)=>{
            if(r.ok)dispatch(logoutSucceeded())
            throw new Error("Network failure")
        })
        .catch((err) => {
            dispatch(logoutFailed())
        })
    }
}

export function checkSession(){
    return async (dispatch, getState) => {
        fetch("/checksession").then((r) => {
            if(r.ok){return r.json()}
            else if(r.status === 404) throw new Error("Error, could not find user data in session")
            throw new Error("Network Error")
        })
        .then((r) => dispatch(loginSucceeded(r)))
        .catch((err) => {
            console.log(err)
        })
    }
}

export const { loginPending, loginFailed, loginSucceeded, logoutSucceeded, logoutPending, logoutFailed } = loggedInUserSlice.actions
export default loggedInUserSlice.reducer