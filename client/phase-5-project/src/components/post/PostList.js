import { useSelector, useDispatch } from "react-redux"
import CreatePost from "./CreatePost"
import { useEffect } from "react"
import { getPosts } from "../../features/post-slice/allPosts"
import PostBlock from "./PostBlock"
import "../../CSS/postlist.css"
import { CardGroup } from "semantic-ui-react"
import 'semantic-ui-css/semantic.min.css'


export default function PostList(){

    const posts = useSelector(state => state.allPost.value)
    console.log(posts)
    const dispatch = useDispatch()

    useEffect(()=>{
        dispatch(getPosts())  
    },[])


    return(
        <div className="flex-container-postlist">
            <CreatePost className="flex-item-postlist-create-post"/>
            {posts ? 
            <CardGroup itemsPerRow={1} className="flex-item-postlist">
                {posts.map((post) => {
                    return <PostBlock key={post.id} post={post}/>
                })}
            </CardGroup>
            :
            null
            }
        </div>
    )
}