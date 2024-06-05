import { useParams } from "react-router-dom"
import { useSelector } from "react-redux"
import ProfileInfo from "./ProfileInfo"
import { useDispatch } from "react-redux"
import 'semantic-ui-css/semantic.min.css'
import "../../CSS/profile.css"
import { useEffect } from "react"
import { fetchSpecificUser } from "../../features/user-slice/userList"

function Profile(){

    const {userid} = useParams()
    const dispatch = useDispatch()
    const userBank = useSelector((state) => state.userList.userBank)
    const allPosts = useSelector((state) => state.allPost.value)

    const isUserInBank = userBank.some(userInBank => userInBank.id == userid)
    const isPostInSlice = allPosts.some(userPost => userPost.user_id == userid) 

    useEffect(() => {
        if(!isUserInBank || !isPostInSlice){
            dispatch(fetchSpecificUser(userid))
        }
    },[userid])

    const user = userBank.filter((userInBank) => userInBank.id == userid)[0]
    const posts = allPosts.some(post => post.user_id == userid) ? allPosts.filter((post) => post.user_id == userid) : null

    return(
        <>
            {
                user ?
                <div className="profile-container">
                    <ProfileInfo editable={false} user={user} posts={posts}/>
                </div>
                :
                null
            }
        </>
    )
}

export default Profile