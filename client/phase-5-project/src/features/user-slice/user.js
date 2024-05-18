import { createSlice, current } from '@reduxjs/toolkit'
import { userLogout } from './userList'
import { createSelector } from 'reselect'
import { ReactReduxContext } from 'react-redux'

//specify deleted notification id in CRUD operation please
const noteTypeToURLMapper = [
    {
        type: "comment_like_notifications",
        deleteURL: "/comment/like/notification/"
    },
    {
        type: "comment_notifications",
        deleteURL: "/comment/notification/"
    },
    {
        type: "post_like_notifications",
        deleteURL: "/post/like/notification/"
    }
]

export const userSlice = createSlice({
    name: 'loggedInUser',
    initialState: {
        value: {},
        loginStatus: {
            isLoggedIn: false,
            toggle: "pending"
        },
        loginErrorMessage: "",
        logoutErrorMessage: "",
        deleteNotificationMessage: "",
        friendRequestResponseMessage: "",
        patchUserErrorMessage: "",
        deleteUserErrorMessage: "",
        patchUserPwdErrorMessage: ""
    },
    reducers: {
        //LOGIN==============================================
        loginSucceeded: (state, action) => {
            state.value = action.payload
            state.loginStatus = {
                isLoggedIn: true,
                toggle: "succeeded"
            }

            state.loginErrorMessage = ""
        },
        loginPending: (state) => {
            state.loginStatus = {
                isLoggedIn: false, 
                toggle: "pending"
            }

            state.loginErrorMessage = ""
        },
        loginFailed: (state, action) => {
            state.loginStatus = {
                isLoggedIn: false,
                toggle: "failed"
            }

            state.notifications = []
            state.loginErrorMessage = action.payload
        },
        //LOGOUT=========================================================
        logoutSucceeded: (state) => {
            state.value = {}
            state.loginStatus = {
                isLoggedIn: false,
                toggle: "pending"
            }
            state.notifications = []
            state.logoutErrorMessage = ""
        },
        logoutPending: (state) => {
            state.logoutErrorMessage = ""
        },
        logoutFailed: (state, action) => {
            state.logoutErrorMessage = action.payload
        },
        //DELETE POST LIKE NOTIFICATION MESSAGE===========================
        deleteNotificationSucceeded: (state, action) => {
            //action.payload should be the PostLikeNotification.id
            let newState = state.value
            const type = action.payload.type
            const id = action.payload.id

            for(const property in newState){
                if(property.includes("notifications")){
                    for(let i = 0; i < newState[property].length; i++){
                        if(newState[property][i].id === id && property === type){
                            newState[property].splice(i,1)
                        }
                    }
                }
            }

            state.value = newState
            state.deleteNotificationMessage = ""
        },
        deleteNotificationPending: (state) => {
            state.deleteNotificationMessage = ""
        },
        deleteNotificationFailure: (state, action) => {
            state.deleteNotificationMessage = action.payload
        },
        //RESPOND TO FRIEND REQUEST=======================================
        patchFriendRequestSuccess: (state, action) => {
            //removes friend request notification once PATCH request goes through
            //action.payload should come out to be friendship id of the notification that I am deleting
            let newState = state.value
            for(let i = 0; newState.friend_request_notifications.length; i++){
                const notification = newState.friend_request_notifications[i]
                if(notification.friendship_id === action.payload){
                    newState.friend_request_notifications.splice(i,1)
                }
            }

            state.value = newState
            state.friendRequestResponseMessage = ""
        },
        patchFriendRequestPending: (state) => {
            state.friendRequestResponseMessage = ""
        },
        patchFriendRequestFailure: (state, action) => {
            state.friendRequestResponseMessage = action.payload
        },
        //USER PATCH=======================================================
        patchUserSuccess: (state, action) => {
            //let action be the user object returned from the HTTP response
            state.value = action.payload
            state.patchUserErrorMessage = ""
        },
        patchUserPending: (state) => {
            state.patchUserErrorMessage = ""
        },
        patchUserFailure: (state, action) => {
            state.patchUserErrorMessage = action.payload
        },
        //USER DELETE========================================================
        deleteUserSuccess: (state) => {
            state.value = {}
            state.deleteUser = ""
        },
        deleteUserPending: (state) => {
            state.deleteUserErrorMessage = ""
        },
        deleteUserFailure: (state, action) => {
            state.deleteUserErrorMessage = action.payload
        },
        //EDIT USER PASSWORD==================================================
        patchUserPwdSuccess: (state) => {
            state.patchUserPwdErrorMessage = ""
        },
        patchUserPwdPending: (state) => {
            state.patchUserPwdErrorMessage = ""
        },
        patchUserPwdFailure: (state, action) => {
            state.patchUserErrorMessage = action.payload
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

export function deleteNotification(deleteInfo){
    return async (dispatch, getState) => {
        dispatch(deleteNotificationPending())
        const {type, id} = deleteInfo
        const mappedNoteType = noteTypeToURLMapper.filter((mapper) => mapper.type === type)
        const deleteURL = mappedNoteType[0].deleteURL + `${id}`

        await fetch(deleteURL, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(deleteNotificationSucceeded(deleteInfo))
                return
            }
            else if(r.status === 404) throw new Error("Error, notification could not be deleted")
            throw new Error("Network Error")
        })
        .catch((err) => {
            dispatch(deleteNotificationFailure(err.toString()))
        })
    }
}

export function respondToFriendRequest(friendship_id, response){
    return async (dispatch, getState) => {
        dispatch(patchFriendRequestPending())

        await fetch('/friendships/send_request', {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                friend_request_response: response,
                friend_request_id: friendship_id
            })
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 400) throw new Error("Could not send friend request")
            throw new Error("Network Error")
        })
        .then((r) => {
            dispatch(patchFriendRequestSuccess(friendship_id))
        })
        .catch((err) => {
            dispatch(patchFriendRequestFailure(err.toString()))
        })
    }
}

