import { useFormik } from "formik"
import * as Yup from 'yup'

export default function CreateAccount(){

    function onCreateAccount(value){
        fetch("/users", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("User cannot be created")
            throw new Error("Network Error")
        })
        .then((r) => console.log(r))
        .catch((error) => console.log(error))
    }

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
            first_name: "",
            last_name: "",
            username: "",
            password: "",
            image_uri: ""
        },
        validationSchema: Yup.object({
            first_name: Yup.string().required("*required"),
            last_name: Yup.string().required("*required"),
            username: Yup.string().required("*required"),
            password: Yup.string().min(5, "Password must be at least 5 characters.").required("*required"),
        }),
        onSubmit: (value) => onCreateAccount(value)
    })

    return(
        <>
            <form onSubmit={formik.handleSubmit}>
                <input 
                type="text" 
                id="first_name"
                name="first_name"
                placholder="first name"
                onChange={formik.handleChange}
                value={formik.values.first_name}
                />
                <div>{formik.errors.first_name}</div>

                <input 
                type="text" 
                id="last_name"
                name="last_name"
                placeholder="last name"
                onChange={formik.handleChange}
                value={formik.values.last_name}
                />
                <div>{formik.errors.last_name}</div>

                <input 
                type="text" 
                id="username"
                name="username"
                placeholder="username"
                onChange={formik.handleChange}
                value={formik.values.username}
                />
                <div>{formik.errors.username}</div>

                <input 
                type="password" 
                id="password"
                name="password"
                placeholder="password"
                onChange={formik.handleChange}
                value={formik.values.password}
                />
                <div>{formik.errors.password}</div>

                <input 
                type="file" 
                id="image_uri"
                name="image_uri"
                onChange={onImageChange}
                />

                <input 
                type="submit"
                />
            </form>
        </>
    )
}