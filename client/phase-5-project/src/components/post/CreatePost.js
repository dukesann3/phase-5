import { useFormik } from "formik"
import * as Yup from 'yup'
import { useDispatch } from "react-redux"
import { postPost } from "../../features/post-slice/allPosts"

export default function CreatePost(){

    const dispatch = useDispatch()

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

    const formik = useFormik({
        initialValues: {
            image_uri: "",
            location: "",
            caption: ""
        },
        validationSchema: Yup.object({
            image_uri: Yup.string().required("*required"),
            location: Yup.string().required("*required"),
            caption: Yup.string().required("*required")
        }),
        onSubmit: (value) => dispatch(postPost(value))
    })

    return(
        <form onSubmit={formik.handleSubmit}>
            <input 
            type="file"
            id="image_uri"
            onChange={onImageChange}
            placeholder="image"
            />
            <div>{formik.errors.image_uri}</div>

            <input
            type="text"
            id="location"
            onChange={formik.handleChange}
            value={formik.values.location}
            placeholder="location"
            />
            <div>{formik.errors.location}</div>

            <input
            type="text"
            id="caption"
            onChange={formik.handleChange}
            value={formik.values.caption}
            placeholder="caption"
            />
            <div>{formik.errors.caption}</div>

            <input 
            type="submit"
            />
        </form>
    )
}