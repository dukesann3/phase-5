//no need to use redux for login screen
import { useFormik } from 'formik'
import * as Yup from 'yup'
import { useDispatch } from 'react-redux' 
import { fetchUser } from '../features/user/userLogged'


function Login(){

    const dispatch = useDispatch()

    const formik = useFormik({
        initialValues: {
            username: "",
            password: ""
        },
        validationSchema: Yup.object({
            username: Yup.string().required('*required'),
            password: Yup.string().required("*required")
        }),
        onSubmit: (value) => {dispatch(fetchUser(value))}
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

                <input 
                type="password"
                id="password"
                name="password"
                onChange={formik.handleChange}
                value={formik.values.password}
                />

                <input type='submit' />
            </form>
        </>
    )
}

export default Login;