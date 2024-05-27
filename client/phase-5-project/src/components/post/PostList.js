import { useSelector, useDispatch } from "react-redux"
// import { createSelector } from "reselect"
import CreatePost from "./CreatePost"
import { useEffect } from "react"
import { getPosts } from "../../features/post-slice/allPosts"
import PostBlock from "./PostBlock"
// import { updatedAtComparator } from "../../useful_functions"

export default function PostList(){

    const posts = useSelector(state => state.allPost.value)
    console.log(posts)
    const dispatch = useDispatch()

    useEffect(()=>{
        dispatch(getPosts())  
    },[])


    return(
        <>
            <h2>Post List Bruh</h2>
            <CreatePost />
            {posts ? 
            <>
                {posts.map((post) => {
                    return <PostBlock key={post.id} post={post}/>
                })}
            </>
            :
            null
            }
        </>
    )
}