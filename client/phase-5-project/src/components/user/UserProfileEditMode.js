import { useFormik } from "formik"
import { patchUser } from "../../features/user-slice/user"
import { useDispatch } from "react-redux"

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
        <form onSubmit={formik.handleSubmit}>
            <p>Edit Mode</p>
            <img src={_image_src} />
            <input 
            type="file"
            id="image_uri"
            onChange={onImageChange}
            />
            
            <input
            type="text"
            id="first_name"
            onChange={formik.handleChange}
            value={formik.values.first_name}
            />

            <input
            type="text"
            id="last_name"
            onChange={formik.handleChange}
            value={formik.values.last_name}
            />

            <input
            type="text"
            id="username"
            onChange={formik.handleChange}
            value={formik.values.username}
            />
            
            <input type="submit"/>
            <button onClick={close}>Close</button>
        </form>
    )
}

export default UserProfileEditMode
