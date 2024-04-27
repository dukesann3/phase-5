import { useFormik } from "formik"
import * as Yup from 'yup'

export default function CreatePost(){

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

    function onPost(value){
        fetch('/posts', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Could not create post")
            throw new Error("Network Error")
        })
        .then((r) => console.log(r))
        .catch((error) => console.log(error))
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
        onSubmit: (value) => onPost(value)
    })

    return(
        <form onSubmit={formik.handleSubmit}>
            <input 
            type="file"
            id="image_uri"
            onChange={onImageChange}
            />

            <input
            type="text"
            id="location"
            onChange={formik.handleChange}
            value={formik.values.location}
            />

            <input
            type="text"
            id="caption"
            onChange={formik.handleChange}
            value={formik.values.caption}
            />

            <input 
            type="submit"
            />
        </form>
    )
}