import { createSlice, current } from '@reduxjs/toolkit'

export const postSlice = createSlice({
    name: 'allPosts',
    initialState: {
        value: [],
        getErrorMessage: "",
        postErrorMessage: "",
        patchErrorMessage: "",
        deleteErrorMessage: "",

        postCommentErrorMessage: "",
        patchCommentErrorMessage: "",
        deleteCommentErrorMessage: "",

        postPostLikeErrorMessage: "",
        deletePostLikeErrorMessage: "",

        postCommentLikeErrorMessage: "",
        deleteCommentLikeErrorMessage: ""
    },
    reducers: {
        //GET REQUEST==========================

        postGetSuccessful: (state, action) => {
            state.value = action.payload
            state.getErrorMessage = ""
        },
        postGetPending: (state) => {
            state.getErrorMessage = ""
        },
        postGetFailure: (state, action) => {
            state.getErrorMessage = action.payload
        },
        //POST REQUEST==========================

        postSuccess: (state, action) => {
            const currentValue = state.value
            const updatedValue = currentValue.push(action.payload)
            const sortedUpdatedValue = updatedValue.sort(updatedAtComparator)

            state.value = sortedUpdatedValue
            state.postErrorMessage = ""
        },
        postPending: (state) => {
            state.postErrorMessage = ""
        },
        postFailure: (state, action) => {
            state.postErrorMessage = action.payload
        },
        //PATCH REQUEST=========================

        postPatchSuccess: (state, action) => {
            const currentState = state.value
            const edittedPost = action.payload

            const newState = currentState.map((post) => {
                if(post.id == edittedPost.id) return edittedPost
                return post
            })

            state.value = newState
            state.patchErrorMessage = ""
        },
        postPatchPending: (state) => {
            state.patchErrorMessage = ""
        },
        postPatchFailure: (state, action) => {
            state.patchErrorMessage = action.payload
        },
        //DELETE REQUEST=========================

        postDeleteSuccess: (state, action) => {
            const currentState = state.value

            const newState = currentState.filter((post) => {
                if(post.id !== action.payload){
                    return post
                }
            })
            state.value = newState
            state.deleteErrorMessage = ""
        },
        postDeletePending: (state) => {
            state.deleteErrorMessage = ""
        },
        postDeleteFailure: (state, action) => {
            state.deleteErrorMessage = action.payload
        },

        //POST REQUEST COMMENT=====================
        commentPostSuccess: (state, action) => {
            //the comment response will include post_id. Find the post and 
            //append its comments based on the post_id.
            const stateToBeChanged = state.value
            const post_id = action.payload.post_id

            for(let i = 0; i < stateToBeChanged.length; i++){
                if(stateToBeChanged[i].id === post_id){
                    stateToBeChanged[i].comments.push(action.payload)
                }
            }

            state.value = stateToBeChanged
            state.postCommentErrorMessage = ""
        },
        commentPostPending: (state) => {
            state.postCommentErrorMessage = ""
        },
        commentPostFailure: (state, action) => {
            state.postCommentErrorMessage = action.payload
        },

        //PATCH REQUEST COMMENT=====================
        commentPatchSuccess: (state, action) => {
            const stateToBeChanged = state.value
            const comment_id = action.payload.id

            for(const post of stateToBeChanged){
                for(let i = 0; i < post.comments.length; i++){
                    if(post.comments[i].id === comment_id){
                        post.comments[i] = action.payload
                    }
                }
            }

            state.value = stateToBeChanged
            state.patchCommentErrorMessage = ""
        },
        commentPatchPending: (state) => {
            state.patchCommentErrorMessage = ""
        },
        commentPatchFailure: (state, action) => {
            state.patchCommentErrorMessage = action.payload
        },

        //DELETE REQUEST COMMENT======================
        commentDeleteSuccess: (state, action) => {
            //action.payload for this method is just the commend_id
            const stateToBeChanged = state.value
            const comment_id = action.payload

            for(const post of stateToBeChanged){
                for(let i = 0; i < post.comments.length; i++){
                    if(post.comments[i].id === comment_id){
                        post.comments.shift(i,1)
                    }
                }
            }

            state.value = stateToBeChanged
            state.deleteCommentErrorMessage = ""
        },
        commentDeletePending: (state) => {
            state.deleteCommentErrorMessage = ""
        },
        commentDeleteFailure: (state, action) => {
            state.deleteCommentErrorMessage = action.payload
        },

        //POST REQUEST POSTLIKE=========================
        postLikePostSuccess: (state, action) => {
            const newState = state.value
            for(let i = 0; i < newState.length; i++){
                if(newState[i].id === action.payload.post_id){
                    newState[i].post_likes.push(action.payload)
                }
            }
            state.value = newState
            state.postPostLikeErrorMessage = ""
        },
        postLikePostPending: (state) => {
            state.postPostLikeErrorMessage = ""
        },
        postLikePostFailure: (state, action) => {
            state.postPostLikeErrorMessage = action.payload
            console.log(action.payload)
        },

        //DELETE REQUEST POSTLIKE=======================
        postLikeDeleteSuccess: (state, action) => {
            //again, action.payload for this one is the post_like_id
            const stateToBeChanged = state.value

            for(const post of stateToBeChanged){
                for(let i = 0; i < post.post_likes.length; i++){
                    if(post.post_likes[i].id === action.payload){
                        console.log(action.payload)
                        post.post_likes.shift(i,1)
                    }
                }
            }

            state.value = stateToBeChanged
            state.deletePostLikeErrorMessage = ""
        },
        postLikeDeletePending: (state) => {
            state.deletePostLikeErrorMessage = ""
        },
        postLikeDeleteFailure: (state, action) => {
            state.deletePostLikeErrorMessage = action.payload
        },

        //POST REQUEST COMMENTLIKE=======================
        commentLikePostSuccess: (state, action) => {
            const newState = state.value

            for(const post of newState){
                for(const comment of post.comments){
                    if(comment.id === action.payload.comment_id){
                        comment.comment_likes.push(action.payload)
                    }
                }
            }

            state.value = newState
            state.postCommentLikeErrorMessage = ""
        },
        commentLikePostPending: (state) => {
            state.postCommentLikeErrorMessage = ""
        },
        commentLikePostFailure: (state, action) => {
            state.postCommentLikeErrorMessage = action.payload
        },

        //DELETE REQUEST COMMENTLIKE======================
        commentLikeDeleteSuccess: (state, action) => {
            //again, action.payload for this one is the comment_like_id
            const newState = state.value
            
            for(const post of newState){
                for(const comment of post.comments){
                    for(let i = 0; i < comment.comment_likes.length; i++){
                        if(comment.comment_likes[i].id === action.payload){
                            comment.comment_likes.shift(i,1)
                        }
                    }
                }
            }

            state.value = newState
            state.deleteCommentLikeErrorMessage = ""
        },
        commentLikeDeletePending: (state) => {
            state.deleteCommentLikeErrorMessage = ""
        },
        commentLikeDeleteFailure: (state, action) => {
            state.deleteCommentLikeErrorMessage = action.payload
        }
    }

})

