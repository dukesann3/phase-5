import { createSlice, current } from '@reduxjs/toolkit'
import { userLogout } from './userList'
import { createSelector } from 'reselect'
import { makeSentenceError } from '../../useful_functions'
import { getPosts } from '../post-slice/allPosts'
import { clearAllPosts } from '../post-slice/allPosts'
import { clearAllUsers } from './userList'
import { clearAllFriends } from '../friend-slice/friend'

//specify deleted notification id in CRUD operation please
export const noteTypeToURLMapper = [
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
        },
    }   
})

export function logoutUser(){
    console.log("logout")
    return async (dispatch, getState) => {
        dispatch(logoutPending())
        fetch('/logout', {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(async (r)=>{
            if(r.ok) {
                dispatch(logoutSucceeded())
                dispatch(userLogout())
                dispatch(clearAllPosts())
                dispatch(clearAllUsers())
                dispatch(clearAllFriends())
            }
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .catch((error) => {
            dispatch(logoutFailed(error.toString()))
        })
    }
}

export function checkSession(){
    console.log("checksession")
    return async (dispatch, getState) => {
        fetch("/checksession")
        .then(async (r) => {
            if(r.ok){return r.json()}
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .then((r) => dispatch(loginSucceeded(r)))
        .catch((error) => {
            console.log(error.toString())
        })
    }
}

export function deleteNotification(deleteInfo){
    console.log("deleteNotification")
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
        .then(async (r) => {
            if(r.ok){
                dispatch(deleteNotificationSucceeded(deleteInfo))
                return
            }
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(deleteNotificationFailure(error.toString()))
        })
    }
}

export function respondToFriendRequest(friendship_id, response){
    console.log("respondToFriendRequest")
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
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .then((r) => {
            console.log(r)
            dispatch(patchFriendRequestSuccess(friendship_id))
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(patchFriendRequestFailure(error.toString()))
        })
    }
}

export function respondToFriendRequestAndGetPost(friendship_id, response){
    return async (dispatch, getState) => {
        await dispatch(respondToFriendRequest(friendship_id, response))
        await dispatch(getPosts())
    }
}

export function patchUser(user_id, value){
    console.log("patchUser")
    return async (dispatch, getState) => {
        dispatch(patchUserPending())

        await fetch(`/users/${user_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .then((resp) => {
            dispatch(patchUserSuccess(resp))
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(patchUserFailure(error.toString()))
        })
    }
}

export function deleteUser(user_id){
    console.log("deleteUser")
    return async (dispatch, getState) => {
        dispatch(deleteUserPending())

        await fetch(`/users/${user_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(async (r) => {
            if(r.ok){
                dispatch(deleteUserSuccess())
                dispatch(logoutSucceeded())
                dispatch(userLogout())
                dispatch(clearAllPosts())
                dispatch(clearAllUsers())
                dispatch(clearAllFriends())
                return
            }
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(deleteUserFailure(error.toString()))
        })
    }
}

export function patchUserPwd(user_id, new_password){
    console.log("patchUserPassword")
    return async (dispatch, getState) => {
        dispatch(patchUserPwdPending())

        fetch(`/users/password/${user_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({password: new_password})
        })
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .then((r) => {
            dispatch(patchUserPwdSuccess())
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(patchUserPwdFailure(error.toString()))
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