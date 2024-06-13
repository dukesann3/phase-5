import { createSlice } from '@reduxjs/toolkit'
import { makeSentenceError } from '../../useful_functions'
import { postSuccess } from '../post-slice/allPosts'

export const userListSlice = createSlice({
    name: 'userList',
    initialState: {
        value: [], //value is the user list projected in the search results... very front-end heavy
        userBank: [], //userBank stores data fetched by search function... serves as information "bank"
        errorMessage: "",
        friendRequestErrorMessage: "",
        addUsersToBankErrorMessage: ""
    },
    reducers: {
        fetchSuccess: (state, action) => {
            state.value = action.payload
            state.errorMessage = ""
        },
        fetchPending: (state) => {
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
            const newState = currentState.map((user) => {
                if(action.payload.reciever_id === user.id){
                    user.isPending = true
                    return user
                }
                return user
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
        },
        //Add Stranger===========================
        addUserToBankSuccess: (state, action) => {
            const currentStrangerArray = state.userBank
            const newStrangerArray = [...currentStrangerArray, action.payload]
            
            state.userBank = newStrangerArray
            state.addUsersToBankErrorMessage = ""
        },
        addUserToBankFailure: (state, action) => {
            state.addUsersToBankErrorMessage = action.payload
        },
        addUserToBankPending: (state) => {
            state.addUsersToBankErrorMessage = ""
        },
        //CLEAR ALL USER VALUE AND BANK
        clearAllUsers: (state) => {
            state.value = []
            state.userBank = []
        }
    }
})

export function fetchUserList(searchQuery){
    console.log("fetchUserList")
    return async (dispatch, getState) => {
        const state = getState()
        dispatch(fetchPending())

        fetch(`/user/search`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchQuery)
        })
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(error => {
                throw new Error(makeSentenceError(error))
            })
        })
        .then((fetchedUserList) => {
            const userBank = state.userList.userBank
            const newUsers = fetchedUserList.filter((fetchedUser) => 
                !userBank.some(userInBank => userInBank.id === fetchedUser.id)
            )
            const newUsersCopy = {...newUsers}

            if(newUsersCopy.length > 0){
                newUsersCopy.forEach((newUser) => {
                    dispatch(addUserToBankSuccess(newUser))
                    const newUserPosts = newUser.posts
                    for(const post in newUserPosts){
                        const postWithAttr = {...post}
                        postWithAttr.isFriendPost = newUser.isFriend ? true : false
                        dispatch(postSuccess(postWithAttr))
                    }
                })
            }
            dispatch(fetchSuccess(fetchedUserList))
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(fetchFailure(error.toString()))
        })
    }
}

export function sendFriendRequest(value){
    console.log("sendFriendRequest")
    return async (dispatch, getState) => {
        dispatch(postFRequestPending())

        await fetch('/friendships/send_request', {
            method: "POST",
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
            dispatch(postFRequestSuccess(resp))
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(postFRequestFailure(error.toString()))
        })
    }
}

export function fetchSpecificUser(userId){
    console.log("fetchSpecificUser")
    return async (dispatch, getState) => {
        const state = getState()
        const userBank = state.userList.userBank
        const allPosts = state.allPost.value
        dispatch(addUserToBankPending())

        fetch(`/user/${userId}`)
        .then(async (r) => {
            if(r.ok) return r.json()
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        })
        .then((fetchedUser) => {
            const isExistingUserInBank = userBank.some(userInBank => userInBank.id == fetchedUser.id)
            const isPostInSlice = allPosts.some(userPost => userPost.user_id == fetchedUser.id) 

            if(!isExistingUserInBank){
                dispatch(addUserToBankSuccess(fetchedUser))
            }
            if(!isPostInSlice){
                let fetchedUserCopy = {...fetchedUser}
                fetchedUserCopy.posts.forEach((post) => {
                    let postCopy = {...post}
                    postCopy.isFriendPost = false
                    dispatch(postSuccess(postCopy))
                })
            }
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(addUserToBankFailure(error.toString()))
        })
    }
}

export const { 
    fetchSuccess, fetchPending, fetchFailure, 
    userLogout, unLoadErrorMsg,
    postFRequestSuccess, postFRequestPending, postFRequestFailure, noResults,
    addUserToBankSuccess, addUserToBankPending, addUserToBankFailure,
    clearAllUsers
 } = userListSlice.actions
export default userListSlice.reducer