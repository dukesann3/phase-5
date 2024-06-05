import { useSelector } from "react-redux"
import CreatePost from "./CreatePost"
import PostBlock from "./PostBlock"
import "../../CSS/postlist.css"
import { CardGroup } from "semantic-ui-react"
import 'semantic-ui-css/semantic.min.css'


export default function PostList(){

    const posts = useSelector(state => state.allPost.value)
    const userBank = useSelector((state) => state.userList.userBank)
    
    return(
        <div className="flex-container-postlist">
            <CreatePost className="flex-item-postlist-create-post"/>
            {posts ? 
            <CardGroup itemsPerRow={1} className="flex-item-postlist">
                {posts.map((post) => {
                    if(post.isFriendPost === true){
                        const user = userBank.filter((userInBank) => userInBank.id == post.user_id)[0]
                        return <PostBlock key={post.id} post={post} postOwner={user}/>
                    }
                })}
            </CardGroup>
            :
            null
            }
        </div>
    )
}