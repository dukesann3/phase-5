//no need to use redux for login screen
import { useFormik } from 'formik'
import * as Yup from 'yup'
import { useSelector, useDispatch } from 'react-redux' 
import { NavLink } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import {Form, FormField} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import { makeSentenceError } from '../useful_functions'
import { loginSucceeded, loginPending, loginFailed } from '../features/user-slice/user'

function Login(){

    const loggedInUser = useSelector((store) => store.user)
    const navigate = useNavigate()
    const dispatch = useDispatch()

    function fetchUser(value){
        dispatch(loginPending())
        fetch('/login', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        }).then(async (r)=>{
            if(r.ok) return r.json()
            return await r.json().then(error => {throw new Error(makeSentenceError(error))})
        }).then((r) => {
            dispatch(loginSucceeded(r))
            navigate(`/home/${r.id}`)
        }).catch((error) => {
            console.log("login error: ",error.toString())
            dispatch(loginFailed(error.toString()))
        })
    }

    const formik = useFormik({
        initialValues: {
            username: "",
            password: ""
        },
        validationSchema: Yup.object({
            username: Yup.string().required('*required'),
            password: Yup.string().required("*required")
        }),
        onSubmit: (value) => {
            fetchUser(value)
        }
    })

    return(
        <>
            <Form onSubmit={formik.handleSubmit}>
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
                onChange={formik.handleChange}
                value={formik.values.password}
                />
                </FormField>
                <div>{formik.errors.password}</div>

                <input type='submit' />
            </Form>
            <p className="warning-message">
                {loggedInUser.loginStatus.toggle === "failed" ? 
                loggedInUser.loginErrorMessage : ""}
            </p>
            <NavLink to="/create_an_account">Create an Account</NavLink>  
        </>
    )
}

export default Login;