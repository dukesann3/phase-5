import { createSlice } from '@reduxjs/toolkit'

export const userListSlice = createSlice({
    name: 'userList',
    initialState: {
        value: [],
        errorMessage: ""
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
        }
    }
})

//redux thunk here
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


export const { fetchSuccess, fetchPending, fetchFailure, userLogout, unLoadErrorMsg } = userListSlice.actions
export default userListSlice.reducer