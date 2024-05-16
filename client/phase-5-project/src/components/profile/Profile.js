import { useParams } from "react-router-dom"
import { useSelector } from "react-redux"
import ProfileInfo from "./ProfileInfo"
import { useDispatch } from "react-redux"
import { useEffect } from "react"
import { getFriends } from "../../features/friend-slice/friend"

function Profile(){
    const dispatch = useDispatch()

    useEffect(() => {
        dispatch(getFriends())
    }, [])

    const userListSlice = useSelector((state) => state.userList)
    const friendsSlice = useSelector((state) => state.friends)
    const postsSLice = useSelector((state) => state.allPost)

    const userList = userListSlice.value
    const friends = friendsSlice.value
    const posts = postsSLice.value

    const altogether = userList.concat(friends)
    const {userid} = useParams()

    const user_info = () => {
        for(const person of altogether){
            console.log(person, userid)
            if(person.id == userid){
                return person
            }
        }
    }

    const post_info = () => {
        let user_posts = []
        for(const post of posts){
            if(post.user_id == userid){
                user_posts.push(post)
            }
        }
        return user_posts
    }

    return(
        <>
            {
                user_info() ?
                <>
                    <ProfileInfo editable={false} user={user_info()} posts={post_info()}/>
                </>
                :
                null
            }
        </>
    )
}

export default Profile