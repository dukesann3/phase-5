import { logoutUser } from "../features/user-slice/user"
import { useDispatch, useSelector } from "react-redux"
import { NavLink } from "react-router-dom"
import { useNavigate } from "react-router-dom"
import "../CSS/navbar.css"

export function Navbar(){

    const dispatch = useDispatch()
    const loggedInUser = useSelector((store) => store.user)
    const navigate = useNavigate()

    return(
        <>
            {
                loggedInUser.loginStatus.isLoggedIn ?
                <div className="nav-container-in">
                    <div className="flatbook-title-container-in">FLATBOOK</div>
                    <div className="in-item-container"><NavLink className="nav-item" to={'/profile'}>Profile</NavLink></div>
                    <div className="in-item-container"><NavLink className="nav-item" to={'/friendslist'}>Friends</NavLink></div>
                    <div className="in-item-container"><NavLink className="nav-item" to={`/home/${loggedInUser.value.id}`}>Home</NavLink></div>
                    <div className="in-item-container"><NavLink className="nav-item" to={'/settings'}>Settings</NavLink></div>
                    <div className="in-item-container">                    
                        <button className="nav-item" onClick={() => {
                            dispatch(logoutUser())
                            navigate("/")
                        }}>Logout</button>
                    </div>
                </div>
                :
                <div className="nav-container-out">
                    <div className="flatbook-title-container">FLATBOOK</div>
                    <div className="out-item-container"><NavLink to="/" className="nav-item">Welcome</NavLink></div>
                </div>
            }
        </>
    )
}