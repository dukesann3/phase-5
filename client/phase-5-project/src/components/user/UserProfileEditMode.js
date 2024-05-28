import { useFormik } from "formik"
import { patchUser } from "../../features/user-slice/user"
import { useDispatch } from "react-redux"
import 'semantic-ui-css/semantic.min.css'
import { Form, FormField, FormGroup } from "semantic-ui-react"
import "../../CSS/profiledit.css"

function UserProfileEditMode({user, close}){

    const dispatch = useDispatch()

    const {_image_src, first_name, last_name, username, id} = user

    const getModifiedValues = (values, initialValues) => {
        let modifiedValues = {};
      
        if (values) {
            Object.entries(values).forEach((entry) => {
            let key = entry[0];
            let value = entry[1];
      
            if (value !== initialValues[key] || (key === "image_uri" && values["image_uri"].length > 0)) {
                modifiedValues[key] = value;
            }
          });
        }
      
        return modifiedValues;
    };

    const formik = useFormik({
        initialValues: {
            first_name: first_name,
            last_name: last_name,
            username: username,
            image_uri: ""
        },
        onSubmit: (value) => {
            console.log(formik.initialValues)
            const modifiedValues = getModifiedValues(value, formik.initialValues)
            console.log(modifiedValues)
            dispatch(patchUser(id, modifiedValues))
            close()
        }
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

    return(
        <Form className="profile-edit-form" onSubmit={formik.handleSubmit}>
            <p>Edit Mode</p>
            <FormField>
                <label>Profile Picture</label>
                <input 
                type="file"
                id="image_uri"
                onChange={onImageChange}
                />
            </FormField>

            <FormGroup>
                <FormField>
                    <label>First Name</label>
                    <input
                    type="text"
                    id="first_name"
                    onChange={formik.handleChange}
                    value={formik.values.first_name}
                    />
                </FormField>

                <FormField>
                    <label>Last Name</label>
                    <input  
                    type="text"
                    id="last_name"
                    onChange={formik.handleChange}
                    value={formik.values.last_name}
                    />
                </FormField>

                <FormField>
                    <label>Username</label>
                    <input
                    type="text"
                    id="username"
                    onChange={formik.handleChange}
                    value={formik.values.username}
                    />
                </FormField>
            </FormGroup>
            
            <input type="submit"/>
            <button onClick={close}>Close</button>
        </Form>
    )
}

export default UserProfileEditMode
