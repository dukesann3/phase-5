import 'semantic-ui-css/semantic.min.css'
import "../../CSS/profileinfo.css"

function UserProfile({user, open}){

    const {_image_src, first_name, last_name, username} = user

    return(
        <div className="profile-card-group-container">
            <div className="profile-title">
                <span>PROFILE PAGE</span>
            </div>
            <div className="profile-card-container">
                <div className="profile-image-container">
                    <img src={_image_src}/>
                </div>
                <div className="profile-description-container">
                    <div>FIRST NAME: {first_name}</div>
                    <div>LAST NAME:{last_name}</div>
                    <div>USERNAME: {username}</div>
                </div>
                <button className="edit-profile-button" onClick={open}>Edit Profile</button>
            </div>
        </div>
    )
}

export default UserProfile;