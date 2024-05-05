import { useFormik } from "formik"
import * as Yup from 'yup'
import { useDispatch } from "react-redux"
import { postComment } from "../../features/post-slice/allPosts"

export default function CreateComment({post_id}){

    const dispatch = useDispatch()

    const formik = useFormik({
        initialValues: {
            post_id: post_id,
            text: ""
        },
        validationSchema: Yup.object({
            text: Yup.string().required("*required")
        }),
        onSubmit: (value) => dispatch(postComment(value))
    })

    return(
        <form onSubmit={formik.handleSubmit}>
            <input
            type="text"
            id="text"
            onChange={formik.handleChange}
            value={formik.values.text}
            placeholder="comment"
            />

            <input 
            type="submit"
            />
        </form>
    )
}