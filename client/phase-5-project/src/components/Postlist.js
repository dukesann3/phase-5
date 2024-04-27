import { useSelector, useDispatch } from "react-redux"
import CreatePost from "./CreatePost"
import { useEffect } from "react"
import { fetchAllPosts } from "../features/post/allPosts"

export default function Postlist(){

    const posts = useSelector((store) => store.allPost.value)
    const dispatch = useDispatch()

    useEffect(()=>{
        dispatch(fetchAllPosts())  
    },[])

    console.log(posts)

    return(
        <>
            <h2>Post List Bruh</h2>
            <CreatePost />
            {posts ? 
            <>
                {posts.map((post) => {
                    return <div>{post.caption}</div>
                })}
            </>
            :
            null
            }
        </>
    )
}