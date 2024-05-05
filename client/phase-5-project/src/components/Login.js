//no need to use redux for login screen
import { useFormik } from 'formik'
import * as Yup from 'yup'
import { useDispatch, useSelector } from 'react-redux' 
import { fetchUser } from '../features/user-slice/user'
import { NavLink } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'

function Login(){

    const dispatch = useDispatch()
    const loggedInUser = useSelector((store) => store.user)
    const navigate = useNavigate()

    useEffect(()=>{
        if(loggedInUser.value.id) navigate(`/home/${loggedInUser.value.id}`)
    },[loggedInUser])

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
            dispatch(fetchUser(value))
        }
    })

    return(
        <>
            <form onSubmit={formik.handleSubmit}>
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
                onChange={formik.handleChange}
                value={formik.values.password}
                />
                <div>{formik.errors.password}</div>

                <input type='submit' />
            </form>
            <p className="warning-message">
                {loggedInUser.loginStatus.toggle === "failed" ? 
                "incorrect username or password" : ""}
            </p>
            <NavLink to="/create_an_account">Create an Account</NavLink>  
        </>
    )
}

export default Login;