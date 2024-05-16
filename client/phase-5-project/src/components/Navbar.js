import { logoutUser } from "../features/user-slice/user"
import { useDispatch, useSelector } from "react-redux"
import { NavLink } from "react-router-dom"
import { useNavigate } from "react-router-dom"

export function Navbar(){

    const dispatch = useDispatch()
    const loggedInUser = useSelector((store) => store.user)
    const navigate = useNavigate()

    return(
        <>
            {
                loggedInUser.loginStatus.isLoggedIn ?
                <nav className="loggedIn">
                    <button onClick={() => {
                        dispatch(logoutUser())
                        navigate("/")
                    }}>Logout</button>
                    <NavLink to={'/profile'}>Profile</NavLink>
                    <NavLink to={'/friendslist'}>Friends</NavLink>
                </nav>
                :
                <nav className="not-loggedIn">
                    <NavLink to="/login">Login</NavLink>
                </nav>
            }
        </>
    )
}