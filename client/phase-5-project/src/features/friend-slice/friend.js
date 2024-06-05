import { createSlice } from '@reduxjs/toolkit'
import { addUserToBankSuccess } from '../user-slice/userList'
import { postSuccess } from '../post-slice/allPosts'
import { postDeleteSuccess } from '../post-slice/allPosts'

export const friendSlice = createSlice({
    name: 'friend',
    initialState: {
        value: [],
        getFriendsErrorMessage: "",
        deleteFriendErrorMessage: "",
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
        },
        //CLEAR ALL FRIENDS
        clearAllFriends: (state) => {
            state.value = []
        }
    }
})

//GET FRIENDS=================================
export function getFriends(){
    console.log("getFriends")
    return async (dispatch, getState) => {
        const state = getState()
        dispatch(getFriendsPending())

        await fetch("/user/friends")
        .then((r) => {
            if(r.ok) return r.json()
            throw new Error("Network Error")
        })
        .then((fetchedFriendsList) => {
            let userBank = state.userList.userBank
            const newUsers = fetchedFriendsList.filter((fetchedFriend) => 
                !userBank.some(userInBank => userInBank.id === fetchedFriend.id)
            )
            let newUsersCopy = [...newUsers]
            
            if(newUsersCopy.length > 0){
                newUsersCopy.forEach((newUser) => {
                    dispatch(addUserToBankSuccess(newUser))
                    const userPost = [...newUser.posts]
                    userPost.forEach((post) => {
                        let copyPost = {...post}
                        copyPost.isFriendPost = newUser.status === "accepted" ? true : false
                        dispatch(postSuccess(copyPost))
                    })
                })
            }

            dispatch(getFriendsSuccess(fetchedFriendsList))
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(getFriendsFailure(error.toString()))
        })
    }
}

//UNFRIEND====================================
export function unfriend(f_id){
    console.log("unfriend")
    return async (dispatch, getState) => {
        dispatch(deleteFriendPending())
        const state = getState()
        const allPosts = state.allPost.value
        const friendPosts = allPosts.filter((post) => post.user_id == f_id)

        await fetch(`/user/friends/${f_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((r) => {
            if(r.ok){
                dispatch(deleteFriendSuccess(f_id))
                for(const post of friendPosts){
                    dispatch(postDeleteSuccess(post.id))
                }
                return
            }
            else if(r.status === 404) throw new Error("Unfriend action cannot be completed")
            throw new Error("Network Error")
        })
        .catch((error) => {
            console.log(error.toString())
            dispatch(deleteFriendFailure(error.toString()))
        })
    }
}


export const { 
    getFriendsSuccess, getFriendsPending, getFriendsFailure,
    deleteFriendSuccess, deleteFriendPending, deleteFriendFailure,
    clearAllFriends
} = friendSlice.actions
export default friendSlice.reducer