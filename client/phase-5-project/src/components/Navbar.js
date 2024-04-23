import { logoutUser } from "../features/user/userLogged"
import { useDispatch, useSelector } from "react-redux"

export function Navbar(){

    const dispatch = useDispatch()
    const loggedInUser = useSelector((store) => store.loggedInUser.value)
    console.log(loggedInUser)

    return(
        <>
            {Object.keys(loggedInUser).length > 0 ? <button onClick={() => dispatch(logoutUser())}>Logout</button> : null}
        </>
    )
}