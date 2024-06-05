import { useDispatch, useSelector } from "react-redux"
import { useFormik } from "formik"
import { patchComment, deleteComment, postCommentLike, deleteCommentLike } from "../../features/post-slice/allPosts"
import { useState } from "react"
import { NavLink } from "react-router-dom"
import 'semantic-ui-css/semantic.min.css'
import "../../CSS/commentblock.css"
import "../../CSS/commentedit.css"
import { CommentContent, CommentAuthor, CommentText, 
    CommentActions, CommentMetadata, CommentAvatar, 
    Button, Form, FormField } from "semantic-ui-react"

export default function CommentBlock({comment}){

    const [editMode, setEditMode] = useState(false)
    const {text, created_at, updated_at, user_id, id, comment_likes, user} = comment

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
                
                <div className="comment-edit-form-container">
                    <Form className="comment-edit-form" onSubmit={formik.handleSubmit}>
                        <FormField>
                            <label>Edit Comment</label>
                            <input 
                            type="text"
                            id="text"
                            onChange={formik.handleChange}
                            placeholder="comment"
                            />
                        </FormField>

                        <input
                        type="submit"
                        />

                        <button onClick={exitEditMode}>exit edit mode</button>

                    </Form>
                </div>
                :
                <>
                    <CommentAvatar src={user._image_src}/>
                    <CommentContent>
                        <div className="comment-metadata">
                            <CommentAuthor>
                                <NavLink to={user.id == userInfo.id ? `/profile` : `/user/${user_id}/profile`}>
                                    <span>{user.username}</span>
                                </NavLink>
                            </CommentAuthor>
                            <CommentMetadata>
                                <p className="comment-date">Created At: {created_at}</p>
                            </CommentMetadata>
                        </div>
                        <CommentText>{text}</CommentText>
                        <CommentActions>
                            <div className="comment-action-like">
                                <div>❤</div>
                                <div>{comment_likes.length}</div>
                                <Button onClick={() => pressLike()}>Like</Button>
                            </div>
                        </CommentActions>
                        <CommentActions>
                            {
                                userInfo.id === user_id ?
                                <div className="comment-edit-container">
                                    <button className="comment-edit-button " onClick={() => dispatch(deleteComment(id))}>
                                        <span className="button-word">DELETE</span>
                                    </button>
                                    <button className="comment-edit-button" onClick={enterEditMode}>
                                        <span className="button-word">EDIT</span>
                                    </button>
                                </div>
                                :
                                null
                            }
                        </CommentActions>
                    </CommentContent>
                </>
            }
        </>
    )
}