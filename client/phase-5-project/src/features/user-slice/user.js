import { createSlice } from '@reduxjs/toolkit'
import { userLogout } from './userList'

export const userSlice = createSlice({
    name: 'loggedInUser',
    initialState: {
        value: {},
        loginStatus: {
            isLoggedIn: false,
            toggle: "pending"
        },
        notifications: []
    },
    reducers: {
        loginSucceeded: (state, action) => {
            state.value = action.payload
            state.loginStatus = {
                isLoggedIn: true,
                toggle: "succeeded"
            }

            const friendReqNotifications = action.payload.friend_request_notifications.map((frn) => {
                return {
                    type: "friend_request",
                    value: frn
                }
            })
            const postLikeNotifications = action.payload.post_like_notifications.map((pln) => {
                return {
                    type: "post_like",
                    value: pln
                }
            })
            const altogether = friendReqNotifications.concat(postLikeNotifications)
            const sortedArray = altogether.sort(updateDateComparison)
            state.notifications = sortedArray
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
        }).catch((err) => {
            dispatch(loginFailed())
            console.log(err)
        })
    }
}

export function logoutUser(){
    return async (dispatch, getState) => {
        dispatch(logoutPending())
        fetch('/logout', {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r)=>{
            if(r.ok) return
            throw new Error("Network failure")
        })
        .then(() => {
            dispatch(logoutSucceeded())
            dispatch(userLogout())
        })
        .catch((err) => {
            console.log(err)
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

function updateDateComparison(a, b){
    if(a.updated_at < b.updated_at){
        return -1
    }
    if(a.updated_at > b.updated_at){
        return 1
    }
    return 0
}

export const { 
    loginPending, loginFailed, loginSucceeded, 
    logoutSucceeded, logoutPending, logoutFailed } = userSlice.actions
export default userSlice.reducer