//GET REQUEST==================================================

export function getPosts(){
    return async (dispatch, getState) => {
        dispatch(postGetPending())

        await fetch('/posts')
        .then((r)=>{
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(postGetSuccessful(resp))
        })
        .catch((error) => {
            dispatch(postGetFailure(error.toString()))
        })
    }
}


//POST REQUEST==================================================
export function postPost(value){
    return async (dispatch, getState) => {
        dispatch(postPending())

        await fetch('/posts', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(postPost(resp))
        })
        .catch((error) => {
            dispatch(postFailure(error.toString()))
        })
    }
}

//PATCH REQUEST===================================================
export function patchPost(value, p_id){
    return async (dispatch, getState) => {
        dispatch(postPatchPending())
        console.log(value, p_id)
        await fetch(`/post/${p_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(postPatchSuccess(resp))
        })
        .catch((error) => {
            dispatch(postPatchFailure(error.toString()))
        })
    }
}

//DELETE REQUEST===================================================
export function deletePost(p_id){
    return async (dispatch, getState) => {
        dispatch(postDeletePending())

        await fetch(`/post/${p_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(postDeleteSuccess(p_id))
                return
            }
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .catch((error) => {
            dispatch(postDeleteFailure(error.toString()))
        })
    }
}

//POST COMMENT REQUEST============================================
export function postComment(value){
    return async(dispatch, getState) => {
        dispatch(commentPostPending())

        await fetch('/comment', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(commentPostSuccess(resp))
        })
        .catch((error) => {
            dispatch(commentPostFailure(error.toString()))
        })
    }
}

