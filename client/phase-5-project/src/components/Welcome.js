import "../CSS/welcome.css"
import Login from "./Login"

export default function Welcome(){
    return(
        <div className="grid-container">
            <div className="grid-item login-container">
                <Login />
            </div>
            <div className="grid-item image-container">
                <img className="welcome-image" src="/used_in_website/merakist-CNbRsQj8mHQ-unsplash.jpg" alt="social media"/>
            </div>
        </div>
    )
}