export function patchUser(user_id, value){
    return async (dispatch, getState) => {
        dispatch(patchUserPending())

        await fetch(`/users/${user_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Could not edit user")
            throw new Error("Network Error")
        })
        .then((resp) => {
            console.log(resp)
            dispatch(patchUserSuccess(resp))
        })
        .catch((err) => {
            dispatch(patchUserFailure(err.toString()))
        })
    }
}

export function deleteUser(user_id){
    return async (dispatch, getState) => {
        dispatch(deleteUserPending())

        await fetch(`/users/${user_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(deleteUserSuccess())
                //see if I have to add anything at the end
                return
            }
            else if(r.status === 404) throw new Error("Unable to delete user")
            throw new Error("Network Error")
        })
        .catch((err) => {
            dispatch(deleteUserFailure(err.toString()))
        })
    }
}

export function patchUserPwd(user_id, new_password){
    return async (dispatch, getState) => {
        dispatch(patchUserPwdPending())

        fetch(`/users/password/${user_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({password: new_password})
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Password could not be changed")
            throw new Error("Network Error")
        })
        .then((r) => {
            dispatch(patchUserPwdSuccess())
        })
        .catch((err) => {
            dispatch(patchUserPwdFailure(err.toString()))
        })
    }
}

export const notificationSelector = createSelector(
    state => state.user,
    (user) => {
        let currentState = user.value
        let notifications = []

        for(const property in currentState){
            if(property.includes("notifications")){
                for(let i = 0; i < currentState[property].length; i++){
                    notifications.push({
                        type: property,
                        value: currentState[property][i]
                    })
                }
            }
        }

        return notifications
    }
)

export const { 
    loginPending, loginFailed, loginSucceeded, 
    logoutSucceeded, logoutPending, logoutFailed,
    deleteNotificationSucceeded, deleteNotificationPending, deleteNotificationFailure,
    patchFriendRequestSuccess, patchFriendRequestPending, patchFriendRequestFailure,
    patchUserSuccess, patchUserPending, patchUserFailure,
    deleteUserSuccess, deleteUserPending, deleteUserFailure,
    patchUserPwdSuccess, patchUserPwdPending, patchUserPwdFailure
} = userSlice.actions
export default userSlice.reducer