//PATCH COMMENT REQUEST===========================================
export function patchComment(value, c_id){
    return async(dispatch, getState) => {
        dispatch(commentPatchPending())

        await fetch(`/comment/${c_id}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(commentPatchSuccess(resp, c_id))
        })
        .catch((error) => {
            dispatch(commentPatchFailure(error.toString()))
        })
    }
}

//DELETE COMMENT REQUEST========================================
export function deleteComment(c_id){
    return async(dispatch, getState) => {
        dispatch(commentDeletePending())

        await fetch(`/comment/${c_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(commentDeleteSuccess(c_id))
                return
            }
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .catch((error) => {
            dispatch(commentDeleteFailure(error.toString()))
        })
    }
}

//POST POSTLIKE REQUEST=========================================
export function postPostLike(value){
    return async(dispatch, getState) => {
        dispatch(postLikePostPending())

        await fetch('/post/like',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(postLikePostSuccess(resp))
        })
        .catch((error) => {
            dispatch(postLikePostFailure(error.toString()))
        })
    }
}

//DELETE POSTLIKE REQUEST========================================
export function deletePostLike(post_like_id){
    return async(dispatch, getState) => {
        dispatch(postLikeDeletePending())
        await fetch(`/post/like/${post_like_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(postLikeDeleteSuccess(post_like_id))
                return
            }
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .catch((error) => {
            dispatch(postLikeDeleteFailure(error.toString()))
        })
    }
}

//POST COMMENTLIKE REQUEST======================================
export function postCommentLike(value){
    return async(dispatch, getState) => {
        dispatch(commentLikePostPending())

        await fetch('/comment/like', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .then((resp) => {
            dispatch(commentLikePostSuccess(resp))
        })
        .catch((error) => {
            dispatch(commentLikePostFailure(error.toString()))
        })
    }
}

//DELETE COMMENTLIKE REQUEST====================================
export function deleteCommentLike(comment_like_id){
    return async(dispatch, getState) => {
        dispatch(commentLikeDeletePending())

        fetch(`/comment/like/${comment_like_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok){
                dispatch(commentLikeDeleteSuccess(comment_like_id))
                return
            }
            else if(r.status === 404) throw new Error(r.json())
            throw new Error("Network Error")
        })
        .catch((error) => {
            dispatch(commentLikeDeleteFailure(error.toString()))
        })
    }   
}

function updatedAtComparator(a,b){
    if(a.updated_at < b.updated_at) return -1
    else if(a.updated_at > b.updated_at) return 1
    return 0
}

export const { 
    postGetSuccessful, postGetPending, postGetFailure, 
    postSuccess, postFailure, postPending,
    postPatchSuccess, postPatchFailure, postPatchPending,
    postDeleteSuccess, postDeleteFailure, postDeletePending,
    commentPostSuccess, commentPostFailure, commentPostPending,
    commentPatchSuccess, commentPatchFailure, commentPatchPending,
    commentDeleteSuccess, commentDeleteFailure, commentDeletePending,
    postLikePostSuccess, postLikePostFailure, postLikePostPending,
    postLikeDeleteSuccess, postLikeDeleteFailure, postLikeDeletePending,
    commentLikePostSuccess, commentLikePostFailure, commentLikePostPending,
    commentLikeDeleteSuccess, commentLikeDeleteFailure, commentLikeDeletePending
} = postSlice.actions

export default postSlice.reducer
