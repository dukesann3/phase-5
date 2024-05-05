import CommentList from "../comment/CommentList"
import { useSelector, useDispatch } from "react-redux"
import { patchPost, deletePost } from "../../features/post-slice/allPosts"
import { useState } from "react"
import { useFormik } from "formik"

export default function PostBlock({post}){

    const [editMode, setEditMode] = useState(false)
    const enterEditMode = () => setEditMode(true)
    const exitEditMode = () => setEditMode(false)

    const userInfo = useSelector((store) => store.user.value)
    const dispatch = useDispatch()
    
    const {caption, location, created_at, updated_at, _image_src, comments, id, user_id} = post

    const formik = useFormik({
        initialValues: {
            image_uri: "",
            location: "",
            caption: ""
        },
        onSubmit: (value) => patch(value)
    })

    function onImageChange(e){
        try{
            const reader = new FileReader()
            reader.readAsDataURL(e.target.files[0])
            reader.addEventListener("load", () => {
                const uri = reader.result
                formik.values.image_uri = uri
            })
        }
        catch(error){
            console.log(error)
        }
    }

    function patch(value){
        dispatch(patchPost(value, id))
        setEditMode(false)
    }

    return(
        <div>
            {
            editMode ?
            <>
                <form onSubmit={formik.handleSubmit}>
                    <input 
                    type="file"
                    id="image_uri"
                    onChange={onImageChange}
                    placeholder="image"
                    />

                    <input
                    type="text"
                    id="location"
                    onChange={formik.handleChange}
                    value={formik.values.location}
                    placeholder="location"
                    />

                    <input
                    type="text"
                    id="caption"
                    onChange={formik.handleChange}
                    value={formik.values.caption}
                    placeholder="caption"
                    />

                    <input 
                    type="submit"
                    />
                    <button onClick={exitEditMode}>exit edit mode</button>
                </form>
            </>
            :
            <>
                <img src={_image_src}/>
                <span>{caption}</span>
                <span>{location}</span>
                <span>Created at: {created_at}</span>
                <span>Updated at: {updated_at}</span>
                <CommentList comments={comments} post_id={id}/>
                {
                    userInfo.id === user_id?
                    <>
                        <button onClick={() => dispatch(deletePost(id))}>DELETE</button>
                        <button onClick={enterEditMode}>EDIT</button>
                    </>
                    :
                    null
                }
            </>
            }
        </div>
    )
}

