import { createSlice } from '@reduxjs/toolkit'

export const userListSlice = createSlice({
    name: 'userList',
    initialState: {
        value: [],
    },
    reducers: {
        fetchSuccess: (state, action) => {
            console.log("success")
            state.value = action.payload
        }
    }
})

//redux thunk here
export function fetchUserList(){
    return async (dispatch, getState) => {
        fetch("/users", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
            //need this for app.py to read cookies
            credentials: "same-origin"
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Could not fetch users")
            throw new Error("Network Error")
        })
        .then((r) => {
            dispatch(fetchSuccess(r))
            console.log(r)
        })
        .catch((error) => console.log(error))
    }
}


export const { fetchSuccess } = userListSlice.actions
export default userListSlice.reducer