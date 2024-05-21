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
            console.log(action.payload)
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
            const newState = currentState.map((user) => {
                if(action.payload.reciever_id === user.id){
                    user.isPending = true
                    return
                }
                return
            })
            state.value = newState
            state.friendRequestErrorMessage = ""
        },
        postFRequestPending: (state) => {
            state.friendRequestErrorMessage = ""
        },
        postFRequestFailure: (state, action) => {
            state.friendRequestErrorMessage = action.payload
        },
        //no results from userlist
        noResults: (state) => {
            state.value = []
        }
    }
})

export function fetchUserList(searchQuery){
    return async (dispatch, getState) => {
        fetch(`/user/search`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchQuery)
        })
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(err => {
                if(r.status === 401 || r.status === 402){
                    dispatch(noResults())
                }
                throw new Error(err.error)
            })
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
    postFRequestSuccess, postFRequestPending, postFRequestFailure, noResults
 } = userListSlice.actions
export default userListSlice.reducer