import { createSlice } from '@reduxjs/toolkit'

export const allPostSlice = createSlice({
    name: 'allPosts',
    initialState: {
        value: []
    },
    reducers: {
        allPostsGetSuccessful: (state, action) => {
            console.log("successful retrieval")
            console.log(action.payload)
            state.value = action.payload
        },
        allPostsGetPending: () => {
            console.log("pending retrieval")
        },
        allPostsGetFailure: (state, action) => {
            console.log("retrieval failure")
        }
    }
})

export function fetchAllPosts(){
    return async (dispatch, getState) => {
        dispatch(allPostsGetPending())
        await fetch('/posts')
        .then((r)=>{
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Error, could not retrieve posts")
            throw new Error("Network Error")
        }).then((r) => {
            dispatch(allPostsGetSuccessful(r))
        }).catch((err) => {
            dispatch(allPostsGetFailure())
            console.log(err)
        })
    }
}

export const { allPostsGetSuccessful, allPostsGetPending, allPostsGetFailure } = allPostSlice.actions
export default allPostSlice.reducer
