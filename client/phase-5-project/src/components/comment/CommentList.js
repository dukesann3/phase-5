import CommentBlock from "./CommentBlock"
import CreateComment from "./CreateComment"
import 'semantic-ui-css/semantic.min.css'
import { CommentGroup, Comment } from "semantic-ui-react"

export default function CommentList({comments, post_id}){
    return(
        <>
            <CommentGroup>
                {comments.map((comment) => {
                    return <Comment><CommentBlock key={post_id+comment.id} comment={comment}/></Comment>
                })}
            </CommentGroup>
            <CreateComment post_id={post_id}/>
        </>
    )
}