import { useFormik } from "formik"
import * as Yup from 'yup'
import { useDispatch } from "react-redux"
import { postComment } from "../../features/post-slice/allPosts"
import 'semantic-ui-css/semantic.min.css'
import { Form, FormField } from "semantic-ui-react"

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
        onSubmit: (value) => {
            dispatch(postComment(value))
            formik.values.text = ""
        }
    })

    return(
        <Form onSubmit={formik.handleSubmit}>
            <FormField>
                <label>Comment</label>
                <input
                type="text"
                id="text"
                onChange={formik.handleChange}
                value={formik.values.text}
                placeholder="comment"
                />
            </FormField>

            <input 
            type="submit"
            />
        </Form>
    )
}