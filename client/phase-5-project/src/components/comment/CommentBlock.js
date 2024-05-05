import { useDispatch, useSelector } from "react-redux"
import { useFormik } from "formik"
import { patchComment, deleteComment } from "../../features/post-slice/allPosts"
import { useState } from "react"

export default function CommentBlock({comment}){

    const [editMode, setEditMode] = useState(false)
    const {text, post_id, created_at, updated_at, user_id, id} = comment

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

                </form>
                :
                <>
                    <h6>This is Comment Block</h6>
                    <span>{text}</span>
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