import { createSlice } from '@reduxjs/toolkit'

export const userListSlice = createSlice({
    name: 'userList',
    initialState: {
        value: [],
        errorMessage: "",
        friendRequestErrorMessage: ""
    },
    reducers: {
        fetchSuccess: (state, action) => {
            console.log("success")
            state.value = action.payload
            state.errorMessage = ""
        },
        fetchPending: (state) => {
            console.log("User list fetch pending")
            state.errorMessage = ""
        },
        fetchFailure: (state, action) => {
            state.errorMessage = action.payload
        },
        userLogout: (state) => {
            state.value = []
            state.errorMessage = ""
        },
        unLoadErrorMsg: (state) => {
            state.errorMessage = ""
        },
        postFRequestSuccess: (state, action) => {
            //this is more of a patch, but it is what it is
            const currentState = state.value
            const newState = currentState.filter((user) => {
                if(action.payload.reciever_id === user.id){
                    return false
                }
                return true
            })
            state.value = newState
            state.friendRequestErrorMessage = ""
        },
        postFRequestPending: (state) => {
            state.friendRequestErrorMessage = ""
        },
        postFRequestFailure: (state, action) => {
            state.friendRequestErrorMessage = action.payload
        }
    }
})

export function fetchUserList(user_id){
    return async (dispatch, getState) => {
        fetch(`/users/${user_id}`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
            //need this for app.py to read cookies
            credentials: "same-origin"
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 401) throw new Error("Error, could not fetch users")
            throw new Error("Network Error")
        })
        .then((r) => {
            dispatch(fetchSuccess(r))
        })
        .catch((error) => {
            dispatch(fetchFailure(error.toString()))
        })
    }
}

export function sendFriendRequest(value){
    return async (dispatch, getState) => {
        dispatch(postFRequestPending())

        await fetch('/friendships/send_request', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Either the sender or reciever of the friend request does not exist")
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(postFRequestSuccess(resp))
        })
        .catch((err) => {
            dispatch(postFRequestFailure(err.toString()))
        })
    }
}


export const { 
    fetchSuccess, fetchPending, fetchFailure, 
    userLogout, unLoadErrorMsg,
    postFRequestSuccess, postFRequestPending, postFRequestFailure
 } = userListSlice.actions
export default userListSlice.reducer