import { useSelector, useDispatch } from "react-redux"
import CreatePost from "./CreatePost"
import { useEffect } from "react"
import { getPosts } from "../../features/post-slice/allPosts"
import PostBlock from "./PostBlock"

export default function PostList(){

    const posts = useSelector((store) => store.allPost.value)
    const dispatch = useDispatch()

    useEffect(()=>{
        dispatch(getPosts())  
    },[])

    console.log(posts)

    return(
        <>
            <h2>Post List Bruh</h2>
            <CreatePost />
            {posts ? 
            <>
                {posts.map((post) => {
                    return <PostBlock post={post}/>
                })}
            </>
            :
            null
            }
        </>
    )
}