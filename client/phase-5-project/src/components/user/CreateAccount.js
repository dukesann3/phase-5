import { useFormik } from "formik"
import * as Yup from 'yup'
import { useNavigate } from "react-router-dom"
import {Form, FormField} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import "../../CSS/createanaccount.css"

export default function CreateAccount(){

    const navigate = useNavigate()

    //create react component that leads to successful creation page
    function onCreateAccount(value){
        fetch("/create_an_account", {
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
        .then(() => navigate("/"))
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
        <div className="create-an-account-container">
            <Form onSubmit={formik.handleSubmit} className="create-an-account-item">
                <h3>CREATE AN ACCOUNT</h3>
                <FormField>
                <label>FIRST NAME</label>
                <input 
                type="text" 
                id="first_name"
                name="first_name"
                placholder="first name"
                onChange={formik.handleChange}
                value={formik.values.first_name}
                />
                </FormField>
                <div>{formik.errors.first_name}</div>

                <FormField>
                <label>LAST NAME</label>
                <input 
                type="text" 
                id="last_name"
                name="last_name"
                placeholder="last name"
                onChange={formik.handleChange}
                value={formik.values.last_name}
                />
                </FormField>
                <div>{formik.errors.last_name}</div>

                <FormField>
                <label>USERNAME</label>
                <input 
                type="text" 
                id="username"
                name="username"
                placeholder="username"
                onChange={formik.handleChange}
                value={formik.values.username}
                />
                </FormField>
                <div>{formik.errors.username}</div>

                <FormField>
                <label>PASSWORD</label>
                <input 
                type="password" 
                id="password"
                name="password"
                placeholder="password"
                onChange={formik.handleChange}
                value={formik.values.password}
                />
                </FormField>
                <div>{formik.errors.password}</div>

                <FormField>
                <label>PROFILE PICTURE</label>
                <input 
                type="file" 
                id="image_uri"
                name="image_uri"
                onChange={onImageChange}
                />
                </FormField>

                <input 
                type="submit"
                />
            </Form>
        </div>
    )
}