//async thunk operation going on here... Test only

import { createSlice } from "@reduxjs/toolkit";

export const testThunkSlice = createSlice({
    name: "testThunkSlice",
    initialState: {
        value: []
    },
    reducers: {
        requestStarted: () => {
            return {message: "Fetch process initiated."}
        },
        requestNetworkFail: (state, action) => {
            return action.payload
        },
        requesttSucceeded: (state, action) => {
            state.value = action.payload
        }
    }
})

// //thunk action creators and thunk functions
// export function fetchAllUsers(){
//     return async (dispatch, getState) => {
//         dispatch(requestStarted())
//         try{
//             const users = await fetch('/users').then((r) => {
//                 if(r.ok) return r.json()
//             }).catch((err) => {throw new Error("Could not fetch users.")})
//             dispatch(requesttSucceeded(users))
//         }
//         catch (err) {
//             dispatch(requestNetworkFail(err))
//         }
//     }
// }

export const { requestStarted, requestNetworkFail, requesttSucceeded } = testThunkSlice.actions
export default testThunkSlice.reducer

