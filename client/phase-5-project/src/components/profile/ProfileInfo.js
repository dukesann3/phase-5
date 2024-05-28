import PostBlock from "../post/PostBlock"
import 'semantic-ui-css/semantic.min.css'
import "../../CSS/profileinfo.css"
import { Card } from "semantic-ui-react"

function ProfileInfo({user, posts}){

    const {first_name, last_name, username, _image_src, id} = user

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
            </div>
            {
                posts.map((post) => {
                    return <Card><PostBlock key={post.id} post={post}/></Card>
                })
            }
        </div>
    )
}

export default ProfileInfo