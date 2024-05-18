import { useDispatch, useSelector } from "react-redux"
import { deleteUser } from "../features/user-slice/user"
import { useNavigate } from "react-router-dom"

function Settings(){

    const dispatch = useDispatch()
    const navigate = useNavigate()
    const user = useSelector((state) => state.user.value)
    
    const deleteUserHandler = () => {
        dispatch(deleteUser(user.id))
        navigate("/")
    }

    return(
        <>
            <button onClick={deleteUserHandler}>Delete User</button>
            <button></button>
        </>
    )
}

export default Settings