import { useDispatch, useSelector } from "react-redux"
import { deleteUser } from "../features/user-slice/user"
import { useNavigate } from "react-router-dom"
import 'semantic-ui-css/semantic.min.css'
import '../CSS/settings.css'
import { Confirm, Button } from "semantic-ui-react"
import { useState } from "react"

function Settings(){

    const dispatch = useDispatch()
    const navigate = useNavigate()
    const user = useSelector((state) => state.user.value)
    const [state, setState] = useState({open: false})

    const open = () => setState({open: true})
    const close = () => setState({open: false})
    
    const deleteUserHandler = () => {
        close()
        dispatch(deleteUser(user.id))
        navigate("/")
    }

    return(
        <div className="settings-container">
            <h1 className="settings-font">Settings</h1>
            <Button onClick={open}>Delete User</Button>
            {
                state.open ?
                <Confirm 
                    open={open}
                    onCancel={close}
                    onConfirm={deleteUserHandler}
                />
                : null
            }

        </div>
    )
}

export default Settings