import { useDispatch, useSelector } from "react-redux"
import { useFormik } from "formik"
import { patchComment, deleteComment, postCommentLike, deleteCommentLike } from "../../features/post-slice/allPosts"
import { useState } from "react"

export default function CommentBlock({comment}){

    const [editMode, setEditMode] = useState(false)
    const {text, created_at, updated_at, user_id, id, comment_likes} = comment

    const enterEditMode = () => setEditMode(true)
    const exitEditMode = () => setEditMode(false)

    const userInfo = useSelector((store) => store.user.value)
    const dispatch = useDispatch()
    
    const formik = useFormik({
        initialValues: {
            text: ""
        },
        onSubmit: (value) => patch(value)
    })

    function patch(value){
        dispatch(patchComment(value, id))
        exitEditMode()
    }

    const isLikedByUser = () => {
        for(const like of comment_likes){
            if(like.user_id === userInfo.id){
                return {
                    isLiked: true,
                    comment_like_id: like.id
                }
            }
        }
        return {
            isLiked: false,
            comment_like_id: -1
        }
    }

    function pressLike(){
        const commentLikeStatus = isLikedByUser()
        if(commentLikeStatus.isLiked){
            dispatch(deleteCommentLike(commentLikeStatus.comment_like_id))
        }
        else{
            dispatch(postCommentLike({
                comment_id: id,
                isLiked: true
            }))
        }
    }

    return(
        <>
            {   
                editMode ?

                <form onSubmit={formik.handleSubmit}>

                    <input 
                    type="text"
                    id="text"
                    onChange={formik.handleChange}
                    placeholder="comment"
                    />

                    <input
                    type="submit"
                    />

                    <button onClick={exitEditMode}>exit edit mode</button>

                </form>
                :
                <>
                    <h6>This is Comment Block</h6>
                    <span>{text}</span>
                    <span>Likes: {comment_likes.length}</span>
                    <button onClick={() => pressLike()}>Like</button>
                    <span>Created At: {created_at}</span>
                    <span>Updated At: {updated_at}</span>
                    {
                        userInfo.id === user_id ?
                        <>
                            <button onClick={() => dispatch(deleteComment(id))}>DELETE</button>
                            <button onClick={enterEditMode}>EDIT</button>
                        </>
                        :
                        null
                    }
                </>
            }
        </>
    )
}