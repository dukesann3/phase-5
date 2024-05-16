import { createSlice } from '@reduxjs/toolkit'

export const friendSlice = createSlice({
    name: 'friend',
    initialState: {
        value: [],
        getFriendsErrorMessage: "",
        deleteFriendErrorMessage: ""
    },
    reducers: {
        //GET Friends==========================
        getFriendsSuccess: (state, action) => {
            state.value = action.payload
            state.getFriendsErrorMessage = ""
        },
        getFriendsPending: (state) => {
            state.getFriendsErrorMessage = ""
        },
        getFriendsFailure: (state, action) => {
            state.getFriendsErrorMessage = action.payload
        },
        //DELETE Friend========================
        deleteFriendSuccess: (state, action) => {
            //where action is the friendship id
            let currentState = state.value
            let newState = currentState.filter((friend) => {
                if(friend.id === action.payload){
                    return false
                }
                return true
            })
            state.value = newState
            state.deleteFriendErrorMessage = ""
        },
        deleteFriendPending: (state) => {
            state.deleteFriendErrorMessage = ""
        },
        deleteFriendFailure: (state, action) => {
            state.deleteFriendErrorMessage = action.payload
        }
    }
})

//GET FRIENDS=================================
export function getFriends(){
    return async (dispatch, getState) => {
        dispatch(getFriendsPending())

        await fetch("/user/friends")
        .then((r) => {
            if(r.ok) return r.json()
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(getFriendsSuccess(resp))
        })
        .catch((err) => {
            dispatch(getFriendsFailure(err.toString()))
        })
    }
}

//UNFRIEND====================================
export function unfriend(f_id){
    return async (dispatch, getState) => {
        dispatch(deleteFriendPending())

        await fetch(`/user/friends/${f_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((r) => {
            if(r.ok){
                dispatch(deleteFriendSuccess(f_id))
                return
            }
            else if(r.status === 404) throw new Error("Unfriend action cannot be completed")
            throw new Error("Network Error")
        })
        .catch((err) => {
            dispatch(deleteFriendFailure(err.toString()))
        })
    }
}



export const { 
    getFriendsSuccess, getFriendsPending, getFriendsFailure,
    deleteFriendSuccess, deleteFriendPending, deleteFriendFailure
} = friendSlice.actions
export default friendSlice.reducer